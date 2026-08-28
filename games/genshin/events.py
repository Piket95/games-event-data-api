from bs4 import BeautifulSoup
# import requests
# import mqtt
import re
from datetime import datetime

# import database.database as db
# from helpers.games import Game
# from config.environments import Environment
from helpers.log import Log
from classes.days_left_calculator import DaysLeftCalculator
from helpers.playwright import fetch_page_content_sync

def scrape_events(soup=None):
    """
    Scrape the Genshin events from the website.
    
    Args:
        soup (BeautifulSoup, optional): Pre-fetched BeautifulSoup object. If None, will fetch the page.
    """

    Log()('Scraping Genshin events...')
    
    if soup is None:
        Log()('Scraping website...')
        url_to_scrape = "https://game8.co/games/Genshin-Impact/archives/301601"
        # Use Playwright to fetch content for JavaScript-rendered pages
        soup = fetch_page_content_sync(url_to_scrape, wait_time=5000)

    # Find the ongoing events table with error handling
    header = soup.find('h3', {'class': 'a-header--3', 'id': 'hm_1'})
    if not header:
        Log()('Error: Could not find events header. HTML structure may have changed.')
        return {"game": "Genshin Impact", "event_name": "Data couldn't be fetched - HTML structure changed", "days_left": 0, "end_timestamp": 0}
    
    ongoing_events_table = header.find_next_sibling('table')
    if not ongoing_events_table:
        Log()('Error: Could not find events table. HTML structure may have changed.')
        return {"game": "Genshin Impact", "event_name": "Data couldn't be fetched - HTML structure changed", "days_left": 0, "end_timestamp": 0}

    # Find all table rows (skip the header row)
    rows = ongoing_events_table.find_all('tr')[1:]  # Skip first row (header)

    result = []

    for row in rows:
        # Get all cells in this row
        cells = row.find_all('td')
        
        if len(cells) >= 2:
            # First column: event name and link
            first_cell = cells[0]
            event_link = first_cell.find('a')
            event_name = event_link.get_text(strip=True) if event_link else first_cell.get_text(strip=True)
            
            # Second column: dates and requirements
            second_cell = cells[1]
            dates_text = second_cell.get_text(strip=True)
            
            # Extract dates using regex
            date_pattern = r'(\d{1,2}/\d{1,2})\s*-\s*(\d{1,2}/\d{1,2}|\w+\s+\d{1,2},\s+\d{4})'
            date_match = re.search(date_pattern, dates_text)
            
            if date_match:
                start_date_str = date_match.group(1)
                end_date_str = date_match.group(2)
                
                # Convert start date to timestamp
                start_date_year = datetime.now().year + (1 if datetime.strptime(start_date_str, '%m/%d').month < datetime.now().month else 0)
                start_date = datetime.strptime(f'{start_date_str}/{start_date_year}', '%m/%d/%Y')
                start_timestamp = int(start_date.timestamp())
                
                # Handle end date
                end_date_year = datetime.now().year + (1 if datetime.strptime(end_date_str, '%m/%d').month < datetime.now().month else 0)
                end_date = datetime.strptime(f'{end_date_str}/{end_date_year}', '%m/%d/%Y')
                end_timestamp = int(end_date.timestamp())
                end_date_display = end_date_str
                
                days_left = DaysLeftCalculator().calculate_days_left(end_date)
                
                result.append({
                    'game': 'Genshin Impact',
                    'event_name': event_name,
                    'dates_text': dates_text,
                    'start_timestamp': start_timestamp,
                    'start_date': start_date_str,
                    'end_timestamp': end_timestamp,
                    'end_date': end_date_display,
                    'days_left': days_left
                })
            else:
                result.append({
                    'game': 'Genshin Impact',
                    'event_name': event_name,
                    'dates_text': f"Could not parse dates from: {dates_text}",
                    'days_left': None,
                })

    Log()('Finished scraping Genshin events from game8.')
    
    # write results into a file in root
    with open('logs/events_genshin.txt', 'w', encoding='utf-8') as file:
        for element in result:
            file.write(str(element) + "\n")

    # Filter out entries where days_left is None or the end date is already passed
    result = DaysLeftCalculator().filter_events(result)
    
    # Return the entry with the least number of days left
    return min(result, key=lambda entry: entry.get('days_left', float('inf')))

if __name__ == "__main__":
    scrape_events()