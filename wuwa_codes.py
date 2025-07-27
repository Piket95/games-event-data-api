from bs4 import BeautifulSoup
import requests

import database.database as db
from games import Game

def getHTMLdocument(url):
  response = requests.get(url)
  return response.text

def scrapeCodes():
    print('Scraping WuWa codes...')

    url_to_scrape = "https://www.gamesradar.com/games/rpg/wuthering-waves-codes-redeem/"
    html_document = getHTMLdocument(url_to_scrape)
    # with open('./website-sources/wuwa-codes.html', 'r', encoding='utf-8') as f:
    #     html_document = f.read()

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
    print('Saving WuWa codes to database...')
    
    conn, cursor = db.connect()

    entries = cursor.execute('''
        SELECT * FROM codes WHERE game = ?
    ''', (Game.WUTHERING_WAVES.value,)).fetchall()

    existing_codes = [entry[1] for entry in entries]

    saving = False

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

                continue
            
            saving = True
            cursor.execute('''
                INSERT INTO codes (code, description, game, expired)
                VALUES (?, ?, ?, ?)
            ''', (code, description, Game.WUTHERING_WAVES.value, expired))
            conn.commit()

    if saving:
        print('WuWa codes saved to database.')
    else:
        print('No new WuWa codes found.')

    conn.close()

