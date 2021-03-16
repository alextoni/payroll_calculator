import pytest

from payroll.RateModel import RateModel
from payroll.ScheduleModel import ScheduleModel


@pytest.fixture
def rate_model():
    return RateModel()


@pytest.fixture
def schedule_model():
    return ScheduleModel()