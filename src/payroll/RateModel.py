"""
    RateModel.py
    This module contains the RateModel class.
"""
__author__ = "Alejandro Perez"

import sys
import csv
from datetime import time

from src.payroll.constants import *


def _round_hour(t: time):
    """
    Rounds the time object to the nearest hour.
    :param t: time object.
    :return: rounded time object.
    """
    hour = t.hour
    if t.minute > 30:
        hour = (hour + 1) % 24
    return hour


class RateModel:
    """
    The RateModel class represents a model for paying rates in a working week.
    The hourly rate is based on the day of the week and the time of the day.

    :ivar dict rate_map: The map containing the rate for each day and hour.
                         For example:
                         MO: [25, 25, 25, ... < 24 slots > ..., 20, 20, 20]
                         TU: [25, 25, 25, ... < 24 slots > ..., 20, 20, 20]
                         ...
                         SU: [30, 30, 30, ... < 24 slots > ..., 25, 25, 25]
    """

    def __init__(self, filename=None):
        """
        Creates a new rate model object.

        :param filename: CSV file with the rate information (optional).
                         Each line defines a rate for a week interval.
                         For example:
                         MO,00:01,09:00,25
                         MO,09:01,18:00,15
                         ...
                         SU,18:01,00:00,25
        """
        self.rate_map = {}
        for d in WEEKDAYS:
            self.rate_map[d] = [0] * DAYHOURS
        if filename:
            self.load_model(filename)

    def load_model(self, filename):
        """
        Loads the rate model into this object.

        :param filename: The CSV file path.
        """
        try:
            csv_file = open(filename)
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                self.update_model(row['day'], row['start'], row['end'], row['rate'])
        except FileNotFoundError:
            sys.exit("ERROR: File not found: '%s'" % filename)
        except KeyError:
            sys.exit("ERROR: Bad file format: '%s'" % filename)

    def update_model(self, weekday, start, end, rate):
        """
        Updates the model with a single week interval and its rate.

        :param weekday: Day of the week, in abbreviated string format.
        :param start: Begin of interval, in time iso format.
        :param end: End of interval, in time iso format.
        :param rate: Rate defined for the interval, in USD.
        """
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
            sys.exit("ERROR: Invalid input: " + str(e))

    def get_model(self, weekday):
        """
        Get the rate model for a single day of the week.

        :param weekday: Day of the week, in abbreviated string format.
        :return: The rate model of the day, in a list format.
        """
        try:
            day_model = self.rate_map[weekday]
        except KeyError:
            day_model = None
        return day_model

    def print(self):
        """
        Prints the rate model in the standard output.
        """
        for elem in self.rate_map:
            print(elem, self.rate_map[elem])
