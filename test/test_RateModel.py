import pytest


def test_load_model_from_nonexistent_file(rate_model):
    with pytest.raises(SystemExit) as ex:
        rate_model.load_model("ghost_file.csv")
    assert "ERROR: File not found: 'ghost_file.csv'" == str(ex.value)


def test_load_model_from_bad_formatted_file(rate_model):
    with pytest.raises(SystemExit) as ex:
        rate_model.load_model("conftest.py")
    assert "ERROR: Bad file format: 'conftest.py'" == str(ex.value)


def test_update_with_rounded_hours(rate_model):
    rate_model.update_model('WE', '09:00', '12:00', 20)
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] == rate_model.rate_map['WE']


def test_update_with_non_rounded_hours(rate_model):
    rate_model.update_model("MO", "03:25", "04:31", 33)
    rate_model.update_model("MO", "19:59", "22:29", 22)
    assert [0, 0, 0, 33, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 22, 0, 0] == rate_model.rate_map['MO']


def test_update_with_edge_hours(rate_model):
    rate_model.update_model('SA', '00:00', '01:00', 44)
    rate_model.update_model('SA', '22:00', '00:00', 44)
    assert [44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 44, 44] == rate_model.rate_map['SA']


def test_update_with_daylong_interval(rate_model):
    rate_model.update_model('TU', '00:00', '00:00', 9)
    assert [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9] == rate_model.rate_map['TU']


def test_update_with_zero_interval(rate_model):
    rate_model.update_model('TH', '12:33', '12:33', 20)
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] == rate_model.rate_map['TH']


def test_update_with_wrong_interval(rate_model):
    rate_model.update_model('FR', '12:00', '03:00', 20)
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] == rate_model.rate_map['FR']


def test_update_with_invalid_day(rate_model):
    with pytest.raises(SystemExit) as ex:
        rate_model.update_model('fri', '07:00', '13:00', 20)
    assert "ERROR: Invalid input: 'fri' is not a valid weekday" == str(ex.value)


def test_update_with_invalid_hours(rate_model):
    with pytest.raises(SystemExit) as ex:
        rate_model.update_model('FR', '03:99', '27:00', 20)
    assert "ERROR: Invalid input: minute must be in 0..59" == str(ex.value)


def test_update_with_invalid_rate(rate_model):
    with pytest.raises(SystemExit) as ex:
        rate_model.update_model('FR', '03:00', '20:00', 'twenty')
    assert "ERROR: Invalid input: invalid literal for int() with base 10: 'twenty'" == str(ex.value)


def test_get_model_with_valid_day(rate_model):
    day_model = rate_model.get_model("MO")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] == day_model


def test_get_model_with_invalid_day(rate_model):
    day_model = rate_model.get_model("Monday")
    assert day_model is None
