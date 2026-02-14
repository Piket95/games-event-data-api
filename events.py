import random
import time
import subprocess

# from dotenv import load_dotenv

import games.wuwa.events as wuwa_events
import database.database as db
from helpers.time_delay import calculate_delay
from helpers.log import Log

def start_api():
    pass

def run_scrapers():
    return wuwa_events.scrape_events()

if __name__ == "__main__":
    # load_dotenv()
    
    # if not db.check_table_exists('events'):
    #     db.migrate()

    start_api()

    result = []
    result.append(run_scrapers())
    # summerize days left per game
    # save results in file per day, so if i want to ask again i dont have to request it (pseudo cache)

    game_event_list = sorted(result, key=lambda x: x['days_left'])
    game_event_list = [f'{game["event_name"]}: {game["days_left"]} days left ({game["end_date"]})' for game in game_event_list]
        
    subprocess.run([
        'notify-send',
        '-t', '10000',
        '-a', 'Game Events Scraper',
        'Game Events Scraper',
        '\n'.join(game_event_list),
    ])