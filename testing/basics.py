import os
import sys
import time

from typing import List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from helpers.time_delay import calculate_delay
from helpers.log import Log

def run() -> List[int]:
    test_results = [0,0]

    results = test_calculate_delay()
    test_results[0] += results[0]
    test_results[1] += results[1]
    
    return test_results

def test_calculate_delay() -> List[int]:
    test_results = [0,0]

    delay = calculate_delay()

    # check if the delay ends within 4 to 7 hours from now
    if delay >= 4 * 3600 and delay <= 7 * 3600:
        Log().success('✅ Delay is within 4 to 7 hours.')
        test_results[0] += 1
    else:
        Log().error('❌ Delay is not within 4 to 7 hours.')
        Log().error(f'Expected: Delay to be between 4 and 7 hours')
        Log().error(f'Actual: Delay is {delay / 3600} hours')
        test_results[1] += 1
    
    return test_results
    