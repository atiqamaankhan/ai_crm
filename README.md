# AI-Powered CRM (Demo)

## Overview
Small demo CRM with:
- Flask web UI for customer CRUD
- Simple churn prediction (RandomForest)
- Text sentiment for customer feedback (TextBlob)
- SQLite backend

## Setup
1. Clone repo and `cd` into it.

2. Create virtual env (recommended) and install:
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Train model:
python train_model.py

4. Run web app:
python app.py

5. Open `http://127.0.0.1:5000/`

## Notes
- `train_model.py` will create a small synthetic dataset `sample_data.csv` and `churn_model.pkl`.
- Sentiment analysis uses TextBlob.
