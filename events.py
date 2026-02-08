import random
import time

from dotenv import load_dotenv

import games.wuwa.codes as wuwa_codes
import database.database as db
from helpers.time_delay import calculate_delay
from helpers.log import Log

def start_api():
    pass

def run_scrapers():
    wuwa_codes.scrape_codes()

if __name__ == "__main__":
    load_dotenv()
    
    if not db.check_table_exists('events'):
        db.migrate()

    start_api()

    while True:
        run_scrapers()

        delay = calculate_delay()
        next_execution_time = time.time() + delay
        next_execution_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(next_execution_time))
        Log()('Next execution: \033[1m' + next_execution_time_formatted + '\033[0m')
        time.sleep(delay)