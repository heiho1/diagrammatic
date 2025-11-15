"""
Quantum Grammar Parser

Implements parsing logic for Quantum Grammar as documented in:
docs/QUANTUM_GRAMMAR_DOCUMENT.md

Core principle: Facts are established by the 5,6,7 pattern (POSITION-LODIAL-FACT)
"""

import re
from typing import List, Dict, Tuple, Optional


class QuantumGrammarParser:
    """Parser for Quantum Grammar analysis"""

    # Numeric code definitions
    CODES = {
        0: "CONJUNCTION",
        1: "ADVERB",
        2: "VERB",
        3: "ADJECTIVE",
        4: "PRONOUN",
        5: "POSITION",
        6: "LODIAL",
        7: "FACT",
        8: "PAST-TIME-FICTION",
        9: "FUTURE-TIME-FICTION",
    }

    # Word categorizations
    CONJUNCTION_WORDS = {"and", "&", "or", "/"}

    POSITION_WORDS = {
        "by", "for", "in", "out", "of", "as", "with", "off", "on",
        "outside", "within", "up", "down", "round", "through", "into"
    }

    LODIAL_WORDS = {
        "a", "an", "any", "each", "either", "every", "the", "this",
        "these", "those", "their", "his", "her", "my", "your", "our"
    }

    # Common verbs (basic list, can be expanded)
    COMMON_VERBS = {
        "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did",
        "will", "would", "should", "could", "may", "might", "must",
        "can", "go", "goes", "went", "run", "runs", "ran",
        "jump", "jumps", "jumped", "sit", "sits", "sat",
        "say", "says", "said", "get", "gets", "got",
        "make", "makes", "made", "take", "takes", "took",
        "give", "gives", "gave", "find", "finds", "found",
        "think", "thinks", "thought", "see", "sees", "saw",
        "come", "comes", "came", "know", "knows", "knew"
    }

    # Tense indicators
    PAST_TENSE_SUFFIXES = {"ed", "t"}
    PAST_TENSE_VERBS = {"was", "were", "had", "went", "ran", "sat", "said", "made", "took", "gave", "found", "thought", "saw", "came", "knew"}

    FUTURE_TENSE_MARKERS = {"will", "going", "gonna", "shall"}
    FUTURE_TENSE_SUFFIXES = {"ing"}  # "going" in context

    def __init__(self):
        """Initialize the parser"""
        pass

    def parse(self, text: str) -> Dict:
        """
        Parse text using Quantum Grammar rules

        Args:
            text: Input sentence to parse

        Returns:
            Dictionary containing parsed results
        """
        # Tokenize
        tokens = self._tokenize(text)

        # Tag words with initial codes
        tagged_tokens = [self._tag_word(token) for token in tokens]

        # Apply contextual rules
        tagged_tokens = self._apply_contextual_rules(tagged_tokens)

        # Detect modification patterns
        modification_chain = self._detect_modifications(tagged_tokens)

        # Check for 5,6,7 patterns (fact establishment)
        has_facts = self._check_for_facts(tagged_tokens)

        # Calculate statistics
        stats = self._calculate_statistics(tagged_tokens, has_facts)

        return {
            "success": True,
            "text": text,
            "tokens": tagged_tokens,
            "modification_chain": modification_chain,
            "has_facts": has_facts,
            "fact_establishment": "Facts are established" if has_facts else "No facts established - fictional language",
            "statistics": stats
        }

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Simple tokenization - split on whitespace and punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    def _tag_word(self, word: str) -> Dict:
        """
        Determine initial code for a word

        Returns dictionary with word info and primary code
        """
        word_lower = word.lower()

        # Check conjunctions
        if word_lower in self.CONJUNCTION_WORDS:
            return {
                "text": word,
                "code": "0",
                "category": "CONJUNCTION",
                "primary_category": "CONJUNCTION",
                "is_verb": False,
                "tense": None
            }

        # Check position words
        if word_lower in self.POSITION_WORDS:
            return {
                "text": word,
                "code": "5",
                "category": "POSITION",
                "primary_category": "POSITION",
                "is_verb": False,
                "tense": None
            }

        # Check lodial words
        if word_lower in self.LODIAL_WORDS:
            return {
                "text": word,
                "code": "6",
                "category": "LODIAL",
                "primary_category": "LODIAL",
                "is_verb": False,
                "tense": None
            }

        # Check verbs
        if word_lower in self.COMMON_VERBS or self._is_likely_verb(word_lower):
            tense = self._detect_tense(word_lower)
            code = "2"
            if tense == "past":
                code = "2.8"
            elif tense == "future":
                code = "2.9"

            return {
                "text": word,
                "code": code,
                "category": "VERB",
                "primary_category": "VERB",
                "is_verb": True,
                "tense": tense
            }

        # Check for adjectives (very basic heuristic)
        if self._is_likely_adjective(word_lower):
            return {
                "text": word,
                "code": "3",
                "category": "ADJECTIVE",
                "primary_category": "ADJECTIVE",
                "is_verb": False,
                "tense": None
            }

        # Check for adverbs (words ending in -ly)
        if word_lower.endswith("ly"):
            tense = self._detect_tense(word_lower)
            code = "1"
            if tense == "past":
                code = "1.8"
            elif tense == "future":
                code = "1.9"

            return {
                "text": word,
                "code": code,
                "category": "ADVERB",
                "primary_category": "ADVERB",
                "is_verb": False,
                "tense": tense
            }

        # Default: noun/fact or pronoun
        return {
            "text": word,
            "code": "7",
            "category": "FACT",
            "primary_category": "FACT",
            "is_verb": False,
            "tense": None
        }

    def _detect_tense(self, word: str) -> Optional[str]:
        """Detect if word indicates past or future tense"""
        word_lower = word.lower()

        # Past tense detection
        if word_lower in self.PAST_TENSE_VERBS:
            return "past"
        for suffix in self.PAST_TENSE_SUFFIXES:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix):
                return "past"

        # Future tense detection
        if word_lower in self.FUTURE_TENSE_MARKERS:
            return "future"
        if word_lower.endswith("ing") and word_lower not in {"being", "doing", "going"}:
            return "future"

        # Special cases
        if word_lower == "going":
            return "future"
        if word_lower == "yesterday":
            return "past"
        if word_lower in {"tomorrow", "tomorrow's", "soon"}:
            return "future"

        return None

    def _is_likely_verb(self, word: str) -> bool:
        """Basic heuristic for identifying verbs"""
        # Check for common verb endings or patterns
        verb_indicators = {"ate", "ify", "ize", "en"}
        for indicator in verb_indicators:
            if word.endswith(indicator):
                return True
        return False

    def _is_likely_adjective(self, word: str) -> bool:
        """Basic heuristic for identifying adjectives"""
        adjective_endings = {"ful", "less", "ous", "ive", "able", "ible", "al"}
        for ending in adjective_endings:
            if word.endswith(ending):
                return True
        return False

    def _apply_contextual_rules(self, tokens: List[Dict]) -> List[Dict]:
        """
        Apply contextual rules from documentation:
        - POSITION without LODIAL -> ADVERB
        - LODIAL without POSITION -> ADVERB
        - FACT (7) can ONLY exist when preceded by POSITION (5) + LODIAL (6)
        - FACT without 5,6 preceding it -> PRONOUN (4)
        """
        modified_tokens = []

        for i, token in enumerate(tokens):
            token_copy = token.copy()

            # Rule 1: POSITION without following LODIAL
            if token_copy["code"] == "5":
                if i + 1 < len(tokens) and tokens[i + 1]["code"] != "6":
                    token_copy["code"] = "1"
                    token_copy["category"] = "ADVERB"

            # Rule 2: LODIAL without preceding POSITION
            elif token_copy["code"] == "6":
                if i == 0 or tokens[i - 1]["code"] != "5":
                    token_copy["code"] = "1"
                    token_copy["category"] = "ADVERB"

            # Rule 3: FACT (7) can ONLY exist if preceded by POSITION (5) + LODIAL (6)
            elif token_copy["code"] == "7":
                # Check if preceded by 5,6 pattern
                if not (i >= 2 and tokens[i - 2]["code"] == "5" and tokens[i - 1]["code"] == "6"):
                    token_copy["code"] = "4"
                    token_copy["category"] = "PRONOUN"

            modified_tokens.append(token_copy)

        return modified_tokens

    def _check_for_facts(self, tokens: List[Dict]) -> bool:
        """
        Check if sentence contains 5,6,7 pattern (facts established)

        A fact is established by the sequence POSITION (5) > LODIAL (6) > FACT (7)
        """
        for i in range(len(tokens) - 2):
            # Look for 5,6,7 pattern
            if (tokens[i]["code"].startswith("5") and
                tokens[i + 1]["code"].startswith("6") and
                tokens[i + 2]["code"].startswith("7")):
                return True

        return False

    def _detect_modifications(self, tokens: List[Dict]) -> str:
        """
        Detect modification patterns showing how words relate to each other

        Returns a string representation of the modification chain
        """
        if not tokens:
            return ""

        # Build simple modification chain
        chain_parts = []
        for i, token in enumerate(tokens):
            code = token["code"].split(".")[0]  # Get base code
            chain_parts.append(code)

        # Analyze patterns
        modification_chain = " ".join(chain_parts)

        # Add directional indicators for common patterns
        # This is a simplified analysis
        if self._contains_pattern(chain_parts, ["5", "6", "7"]):
            modification_chain += " [POSITIONED-FACT-PATTERN: 5>6>7]"

        if self._contains_pattern(chain_parts, ["1", "2"]):
            modification_chain += " [ADVERB-MODIFIES-VERB: 1>2]"

        if self._contains_pattern(chain_parts, ["4", "1", "2"]):
            modification_chain += " [PRONOUN-ADVERB-VERB: 4<1>2]"

        return modification_chain

    def _contains_pattern(self, codes: List[str], pattern: List[str]) -> bool:
        """Check if codes contain a specific pattern"""
        for i in range(len(codes) - len(pattern) + 1):
            if codes[i:i + len(pattern)] == pattern:
                return True
        return False

    def _calculate_statistics(self, tokens: List[Dict], has_facts: bool) -> Dict:
        """Calculate statistics about the parsed text"""
        code_counts = {}
        tense_counts = {"present": 0, "past": 0, "future": 0}

        for token in tokens:
            code = token["code"].split(".")[0]
            code_counts[code] = code_counts.get(code, 0) + 1

            if token["tense"]:
                tense_counts[token["tense"]] += 1
            elif code not in ["8", "9"]:
                tense_counts["present"] += 1

        # Map codes to human-readable categories
        category_distribution = {}
        for code, count in code_counts.items():
            category = self.CODES.get(int(code), "UNKNOWN")
            category_distribution[category] = count

        return {
            "token_count": len(tokens),
            "code_distribution": code_counts,
            "category_distribution": category_distribution,
            "tense_distribution": tense_counts,
            "facts_established": has_facts,
            "communication_type": "FACT-COMMUNICATION" if has_facts else "FICTIONAL-COMMUNICATION"
        }


def parse_quantum_grammar(text: str) -> Dict:
    """
    Convenience function to parse text using Quantum Grammar

    Args:
        text: Input sentence to parse

    Returns:
        Dictionary containing parsed results
    """
    parser = QuantumGrammarParser()
    return parser.parse(text)
