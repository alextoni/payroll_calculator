from payroll.RateModel import RateModel


if __name__ == '__main__':
    rates = RateModel("config/default_rates.csv")
    rates.print()

