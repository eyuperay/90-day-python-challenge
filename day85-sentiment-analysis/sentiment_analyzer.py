"""
Sentiment Analyzer Module
Sentiment analysis using TextBlob and NLTK
"""

import re
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from collections import Counter
from typing import List, Dict, Tuple, Optional
import nltk

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


class SentimentAnalyzer:
    """Sentiment analysis using TextBlob"""
    
    def __init__(self):
        self.sentences = []
        self.results = []
        self.summary = {}
        self.positive_words = []
        self.negative_words = []
        self.neutral_words = []
        
        os.makedirs("output", exist_ok=True)
    
    # ==================== TEXT LOADING ====================
    
    def load_text(self, text: str):
        """Load text for analysis"""
        self.text = text
        self.sentences = [s.strip() for s in text.split('.') if s.strip()]
        print(f"[OK] Loaded text: {len(self.text)} characters, {len(self.sentences)} sentences")
        return self
    
    def load_sample_reviews(self):
        """Load sample reviews"""
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
        self.sentences = [s.strip() for s in self.text.split('.') if s.strip()]
        print(f"[OK] Loaded sample reviews: {len(self.sentences)} sentences")
        return self
    
    def load_sample_tweets(self):
        """Load sample tweets"""
        self.text = """
        I love this new update! It's amazing and so fast. Best app ever!
        This is terrible, the worst experience ever. I hate it.
        The weather today is nice. I think I will go for a walk.
        Can't believe how good this is! Absolutely fantastic!
        Worst customer service ever. Never buying from them again.
        The product is okay, nothing special but it works.
        """
        self.sentences = [s.strip() for s in self.text.split('.') if s.strip()]
        print(f"[OK] Loaded sample tweets: {len(self.sentences)} sentences")
        return self
    
    def load_custom_text(self, text: str):
        """Load custom text"""
        self.text = text
        self.sentences = [s.strip() for s in text.split('.') if s.strip()]
        return self
    
    # ==================== SENTIMENT ANALYSIS ====================
    
    def analyze_sentence(self, sentence: str) -> Dict:
        """Analyze sentiment of a single sentence"""
        blob = TextBlob(sentence)
        
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Extract words
        words = sentence.lower().split()
        
        return {
            'sentence': sentence,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment,
            'words': words,
            'word_count': len(words)
        }
    
    def analyze_all(self) -> List[Dict]:
        """Analyze all sentences"""
        self.results = []
        for sentence in self.sentences:
            if sentence:
                result = self.analyze_sentence(sentence)
                self.results.append(result)
        
        print(f"[OK] Analyzed {len(self.results)} sentences")
        return self.results
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze entire text"""
        blob = TextBlob(text)
        
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'sentiment': 'positive' if blob.sentiment.polarity > 0.1 else 'negative' if blob.sentiment.polarity < -0.1 else 'neutral'
        }
    
    # ==================== SUMMARY STATISTICS ====================
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        if not self.results:
            self.analyze_all()
        
        # Count sentiments
        sentiments = [r['sentiment'] for r in self.results]
        sentiment_counts = Counter(sentiments)
        
        # Average polarity and subjectivity
        avg_polarity = sum(r['polarity'] for r in self.results) / len(self.results) if self.results else 0
        avg_subjectivity = sum(r['subjectivity'] for r in self.results) / len(self.results) if self.results else 0
        
        # Extract positive, negative, neutral words
        positive_words = []
        negative_words = []
        neutral_words = []
        
        for r in self.results:
            if r['sentiment'] == 'positive':
                positive_words.extend(r['words'])
            elif r['sentiment'] == 'negative':
                negative_words.extend(r['words'])
            else:
                neutral_words.extend(r['words'])
        
        self.positive_words = positive_words
        self.negative_words = negative_words
        self.neutral_words = neutral_words
        
        self.summary = {
            'total_sentences': len(self.results),
            'sentiment_counts': dict(sentiment_counts),
            'avg_polarity': avg_polarity,
            'avg_subjectivity': avg_subjectivity,
            'positive_words_count': len(positive_words),
            'negative_words_count': len(negative_words),
            'neutral_words_count': len(neutral_words),
            'positive_percentage': (sentiment_counts.get('positive', 0) / len(self.results)) * 100 if self.results else 0,
            'negative_percentage': (sentiment_counts.get('negative', 0) / len(self.results)) * 100 if self.results else 0,
            'neutral_percentage': (sentiment_counts.get('neutral', 0) / len(self.results)) * 100 if self.results else 0
        }
        
        return self.summary
    
    def print_summary(self):
        """Print summary"""
        if not self.summary:
            self.get_summary()
        
        print("\n" + "="*50)
        print("SENTIMENT ANALYSIS SUMMARY")
        print("="*50)
        
        print(f"\nTotal Sentences Analyzed: {self.summary['total_sentences']}")
        
        print(f"\nSentiment Distribution:")
        print(f"  Positive: {self.summary['sentiment_counts'].get('positive', 0)} ({self.summary['positive_percentage']:.1f}%)")
        print(f"  Negative: {self.summary['sentiment_counts'].get('negative', 0)} ({self.summary['negative_percentage']:.1f}%)")
        print(f"  Neutral:  {self.summary['sentiment_counts'].get('neutral', 0)} ({self.summary['neutral_percentage']:.1f}%)")
        
        print(f"\nAverage Polarity: {self.summary['avg_polarity']:.3f} (range: -1 to 1)")
        print(f"Average Subjectivity: {self.summary['avg_subjectivity']:.3f} (range: 0 to 1)")
        
        print(f"\nWord Counts:")
        print(f"  Positive words: {self.summary['positive_words_count']}")
        print(f"  Negative words: {self.summary['negative_words_count']}")
        print(f"  Neutral words:  {self.summary['neutral_words_count']}")
        
        print("="*50)
    
    # ==================== DETAILED RESULTS ====================
    
    def get_positive_sentences(self) -> List[str]:
        """Get positive sentences"""
        return [r['sentence'] for r in self.results if r['sentiment'] == 'positive']
    
    def get_negative_sentences(self) -> List[str]:
        """Get negative sentences"""
        return [r['sentence'] for r in self.results if r['sentiment'] == 'negative']
    
    def get_neutral_sentences(self) -> List[str]:
        """Get neutral sentences"""
        return [r['sentence'] for r in self.results if r['sentiment'] == 'neutral']
    
    def get_most_positive(self, n: int = 5) -> List[Dict]:
        """Get most positive sentences"""
        sorted_results = sorted(self.results, key=lambda x: x['polarity'], reverse=True)
        return sorted_results[:n]
    
    def get_most_negative(self, n: int = 5) -> List[Dict]:
        """Get most negative sentences"""
        sorted_results = sorted(self.results, key=lambda x: x['polarity'])
        return sorted_results[:n]
    
    # ==================== VISUALIZATIONS ====================
    
    def plot_sentiment_distribution(self, filename: str = "sentiment_distribution.png"):
        """Plot sentiment distribution"""
        if not self.summary:
            self.get_summary()
        
        sentiments = ['Positive', 'Negative', 'Neutral']
        counts = [
            self.summary['sentiment_counts'].get('positive', 0),
            self.summary['sentiment_counts'].get('negative', 0),
            self.summary['sentiment_counts'].get('neutral', 0)
        ]
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(sentiments, counts, color=colors, edgecolor='black')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(count), ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.title('Sentiment Distribution', fontsize=16)
        plt.ylabel('Number of Sentences', fontsize=12)
        plt.ylim(0, max(counts) * 1.2 if counts else 10)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Sentiment distribution saved to: output/{filename}")
    
    def plot_polarity_distribution(self, filename: str = "polarity_distribution.png"):
        """Plot polarity distribution"""
        if not self.results:
            self.analyze_all()
        
        polarities = [r['polarity'] for r in self.results]
        
        plt.figure(figsize=(10, 6))
        plt.hist(polarities, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Neutral (0)')
        plt.axvline(x=0.1, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Positive threshold')
        plt.axvline(x=-0.1, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Negative threshold')
        
        plt.xlabel('Polarity Score', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Polarity Distribution', fontsize=16)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Polarity distribution saved to: output/{filename}")
    
    def plot_sentiment_pie(self, filename: str = "sentiment_pie.png"):
        """Plot sentiment pie chart"""
        if not self.summary:
            self.get_summary()
        
        sentiments = ['Positive', 'Negative', 'Neutral']
        counts = [
            self.summary['sentiment_counts'].get('positive', 0),
            self.summary['sentiment_counts'].get('negative', 0),
            self.summary['sentiment_counts'].get('neutral', 0)
        ]
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        
        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=sentiments, colors=colors, autopct='%1.1f%%', 
                startangle=90, explode=(0.05, 0.05, 0.05))
        plt.title('Sentiment Distribution', fontsize=16)
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Sentiment pie chart saved to: output/{filename}")
    
    def plot_word_cloud(self, filename: str = "word_cloud.png"):
        """Plot word cloud (simple version)"""
        # Simple word frequency bar chart instead of word cloud
        if not self.results:
            self.analyze_all()
        
        all_words = []
        for r in self.results:
            all_words.extend(r['words'])
        
        word_freq = Counter(all_words)
        common_words = word_freq.most_common(15)
        
        if not common_words:
            print("[INFO] No words to display")
            return
        
        words, counts = zip(*common_words)
        
        plt.figure(figsize=(12, 6))
        plt.bar(words, counts, color='#2c3e50', edgecolor='black')
        plt.xlabel('Words', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Most Common Words', fontsize=16)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'output/{filename}')
        plt.close()
        print(f"[OK] Word frequency chart saved to: output/{filename}")
    
    def generate_all_plots(self):
        """Generate all plots"""
        self.plot_sentiment_distribution()
        self.plot_polarity_distribution()
        self.plot_sentiment_pie()
        self.plot_word_cloud()
        print("[OK] All plots generated")
    
    # ==================== SAVE RESULTS ====================
    
    def save_results(self, filename: str = "sentiment_results.json"):
        """Save results to JSON"""
        if not self.summary:
            self.get_summary()
        
        data = {
            'summary': self.summary,
            'results': self.results,
            'positive_sentences': self.get_positive_sentences(),
            'negative_sentences': self.get_negative_sentences(),
            'neutral_sentences': self.get_neutral_sentences(),
            'most_positive': self.get_most_positive(5),
            'most_negative': self.get_most_negative(5)
        }
        
        with open(f"output/{filename}", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Results saved to: output/{filename}")
    
    # ==================== BATCH ANALYSIS ====================
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts"""
        results = []
        for text in texts:
            result = self.analyze_text(text)
            results.append({
                'text': text,
                'polarity': result['polarity'],
                'subjectivity': result['subjectivity'],
                'sentiment': result['sentiment']
            })
        return results
