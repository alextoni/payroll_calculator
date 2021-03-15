import sys
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
        try:
            csv_file = open(filename)
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.update_model(row['day'], row['start'], row['end'], row['rate'])
        except FileNotFoundError as e:
            sys.exit("ERROR: File not found: '%s'" % filename)
        except KeyError as e:
            sys.exit("ERROR: Bad file format: '%s'" % filename)

    def update_model(self, weekday, start, end, rate):
        try:
            if weekday not in WEEKDAYS:
                raise ValueError("'%s' is not a valid weekday" % weekday)
            start_time = time.fromisoformat(start)
            end_time = time.fromisoformat(end)
            first_hour = _round_hour(start_time)
            last_hour = ((_round_hour(end_time) - 1) % DAYHOURS) + 1
            rate_value = int(rate)
            for pos in range(first_hour, last_hour):
                self.rate_map[weekday][pos] = rate_value
        except ValueError as e:
            sys.exit("ERROR: Invalid input: " + str(e) )

    def get_model(self, weekday):
        try:
            day_model = self.rate_map[weekday]
        except KeyError:
            day_model = None
        return day_model

    def print(self):
        for elem in self.rate_map:
            print(elem, self.rate_map[elem])
