from bs4 import BeautifulSoup
import requests
import mqtt
import os

import database.database as db
from helpers.games import Game
from config.environments import Environment

def getHTMLdocument(url):
    """
    Get the HTML document from the given URL.
    """
    response = requests.get(url)
    return response.text

def scrapeCodes():
    """
    Scrape the WuWa codes from the website.
    """

    print('Scraping WuWa codes...')

    if (os.getenv('ENVIRONMENT') == Environment.TESTING.value):
        url_to_scrape = "./website-sources/wuwa-codes.html"
        with open(url_to_scrape, 'r', encoding='utf-8') as f:
            html_document = f.read()
    else:
        url_to_scrape = "https://www.gamesradar.com/games/rpg/wuthering-waves-codes-redeem/"
        html_document = getHTMLdocument(url_to_scrape)

    soup = BeautifulSoup(html_document, 'html.parser')

    active_codes_heading = soup.find('h2', id='section-wuthering-waves-codes')

    actives_codes = dict()
    codes_list = active_codes_heading.find_next_sibling('ul')

    for li in codes_list.find_all('li'):
        code = li.find('strong')
        if not code:
            continue
        code = code.text.strip()
        full_text = li.get_text(strip=True, separator=' ')
        description = full_text.replace(code, '').strip()
        for sep in ['–', '-']:
            if sep in description:
                description = description.split(sep, 1)[1].strip()
                break
        actives_codes[code] = description

    expired_codes_heading = soup.find('h3', id='section-expired-wuthering-waves-codes')
    expired_codes = dict()
    codes_list = expired_codes_heading.find_next_sibling('ul')

    for li in codes_list.find_all('li'):
        code = li.find('del')
        if not code:
            continue
        code = code.text.strip()
        full_text = li.get_text(strip=True, separator=' ')
        description = full_text.replace(code, '').strip()
        for sep in ['–', '-']:
            if sep in description:
                description = description.split(sep, 1)[1].strip()
                break
        expired_codes[code] = description

    result = {
        'active_codes': actives_codes,
        'expired_codes': expired_codes,
    }

    print('Finished scraping WuWa codes.')

    saveCodes(result)

    return result

def saveCodes(codes):
    """
    Save the scraped codes to the database.
    """

    print('Saving WuWa codes to database...')
    
    conn, cursor = db.connect()

    entries = cursor.execute('''
        SELECT * FROM codes WHERE game = ?
    ''', (Game.WUTHERING_WAVES.value,)).fetchall()

    existing_codes = [entry[1] for entry in entries]

    updates = dict()

    for type, inner_codes in codes.items():
        expired = type == 'expired_codes'

        for code, description in inner_codes.items():
            if code in existing_codes:

                for entry in entries:
                    if entry[1] == code:
                        if expired != entry[4]:
                            print('Updating code: [' + Game.WUTHERING_WAVES.value + '] ' + code + ' to ' + ('expired' if expired else 'active'))

                            cursor.execute('''
                                UPDATE codes SET expired = ? WHERE code = ? AND game = ?
                            ''', (expired, code, Game.WUTHERING_WAVES.value))
                            conn.commit()

                            code_update = dict()
                            code_update['description'] = description
                            code_update['state'] = 'expired' if expired else 'active'

                            updates[code] = code_update

                continue
            
            cursor.execute('''
                INSERT INTO codes (code, description, game, expired)
                VALUES (?, ?, ?, ?)
            ''', (code, description, Game.WUTHERING_WAVES.value, expired))
            conn.commit()

            new_code = dict()
            new_code['description'] = description
            new_code['state'] = 'new'
            updates[code] = new_code
    
    # print(updates)

    if len(updates) > 0:
        print('WuWa codes saved to database.')
        print('Broadcasting new codes...')
        broadcastNewCodeSignal(updates)
    else:
        print('No new WuWa codes found.')

    conn.close()

def broadcastNewCodeSignal(updates):
    """
    Broadcast all new or updated codes to the MQTT broker.
    """

    try:
        mqtt.broadcast_new_code(updates, Game.WUTHERING_WAVES.value)
    except Exception as e:
        print(f'\033[91mError broadcasting new codes: {e}\033[0m')

