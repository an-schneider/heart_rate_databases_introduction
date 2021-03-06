import numpy

time_format = '%Y-%m-%d %H:%M:%S.%f'


def hr_avg(heart_rates):
    """
    Calculates the average heart of an input list
    :param heart_rates:
    :return: avg
    """

    avg = numpy.mean(heart_rates)
    return avg


def find_cutoff_index(time_input, heart_rate_times):
    """
    Finds the index in a time array corresponding to the specified time cutoff
    :param time_input:
    :param heart_rate_times:
    :return: cutoff_index
    """
    time_delta = []
    time_delta_sign = []
    for reading in heart_rate_times:
        delta = reading - time_input
        time_delta.append(abs(delta))
        time_delta_sign.append(numpy.sign(delta.total_seconds()))
    cutoff_value = numpy.min(time_delta)  # Finds delta closest to zero
    index = time_delta.index(cutoff_value)
    if time_delta_sign[index] == 1.:
        cutoff_index = index
    else:
        cutoff_index = index + 1
    return cutoff_index


def check_tachycardia(age, avg_hr):
    """
    Checks if patient data indicates tachycardia
    :param age:
    :param avg_hr:
    :return: tach
    """

    if 0 <= age <= 1 and avg_hr > 159:
        tach = 1
    elif 1 < age <= 2 and avg_hr > 151:
        tach = 1
    elif 2 < age <= 4 and avg_hr > 137:
        tach = 1
    elif 4 < age <= 7 and avg_hr > 133:
        tach = 1
    elif 7 < age <= 11 and avg_hr > 130:
        tach = 1
    elif 11 < age <= 15 and avg_hr > 119:
        tach = 1
    elif age > 15 and avg_hr > 100:
        tach = 1
    else:
        tach = 0
    return tach
