from datetime import datetime

class DaysLeftCalculator:
    def calculate_days_left(self, end_date):
        return (end_date - datetime.now()).days + 1

    def filter_events(self, events):
        return [event for event in events if event['days_left'] is not None and (event['end_timestamp'] is None or event['end_timestamp'] > int(datetime.now().timestamp()))]