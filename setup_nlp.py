#!/usr/bin/env python3
"""
Setup script to download Stanza language models for the Diagrammatic app
Run this once after installing Python dependencies
"""

import stanza
import sys

# List of language codes to download models for
LANGUAGES = [
    'en',  # English
    'es',  # Spanish
    'fr',  # French
    'de',  # German
    'it',  # Italian
    'pt',  # Portuguese
    'ru',  # Russian
    'zh',  # Chinese
    'ja',  # Japanese
    'ar',  # Arabic
    'tr',  # Turkish
    'uk',  # Ukrainian
    'pl',  # Polish
    'nl',  # Dutch
    'sv',  # Swedish
    'vi',  # Vietnamese
    'th',  # Thai
    'hi',  # Hindi
]

def download_models():
    """Download Stanza models for all supported languages"""
    print(f"Downloading Stanza models for {len(LANGUAGES)} languages...")
    print("This may take several minutes depending on your internet connection.\n")

    failed = []
    for lang_code in LANGUAGES:
        try:
            print(f"Downloading {lang_code}...", end=" ", flush=True)
            stanza.download(lang_code, processors='tokenize,pos,lemma,depparse')
            print("✓")
        except Exception as e:
            print(f"✗ Failed: {e}")
            failed.append((lang_code, str(e)))

    print("\n" + "="*50)
    if failed:
        print(f"Failed to download {len(failed)} language(s):")
        for lang, error in failed:
            print(f"  - {lang}: {error}")
        print("\nYou can try downloading these manually later.")
    else:
        print("All models downloaded successfully!")
    print("="*50)

if __name__ == '__main__':
    download_models()
