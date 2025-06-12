from flask import Flask, render_template, request, send_file, redirect, url_for
import json
import os
import csv
from io import StringIO, BytesIO
from crawler.update_data import update_ticker  # Make sure this exists and works

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    data = load_data()
    ticker = request.args.get('ticker')
    sentiment = request.args.get('sentiment')

    # Flatten the data
    all_news = []
    for tk, news_list in data.items():
        all_news.extend(news_list)

    # Filtering
    if ticker:
        all_news = [item for item in all_news if item['ticker'] == ticker]
    if sentiment:
        all_news = [item for item in all_news if item.get('sentiment', '').lower() == sentiment.lower()]

    tickers = sorted(data.keys())
    sentiments = ['Positive', 'Negative', 'Neutral']

    return render_template('index.html', news=all_news, tickers=tickers, sentiments=sentiments)

@app.route('/refresh', methods=['POST'])
def refresh():
    ticker = request.form.get('ticker', '').upper()
    if not ticker:
        return redirect(url_for('index'))

    update_ticker(ticker)
    return redirect(url_for('index', ticker=ticker))

@app.route('/export')
def export_csv():
    data = load_data()
    all_news = []
    for tk, news_list in data.items():
        all_news.extend(news_list)

    if not all_news:
        return "No data to export", 404

    csv_string = StringIO()
    writer = csv.DictWriter(csv_string, fieldnames=all_news[0].keys())
    writer.writeheader()
    writer.writerows(all_news)

    mem = BytesIO()
    mem.write(csv_string.getvalue().encode('utf-8'))
    mem.seek(0)

    return send_file(
        mem,
        mimetype='text/csv',
        download_name='news_sentiment.csv',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
