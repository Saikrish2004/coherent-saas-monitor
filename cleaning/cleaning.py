import json
import re
import pandas as pd
import logging
from sqlalchemy import create_engine
import os
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")

# Shared Docker volume path
RAW_FILE = os.getenv("RAW_FILE", "/app/shared/raw_pricing.json")

# Standardize currency and price
CURRENCY_REGEX = re.compile(r"[\$€£]")
PRICE_REGEX = re.compile(r"[\d,.]+")


def clean_price(price_str):
    if not price_str:
        return None, None

    currency = None
    price = None

    try:
        currency_match = CURRENCY_REGEX.search(price_str)

        if currency_match:
            currency = currency_match.group()

        price_match = PRICE_REGEX.search(price_str.replace(",", ""))

        if price_match:
            price = float(price_match.group())

    except Exception as e:
        logging.warning(f"Failed to clean price '{price_str}': {e}")

    return currency, price


def clean_data(records):
    cleaned = []

    for rec in records:
        plan = rec.get("plan", "Unknown").strip()
        price_str = rec.get("price", "").strip()

        currency, price = clean_price(price_str)

        features = rec.get("features", [])
        source = rec.get("source", "Unknown")

        cleaned.append({
            "plan": plan,
            "price": price,
            "currency": currency,
            "features": ", ".join(features),
            "source": source,
            "scraped_at": datetime.utcnow().isoformat()
        })

    return cleaned


def wait_for_file(file_path, timeout=60):
    start = time.time()

    while not os.path.exists(file_path):
        if time.time() - start > timeout:
            raise FileNotFoundError(f"{file_path} not found after waiting.")

        print(f"Waiting for {file_path}...")
        time.sleep(2)


def main():
    # Wait for scraper output
    wait_for_file(RAW_FILE)

    # Load raw data
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    logging.info(f"Loaded {len(raw)} raw records")

    # Clean data
    cleaned = clean_data(raw)

    df = pd.DataFrame(cleaned)

    # Store in DB
    engine = create_engine(DATABASE_URL)

    df.to_sql("pricing", engine, if_exists="replace", index=False)

    logging.info(f"Inserted {len(df)} cleaned records into DB")

    # Export cleaned data
    df.to_csv("/app/shared/cleaned_pricing.csv", index=False)

    logging.info("Exported cleaned data to cleaned_pricing.csv")


if __name__ == "__main__":
    main()