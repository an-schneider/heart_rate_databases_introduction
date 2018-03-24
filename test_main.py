import main
import pytest


def test_main():

    # Test errors in check_add_hr_reading_input
    with pytest.raises(ValueError):
        input_dict = {"user_email": "ans52@duke.edu"}
        main.check_add_hr_reading_input(input_dict)

    # Test errors in check_calc_avg_hr_interval_input
    with pytest.raises(ValueError):
        input_dict = {"user_email": "ans52@duke.edu"}
        main.check_calc_avg_hr_interval_input(input_dict)
