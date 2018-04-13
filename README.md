# heart_rate_databases_starter [![Build Status](https://travis-ci.org/an-schneider/heart_rate_databases_introduction.svg?branch=master)](https://travis-ci.org/an-schneider/heart_rate_databases_introduction)
Starter codebase for BME590 Databases Assignment (which can be found [here](https://github.com/mlp6/Medical-Software-Design/blob/master/Lectures/databases/main.md#mini-projectassignment)). 

# Heart Rate Database Info
## About this software
This program utilizes Flask and MongoDB to create a database to which a patient's heart rate measurements can be added and stored. The heart rate readings, as well as the times at which they were added can then be retrieved. A patient's total average heart rate as well as the average heart rate since a specified time can also be retrieved. The program will also return whether or not the patient's average heart rate would be considered tachycardic for their age. If a heart rate reading is added for a user not already in the database, a new user will be created. 

## Set-Up Instructions
First, begin running your mongodb database, which can be done with the following command:
```
docker run -v $PWD/db:/data/db -p 27017:27017 mongo
```
If you plan on running your database on a virtual machine, you must replace the `connect` URI string in main.py. Replace `localhost` with a VM address. Example:

```py
connect("mongodb://vcm-0000.vm.duke.edu:27017/heart_rate_app") # open up connection to db
```
Next, activate install the necessary depencies by running:
```pip install -r requirements.txt```
after changing directories to 'heart_rate_databases_introduction'. Activate your virtual environment by running:
```source env/bin/activate```
Finally, run your program with 
```python main.py```
and it will be ready to accept GET and POST requests/

## Using the Database
### POST Requests
* `POST /api/heart_rate` with
  ```sh
  {
      "user_email": "ans52@duke.edu",
      "user_age": 21, // in years
      "heart_rate": 60
  }
  ```
  This will add a heart rate measurement with a timestamp to the specified user. If the specified user is not already in the data, they will be added.
  
  * `POST /api/heart_rate/interval_average` with 
  ```
  {
      "user_email": "ans52@duke.edu",
      "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string
  }
  ```
This will return the user's average heart rates since the specified date. This will also return whether or not this average heart rate is tachycardic given the patient's age. The data will be output as a JSON. 

### GET Requests
* `GET /api/heart_rate/<user_email>`
This will return all recorded heart rates for the specified user, as well as the time at which each measurement was recorded.
* `GET /api/heart_rate/average/<user_email>` 
This will return the average heart rate for the specified user over all recorded time points. 
## Other Notes
Time inputs must be in "YYYY-MM-DD hh:mm:ss.ssssss" format where hours are expressed as 24 hour time
