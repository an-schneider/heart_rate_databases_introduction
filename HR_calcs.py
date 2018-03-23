import numpy

time_format = '%Y-%m-%d %H:%M:%S.%f'


def hr_avg(heart_rates):
    avg = numpy.mean(heart_rates)
    return avg


def find_cutoff_index(time_input, heart_rate_times):
    time_delta = []
    for reading in heart_rate_times:
        time_delta.append(abs(reading - time_input))
    cutoff_value = numpy.min(time_delta)  # Finds delta closest to zero
    cutoff_index = time_delta.index(cutoff_value)
    return cutoff_index




