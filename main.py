from pymodm import connect
from flask import Flask, jsonify, request
from pymodm.errors import DoesNotExist
import models
import datetime
import HR_calcs

app = Flask(__name__)
connect("mongodb://localhost:27017/db")


@app.route("/api/heart_rate", methods=["POST"])
def add_hr_reading():
    r = request.get_json()
    email = r["user_email"]
    heart_rate = r["heart_rate"]
    age = r["user_age"]
    time = datetime.datetime.now()

    try:
        add_heart_rate(email, heart_rate,time)
        output = 'Data added'
    except DoesNotExist:
        create_user(email, age, heart_rate, time)
        output = 'User created, data addd'
    return output


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def calc_avg_hr(user_email):
    user = models.User.objects.raw({"_id": user_email}).first()
    hr_measurements = user.heart_rate
    avg = HR_calcs.hr_avg(hr_measurements)
    return jsonify(avg)


def create_user(email, age, heart_rate, time):
    """
    Creates a user with the specified email and age. If the user already exists in the DB this WILL
    overwrite that user. It also adds the specified heart_rate to the user
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
    :param email: str email of the user of interest
    :return:
    """
    email = user_email
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)
    return jsonify(user.heart_rate),


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def calc_avg_hr_interval():
    r = request.get_json()
    email = r["user_email"]
    time_input_string = r["heart_rate_average_since"]
    time_input = datetime.datetime.strptime(time_input_string, '%Y-%m-%d %H:%M:%S.%f') # Parse time string
    user = models.User.objects.raw({"_id":email}).first()
    heart_rate_times = user.heart_rate_times
    heart_rate = user.heart_rate
    cutoff_index = HR_calcs.find_cutoff_index(time_input,heart_rate_times)
    interval_list = heart_rate[cutoff_index:]
    interval_avg = HR_calcs.hr_avg(interval_list)
    return jsonify(interval_avg)


def add_heart_rate(email, heart_rate,time):
    """
    Appends a heart_rate measurement at a specified time to the user specified by
    email. It is assumed that the user specified by email exists already.
    :param email: str email of the user
    :param heart_rate: number heart_rate measurement of the user
    :param time: the datetime of the heart_rate measurement
    """

    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    user.heart_rate.append(heart_rate)  # Append the heart_rate to the user's list of heart rates
    user.heart_rate_times.append(time)  # append the current time to the user's list of heart rate times
    user.save()  # save the user to the database
    return jsonify("Data recorded")

if __name__ == "__main__":
    create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60, time=datetime.datetime.now())
    create_user(email="ans52@duke.edu", age=21, heart_rate=60, time=datetime.datetime.now())
