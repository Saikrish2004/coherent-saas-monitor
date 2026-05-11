# SaaS Competitor Pricing Monitor

## Problem Statement
B2B SaaS companies need to monitor competitors’ pricing and feature changes to stay competitive. This pipeline scrapes public SaaS pricing pages, cleans and standardizes the data, stores it in a database, and exposes an API for business users to query the latest information.

## Repo Structure
```
my-b2b-pipeline/
├── README.md              ← Problem statement, setup, env vars
├── scraper/               ← Data collection logic
├── cleaning/              ← Cleaning + transformation scripts
├── pipeline/              ← Scheduler / automation
├── api/                   ← Deployed endpoint / interface
├── ml/                    ← Bonus: AI / ML layer (optional)
├── .env.example           ← Template for required env vars
└── docker-compose.yml     ← One-command setup (recommended)
```

## Setup
1. Clone the repo
2. Copy `.env.example` to `.env` and fill in values
3. Run `docker-compose up --build` (or see local setup instructions)

## Required Environment Variables
```
DATABASE_URL=sqlite:///data.db
SCRAPER_SCHEDULE=0 0 * * *  # daily at midnight
API_KEY=your_api_key_here   # if applicable
```


## Phases
- **Scraper:** Collects SaaS pricing data (handles pagination, errors, missing fields) **[Done]**
- **Cleaning:** Standardizes and cleans data, stores in DB **[Done]**
- **Pipeline:** Automated, scheduled runs **[Done]**
- **API:** Exposes endpoints for business users **[Done]**
- **ML (Bonus):** Price anomaly detection using Isolation Forest, with `/anomalies` API endpoint **[Done]**

## ML/AI Layer (Bonus)
This project includes an anomaly detection module using Isolation Forest to flag unusual SaaS pricing. The `/anomalies` endpoint in the API returns detected price anomalies, helping business users spot outliers or potential pricing errors.

**Why Isolation Forest?**
- Robust for unsupervised anomaly detection
- Works well with small and large datasets
- No need for labeled data

**Trade-offs:**
- Detects only statistical outliers (may miss context-specific anomalies)
- Simple, fast, and interpretable for business use

**Endpoint:**
- `GET /anomalies` — Returns recent pricing anomalies

---

---

## References
- [Assignment Brief](https://www.notion.so/Coherent-Market-Assignment-35d573730b5a808b99bfd04857479466?source=copy_link)
- [Assignment PDF](https://drive.google.com/file/d/1SzqG41CmrIxNzO3WCxkwyQ7-9emYtY8W/view?usp=drive_link)
