from flask import Flask, render_template, request, send_file
import json
import os
import csv
from io import StringIO

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    news = load_data()
    ticker = request.args.get('ticker')
    sentiment = request.args.get('sentiment')

    if ticker:
        news = [item for item in news if item['ticker'] == ticker]
    if sentiment:
        news = [item for item in news if item['sentiment'].lower() == sentiment.lower()]

    tickers = sorted(set(item['ticker'] for item in load_data()))
    sentiments = ['Positive', 'Negative', 'Neutral']

    return render_template('index.html', news=news, tickers=tickers, sentiments=sentiments)

from io import BytesIO

@app.route('/export')
def export_csv():
    news = load_data()
    if not news:
        return "No data to export", 404

    # Create CSV string
    csv_string = StringIO()
    writer = csv.DictWriter(csv_string, fieldnames=news[0].keys())
    writer.writeheader()
    writer.writerows(news)

    # Convert to bytes
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
