from bs4 import BeautifulSoup
import requests
# import mqtt
import os
import re
from datetime import datetime

# import database.database as db
# from helpers.games import Game
from config.environments import Environment
from helpers.log import Log

def scrape_events():
    """
    Scrape the WuWa events from the website.
    """

    Log()('Scraping WuWa events...')
    Log()('Scraping website...')
    url_to_scrape = "https://game8.co/games/Wuthering-Waves/archives/453473"

    response = requests.get(url_to_scrape)
    soup = BeautifulSoup(response.text, 'html.parser')

    ongoing_events_table = soup.find('h3', {'class': 'a-header--3', 'id': 'hm_1'}).find_next_sibling('table')

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
            event_url = event_link.get('href') if event_link else None
            
            # Second column: dates and requirements
            second_cell = cells[1]
            dates_text = second_cell.get_text(strip=True)
            
            # Extract dates using regex
            date_pattern = r'(\w+ \d+, \d+)\s*-\s*(\w+ \d+, \d+|Permanent)'
            date_match = re.search(date_pattern, dates_text)
            
            if date_match:
                start_date_str = date_match.group(1)
                end_date_str = date_match.group(2)
                
                # Convert start date to timestamp
                start_date = datetime.strptime(start_date_str, '%B %d, %Y')
                start_timestamp = int(start_date.timestamp())
                
                # Handle end date
                if end_date_str == 'Permanent':
                    continue
                    end_timestamp = None
                    end_date_display = 'Permanent'
                else:
                    end_date = datetime.strptime(end_date_str, '%B %d, %Y')
                    end_timestamp = int(end_date.timestamp())
                    end_date_display = end_date_str
                
                days_left = (end_date - datetime.now()).days + 1
                
                result.append({
                    'game': 'Wuthering Waves',
                    'event_name': event_name,
                    'event_url': event_url,
                    'dates_text': dates_text,
                    'start_timestamp': start_timestamp,
                    'start_date': start_date_str,
                    'end_timestamp': end_timestamp,
                    'end_date': end_date_display,
                    'days_left': days_left
                })

                
            else:
                result.append({
                    'game': 'Wuthering Waves',
                    'event_name': event_name,
                    'event_url': event_url,
                    'dates_text': f"Could not parse dates from: {dates_text}",
                    'days_left': None,
                })

    Log()('Finished scraping WuWa events from game8.')
    
    # write results into a file in root
    with open('logs/events_wuwa.txt', 'w', encoding='utf-8') as file:
        for element in result:
            file.write(str(element) + "\n")

    # Filter out entries where days_left is None or the end date is already passed
    result = [entry for entry in result if entry['days_left'] is not None and (entry['end_timestamp'] is None or entry['end_timestamp'] > int(datetime.now().timestamp()))]
    
    # Return the entry with the least number of days left
    return min(result, key=lambda entry: entry.get('days_left', float('inf')))

if __name__ == "__main__":
    scrape_events()