import HR_calcs
import datetime

time_format = '%Y-%m-%d %H:%M:%S.%f'


def test_hr_calcs():
    test_hr = [60, 65, 70, 65, 70]
    test_times = [datetime.datetime.strptime("2018-03-09 11:00:36.372339", time_format),
                  datetime.datetime.strptime("2018-03-09 18:00:44.413444", time_format),
                  datetime.datetime.strptime("2018-03-10 09:21:00.459253", time_format),
                  datetime.datetime.strptime("2018-03-10 20:45:47.545165", time_format),
                  datetime.datetime.strptime("2018-03-11 08:30:29.597243", time_format)]
    test_cutoff1 = datetime.datetime.strptime("2018-03-10 12:00:00.000000", time_format)
    test_cutoff2 = datetime.datetime.strptime("2018-03-10 20:45:48.000000", time_format)

    # Test HR Avg
    assert HR_calcs.hr_avg(test_hr) == 66

    # Test find_cutoff_index
    assert HR_calcs.find_cutoff_index(test_cutoff1, test_times) == 3
    assert HR_calcs.find_cutoff_index(test_cutoff2, test_times) == 4

    # Test check_tachycardia
    test_age1 = 5
    test_age2 = 10
    test_hr1 = 170
    test_hr2 = 60

    assert HR_calcs.check_tachycardia(test_age1, test_hr1) == 1
    assert HR_calcs.check_tachycardia(test_age1, test_hr2) == 0
    assert HR_calcs.check_tachycardia(test_age2, test_hr1) == 1
    assert HR_calcs.check_tachycardia(test_age2, test_hr2) == 0


test_hr_calcs()


