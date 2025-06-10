import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load existing scraped news
with open('crawler/data.json', 'r') as f:
    news_data = json.load(f)

# Set up VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.3:
        return "Positive"
    elif score <= -0.3:
        return "Negative"
    else:
        return "Neutral"

# Add sentiment to each news item
for item in news_data:
    sentiment = classify_sentiment(item['headline'])
    item['sentiment'] = sentiment

# Save the new data with sentiment
with open('crawler/data.json', 'w') as f:
    json.dump(news_data, f, indent=2)

print(f"✅ Added sentiment to {len(news_data)} items.")
