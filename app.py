# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from crm_db import get_session, Customer
from models import load_churn_model, predict_churn_from_features, sentiment_of_text
import os
import datetime

app = Flask(__name__)
app.secret_key = "replace_with_a_secure_secret"

# DB session
session = get_session()

# Load churn model if available
churn_model = None
try:
    churn_model = load_churn_model()
except Exception as e:
    print("Churn model not loaded:", e)

@app.route("/")
def index():
    customers = session.query(Customer).all()
    return render_template("index.html", customers=customers)

@app.route("/add", methods=["GET","POST"])
def add_customer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        total_purchases = float(request.form.get("total_purchases") or 0)
        avg_session_time = float(request.form.get("avg_session_time") or 0)
        cust = Customer(
            name=name, email=email, phone=phone,
            total_purchases=total_purchases,
            avg_session_time=avg_session_time,
            last_activity=datetime.datetime.utcnow()
        )
        session.add(cust)
        session.commit()
        flash("Customer added", "success")
        return redirect(url_for("index"))
    return render_template("add_customer.html")

@app.route("/customer/<int:cust_id>")
def customer_detail(cust_id):
    cust = session.get(Customer, cust_id)
    churn_result = None
    if cust and churn_model:
        features = {
            "total_purchases": cust.total_purchases or 0.0,
            "avg_session_time": cust.avg_session_time or 0.0,
            "num_logins": 5.0,
            "days_since_last": (datetime.datetime.utcnow() - (cust.last_activity or datetime.datetime.utcnow())).days
        }
        pred, prob = predict_churn_from_features(churn_model, features)
        churn_result = {"pred": pred, "prob": prob, "features": features}
    return render_template("customer_detail.html", cust=cust, churn=churn_result)

@app.route("/analyze_sentiment", methods=["POST"])
def analyze_sentiment():
    text = request.form.get("feedback_text", "")
    label, polarity = sentiment_of_text(text)
    return {"sentiment": label, "polarity": polarity}

if __name__ == "__main__":
    # Make sure templates and static directories exist
    os.makedirs("static/plots", exist_ok=True)
    app.run(debug=True, port=5000)
