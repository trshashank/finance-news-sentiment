import feedparser
import json
import time

# Stock tickers
TICKERS = ['AAPL', 'MSFT', 'TSLA']

# Yahoo RSS feed base URL
RSS_URL = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US'

def fetch_news_rss(ticker):
    url = RSS_URL.format(ticker)
    feed = feedparser.parse(url)
    news_items = []

    for entry in feed.entries:
        news_items.append({
            'ticker': ticker,
            'headline': entry.title,
            'link': entry.link,
            'timestamp': entry.published if 'published' in entry else 'N/A',
        })

    return news_items

def run_scraper():
    all_news = []
    for ticker in TICKERS:
        print(f"🔍 Fetching news for {ticker}...")
        news = fetch_news_rss(ticker)
        print(f"✅ {len(news)} items found.")
        all_news.extend(news)
        time.sleep(1)  # avoid hitting feed too fast

    # Save output
    with open('crawler/data.json', 'w') as f:
        json.dump(all_news, f, indent=2)

    print(f"\n🎉 Done. Saved {len(all_news)} news items to crawler/data.json")

if __name__ == "__main__":
    run_scraper()
