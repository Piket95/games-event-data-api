import os
import sys

from typing import List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import database.database as database
import wuwa_codes
from helpers.games import Game
from helpers.log import Log

def run() -> List[int]:
    test_results = [0,0]

    database.migrate()
    results = scraping_wuwa_codes()
    test_results[0] += results[0]
    test_results[1] += results[1]

    database.drop_all_tables(silent=True)

    return test_results

def scraping_wuwa_codes() -> List[int]:

    # TODO: setup mqtt listener and check if the codes where broadcasted correctly
    test_results = [0,0]

    wuwa_codes.scrapeCodes()

    # check if all entries are correctly in db
    conn, cursor = database.connect()
    entries = cursor.execute('''
        SELECT * FROM codes WHERE game = ?
    ''', (Game.WUTHERING_WAVES.value,)).fetchall()
    conn.close()

    if len(entries) == 24:
        Log().success('✅ All WuWa codes found in database.')
        test_results[0] += 1
    else:
        Log().error('❌ WuWa codes not found in database.')
        Log().error(f'Expected: Found 24 entries')
        Log().error(f'Actual: Found {len(entries)} entries')
        test_results[1] += 1

    
    # check if all expired is set correctly for the found codes
    expired_entries = [entry for entry in entries if entry[4]]
    valid_entries = [entry for entry in entries if not entry[4]]
    if len(expired_entries) == 23 and len(valid_entries) == 1:
        Log().success('✅ All WuWa expired and valid codes correctly saved in the database.')
        test_results[0] += 1
    else:
        Log().error('❌ WuWa expired and valid codes not correctly saved in the database.')
        Log().error(f'Expected: Found 23 expired entries and 1 valid entry')
        Log().error(f'Actual: Found {len(expired_entries)} expired entries and {len(valid_entries)} valid entries')
        test_results[1] += 1
    
    blackshores = [entry for entry in entries if entry[1] == 'BLACKSHORES']
    # check for some codes specifically
    if len(blackshores) == 1 and blackshores[0][4] == True:
        Log().success('✅ WuWa code [BLACKSHORES] found in database and expired is set correctly.')
        test_results[0] += 1
    else:
        Log().error('❌ WuWa code [BLACKSHORES] not found in database or expired is not set correctly.')
        Log().error(f'Expected: Found 1 entry with expired set to True')

        print_string = f'Actual: Found {"1" if len(blackshores) == 1 else "no"} entry'

        if (len(blackshores) == 1):
            print_string += f' with expired set to {"True" if blackshores[0][4] else "False"}'

        Log().error(print_string)
        test_results[1] += 1

    return test_results