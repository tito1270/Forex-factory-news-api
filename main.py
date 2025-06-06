from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

def fetch_forex_factory_news():
    url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.xml"
    response = requests.get(url)
    news_data = []
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for event in root.findall("event"):
            currency = event.get("currency")
            impact = event.get("impact")
            forecast = event.get("forecast", "")
            previous = event.get("previous", "")
            actual = event.get("actual", "")
            date_str = event.get("date")
            time_str = event.get("time")
            timestamp = f"{date_str} {time_str}"
            sentiment = analyze_sentiment(actual, forecast, previous)
            news_data.append({
                "currency": currency,
                "time": timestamp,
                "impact": impact,
                "sentiment": sentiment
            })
    return news_data

def analyze_sentiment(actual, forecast, previous):
    try:
        a, f, p = float(actual), float(forecast), float(previous)
        if a > f and a > p:
            return "Bullish"
        elif a < f and a < p:
            return "Bearish"
        else:
            return "Neutral"
    except:
        return "Neutral"

@app.route("/news")
def news():
    data = fetch_forex_factory_news()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)