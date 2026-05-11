from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
import os
import pandas as pd

from ml_endpoint import router as ml_router

app = FastAPI(title="SaaS Pricing Monitor API")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../data.db")
engine = create_engine(DATABASE_URL)

@app.get("/pricing")
def get_pricing(source: str = Query(None, description="SaaS provider name"), plan: str = Query(None, description="Plan name")):
    query = "SELECT * FROM pricing"
    filters = []
    params = {}
    if source:
        filters.append("source = :source")
        params["source"] = source
    if plan:
        filters.append("plan = :plan")
        params["plan"] = plan
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY scraped_at DESC LIMIT 100"
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = [dict(row._mapping) for row in result]
    if not rows:
        raise HTTPException(status_code=404, detail="No data found")
    return rows

@app.get("/providers")
def get_providers():
    query = "SELECT DISTINCT source FROM pricing"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        providers = [row[0] for row in result]
    return {"providers": providers}

@app.get("/health")
def health():
    return {"status": "ok"}

# Mount ML router
app.include_router(ml_router)
