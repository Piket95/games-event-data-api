from bs4 import BeautifulSoup
import requests

def getHTMLdocument(url):
  response = requests.get(url)
  return response.text

url_to_scrape = "https://www.gamesradar.com/games/rpg/wuthering-waves-codes-redeem/"
# html_document = getHTMLdocument(url_to_scrape)
with open('wuwa-codes.html', 'r', encoding='utf-8') as f:
  html_document = f.read()

# soup = BeautifulSoup(html_document, 'html.parser')
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
print(result)