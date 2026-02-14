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
    Scrape the ZZZ events from the website.
    """

    Log()('Scraping ZZZ events...')
    Log()('Scraping website...')
    url_to_scrape = "https://game8.co/games/Zenless-Zone-Zero/archives/457176"

    response = requests.get(url_to_scrape)
    soup = BeautifulSoup(response.text, 'html.parser')

    ongoing_events_table = soup.find('h3', {'class': 'a-header--3', 'id': 'hm_1'}).find_next_sibling('table')

    # Find all table rows (skip the header row)
    rows = ongoing_events_table.find_all('tr')[1:]  # Skip first row (header)

    result = []
    i = 0
    
    while i < len(rows):
        row = rows[i]
        cells = row.find_all(['td', 'th'])
        
        # Check if this is a start row (has rowspan and event info)
        if len(cells) >= 3 and cells[0].get('rowspan') == '2':
            # First row: event name and start date
            first_cell = cells[0]
            event_link = first_cell.find('a')
            event_name = event_link.get_text(strip=True) if event_link else first_cell.get_text(strip=True)
            event_url = event_link.get('href') if event_link else None
            
            # Start date is in the third cell
            start_date_text = cells[2].get_text(strip=True)
            
            # Get the next row for end date
            if i + 1 < len(rows):
                next_row = rows[i + 1]
                next_cells = next_row.find_all(['td', 'th'])
                
                if len(next_cells) >= 2:
                    # End date is in the second cell of the next row
                    end_date_text = next_cells[1].get_text(strip=True)
                    
                    # Parse dates
                    dates_text = f"{start_date_text} - {end_date_text}"
                    
                    # Extract dates using regex
                    date_pattern = r'(\w+ \d+, \d+).*?-\s*(\w+ \d+, \d+|\w+ \d+ \d+|\w+ \d+|\w+ of \w+ \d+\.\d+)'
                    date_match = re.search(date_pattern, dates_text)
                    
                    if date_match:
                        start_date_str = date_match.group(1)
                        end_date_str = date_match.group(2)
                        
                        try:
                            # Convert start date to timestamp
                            start_date = datetime.strptime(start_date_str, '%B %d, %Y')
                            start_timestamp = int(start_date.timestamp())
                            
                            # Handle end date
                            if 'End of' in end_date_str or 'end of' in end_date_str.lower():
                                # Skip "End of Version" events
                                days_left = None
                                end_timestamp = None
                                end_date_display = end_date_str
                            else:
                                # Try different date formats
                                try:
                                    end_date = datetime.strptime(end_date_str, '%B %d, %Y')
                                except ValueError:
                                    try:
                                        end_date = datetime.strptime(end_date_str, '%B %d %Y')
                                    except ValueError:
                                        # Handle "Month Day" format (current year)
                                        end_date = datetime.strptime(f"{end_date_str} {datetime.now().year}", '%B %d %Y')
                                
                                end_timestamp = int(end_date.timestamp())
                                end_date_display = end_date_str
                                days_left = (end_date - datetime.now()).days
                            
                            result.append({
                                'game': 'Zenless Zone Zero',
                                'event_name': event_name,
                                'event_url': event_url,
                                'dates_text': dates_text,
                                'start_timestamp': start_timestamp,
                                'start_date': start_date_str,
                                'end_timestamp': end_timestamp,
                                'end_date': end_date_display,
                                'days_left': days_left
                            })
                            
                        except ValueError as e:
                            result.append({
                                'game': 'Zenless Zone Zero',
                                'event_name': event_name,
                                'event_url': event_url,
                                'dates_text': f"Could not parse dates from: {dates_text} ({str(e)})",
                                'days_left': None,
                            })
                    else:
                        result.append({
                            'game': 'Zenless Zone Zero',
                            'event_name': event_name,
                            'event_url': event_url,
                            'dates_text': f"Could not parse dates from: {dates_text}",
                            'days_left': None,
                        })
                    
                    # Skip the next row since we processed it
                    i += 2
                    continue
        
        # If not a paired row, just move to next
        i += 1

    Log()('Finished scraping ZZZ events from game8.')
    
    # write results into a file in root
    with open('logs/events_zzz.txt', 'w', encoding='utf-8') as file:
        for element in result:
            file.write(str(element) + "\n")
    
    # Filter out entries where days_left is None or the end date is already passed
    result = [entry for entry in result if entry['days_left'] is not None and (entry['end_timestamp'] is None or entry['end_timestamp'] > int(datetime.now().timestamp()))]
    
    # Return the entry with the least number of days left
    return min(result, key=lambda entry: entry.get('days_left', float('inf'))) if result else None

if __name__ == "__main__":
    scrape_events()