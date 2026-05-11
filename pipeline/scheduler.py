import os
import subprocess
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

logging.basicConfig(level=logging.INFO)

SCRAPER_SCRIPT = os.getenv("SCRAPER_SCRIPT", "../scraper/scraper.py")
CLEANING_SCRIPT = os.getenv("CLEANING_SCRIPT", "../cleaning/cleaning.py")
SCHEDULE = os.getenv("SCRAPER_SCHEDULE", "0 0 * * *")  # Default: daily at midnight


def run_script(script_path):
    try:
        logging.info(f"Running {script_path} at {datetime.now()}")
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        logging.error(f"Failed to run {script_path}: {e}")


def pipeline_job():
    run_script(SCRAPER_SCRIPT)
    run_script(CLEANING_SCRIPT)


def main():
    scheduler = BlockingScheduler()
    # Run immediately on start
    pipeline_job()
    # Schedule future runs
    scheduler.add_job(pipeline_job, 'cron', **parse_cron(SCHEDULE))
    logging.info(f"Scheduled pipeline with cron: {SCHEDULE}")
    scheduler.start()


def parse_cron(cron_str):
    # Converts cron string to APScheduler args
    fields = cron_str.strip().split()
    if len(fields) != 5:
        raise ValueError("Invalid cron format. Use 'min hour day month weekday'")
    return {
        'minute': fields[0],
        'hour': fields[1],
        'day': fields[2],
        'month': fields[3],
        'day_of_week': fields[4]
    }

if __name__ == "__main__":
    main()
