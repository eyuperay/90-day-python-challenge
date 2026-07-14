#!/usr/bin/env python3
"""
Day 85 - NLP Sentiment Analysis
Sentiment analysis using TextBlob
"""

import os
from sentiment_analyzer import SentimentAnalyzer


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def demo_review_analysis():
    """Demonstrate sentiment analysis on reviews"""
    print_section("1. REVIEW SENTIMENT ANALYSIS")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_sample_reviews()
    analyzer.analyze_all()
    
    # Print summary
    analyzer.print_summary()
    
    # Show examples
    print("\nPositive sentences:")
    for s in analyzer.get_positive_sentences()[:3]:
        print(f"  + {s}")
    
    print("\nNegative sentences:")
    for s in analyzer.get_negative_sentences()[:3]:
        print(f"  - {s}")
    
    print("\nMost Positive:")
    for r in analyzer.get_most_positive(3):
        print(f"  {r['polarity']:.3f}: {r['sentence'][:60]}...")
    
    print("\nMost Negative:")
    for r in analyzer.get_most_negative(3):
        print(f"  {r['polarity']:.3f}: {r['sentence'][:60]}...")
    
    # Generate plots
    analyzer.generate_all_plots()
    analyzer.save_results('review_results.json')


def demo_tweet_analysis():
    """Demonstrate sentiment analysis on tweets"""
    print_section("2. TWEET SENTIMENT ANALYSIS")
    
    analyzer = SentimentAnalyzer()
    analyzer.load_sample_tweets()
    analyzer.analyze_all()
    
    analyzer.print_summary()
    analyzer.generate_all_plots()
    analyzer.save_results('tweet_results.json')


def demo_custom_text():
    """Demonstrate custom text analysis"""
    print_section("3. CUSTOM TEXT ANALYSIS")
    
    texts = [
        "This movie was fantastic! I loved every minute of it.",
        "The food was terrible and the service was even worse.",
        "The weather today is nice, I think I'll go outside.",
        "I'm so happy with my new phone, it's amazing!",
        "This is the worst product I've ever bought. Disgusting!",
        "The book was okay, nothing special but it was readable."
    ]
    
    analyzer = SentimentAnalyzer()
    
    print("\nAnalyzing custom texts:\n")
    results = analyzer.analyze_batch(texts)
    
    for result in results:
        emoji = '😊' if result['sentiment'] == 'positive' else '😡' if result['sentiment'] == 'negative' else '😐'
        print(f"  {emoji} {result['sentiment'].upper():10} | Polarity: {result['polarity']:.3f} | {result['text'][:50]}...")
    
    # Save results
    with open("output/custom_results.json", 'w', encoding='utf-8') as f:
        import json
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\n[OK] Results saved to: output/custom_results.json")


def demo_compare_texts():
    """Compare sentiment of different texts"""
    print_section("4. COMPARE TEXTS")
    
    texts = {
        "Positive Review": """
        I absolutely love this product! It exceeded all my expectations. 
        The quality is amazing and the customer service is fantastic. 
        I would recommend it to anyone looking for a great product.
        """,
        "Negative Review": """
        This product is terrible. It broke within a week and the customer 
        service refused to help. I wasted my money on this garbage. 
        Never buying from this company again.
        """,
        "Mixed Review": """
        The product itself is good but the shipping took forever. 
        The quality is decent but the price is too high. 
        I would recommend it if you can find it on sale.
        """
    }
    
    analyzer = SentimentAnalyzer()
    
    print("\nComparing different reviews:\n")
    print("-"*60)
    
    for name, text in texts.items():
        result = analyzer.analyze_text(text)
        emoji = '😊' if result['sentiment'] == 'positive' else '😡' if result['sentiment'] == 'negative' else '😐'
        print(f"  {name}:")
        print(f"    {emoji} Sentiment: {result['sentiment'].upper()}")
        print(f"    Polarity: {result['polarity']:.3f}")
        print(f"    Subjectivity: {result['subjectivity']:.3f}")
        print()


def demo_sentence_level():
    """Demonstrate sentence-level analysis"""
    print_section("5. SENTENCE-LEVEL ANALYSIS")
    
    text = """
    The hotel room was clean and comfortable. The staff were friendly and helpful. 
    However, the breakfast was terrible and the WiFi was very slow. 
    The location was perfect, close to all attractions. 
    I would stay here again despite the breakfast issues.
    """
    
    analyzer = SentimentAnalyzer()
    analyzer.load_custom_text(text)
    analyzer.analyze_all()
    
    print("\nSentence-by-sentence analysis:\n")
    for r in analyzer.results:
        emoji = '😊' if r['sentiment'] == 'positive' else '😡' if r['sentiment'] == 'negative' else '😐'
        print(f"  {emoji} Polarity: {r['polarity']:.3f} | {r['sentence'][:60]}...")
    
    analyzer.print_summary()
    analyzer.generate_all_plots()
    analyzer.save_results('sentence_results.json')


def print_summary():
    """Print summary"""
    print_section("SUMMARY")
    print("""
Sentiment Analysis - Key Concepts:

1. What is Sentiment Analysis?
   - Determining the emotional tone of text
   - Positive, Negative, or Neutral

2. Key Metrics:
   - Polarity: -1 (negative) to +1 (positive)
   - Subjectivity: 0 (factual) to 1 (opinion)

3. Applications:
   - Product reviews
   - Social media monitoring
   - Customer feedback
   - Market research

4. Tools Used:
   - TextBlob: Simple sentiment analysis
   - NLTK: Tokenization and NLP
   - Matplotlib/Seaborn: Visualization

5. Analysis Levels:
   - Document-level (entire text)
   - Sentence-level (each sentence)
   - Aspect-based (specific features)

6. Interpretation:
   - Polarity > 0.1: Positive
   - Polarity < -0.1: Negative
   - Otherwise: Neutral
    """)
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("[OK] Check the 'output' folder for results and plots")
    print("="*60 + "\n")


def main():
    print("=" * 60)
    print("DAY 85 - NLP SENTIMENT ANALYSIS")
    print("=" * 60 + "\n")
    
    print("This demo shows sentiment analysis using TextBlob.\n")
    
    demo_review_analysis()
    demo_tweet_analysis()
    demo_custom_text()
    demo_compare_texts()
    demo_sentence_level()
    
    print_summary()


if __name__ == "__main__":
    main()
