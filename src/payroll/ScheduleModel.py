import re
from datetime import time

from .constants import *
from .RateModel import RateModel


def _parse_input(raw_input_line):
    name, raw_schedule_line = raw_input_line.split('=')
    intervals = re.findall("(\D{2})(\d{2}:\d{2})-(\d{2}:\d{2})", raw_schedule_line)
    return name, intervals


class ScheduleModel:

    def __init__(self, schedule_input=None):
        self.employee_name = None
        self.work_intervals = []
        self.schedule_map = {}
        if schedule_input:
            self.load_schedule(schedule_input)

    def get_name(self):
        return self.employee_name

    def get_work_intervals(self):
        return self.work_intervals

    def load_schedule(self, input_line):
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
                self.schedule_map[day][first_hour] = (60 - start_time.minute) / 60      # fraction of hours
                self.schedule_map[day][last_hour] = end_time.minute / 60

    def calculate_payment(self, rate_model: RateModel):
        payment = 0
        for day in self.schedule_map:
            work_map = self.schedule_map[day]
            rate_map = rate_model.get_model(day)
            day_payment = sum([w * r for w, r in zip(work_map, rate_map)])
            payment += day_payment
        return payment

    def print(self):
        for elem in self.schedule_map:
            print(elem, self.schedule_map[elem])
