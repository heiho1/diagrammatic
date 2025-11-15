# Diagrammatic - Sentence Diagramming with Advanced NLP

A powerful sentence diagramming web application with real-time dependency parsing and grammatical analysis. Supports 20+ languages with state-of-the-art NLP models from Stanza (Stanford CoreNLP).

## Features

- **Multi-language Support**: Parse sentences in 20+ languages including English, Spanish, French, German, Chinese, Japanese, Arabic, Turkish, and more
- **Dependency Parsing**: Visualize sentence structure with interactive dependency trees
- **Rich Grammatical Analysis**:
  - Part-of-speech (POS) tagging
  - Lemmatization
  - Dependency relations
  - Morphological analysis
- **Statistics & Insights**: View token distribution and part-of-speech breakdowns
- **Beautiful UI**: Built with Vue 3, Quasar, and Vite
- **Real-time Processing**: Instant grammatical analysis as you type

## Architecture

This project consists of two main components:

1. **Frontend** (Vue 3 + Vite + Quasar)
   - Interactive sentence input
   - Dependency tree visualization
   - Token analysis tables
   - Grammar statistics

2. **Backend** (Python Flask + Stanza)
   - Multi-language NLP processing
   - Dependency parsing
   - POS tagging and lemmatization
   - Language detection

## Prerequisites

- **Node.js** 14+ and npm
- **Python** 3.7+ with pip

## Installation & Setup

### 1. Install Frontend Dependencies

```bash
cd /path/to/diagrammatic
npm install
```

### 2. Install Python Dependencies

```bash
# Create a Python virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt
```

### 3. Download Stanza Language Models

This is required for NLP processing. Models are downloaded once and cached locally.

```bash
# Automated download of all supported languages
python3 setup_nlp.py
```

This will download models for: English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Arabic, Turkish, Ukrainian, Polish, Dutch, Swedish, Vietnamese, Thai, and Hindi.

**Note**: This may take 10-30 minutes depending on your internet connection. The models (~5.3GB total) are stored in `~/stanza_resources/` (or `/Users/YOUR_USERNAME/stanza_resources/`).

### 4. Run the Backend Server

```bash
# Make sure your Python virtual environment is activated
python3 nlp_backend.py
```

You should see:
```
Starting NLP Backend Server
Supported languages: 18
 * Running on http://127.0.0.1:5000
```

### 5. Run the Frontend (in a new terminal)

```bash
# Make sure you're in the project directory
npm run dev
```

The app will open at `http://localhost:5173`

## Usage

1. **Enter a sentence** in the input field
2. **Optionally select a language** (auto-detection works for most languages)
3. **Click "Analyze & Diagram"** or press Enter
4. **View results**:
   - **Dependency Tree**: Visual representation of sentence structure
   - **Token Analysis**: Detailed table of words, lemmas, POS tags, and dependencies
   - **Statistics**: Overall metrics and POS distribution

## API Endpoints

The backend server provides these endpoints:

### Health Check
```
GET /api/health
```

### Get Supported Languages
```
GET /api/languages
```

### Parse a Sentence
```
POST /api/parse
Content-Type: application/json

{
  "text": "The quick brown fox jumps over the lazy dog",
  "language": "en"  // Optional, auto-detects if not provided
}
```

### Parse with Detailed Analysis
```
POST /api/parse-detailed
Content-Type: application/json

{
  "text": "Your sentence here",
  "language": "en"  // Optional
}
```

Returns token data plus statistics (POS distribution, dependency types, etc.)

## Supported Languages

| Code | Language      | Code | Language      | Code | Language      |
|------|---------------|------|---------------|------|---------------|
| en   | English       | pl   | Polish        | vi   | Vietnamese    |
| es   | Spanish       | nl   | Dutch         | th   | Thai          |
| fr   | French        | sv   | Swedish       | hi   | Hindi         |
| de   | German        | no   | Norwegian     | bn   | Bengali       |
| it   | Italian       | da   | Danish        | fa   | Persian       |
| pt   | Portuguese    | fi   | Finnish       | he   | Hebrew        |
| ru   | Russian       | uk   | Ukrainian     |      |               |
| zh   | Chinese       | ar   | Arabic        |      |               |
| ja   | Japanese      | tr   | Turkish       |      |               |

## Project Structure

```
diagrammatic/
├── index.html                 # Entry point
├── vite.config.js            # Vite configuration
├── nlp_backend.py            # Flask NLP server
├── setup_nlp.py              # Stanza model downloader
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
├── src/
│   ├── main.js              # Vue app initialization
│   ├── App.vue              # Main app layout
│   └── components/
│       └── SentenceDiagrammer.vue  # Main diagramming component
└── README.md                # This file
```

## Development

### Start Development Servers

```bash
# Terminal 1: Backend (Python)
source venv/bin/activate
python3 nlp_backend.py

# Terminal 2: Frontend (Node.js)
npm run dev
```

### Build for Production

```bash
# Frontend
npm run build

# Backend can be run as-is or containerized with Docker
```

## Technology Stack

**Frontend:**
- Vue 3 (Composition API)
- Vite (build tool)
- Quasar (UI framework)
- Canvas API (visualization)

**Backend:**
- Python 3.7+
- Flask (web framework)
- Stanza (NLP)
- spaCy (NLP support)

## Performance Notes

- **First request** per language: ~2-5 seconds (loading NLP pipeline)
- **Subsequent requests**: ~100-500ms (depending on sentence length and language)
- **Language detection**: Automatic for non-Latin scripts
- **Model size**: ~25-30MB per language (total ~500MB for all)

## Troubleshooting

### Backend won't start
```bash
# Make sure Flask is installed
pip install Flask Flask-CORS

# Check Python version (3.7+)
python3 --version
```

### "Connection refused" error
- Ensure the backend is running on http://localhost:5000
- Check that no other service is using port 5000
- Check frontend console for CORS errors

### Language models not downloading
```bash
# Try downloading a single language
python3 -c "import stanza; stanza.download('en')"

# If it fails, check internet connection and disk space
```

### Slow performance

- First request per language loads the NLP pipeline (~2-5s)
- Subsequent requests are faster
- Larger sentences take longer to parse
- Consider increasing system RAM for better performance

## Future Enhancements

- [ ] Interactive diagram editing
- [ ] Sentence comparison
- [ ] Grammar rule suggestions
- [ ] Export diagrams as images/PDF
- [ ] Custom grammar rule definitions
- [ ] Machine translation
- [ ] Offline model support
- [ ] Mobile app version

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT

## Resources

- [Stanza Documentation](https://stanfordnlp.github.io/stanza/)
- [spaCy Documentation](https://spacy.io/)
- [Quasar Documentation](https://quasar.dev/)
- [Vue 3 Documentation](https://vuejs.org/)
