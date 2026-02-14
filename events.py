import random
import time
import subprocess

# from dotenv import load_dotenv

import games.wuwa.events as wuwa_events
import games.genshin.events as genshin_events
import games.star_rail.events as star_rail_events
import games.zzz.events as zzz_events
import games.endfield.events as endfield_events
import database.database as db
from helpers.time_delay import calculate_delay
from helpers.log import Log

def start_api():
    pass

def run_scrapers():
    results = []

    results.append(wuwa_events.scrape_events())
    results.append(genshin_events.scrape_events())
    results.append(star_rail_events.scrape_events())
    results.append(zzz_events.scrape_events())
    results.append(endfield_events.scrape_events())

    return results

if __name__ == "__main__":
    # load_dotenv()
    
    # if not db.check_table_exists('events'):
    #     db.migrate()

    start_api()

    results = run_scrapers()
    # summerize days left per game
    # save results in file per day, so if i want to ask again i dont have to request it (pseudo cache)

    game_event_list = sorted(results, key=lambda x: x['days_left'])
    game_event_list = [f'• [{game["game"]}] {game["event_name"]}: <b>{game["days_left"]} days left</b> ({game["end_date"]})' for game in game_event_list]
        
    subprocess.run([
        'notify-send',
        '-t', '-1',
        '-u', 'critical', # -1 gets ignored so we have to force this here so the notification doesnt close itself but have to be closed manually
        '-a', 'Game Events Notifier',
        'Game Events Notifier',
        '\n'.join(game_event_list),
    ])