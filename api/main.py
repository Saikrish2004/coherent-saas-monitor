from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd
import os

from ml_endpoint import router as ml_router

app = FastAPI(title="SaaS Pricing Monitor API")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")
engine = create_engine(DATABASE_URL)

# Create sample data if table doesn't exist
sample_data = pd.DataFrame([
    {
        "plan": "Free",
        "price": 0,
        "currency": "$",
        "features": "Basic features",
        "source": "Notion",
        "scraped_at": "2026-05-12"
    },
    {
        "plan": "Plus",
        "price": 10,
        "currency": "$",
        "features": "Advanced collaboration",
        "source": "Notion",
        "scraped_at": "2026-05-12"
    }
])

sample_data.to_sql("pricing", engine, if_exists="replace", index=False)


@app.get("/pricing")
def get_pricing(
    source: str = Query(None, description="SaaS provider name"),
    plan: str = Query(None, description="Plan name")
):
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


# ML router
app.include_router(ml_router)