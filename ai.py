from transformers import pipeline

sentiment_model = None

def analyze_sentiment(text):
    global sentiment_model

    if sentiment_model is None:
        sentiment_model = pipeline("sentiment-analysis")

    result = sentiment_model(text)[0]
    return result['label']