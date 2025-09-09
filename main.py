import random
import time

from dotenv import load_dotenv

import wuwa_codes
import database.database as db
from helpers.time_delay import calculate_delay

def run_scrapers():
    wuwa_codes.scrape_codes()

if __name__ == "__main__":
    load_dotenv()
    
    if not db.check_table_codes_existing():
        db.migrate()

    time.sleep(calculate_delay())

    while True:
        run_scrapers()

        time.sleep(calculate_delay())