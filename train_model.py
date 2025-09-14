# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
import nltk
from textblob import download_corpora as tb_download

# Ensure TextBlob corpora present (for sentiment, if used later)
try:
    nltk.data.find('tokenizers/punkt')
except:
    print("Downloading punkt...")
    nltk.download('punkt')
try:
    tb_download.download_all()
except Exception as e:
    print("TextBlob corpora download error (may still be fine):", e)

SAMPLE_CSV = "sample_data.csv"
MODEL_OUT = "churn_model.pkl"

def create_synthetic_dataset(n=500, seed=42):
    np.random.seed(seed)
    # features: total_purchases, avg_session_time, num_logins_last_30, days_since_last_activity
    total_purchases = np.round(np.random.exponential(scale=200, size=n), 2)
    avg_session_time = np.round(np.random.normal(loc=15, scale=5, size=n).clip(1), 2)
    num_logins = np.random.poisson(lam=5, size=n)
    days_since_last = np.random.exponential(scale=30, size=n).astype(int)
    # churn label: heuristics — high days_since_last and low purchases more likely churn
    churn_prob = (days_since_last / (days_since_last.max()+1)) * 0.6 + (1 - (total_purchases / (total_purchases.max()+1))) * 0.4
    churn = (churn_prob + np.random.normal(scale=0.05, size=n)) > 0.5
    df = pd.DataFrame({
        "total_purchases": total_purchases,
        "avg_session_time": avg_session_time,
        "num_logins": num_logins,
        "days_since_last": days_since_last,
        "churn": churn.astype(int)
    })
    df.to_csv(SAMPLE_CSV, index=False)
    print(f"Created synthetic dataset: {SAMPLE_CSV}")
    return df

def train_model(csv_path=SAMPLE_CSV):
    if not os.path.exists(csv_path):
        df = create_synthetic_dataset()
    else:
        df = pd.read_csv(csv_path)
    X = df.drop(columns=["churn"])
    y = df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=150, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    joblib.dump(clf, MODEL_OUT)
    print(f"Saved model to {MODEL_OUT}")

if __name__ == "__main__":
    train_model()
