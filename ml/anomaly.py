import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy import create_engine
import os
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data.db")
engine = create_engine(DATABASE_URL)


def detect_price_anomalies():
    # Load latest pricing data
    query = "SELECT * FROM pricing ORDER BY scraped_at DESC LIMIT 500"
    df = pd.read_sql(query, engine)
    if df.empty or 'price' not in df.columns:
        logging.warning("No pricing data available for anomaly detection.")
        return None
    # Prepare data
    df = df.dropna(subset=["price"])  # Remove missing prices
    if df.empty:
        logging.warning("No valid price data for anomaly detection.")
        return None
    X = df[["price"]].values
    # Fit Isolation Forest
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(X)
    # Mark anomalies
    anomalies = df[df["anomaly"] == -1]
    if not anomalies.empty:
        anomalies.to_csv("price_anomalies.csv", index=False)
        logging.info(f"Detected {len(anomalies)} price anomalies. Exported to price_anomalies.csv.")
    else:
        logging.info("No price anomalies detected.")
    return anomalies


def main():
    detect_price_anomalies()

if __name__ == "__main__":
    main()
