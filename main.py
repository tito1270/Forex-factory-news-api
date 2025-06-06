from flask import Flask, jsonify, Response
import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "API is working!"  # <--- Para hindi na mag-404 si Render health check

def fetch_news():
    url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.xml"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch Forex Factory news")
    return response.content

def parse_and_analyze(xml_data):
    root = ET.fromstring(xml_data)
    currency_stats = defaultdict(list)

    for item in root.findall("event"):
        currency = item.find("currency").text
        impact = item.find("impact").text
        actual = item.find("actual").text
        forecast = item.find("forecast").text

        if impact in ("High", "Medium") and actual and forecast:
            try:
                actual_val = float(actual.replace("K", "000").replace("M", "000000").replace("%", ""))
                forecast_val = float(forecast.replace("K", "000").replace("M", "000000").replace("%", ""))
                if actual_val > forecast_val:
                    currency_stats[currency].append("Bullish")
                elif actual_val < forecast_val:
                    currency_stats[currency].append("Bearish")
                else:
                    currency_stats[currency].append("Neutral")
            except:
                continue

    final_result = {}
    for currency, signals in currency_stats.items():
        if not signals:
            final_result[currency] = "Neutral"
            continue
        score = signals.count("Bullish") - signals.count("Bearish")
        if score > 0:
            final_result[currency] = "Bullish"
        elif score < 0:
            final_result[currency] = "Bearish"
        else:
            final_result[currency] = "Neutral"

    return final_result

@app.route('/news')
def news_json():
    xml_data = fetch_news()
    result = parse_and_analyze(xml_data)
    return jsonify(result)

@app.route('/summary.txt')
def news_summary_txt():
    xml_data = fetch_news()
    result = parse_and_analyze(xml_data)

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M GMT")
    lines = [f"Date: {now}", ""]
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "NZD", "CHF", "CAD"]
    for c in currencies:
        sentiment = result.get(c, "Neutral")
        lines.append(f"{c} - {sentiment}")

    output = "\n".join(lines)
    return Response(output, mimetype="text/plain")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

