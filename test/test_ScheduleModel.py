import pytest


def test_load_schedule_with_single_interval(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=WE10:00-13:00")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
           == schedule_model.schedule_map["WE"]


def test_load_schedule_with_multiple_intervals(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=WE10:00-13:00,WE17:00-19:00")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0] \
           == schedule_model.schedule_map["WE"]


def test_load_schedule_empty(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=")
    assert {} == schedule_model.schedule_map


def test_load_schedule_with_fraction_hours(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=SU10:15-13:15")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.75, 1, 1, 0.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
           == schedule_model.schedule_map["SU"]


def test_load_schedule_with_edge_hours(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=SU18:00-00:00,SU00:00-05:00")
    assert [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1] \
           == schedule_model.schedule_map["SU"]


def test_load_schedule_with_zero_interval(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=SU18:00-18:00")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
           == schedule_model.schedule_map["SU"]


def test_load_schedule_with_daylong_interval(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=SU00:00-00:00")
    assert [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] \
           == schedule_model.schedule_map["SU"]


def test_load_schedule_with_overlapping_intervals(schedule_model):
    schedule_model.load_schedule("ALEJANDRO=SU10:00-18:00,SU12:00-20:00")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0] \
           == schedule_model.schedule_map["SU"]


def test_load_schedule_invalid_day(schedule_model):
    with pytest.raises(SystemExit) as ex:
        schedule_model.load_schedule("ALEJANDRO=Sunday10:00-18:00,SU12:00-20:00")
    assert "ERROR: Bad input format: invalid weekday" == str(ex.value)


def test_load_schedule_invalid_time(schedule_model):
    with pytest.raises(SystemExit) as ex:
        schedule_model.load_schedule("ALEJANDRO=SU10:60-18:00,SU12:00-20:00")
    assert "ERROR: Bad input format: minute must be in 0..59" == str(ex.value)


def test_load_schedule_bad_format(schedule_model):
    with pytest.raises(SystemExit) as ex:
        schedule_model.load_schedule("ALEJANDRO")
    assert "ERROR: Bad input format: not enough values to unpack (expected 2, got 1)" == str(ex.value)


def test_calculate_payment(schedule_model, rate_model):
    schedule_model.load_schedule("ALEJANDRO=SU10:00-18:00")
    rate_model.update_model("SU", "00:00", "12:00", 20)
    rate_model.update_model("SU", "12:00", "00:00", 30)
    assert 220 == schedule_model.calculate_payment(rate_model)


def test_calculate_payment_with_fraction_hours(schedule_model, rate_model):
    schedule_model.load_schedule("ALEJANDRO=SU10:15-18:45")
    rate_model.update_model("SU", "00:00", "12:00", 20)
    rate_model.update_model("SU", "12:00", "00:00", 30)
    assert 237.5 == schedule_model.calculate_payment(rate_model)
