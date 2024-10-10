from src.payroll.RateModel import RateModel
from src.payroll.ScheduleModel import ScheduleModel

if __name__ == '__main__':
    rate_model = RateModel("config/default_rates.csv")
    # rate_model.print()

    with open("sample_data/employees.txt") as f:
        for input_line in f:
            schedule = ScheduleModel(input_line)
            payment = schedule.calculate_payment(rate_model)
            # print(schedule.get_name(), schedule.get_work_intervals())
            print("The amount to pay", schedule.get_name(), "is", round(payment,2), "USD")
