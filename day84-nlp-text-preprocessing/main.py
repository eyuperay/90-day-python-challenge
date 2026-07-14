#!/usr/bin/env python3
"""
Day 84 - NLP Text Preprocessing
Demonstrates text preprocessing for NLP
"""

import os
from text_processor import TextProcessor


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_basic_cleaning():
    """Demonstrate basic text cleaning"""
    print_section("1. BASIC TEXT CLEANING")
    
    processor = TextProcessor()
    processor.load_sample_text('short')
    
    print("\nOriginal text:")
    print(f"  {processor.text}")
    
    processor.clean_text()
    print(f"\nAfter cleaning:")
    print(f"  {processor.text}")
    
    processor.remove_punctuation()
    print(f"\nAfter removing punctuation:")
    print(f"  {processor.text}")
    
    processor.remove_numbers()
    print(f"\nAfter removing numbers:")
    print(f"  {processor.text}")


def demo_tokenization():
    """Demonstrate tokenization"""
    print_section("2. TOKENIZATION")
    
    processor = TextProcessor()
    processor.load_sample_text('short')
    processor.clean_text()
    
    # Word tokenization
    processor.tokenize_words()
    print(f"\nWord tokens: {processor.tokens}")
    
    # Sentence tokenization
    sentences = processor.tokenize_sentences()
    print(f"\nSentences:")
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}. {sent}")


def demo_stopwords_removal():
    """Demonstrate stopword removal"""
    print_section("3. STOPWORD REMOVAL")
    
    processor = TextProcessor()
    processor.load_sample_text('short')
    processor.clean_text()
    processor.tokenize_words()
    
    print(f"\nTokens before stopword removal ({len(processor.tokens)}):")
    print(f"  {processor.tokens}")
    
    processor.remove_stopwords()
    print(f"\nTokens after stopword removal ({len(processor.cleaned_tokens)}):")
    print(f"  {processor.cleaned_tokens}")


def demo_stemming():
    """Demonstrate stemming"""
    print_section("4. STEMMING")
    
    words = ['running', 'ran', 'runner', 'runs', 'studying', 'studied', 'studies']
    processor = TextProcessor()
    processor.text = ' '.join(words)
    processor.tokenize_words()
    processor.remove_stopwords()
    
    print(f"\nOriginal words: {words}")
    
    stemmed = processor.stem_tokens()
    print(f"\nStemmed words: {stemmed}")


def demo_lemmatization():
    """Demonstrate lemmatization"""
    print_section("5. LEMMATIZATION")
    
    words = ['running', 'ran', 'runner', 'runs', 'studying', 'studied', 'studies']
    processor = TextProcessor()
    processor.text = ' '.join(words)
    processor.tokenize_words()
    processor.remove_stopwords()
    
    print(f"\nOriginal words: {words}")
    
    lemmatized = processor.lemmatize_tokens(pos='v')
    print(f"\nLemmatized words: {lemmatized}")


def demo_full_pipeline():
    """Demonstrate full preprocessing pipeline"""
    print_section("6. FULL PREPROCESSING PIPELINE")
    
    processor = TextProcessor()
    processor.load_sample_text('long')
    
    print("\nOriginal text (first 200 chars):")
    print(f"  {processor.text[:200]}...")
    
    processor.preprocess_pipeline(
        remove_punct=True,
        remove_stop=True,
        lemmatize=True
    )
    
    print("\nCleaned text (first 200 chars):")
    print(f"  {processor.text[:200]}...")


def demo_review_text():
    """Demonstrate on review text"""
    print_section("7. REVIEW TEXT PROCESSING")
    
    processor = TextProcessor()
    processor.load_sample_text('reviews')
    
    print("\nOriginal text (first 150 chars):")
    print(f"  {processor.text[:150]}...")
    
    # Preprocess
    processor.clean_text()
    processor.remove_punctuation()
    processor.remove_numbers()
    processor.remove_extra_whitespace()
    processor.tokenize_words()
    processor.remove_stopwords()
    processor.lemmatize_tokens()
    
    # Word frequency
    freq = processor.get_word_frequency(10)
    print("\nTop 10 most common words:")
    for word, count in freq:
        print(f"  {word}: {count}")
    
    # Summary
    processor.print_summary()
    
    # Save results
    processor.save_results('review_results.json')


def demo_word_frequency():
    """Demonstrate word frequency analysis"""
    print_section("8. WORD FREQUENCY ANALYSIS")
    
    processor = TextProcessor()
    processor.load_sample_text('long')
    
    # Preprocess
    processor.clean_text()
    processor.remove_punctuation()
    processor.remove_extra_whitespace()
    processor.tokenize_words()
    processor.remove_stopwords()
    
    # Get word frequency
    freq = processor.get_word_frequency(15)
    
    print("\nWord frequency distribution:")
    for word, count in freq:
        bar = '█' * (count // 2)
        print(f"  {word:15} {count:3} {bar}")


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
NLP Text Preprocessing - Key Concepts:

1. Text Cleaning:
   - Lowercase conversion
   - Remove punctuation
   - Remove numbers
   - Remove special characters
   - Remove extra whitespace

2. Tokenization:
   - Word tokenization (split into words)
   - Sentence tokenization (split into sentences)

3. Stopword Removal:
   - Remove common words (the, is, at, etc.)
   - Reduces noise in text

4. Stemming:
   - Reduce words to root form (running -> run)
   - Fast but can be imprecise

5. Lemmatization:
   - Reduce words to dictionary form (running -> run)
   - Slower but more accurate

6. Common Use Cases:
   - Sentiment analysis
   - Text classification
   - Machine translation
   - Information retrieval
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for results")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 84 - NLP TEXT PREPROCESSING")
    print("=" * 60 + "\n")
    
    print("This demo shows text preprocessing for NLP.")
    print("Downloading NLTK data (first time may take a moment)...\n")
    
    demo_basic_cleaning()
    demo_tokenization()
    demo_stopwords_removal()
    demo_stemming()
    demo_lemmatization()
    demo_full_pipeline()
    demo_review_text()
    demo_word_frequency()
    
    print_summary()


if __name__ == "__main__":
    main()
