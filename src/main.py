from payroll.RateModel import RateModel
from payroll.ScheduleModel import ScheduleModel


if __name__ == '__main__':
    rates = RateModel("config/default_rates.csv")
    rates.print()

    with open("sample_data/employees.txt") as f:
        for line in f:
            schedule = ScheduleModel(line)
            payment = schedule.calculate_payment(rates)
            print(schedule.get_name(), schedule.get_work_intervals())
            print("The amount to pay", schedule.get_name(), "is", payment, "USD")
