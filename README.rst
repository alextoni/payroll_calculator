===================
Payroll Calculator
===================

This project implements a solution to the programming exercise of IOET.

Overview
---------
The goal of this exercise is to calculate the total amount that the company ACME
has to pay to their employees, based on the hours they worked and the times during
which they worked.

The hourly rate that the company has to pay is defined in the following table:

- Monday - Friday

    00:01 - 09:00 25 USD

    09:01 - 18:00 15 USD

    18:01 - 00:00 20 USD

- Saturday and Sunday

    00:01 - 09:00 30 USD

    09:01 - 18:00 20 USD

    18:01 - 00:00 25 USD

Moreover, for each employee, the worked schedule is given by an input line
string with the following format:

    ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00

Before designing a solution, the following assumptions were made:

- The input correspond to the working hours of a single week.
- The defined hourly rates always apply to full hours.
- The employees can work during fraction of hours, and should get paid in proportion.

Approach
------------
My approach to address this problem was to divide the week in time slots of one
hour each. Thus, If we divide a week in 7 days, containing 24 time slots each,
we get a total of 168 time slots.

On one side, the company defines an hourly rate based on the day of the week and
the time of the day. In other words, each time slot of the week is bound to a
specific fixed rate. Thus, we can build a table with 7 rows and 24 columns mapping
slots and rate::

    MO: 25 25 25 ... 15 15 15 ... 20 20 20
    TU: 25 25 25 ... 15 15 15 ... 20 20 20
    WE: 25 25 25 ... 15 15 15 ... 20 20 20
    TH: 25 25 25 ... 15 15 15 ... 20 20 20
    FR: 25 25 25 ... 15 15 15 ... 20 20 20
    SA: 30 30 30 ... 20 20 20 ... 25 25 25
    SU: 30 30 30 ... 20 20 20 ... 25 25 25

On the other side, an employee defines a weekly schedule with worked time slots
and not worked time slots. In this case, some time slots may be partially worked.
Thus, we can build a table with 7 rows and 24 columns mapping the slots with
real values between 0 and 1. 0 means "not worked", 1 means "worked", and any value
in between means "partially worked"::

    MO: 0 0 0 0.5 1 1 1 0.5 0 0 0 ...
    TU: 0 0 0 0.5 1 1 1 0.5 0 0 0 ...
    WE: 0 0 0 0 0 0 0 0 0 0 0 0 0 ...
    TH: 0 0 0 0.25 1 1 1 0.5 0 0 0 ...
    FR: 0 0 0 0.75 1 1 1 0.5 0 0 0 ...
    SA: 0 0 0 0 0 1 1 1 0.5 0 0 0 ...
    SU: 0 0 0 0 0 0 0 0 0 0 0 0 0 ...


Once we have built the two tables, calculating the payment amount is easy.
We just need to combine both tables. More precisely, we need to multiply the two
7x24 matrices element-wise and sum the results.

Architecture
-------------
To make the design as simple as possible, the project contains two main modules:

- RateModel, to model the rate map.
- ScheduleModel, to model the employee working schedule.

RateModel takes as input a config file with the hourly rates defined. By default,
it loads a file with the table given in the exercise. Although this feature was
out of the scope of the exercise, this solution add flexibility and separates
data from code logic.

ScheduleModel takes as input a single line of the txt input file. It loads the
schedule info and maps it to the table. It also combines the rate model to
calculate the payment amount of the employee.

Methodology
-----------
The methodologies followed are:

- Object-Oriented programming.
- Test-driven development.

Regarding the design, I didn't find any appropriate design pattern to apply
to this problem. I believe the approach followed is simple and efficient.

Requirements
-------------
Python 3.7 or newer

Usage
-------
To install the package::

    python setup.py install

To run the program::

    python -m payroll sample_data/employees.txt

To get inline help::

    python -m payroll -h

To run the unit tests::

    python -m pytest

Example
--------
The execution should look like this::

    $ python -m payroll sample_data/employees.txt
    The amount to pay RENE is 215.0 USD
    The amount to pay ASTRID is 85.0 USD
    The amount to pay MONICA is 445.75 USD
    The amount to pay NATHALY is 313.33 USD
    The amount to pay JUACHO is 410.0 USD
