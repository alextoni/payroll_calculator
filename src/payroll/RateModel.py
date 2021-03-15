import csv
from datetime import time

from .constants import *


def _round_hour(t: time):
    hour = t.hour
    if t.minute > 30:
        hour = (hour + 1) % 24
    return hour


class RateModel:

    def __init__(self, filename=None):
        self.rate_map = {}
        for d in WEEKDAYS:
            self.rate_map[d] = [0] * DAYHOURS
        if filename:
            self.load_model(filename)

    def load_model(self, filename):
        csv_file = open(filename)
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            self.update_model(row)

    def update_model(self, rate):
        start_time = time.fromisoformat(rate['start'])
        end_time = time.fromisoformat(rate['end'])
        first_hour = _round_hour(start_time)
        last_hour = ((_round_hour(end_time)-1) % DAYHOURS) + 1
        week_day = rate['day']
        rate_value = int(rate['rate'])
        for pos in range(first_hour, last_hour):
            self.rate_map[week_day][pos] = rate_value

    def get_model(self, weekday):
        try:
            day_model = self.rate_map[weekday]
        except KeyError:
            print("Invalid day")
            day_model = None
        return day_model

    def print(self):
        for elem in self.rate_map:
            print(elem, self.rate_map[elem])
