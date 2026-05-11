SaaS Pricing Monitor

## Overview

SaaS Pricing Monitor is a complete end-to-end B2B data pipeline designed to help businesses monitor competitor SaaS pricing information automatically.

The system scrapes pricing data from publicly available SaaS pricing pages, cleans and standardizes the data, stores it in a database, and exposes business-friendly APIs for querying and analysis.

This project was built as part of a Data Engineering Intern take-home assignment focused on real-world pipeline engineering.

---

# B2B Problem Being Solved

Businesses frequently need competitor pricing intelligence to:

* Monitor pricing changes
* Compare feature offerings
* Detect pricing anomalies
* Analyze market positioning
* Support sales and strategic decision-making

Manually tracking SaaS pricing across multiple providers is time-consuming and unreliable.

This project automates the process by:

1. Scraping pricing pages
2. Cleaning and standardizing pricing data
3. Storing structured records
4. Providing API access for business users

The pipeline is dynamic and can continuously update as pricing changes over time.

---

# Features

## Scraper Layer

* Scrapes SaaS pricing pages
* Handles retries and request failures gracefully
* Handles missing fields safely
* Exports raw structured JSON data

## Cleaning & Transformation Layer

* Cleans inconsistent pricing formats
* Standardizes currencies and prices
* Handles missing values
* Converts features into structured records
* Stores cleaned data into database

## API Layer

FastAPI-powered endpoints:

* `/pricing`
* `/providers`
* `/health`
* `/anomalies`

## Automation

* Dockerized multi-service architecture
* One-command local setup
* Modular pipeline structure

## Bonus ML Layer

* Basic anomaly detection module
* Detects unusual pricing patterns

---

# Tech Stack

| Component        | Technology               |
| ---------------- | ------------------------ |
| Language         | Python                   |
| API Framework    | FastAPI                  |
| Scraping         | BeautifulSoup + Requests |
| Database         | SQLite / PostgreSQL      |
| Data Processing  | Pandas                   |
| ML               | Scikit-learn             |
| Containerization | Docker                   |
| Deployment       | Render                   |

---

# Project Structure

```text
coherent-saas-monitor/
│
├── api/                  # FastAPI application
├── scraper/              # Web scraping logic
├── cleaning/             # Data cleaning pipeline
├── pipeline/             # Scheduling / automation
├── ml/                   # ML anomaly detection
├── shared/               # Shared pipeline outputs
├── screenshots/          # Project screenshots
├── .env.example          # Environment variable template
├── docker-compose.yml    # Multi-container setup
└── README.md
```

---

# Data Sources

The scraper currently monitors:

* Notion Pricing
* Asana Pricing
* Trello Pricing

These sources were selected because they represent real SaaS competitors with publicly accessible pricing information.

---

# Pipeline Architecture

```text
Scraper → Raw JSON → Cleaning → Database → FastAPI Endpoints → Business User
```

### Step-by-step Flow

1. Scraper collects pricing data
2. Raw data exported as JSON
3. Cleaning layer standardizes formats
4. Cleaned data stored in database
5. FastAPI exposes business APIs
6. ML module analyzes pricing anomalies

---

# API Endpoints

## GET /pricing

Returns pricing information.

### Example

```bash
GET /pricing
```

### Optional Query Parameters

| Parameter | Description        |
| --------- | ------------------ |
| source    | SaaS provider name |
| plan      | Pricing plan name  |

---

## GET /providers

Returns all available SaaS providers.

---

## GET /health

Health check endpoint.

---

## GET /anomalies

Returns anomaly detection output.

---

# Environment Variables

Create a `.env` file using the template below.

```env
DATABASE_URL=sqlite:///data.db
RAW_FILE=/app/shared/raw_pricing.json
SCRAPER_SCHEDULE=*/30 * * * *
```

---

# Running the Project Locally

## Prerequisites

* Docker Desktop
* Git
* Python 3.10+

---

## Clone Repository

```bash
git clone https://github.com/Saikrish2004/coherent-saas-monitor.git
cd coherent-saas-monitor
```

---

## Start Pipeline

```bash
docker compose up --build
```

---

## Open API Docs

Local Swagger UI:

```text
http://localhost:8000/docs
```

---

# Live Deployment

Live API:

[https://coherent-saas-monitor.onrender.com/docs](https://coherent-saas-monitor.onrender.com/docs)
## Deployment Note
The application runs successfully in local Dockerized setup.
Render deployment was partially completed, but persistent SQLite handling on Render free tier caused runtime DB issues.

The full pipeline works locally using:
docker compose up --build

GitHub Repository:

[https://github.com/Saikrish2004/coherent-saas-monitor](https://github.com/Saikrish2004/coherent-saas-monitor)

---

# Cleaning Decisions

The following standardization decisions were implemented:

| Issue            | Solution                             |
| ---------------- | ------------------------------------ |
| Missing values   | Default placeholders used            |
| Currency symbols | Standardized extraction              |
| Price formats    | Converted to numeric floats          |
| Feature lists    | Converted to comma-separated strings |
| Invalid records  | Safely skipped with logging          |

---

# Error Handling

Implemented protections include:

* Retry logic for failed requests
* Graceful handling of missing fields
* Logging for scraper failures
* API exception handling
* Dockerized isolated services

---

# Automation

The pipeline is structured for automated execution.

Components are separated into:

* Scraper service
* Cleaning service
* API service
* Database service

Docker Compose orchestrates the full pipeline.

---

# ML / AI Layer

A lightweight anomaly detection module was added using Scikit-learn.

Purpose:

* Detect unusual pricing values
* Identify outlier pricing patterns
* Demonstrate intelligent business analytics capability

### Trade-offs Considered

* Simpler anomaly detection chosen due to assignment time constraints
* Focus prioritized on pipeline reliability and deployment

---

# Screenshots

Add screenshots in the `/screenshots` folder.

Recommended screenshots:

* Swagger API Docs
* Docker containers running
* Successful API responses
* Render deployment

---

# Challenges Faced

* Dynamic website HTML structures
* Cross-container file sharing
* Render deployment filesystem limitations
* SQLite path handling in cloud containers

These issues were debugged and documented throughout development.

---

# Future Improvements

Potential future enhancements:

* Scheduled cloud scraping
* PostgreSQL cloud database
* Historical trend tracking
* Dashboard UI
* Advanced ML forecasting
* More SaaS providers

---

# Submission Links

## GitHub Repository

[https://github.com/Saikrish2004/coherent-saas-monitor](https://github.com/Saikrish2004/coherent-saas-monitor)

## Live Deployment

[https://coherent-saas-monitor.onrender.com/docs](https://coherent-saas-monitor.onrender.com/docs)
## Deployment Note
The application runs successfully in local Dockerized setup.
Render deployment was partially completed, but persistent SQLite handling on Render free tier caused runtime DB issues.

The full pipeline works locally using:
docker compose up --build

---

# Author

Sai Krishna Elluru

GitHub:

[https://github.com/Saikrish2004](https://github.com/Saikrish2004)

<img width="1918" height="930" alt="swagger_docs" src="https://github.com/user-attachments/assets/d4d8bd24-b8e2-4f39-aad2-2f4de06d4659" />
<img width="1917" height="1017" alt="pricing_response" src="https://github.com/user-attachments/assets/0bed82b7-9b73-442e-af7d-6ab10a73d3ff" />
<img width="1918" height="1078" alt="docker_running" src="https://github.com/user-attachments/assets/2076d707-a324-4c26-bc5e-0ab5ce239a8a" />
<img width="462" height="372" alt="project_structure" src="https://github.com/user-attachments/assets/e06ff717-7fd9-4013-af11-635348b15b66" />

