import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)

# Example SaaS pricing pages to scrape (can be extended)
SITES = [
    {
        "name": "Notion",
        "url": "https://www.notion.so/pricing"
    },
    {
        "name": "Asana",
        "url": "https://asana.com/pricing"
    },
    {
        "name": "Trello",
        "url": "https://trello.com/pricing"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SaaSMonitorBot/1.0)"
}


def fetch_page(url: str, retries: int = 3, delay: int = 2) -> str:
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logging.warning(f"Error fetching {url}: {e}. Retry {attempt+1}/{retries}")
            time.sleep(delay)
    return ""


def parse_notion(html: str) -> List[Dict[str, Any]]:
    # Notion pricing is in articles with class containing 'PricingPlanCard'
    soup = BeautifulSoup(html, "html.parser")
    plans = []
    for article in soup.find_all('article', class_=lambda x: x and 'PricingPlanCard' in x):
        try:
            # Extract plan name
            name_tag = article.find('h3', class_=lambda x: x and 'PricingPlanCard_heading' in x)
            name = name_tag.get_text(strip=True) if name_tag else None

            # Extract price
            price_tag = article.find('div', class_=lambda x: x and 'PricingPlanCard_pricingWrap' in x)
            price = price_tag.get_text(strip=True) if price_tag else None

            # Extract features from description
            desc_tag = article.find('p', class_=lambda x: x and 'PricingPlanCard_description' in x)
            desc = desc_tag.get_text(strip=True) if desc_tag else ""
            # Split description into features by periods and clean
            features = [f.strip() for f in desc.split('.') if f.strip()]

            if name and price:
                plans.append({
                    "plan": name,
                    "price": price,
                    "features": features
                })
        except Exception as e:
            logging.warning(f"Missing field in Notion card: {e}")
    return plans


def parse_asana(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    plans = []
    for card in soup.find_all(class_="PricingPlanCard"):
        try:
            name = card.find(class_="PricingPlanCard__title").get_text(strip=True)
            price = card.find(class_="PricingPlanCard__price").get_text(strip=True)
            features = [li.get_text(strip=True) for li in card.find_all("li")]
            plans.append({
                "plan": name,
                "price": price,
                "features": features
            })
        except Exception as e:
            logging.warning(f"Missing field in Asana card: {e}")
    return plans


def parse_trello(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    plans = []
    for card in soup.find_all(class_="plan-details"):
        try:
            name = card.find(class_="plan-title").get_text(strip=True)
            price = card.find(class_="plan-price").get_text(strip=True)
            features = [li.get_text(strip=True) for li in card.find_all("li")]
            plans.append({
                "plan": name,
                "price": price,
                "features": features
            })
        except Exception as e:
            logging.warning(f"Missing field in Trello card: {e}")
    return plans


def scrape_all_sites() -> List[Dict[str, Any]]:
    all_data = []
    for site in SITES:
        html = fetch_page(site["url"])
        if not html:
            logging.error(f"Failed to fetch {site['name']} page.")
            continue
        if site["name"] == "Notion":
            plans = parse_notion(html)
        elif site["name"] == "Asana":
            plans = parse_asana(html)
        elif site["name"] == "Trello":
            plans = parse_trello(html)
        else:
            plans = []
        for plan in plans:
            plan["source"] = site["name"]
        all_data.extend(plans)
    return all_data


def export_to_json(data: List[Dict[str, Any]], filename: str = "/app/shared/raw_pricing.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info(f"Exported {len(data)} records to {filename}")


def main():
    data = scrape_all_sites()
    export_to_json(data)

if __name__ == "__main__":
    main()
