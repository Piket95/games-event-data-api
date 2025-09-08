import os

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import database.database as database
import wuwa_codes
from helpers.games import Game
from helpers.log import Log

def run():
    database.migrate()
    scraping_wuwa_codes()

    # database.drop_all_tables(conn, cursor)

def scraping_wuwa_codes():

    # TODO: setup mqtt listener and check if the codes where broadcasted correctly

    wuwa_codes.scrapeCodes()
    
    # check db for specific entries
    conn, cursor = database.connect()
    entries = cursor.execute('''
        SELECT * FROM codes WHERE game = ? AND code IN (?, ?)
    ''', (Game.WUTHERING_WAVES.value, 'WUTHERINGGIFT', 'BLACKSHORES')).fetchall()
    conn.close()

    if len(entries) == 2:
        Log().success('✅ WuWa codes found in database.')
    else:
        Log().error('❌ WuWa codes not found in database.')