from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
import os
import pandas as pd

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data.db")
engine = create_engine(DATABASE_URL)

@router.get("/anomalies")
def get_price_anomalies():
    query = "SELECT * FROM pricing ORDER BY scraped_at DESC LIMIT 500"
    df = pd.read_sql(query, engine)
    if df.empty or 'price' not in df.columns:
        raise HTTPException(status_code=404, detail="No pricing data available.")
    # Prepare data
    df = df.dropna(subset=["price"])
    if df.empty:
        raise HTTPException(status_code=404, detail="No valid price data.")
    from sklearn.ensemble import IsolationForest
    X = df[["price"]].values
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(X)
    anomalies = df[df["anomaly"] == -1]
    if anomalies.empty:
        return {"anomalies": []}
    return {"anomalies": anomalies.to_dict(orient="records")}
