"""
Text Processor Module
NLP text preprocessing operations
"""

import re
import string
import nltk
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter
import json
import os
from typing import List, Dict, Tuple, Optional

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4', quiet=True)


class TextProcessor:
    """Text preprocessing operations for NLP"""
    
    def __init__(self):
        self.text = None
        self.tokens = []
        self.cleaned_tokens = []
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.results = {}
        
        os.makedirs("output", exist_ok=True)
    
    def load_text(self, text: str):
        """Load text for processing"""
        self.text = text
        print(f"[OK] Loaded text ({len(text)} characters)")
        return self
    
    def load_sample_text(self, sample: str = 'long'):
        """Load sample text"""
        if sample == 'short':
            self.text = """
            Natural Language Processing (NLP) is a field of artificial intelligence 
            that focuses on the interaction between computers and human language.
            """
        elif sample == 'reviews':
            self.text = """
            I absolutely loved this product! It was amazing and worked perfectly. 
            The quality was outstanding and the price was very reasonable. 
            I would definitely recommend it to everyone. 

            However, the customer service was terrible. They took forever to respond 
            and were very rude. I had to call multiple times just to get a simple answer. 
            The shipping was also very slow, it took over a week to arrive.

            Overall, I would give it 3 stars out of 5. The product itself is great, 
            but the company needs to improve their customer service and shipping speed.
            """
        else:  # long
            self.text = """
            Natural Language Processing (NLP) is a subfield of linguistics, computer science, 
            and artificial intelligence concerned with the interactions between computers and 
            human language, in particular how to program computers to process and analyze large 
            amounts of natural language data.

            The goal of NLP is to build systems that can understand, interpret, and generate 
            human language in a way that is both meaningful and useful. This includes tasks 
            such as machine translation, sentiment analysis, text summarization, and speech recognition.

            Challenges in NLP involve natural language understanding, which is often difficult 
            because human language is ambiguous, context-dependent, and constantly evolving. 
            For example, the same word can have different meanings depending on the context.

            Recent advances in deep learning and neural networks have significantly improved 
            the performance of NLP systems. Transformer-based models like BERT and GPT have 
            achieved state-of-the-art results on many NLP tasks.

            However, there are still many challenges to overcome, such as handling rare words, 
            understanding sarcasm and irony, and dealing with multilingual and low-resource languages.
            """
        
        print(f"[OK] Loaded sample text ({len(self.text)} characters)")
        return self
    
    def clean_text(self):
        """Clean text: lowercase, remove punctuation, extra spaces"""
        text = self.text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        self.text = text
        print("[OK] Text cleaned (lowercase, extra spaces removed)")
        return self
    
    def remove_punctuation(self):
        """Remove punctuation from text"""
        translator = str.maketrans('', '', string.punctuation)
        self.text = self.text.translate(translator)
        print("[OK] Punctuation removed")
        return self
    
    def remove_numbers(self):
        """Remove numbers from text"""
        self.text = re.sub(r'\d+', '', self.text)
        print("[OK] Numbers removed")
        return self
    
    def remove_special_chars(self):
        """Remove special characters"""
        self.text = re.sub(r'[^a-zA-Z\s]', '', self.text)
        print("[OK] Special characters removed")
        return self
    
    def remove_extra_whitespace(self):
        """Remove extra whitespace"""
        self.text = re.sub(r'\s+', ' ', self.text).strip()
        print("[OK] Extra whitespace removed")
        return self
    
    def tokenize_words(self):
        """Tokenize text into words"""
        self.tokens = word_tokenize(self.text)
        print(f"[OK] Word tokenization: {len(self.tokens)} tokens")
        return self
    
    def tokenize_sentences(self):
        """Tokenize text into sentences"""
        sentences = sent_tokenize(self.text)
        print(f"[OK] Sentence tokenization: {len(sentences)} sentences")
        return sentences
    
    def remove_stopwords(self):
        """Remove stopwords from tokens"""
        if not self.tokens:
            self.tokenize_words()
        
        self.cleaned_tokens = [word for word in self.tokens if word.lower() not in self.stop_words]
        print(f"[OK] Stopwords removed: {len(self.tokens)} -> {len(self.cleaned_tokens)} tokens")
        return self
    
    def stem_tokens(self):
        """Apply stemming to tokens"""
        if not self.cleaned_tokens:
            self.remove_stopwords()
        
        stemmed = [self.stemmer.stem(token) for token in self.cleaned_tokens]
        print(f"[OK] Stemming applied")
        return stemmed
    
    def lemmatize_tokens(self, pos: str = 'v'):
        """Apply lemmatization to tokens"""
        if not self.cleaned_tokens:
            self.remove_stopwords()
        
        lemmatized = [self.lemmatizer.lemmatize(token, pos=pos) for token in self.cleaned_tokens]
        print(f"[OK] Lemmatization applied (pos={pos})")
        return lemmatized
    
    def preprocess_pipeline(self, remove_punct: bool = True, 
                           remove_stop: bool = True,
                           lemmatize: bool = True):
        """Run full preprocessing pipeline"""
        print("\n[INFO] Running full preprocessing pipeline...")
        print("-"*50)
        
        original_length = len(self.text)
        print(f"Original text length: {original_length}")
        
        self.clean_text()
        if remove_punct:
            self.remove_punctuation()
        self.remove_numbers()
        self.remove_extra_whitespace()
        
        print(f"After cleaning: {len(self.text)}")
        
        self.tokenize_words()
        print(f"Tokens: {len(self.tokens)}")
        
        if remove_stop:
            self.remove_stopwords()
            print(f"After stopword removal: {len(self.cleaned_tokens)}")
        
        if lemmatize and self.cleaned_tokens:
            lemmatized = self.lemmatize_tokens()
            print(f"After lemmatization: {len(lemmatized)}")
        
        print("-"*50)
        print("[OK] Preprocessing complete!")
        
        self.results['preprocessing'] = {
            'original_length': original_length,
            'cleaned_length': len(self.text),
            'token_count': len(self.tokens),
            'cleaned_token_count': len(self.cleaned_tokens) if self.cleaned_tokens else 0
        }
        
        return self
    
    def get_word_frequency(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get word frequency distribution"""
        if not self.cleaned_tokens:
            self.remove_stopwords()
        
        freq = Counter(self.cleaned_tokens)
        return freq.most_common(top_n)
    
    def get_sentence_stats(self) -> Dict:
        """Get sentence statistics"""
        sentences = sent_tokenize(self.text)
        words = word_tokenize(self.text)
        
        return {
            'sentence_count': len(sentences),
            'word_count': len(words),
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(words))
        }
    
    def save_results(self, filename: str = "preprocessing_results.json"):
        """Save preprocessing results"""
        self.results['cleaned_text'] = self.text
        
        if self.tokens:
            self.results['tokens'] = self.tokens[:50]
        
        if self.cleaned_tokens:
            self.results['cleaned_tokens'] = self.cleaned_tokens[:50]
        
        self.results['word_frequency'] = self.get_word_frequency()
        self.results['sentence_stats'] = self.get_sentence_stats()
        
        with open(f"output/{filename}", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Results saved to: output/{filename}")
    
    def print_summary(self):
        """Print summary"""
        print("\n" + "="*50)
        print("TEXT PROCESSING SUMMARY")
        print("="*50)
        
        print(f"\nOriginal text length: {len(self.text)} characters")
        
        if self.tokens:
            print(f"Total tokens: {len(self.tokens)}")
        
        if self.cleaned_tokens:
            print(f"Tokens after stopword removal: {len(self.cleaned_tokens)}")
        
        stats = self.get_sentence_stats()
        print(f"\nSentence Statistics:")
        print(f"  Sentences: {stats['sentence_count']}")
        print(f"  Words: {stats['word_count']}")
        print(f"  Avg sentence length: {stats['avg_sentence_length']:.2f} words")
        print(f"  Unique words: {stats['unique_words']}")
        
        print("\nTop 10 most common words:")
        freq = self.get_word_frequency()
        for word, count in freq:
            print(f"  {word}: {count}")
        
        print("="*50)
