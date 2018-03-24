import main


def test_main():

    # Test errors in check_add_hr_reading_input
    with pytest.raises(ValueError):
        input_dict = {"user_email": "ans52@duke.edu"}
        main.check_add_hr_reading_input(input_dict)

    # Test errors in check_calc_avg_hr_interval_input
    with pytest.raises(ValueError):
        input_dict = {"user_email": "ans52@duke.edu"}
        main.check_calc_avg_hr_interval_input(input_dict)

    # Test check_int
    with pytest.raises(TypeError):
        input_dict = {"user_email": "ans52@duke.edu",
                      "user_age": '21',
                      "heart_rate": 60}
        main.check_int("user_age", input_dict)
