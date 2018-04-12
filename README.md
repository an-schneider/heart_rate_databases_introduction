# heart_rate_databases_starter [![Build Status](https://travis-ci.org/an-schneider/heart_rate_databases_introduction.svg?branch=master)](https://travis-ci.org/an-schneider/heart_rate_databases_introduction)
Starter codebase for BME590 Databases Assignment (which can be found [here](https://github.com/mlp6/Medical-Software-Design/blob/master/Lectures/databases/main.md#mini-projectassignment)). 

# Heart Rate Database Info
## About this software
This program utilize Flask and MongoDB to create a database to which a patient's heart rate measurements can be added and stored. The heart rate readings, as well as the times at which they were added can then be retrieved. A patient's total average heart rate as well as the average heart rate since a specified time can also be retrieved. The program will also return whether or not the patient's average heart rate would be considered tachycardic for their age. If a heart rate reading is added for a user not already in the database, a new user will be created. 

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
## Other Notes
Time inputs must be in "YYYY-MM-DD hh:mm:ss.ssssss" format where hours are expressed as 24 hour time
