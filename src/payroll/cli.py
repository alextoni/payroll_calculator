"""
Command Line Interface (CLI) for the Payroll Calculator project.
"""
__author__ = "Alejandro Perez"

import argparse

from src.payroll.RateModel import RateModel
from src.payroll.ScheduleModel import ScheduleModel


def main():
    parser = argparse.ArgumentParser(description='Calculate ACME employees payrolls.')
    parser.add_argument('input', help="Input file with employee schedules")
    parser.add_argument('-c', '--config', help="CSV file with rate model", default="config/default_rates.csv")
    args = parser.parse_args()

    rate_model = RateModel(args.config)
    try:
        with open(args.input) as f:
            for input_line in f:
                schedule = ScheduleModel(input_line)
                payment = schedule.calculate_payment(rate_model)
                print("The amount to pay", schedule.get_name(), "is", round(payment, 2), "USD")
    except FileNotFoundError as ex:
        exit("ERROR: File not found: '%s'" % args.input)


if __name__ == '__main__':
    main()
