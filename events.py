import subprocess
import os
import json
import sys

# from dotenv import load_dotenv

import games.wuwa.events as wuwa_events
import games.genshin.events as genshin_events
import games.star_rail.events as star_rail_events
import games.zzz.events as zzz_events
import games.endfield.events as endfield_events
# import database.database as db
# from helpers.time_delay import calculate_delay
# from helpers.log import Log
from datetime import datetime
from helpers.playwright import fetch_multiple_pages_sync

def start_api():
    pass

def run_scrapers():
    results = []

    # Define URLs for all games
    urls = {
        "Wuthering Waves": "https://game8.co/games/Wuthering-Waves/archives/453473",
        "Genshin Impact": "https://game8.co/games/Genshin-Impact/archives/301601",
        "Honkai: Star Rail": "https://game8.co/games/Honkai-Star-Rail/archives/408749",
        "Zenless Zone Zero": "https://game8.co/games/Zenless-Zone-Zero/archives/457176",
        "Arknights Endfield": "https://game8.co/games/Arknights-Endfield/archives/535443"
    }

    # Fetch all pages in a single browser session
    print("Fetching all game pages in single browser session...")
    fetched_pages = fetch_multiple_pages_sync(urls, wait_time=5000)

    # Map game names to scraper functions
    scraper_functions = [
        ("Wuthering Waves", wuwa_events.scrape_events),
        ("Genshin Impact", genshin_events.scrape_events),
        ("Honkai: Star Rail", star_rail_events.scrape_events),
        ("Zenless Zone Zero", zzz_events.scrape_events),
        ("Arknights Endfield", endfield_events.scrape_events)
    ]

    if os.environ.get("ENVIRONMENT") == "DEBUG":
        for game_name, scraper in scraper_functions:
            soup = fetched_pages.get(game_name)
            if soup:
                results.append(scraper(soup))
            else:
                print(f"{game_name}: Could not fetch page")
                results.append({"game": game_name, "event_name": "Data couldn't be fetched", "days_left": 0, "end_timestamp": 0})
    else:
        for game_name, scraper in scraper_functions:
            try:
                soup = fetched_pages.get(game_name)
                if soup:
                    results.append(scraper(soup))
                else:
                    print(f"{game_name}: Could not fetch page")
                    results.append({"game": game_name, "event_name": "Data couldn't be fetched", "days_left": 0, "end_timestamp": 0})
            except Exception as e:
                print(f"{game_name}: Data couldn't be fetched - {e}")
                results.append({"game": game_name, "event_name": "Data couldn't be fetched", "days_left": 0, "end_timestamp": 0})

    return results

if __name__ == "__main__":
    # load_dotenv()
    
    # if not db.check_table_exists('events'):
    #     db.migrate()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        print("Running in debug mode")
        os.environ["ENVIRONMENT"] = "DEBUG"
    else:
        os.environ["ENVIRONMENT"] = "PROD"

    start_api()

    # Check if results file exists and if it has been run today
    results_file = 'data/results.json'

    # if results file exists and has been run today (file modification timestamp check), load it instead of scraping again
    # but only if we aren't in debug mode
    if os.path.exists(results_file) and datetime.fromtimestamp(os.path.getmtime(results_file)).date() == datetime.now().date() and os.environ.get("ENVIRONMENT") != "DEBUG":
        with open(results_file) as f:
            results = json.load(f)
    else:
        results = run_scrapers()
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=4)
    # summerize days left per game
    # save results in file per day, so if i want to ask again i dont have to request it (pseudo cache)

    game_event_list = sorted(results, key=lambda x: x['days_left'])
    game_event_list = [f'• [{game["game"]}] {game["event_name"]}' + (f': <b>{game["days_left"]} days left</b> ({datetime.fromtimestamp(game["end_timestamp"]).strftime("%d. %b %Y")})' if game["days_left"] > 0 else '') for game in game_event_list]
    
    subprocess.run([
        'notify-send',
        '-t', '-1',
        '-u', 'critical', # -1 gets ignored so we have to force this here so the notification doesnt close itself but have to be closed manually
        '-a', 'Game Events Notifier',
        'Game Events Notifier',
        '\n'.join(game_event_list),
    ])