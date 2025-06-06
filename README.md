# ForexFactory News API

This is a simple Flask-based API that fetches live economic news from ForexFactory (via XML) and evaluates whether each event is Bullish, Bearish, or Neutral based on actual, forecast, and previous values.

## Endpoints

- `/news`: Get parsed economic news with sentiment analysis.

## Deployment

Can be deployed on Render.com or similar.

## Example Usage

```bash
curl http://localhost:5000/news
```