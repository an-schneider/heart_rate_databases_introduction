from flask import Flask, jsonify, request
from flask_cors import CORS
from pymodm.errors import DoesNotExist
import models
import datetime
import HR_calcs
from pymodm import connect

app = Flask(__name__)
CORS(app)
connect("mongodb://localhost:27017/db")


@app.route("/api/heart_rate", methods=["POST"])
def add_hr_reading():
    """
    Adds new heart rate readings to users already in the database and
    creates entries for users not already in the database
    :return:
    """
    r = request.get_json()
    try:
        check_add_hr_reading_input(r)
    except ValueError:
        return "Status: 400, More input information required", 400
    try:
        check_int("heart_rate", r)
        check_int("user_age", r)
    except TypeError:
        return "Status: 400, Heart rate and age must be input as integers " \
               "or floats"

    email = r["user_email"]
    heart_rate = r["heart_rate"]
    age = r["user_age"]
    time = datetime.datetime.now()

    try:
        add_heart_rate(email, heart_rate, time)
        output = 'Status: 202, Data added'
        code = 202
    except DoesNotExist:
        create_user(email, age, heart_rate, time)
        output = 'Status: 201, User created'
        code = 201
    return output, code


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def calc_avg_hr(user_email):
    """
    Calculates the average of all heart rate measurements taken for an
    individual
    :param user_email:
    :return: avg
    """

    user = models.User.objects.raw({"_id": user_email}).first()
    hr_measurements = user.heart_rate
    avg = HR_calcs.hr_avg(hr_measurements)
    return jsonify({"Avg HR (BPM)": avg}), 200


def create_user(email, age, heart_rate, time):
    """
    Creates a user with the specified email and age. If the user already
    exists in the DB this WILL overwrite that user. It also adds the
    specified heart_rate to the user
    :param email: str email of the new user
    :param age: number age of the new user
    :param heart_rate: number initial heart_rate of this new user
    :param time: datetime of the initial heart rate measurement
    """

    u = models.User(email, age, [], [])  # create a new User instance
    u.heart_rate.append(heart_rate)  # add initial heart rate
    u.heart_rate_times.append(time)  # add initial heart rate time
    u.save()  # save the user to the database


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def print_user(user_email):
    """
    Prints the user with the specified email
    :param user_email: str email of the user of interest
    :return:
    """

    email = user_email
    try:
        user = models.User.objects.raw({"_id": email}).first()
    except DoesNotExist:
        return "Status: 500, User does not exist"
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)
    HR = user.heart_rate
    Times = user.heart_rate_times
    return jsonify({"Heart_Rates": HR, "Times": Times}), 200


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def calc_avg_hr_interval():
    """"
    Calculates the average heart of a patient's readings after a specified
    time and determines whether patient has tachycardia
    :return: Avg HR
    :return: Tachycardia
    """
    r = request.get_json()
    email = r["user_email"]
    time_input_string = r["heart_rate_average_since"]
    time_input = datetime.datetime.strptime(time_input_string,
                                            '%Y-%m-%d %H:%M:%S.%f')
    try:
        check_calc_avg_hr_interval_input(r)
    except ValueError:
        return "Status Error 400: More input information is required", 400
    user = models.User.objects.raw({"_id": email}).first()
    heart_rate_times = user.heart_rate_times
    heart_rate = user.heart_rate
    age = user.age
    cutoff_index = HR_calcs.find_cutoff_index(time_input, heart_rate_times)
    interval_list = heart_rate[cutoff_index:]
    interval_avg = HR_calcs.hr_avg(interval_list)

    check_tach = HR_calcs.check_tachycardia(age, interval_avg)
    if check_tach == 1:
        tach_output = "Yes"
    else:
        tach_output = "No"

    return jsonify({"Avg HR since specified time (BPM)": interval_avg,
                   "Tachycardia": tach_output}), 200


def add_heart_rate(email, heart_rate, time):
    """
    Appends a heart_rate measurement at a specified time to the user
    specified by email. It is assumed that the user specified by email
    exists already.
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    """

    user = models.User.objects.raw({"_id": email}).first()
    user.heart_rate.append(heart_rate)
    user.heart_rate_times.append(time)
    user.save()
    return jsonify("Data recorded")


def check_add_hr_reading_input(input_dict):
    if "user_email" in input_dict.keys():
        pass
    else:
        raise ValueError('user_email must be specified')
    if "heart_rate" in input_dict.keys():
        pass
    else:
        raise ValueError('heart_rate must be specified')
    if "user_age" in input_dict.keys():
        pass
    else:
        raise ValueError('user_age must be specified')
    pass


def check_calc_avg_hr_interval_input(input_dict):
    if "user_email" in input_dict.keys():
        pass
    else:
        raise ValueError('user_email must be specified')
    if "heart_rate_average_since" in input_dict.keys():
        pass
    else:
        raise ValueError('heart_rate_average_since must be specified')
    pass


def check_int(key, input_dict):
    value = input_dict[key]
    if type(value) != (int or float):
        raise TypeError("Numerical values must be floats or integers ")
    else:
        pass


if __name__ == "__main__":
    create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60,
                time=datetime.datetime.now())
    create_user(email="ans52@duke.edu", age=21, heart_rate=60,
                time=datetime.datetime.now())
