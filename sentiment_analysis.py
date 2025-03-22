import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

# Download VADER if not available
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis
def analyze_sentiment(summary):
    sentiment_score = sia.polarity_scores(summary)
    compound = sentiment_score['compound']

    # Classify sentiment based on compound score
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, sentiment_score

# Function to perform comparative sentiment analysis
def compare_sentiments(articles):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sentiment_scores = []
    coverage_differences = []

    for article in articles:
        sentiment, scores = analyze_sentiment(article["summary"])
        article["sentiment"] = sentiment  # Append sentiment to article
        article["scores"] = scores  # Store scores
        sentiment_counts[sentiment] += 1
        sentiment_scores.append(scores['compound'])  # Store compound scores

    # Generate comparison insights
    if len(sentiment_scores) > 1:
        avg_sentiment = np.mean(sentiment_scores)
        
        if avg_sentiment > 0:
            overall_sentiment = "Mostly Positive"
        elif avg_sentiment < 0:
            overall_sentiment = "Mostly Negative"
        else:
            overall_sentiment = "Mixed Sentiment"

        # Compare sentiment variation
        max_sentiment = max(articles, key=lambda x: x['scores']['compound'])
        min_sentiment = min(articles, key=lambda x: x['scores']['compound'])
        
        coverage_differences.append({
            "Comparison": f"Article '{max_sentiment['title']}' is the most positive, while '{min_sentiment['title']}' is the most negative.",
            "Impact": "This suggests varying perspectives on the company’s latest events."
        })
    
    else:
        overall_sentiment = "Not enough data to compare."

    return sentiment_counts, overall_sentiment, coverage_differences
