"""
    ScheduleModel.py
    This module contains the ScheduleModel class.
"""
__author__ = "Alejandro Perez"

import sys
import re
from datetime import time

from src.payroll.constants import *
from src.payroll.RateModel import RateModel


def _parse_input(raw_input_line):
    """
    Parses the input line to extract the name and time intervals.
    :param raw_input_line: Input string with the employee schedule info.
    :return: The name and the list of intervals.
    """
    name, raw_schedule_line = raw_input_line.split('=')
    intervals = re.findall("(\\D{2})(\\d{2}:\\d{2})-(\\d{2}:\\d{2})", raw_schedule_line)
    return name, intervals


class ScheduleModel:
    """
    The ScheduleModel class represents the working schedule for an employee in a week.

    :ivar employee_name: The employee name.
    :ivar work_intervals: The time intervals when the employee worked. Represented
                          by a list of tuples: (week day, start time, end time).
    :ivar schedule_map: The map containing the week slots worked by the employee.
                        Represented by lists of real values in [0,1] that indicate
                        the fraction worked. For example:
                        MO: [0, 0, 0, 0.5, 1, 1, 0.5, 0, 0, ... < 24 slots > ...]
                        WE: [0, 0, 0, 0, 0, 1, 1, 1, 0.25, 0, ... < 24 slots > ...]
    """

    def __init__(self, schedule_input=None):
        """
        Creates a new schedule model object.

        :param schedule_input: TXT file with the working schedule information (optional).
                               Each line represents a schedule for an employee.
                               For example:
                               RENE=MO10:00-12:00,TU10:00-12:00,...
        """
        self.employee_name = None
        self.work_intervals = []
        self.schedule_map = {}
        if schedule_input:
            self.load_schedule(schedule_input)

    def get_name(self):
        """
        Gets the employee name.
        :return: The employee name.
        """
        return self.employee_name

    def get_work_intervals(self):
        """
        Gets the worked time intervals in the week.
        :return: The list of intervals, represented by tuples.
        """
        return self.work_intervals

    def load_schedule(self, input_line):
        """
        Loads the working schedule into this object.
        :param input_line: Input string with the employee schedule info.
        """
        try:
            name, intervals = _parse_input(input_line)
            self.employee_name = name
            self.work_intervals = intervals

            for day, start, end in intervals:
                if day in WEEKDAYS:
                    if day not in self.schedule_map:
                        self.schedule_map[day] = [0] * DAYHOURS
                    start_time = time.fromisoformat(start)
                    end_time = time.fromisoformat(end)
                    first_hour = start_time.hour
                    last_hour = ((end_time.hour - 1) % DAYHOURS) + 1
                    for pos in range(first_hour, last_hour):
                        self.schedule_map[day][pos] = 1
                    self.schedule_map[day][first_hour] = (60 - start_time.minute) / 60  # fraction of hours
                    if last_hour < DAYHOURS:
                        self.schedule_map[day][last_hour] = end_time.minute / 60
                else:
                    raise ValueError("invalid weekday")
        except ValueError as e:
            sys.exit("ERROR: Bad input format: " + str(e))

    def calculate_payment(self, rate_model: RateModel):
        """
        Calculates the payment amount for the employee, given a rate model to apply.
        :param rate_model: The rate model.
        :return: The payment amount, in USD.
        """
        payment = 0
        for day in self.schedule_map:
            work_map = self.schedule_map[day]
            rate_map = rate_model.get_model(day)
            day_payment = sum([w * r for w, r in zip(work_map, rate_map)])
            payment += day_payment
        return payment

    def print(self):
        """
        Prints the schedule model in the standard output.
        """
        for elem in self.schedule_map:
            print(elem, self.schedule_map[elem])
