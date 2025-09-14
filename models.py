# models.py
import joblib
import os
from textblob import TextBlob

MODEL_FILE = "churn_model.pkl"

def load_churn_model():
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(f"{MODEL_FILE} not found. Run `train_model.py` first.")
    clf = joblib.load(MODEL_FILE)
    return clf

def predict_churn_from_features(model, features_dict):
    """
    features_dict keys: total_purchases, avg_session_time, num_logins, days_since_last
    """
    import pandas as pd
    df = pd.DataFrame([features_dict])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1] if hasattr(model, "predict_proba") else None
    return int(pred), float(prob) if prob is not None else None

def sentiment_of_text(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1..1
    if polarity > 0.2:
        return "positive", polarity
    elif polarity < -0.2:
        return "negative", polarity
    else:
        return "neutral", polarity
