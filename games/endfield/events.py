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
from classes.days_left_calculator import DaysLeftCalculator

def scrape_events():
    """
    Scrape the Endfield events from the website.
    """

    Log()('Scraping Endfield events...')
    Log()('Scraping website...')
    url_to_scrape = "https://game8.co/games/Arknights-Endfield/archives/535443"

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
            
            # Second column: dates and requirements
            second_cell = cells[1]
            dates_text = second_cell.get_text(strip=True)
            
            # Extract dates using regex - look for date pattern in the dates text
            date_pattern = r'(\d{1,2}\/\d{1,2}\/\d{2,4})\s*-\s*(\d{1,2}\/\d{1,2}\/\d{2,4})'
            date_match = re.search(date_pattern, dates_text)
            
            if date_match:
                start_date_str = date_match.group(1)
                end_date_str = date_match.group(2)
                
                # Clean up dates_text by removing everything after the second date
                dates_clean = re.sub(r'(\d{1,2}\/\d{1,2}\/\d{2,4})\s*-\s*(\d{1,2}\/\d{1,2}\/\d{2,4}).*', r'\1 - \2', dates_text)
                
                # Convert start date to timestamp - handle 2-digit and 4-digit years
                if '/' in start_date_str and len(start_date_str.split('/')[-1]) == 2:
                    # Format: MM/DD/YY (2-digit year)
                    start_date = datetime.strptime(start_date_str, '%m/%d/%y')
                else:
                    # Format: MM/DD/YYYY (4-digit year)
                    start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
                start_timestamp = int(start_date.timestamp())
                
                # Handle end date
                if '/' in end_date_str and len(end_date_str.split('/')[-1]) == 2:
                    # Format: MM/DD/YY (2-digit year)
                    end_date = datetime.strptime(end_date_str, '%m/%d/%y')
                else:
                    # Format: MM/DD/YYYY (4-digit year)
                    end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
                end_timestamp = int(end_date.timestamp())
                end_date_display = end_date_str
                
                days_left = DaysLeftCalculator().calculate_days_left(end_date)
                
                result.append({
                    'game': 'Arknights Endfield',
                    'event_name': event_name,
                    'dates_text': dates_clean,
                    'start_timestamp': start_timestamp,
                    'start_date': start_date_str,
                    'end_timestamp': end_timestamp,
                    'end_date': end_date_display,
                    'days_left': days_left
                })
            else:
                result.append({
                    'game': 'Arknights Endfield',
                    'event_name': event_name,
                    'dates_text': f"Could not parse dates from: {dates_text}",
                    'days_left': None,
                })

    Log()('Finished scraping Endfield events from game8.')
    
    # write results into a file in root
    with open('logs/events_endfield.txt', 'w', encoding='utf-8') as file:
        for element in result:
            file.write(str(element) + "\n")
    
    # Filter out entries where days_left is None or the end date is already passed
    result = DaysLeftCalculator().filter_events(result)
    
    # Return the entry with the least number of days left
    return min(result, key=lambda entry: entry.get('days_left', float('inf')))

if __name__ == "__main__":
    scrape_events()