"""
NLP Backend for Diagrammatic - Sentence Diagramming with spaCy and Stanza
Supports 20+ languages with dependency parsing, POS tagging, and morphological analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from spacy.language import Language
import stanza
import logging
from typing import Dict, List, Optional
import json
from quantum_grammar_parser import parse_quantum_grammar

app = Flask(__name__)
# Enable CORS for frontend development
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global cache for loaded models
models_cache: Dict[str, Language] = {}
stanza_pipelines: Dict[str, stanza.Pipeline] = {}

# Language codes supported by Stanza (more comprehensive)
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'pl': 'Polish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish',
    'vi': 'Vietnamese',
    'th': 'Thai',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'fa': 'Persian',
    'he': 'Hebrew',
}


def load_stanza_pipeline(language_code: str) -> stanza.Pipeline:
    """
    Load or retrieve Stanza pipeline from cache
    """
    if language_code not in stanza_pipelines:
        logger.info(f"Loading Stanza pipeline for {language_code}")
        try:
            stanza_pipelines[language_code] = stanza.Pipeline(
                lang=language_code,
                processors='tokenize,pos,lemma,depparse',
                use_gpu=False
            )
        except Exception as e:
            logger.error(f"Failed to load Stanza pipeline for {language_code}: {e}")
            raise
    return stanza_pipelines[language_code]


def parse_with_stanza(text: str, language_code: str) -> Dict:
    """
    Parse text using Stanza for comprehensive NLP analysis
    """
    try:
        nlp = load_stanza_pipeline(language_code)
        doc = nlp(text)

        tokens = []
        sentences = []

        for sent in doc.sentences:
            sent_tokens = []
            for word in sent.words:
                token_data = {
                    'id': word.id,
                    'text': word.text,
                    'lemma': word.lemma,
                    'pos': word.pos,
                    'xpos': word.xpos,
                    'upos': word.upos,
                    'deprel': word.deprel,
                    'head': word.head,
                    'index': word.id - 1  # 0-based index
                }
                sent_tokens.append(token_data)
                tokens.append(token_data)

            sentences.append({
                'text': sent.text,
                'tokens': sent_tokens
            })

        return {
            'success': True,
            'language': language_code,
            'sentences': sentences,
            'tokens': tokens,
            'token_count': len(tokens),
            'sentence_count': len(sentences)
        }

    except Exception as e:
        logger.error(f"Stanza parsing error: {e}")
        return {
            'success': False,
            'error': str(e),
            'language': language_code
        }


def detect_language(text: str) -> str:
    """
    Simple language detection based on character patterns
    Returns language code or 'en' as default
    """
    # Check for common non-Latin scripts
    if any('\u0600' <= char <= '\u06FF' for char in text):  # Arabic
        return 'ar'
    elif any('\u0400' <= char <= '\u04FF' for char in text):  # Cyrillic (Russian, Ukrainian, etc.)
        if any('\u0500' <= char <= '\u052F' for char in text):
            return 'uk'  # Ukrainian
        return 'ru'
    elif any('\u4E00' <= char <= '\u9FFF' for char in text):  # Chinese
        return 'zh'
    elif any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in text):  # Japanese
        return 'ja'
    elif any('\u0E00' <= char <= '\u0E7F' for char in text):  # Thai
        return 'th'
    elif any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari (Hindi)
        return 'hi'

    # Default to English for Latin script
    return 'en'


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0',
        'supported_languages': SUPPORTED_LANGUAGES
    })


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    return jsonify({
        'languages': SUPPORTED_LANGUAGES,
        'count': len(SUPPORTED_LANGUAGES)
    })


@app.route('/api/parse', methods=['POST'])
def parse_sentence():
    """
    Parse a sentence and return rich NLP metadata

    Request body:
    {
        "text": "The quick brown fox jumps over the lazy dog",
        "language": "en"  # Optional, will auto-detect if not provided
    }
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text cannot be empty'}), 400

    # Auto-detect language if not provided
    language = data.get('language')
    if not language:
        language = detect_language(text)

    # Validate language code
    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            'error': f'Language {language} not supported',
            'supported': list(SUPPORTED_LANGUAGES.keys())
        }), 400

    # Parse the text
    result = parse_with_stanza(text, language)

    if not result['success']:
        return jsonify(result), 500

    return jsonify(result)


@app.route('/api/parse-detailed', methods=['POST'])
def parse_detailed():
    """
    Extended parsing with additional analysis
    Includes syntactic and semantic information
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text cannot be empty'}), 400

    language = data.get('language', detect_language(text))

    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            'error': f'Language {language} not supported',
            'supported': list(SUPPORTED_LANGUAGES.keys())
        }), 400

    result = parse_with_stanza(text, language)

    if not result['success']:
        return jsonify(result), 500

    # Add additional analysis
    analysis = {
        'result': result,
        'statistics': {
            'avg_sentence_length': len(result['tokens']) / max(1, result['sentence_count']),
            'pos_distribution': analyze_pos_distribution(result['tokens']),
            'dependency_types': analyze_dependencies(result['tokens'])
        }
    }

    return jsonify(analysis)


def analyze_pos_distribution(tokens: List[Dict]) -> Dict[str, int]:
    """Count POS tag distribution"""
    distribution = {}
    for token in tokens:
        pos = token.get('upos', 'UNKNOWN')
        distribution[pos] = distribution.get(pos, 0) + 1
    return distribution


def analyze_dependencies(tokens: List[Dict]) -> Dict[str, int]:
    """Count dependency relation types"""
    distribution = {}
    for token in tokens:
        deprel = token.get('deprel', 'root')
        distribution[deprel] = distribution.get(deprel, 0) + 1
    return distribution


@app.route('/api/parse-quantum-grammar', methods=['POST'])
def parse_quantum_grammar_endpoint():
    """
    Parse text using Quantum Grammar

    Request body:
    {
        "text": "For the healing of the quantum-body is with the natural-light"
    }

    Returns quantum grammar analysis with numeric codes and patterns
    """
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400

    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Text cannot be empty'}), 400

    try:
        result = parse_quantum_grammar(text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Quantum Grammar parsing error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting NLP Backend Server")
    logger.info(f"Supported languages: {len(SUPPORTED_LANGUAGES)}")
    app.run(debug=True, port=5000, host='127.0.0.1')
