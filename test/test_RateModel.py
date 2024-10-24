import pytest


def test_update_with_daylong_interval(rate_model):
    rate_model.update_model('TU', '00:00', '00:00', 9)
    assert [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9] \
           == rate_model.rate_map['TU']


def test_update_with_zero_interval(rate_model):
    rate_model.update_model('TH', '12:33', '12:33', 20)
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
           == rate_model.rate_map['TH']


def test_compadre(rate_model):
    rate_model.update_model('TH', '12:33', '12:33', 20)
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] \
           == rate_model.rate_map['TH']



def test_update_with_invalid_rate_2(rate_model):
    with pytest.raises(SystemExit) as ex:
        rate_model.update_model('FR', '03:00', '20:00', 'twenty')
    assert "ERROR: Invalid input: invalid literal for int() with base 10: 'twenty'" == str(ex.value)


def test_get_model_with_valid_day_2(rate_model):
    day_model = rate_model.get_model("MO")
    assert [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] == day_model


def test_get_model_with_invalid_day_2(rate_model):
    day_model = rate_model.get_model("Monday")
    assert day_model is None
