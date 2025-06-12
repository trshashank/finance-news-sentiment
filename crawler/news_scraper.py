import feedparser
import json
import time
import os

TICKERS = ['AAPL', 'MSFT', 'TSLA']  # Default tickers

DATA_FILE = 'crawler/data.json'
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


def update_all():
    print("🔁 Updating all tickers...")
    all_data = {}

    for ticker in TICKERS:
        print(f"Fetching {ticker}...")
        news = fetch_news_rss(ticker)
        all_data[ticker] = news
        time.sleep(1)

    with open(DATA_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)

    print("✅ All ticker data updated.\n")


def update_ticker(ticker):
    # Load current data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    else:
        data = {}

    # Fetch and update single ticker
    print(f"🔄 Refreshing {ticker}...")
    data[ticker] = fetch_news_rss(ticker)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ {ticker} updated.")


if __name__ == "__main__":
    update_all()
