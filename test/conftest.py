import pytest

from payroll.RateModel import RateModel


@pytest.fixture
def rate_model():
    return RateModel()
