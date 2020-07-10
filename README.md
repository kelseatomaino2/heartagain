# heartagain 

### Overview
The purpose of this application is to monitor the state of an ex vivo heart during transportation. It stores incoming data from sensor readings to be queried at a later date. 

### Features
The web application uses a background task and the GPIO library to read from ECG, temperature, flow and pressure sensors. The data is displayed using web sockets. The data is stored in a relational database and there is a search tool to filter historical data.

### Running the App Locally

1. Git clone the repository
2. Cd into the project directory 
3. Create a virtual environment
`virtualenv heartenv`
4. Activate the environment
`source heartenv bin activate`
5. Install the requirements 
`pip install -r requirments.txt`
6. Install postgres and create a database with tables matching the models in sensorWorker/models.py. Update the database in settings.py to point to this database or the database of your choosing.
7. Run migrations 
`python manage.py migrate`

#### To run the app without the Raspberry Pi
8. Comment out any lines of code using the GPIO library
9. Cd into the project directory
10. Acitvate the virtual environment
11. Start the redis server 
`redis-server`
12. Start the background task
`python3 manage.py readSensor`
13. Start the web app
`python3 manage.py runserver`
14. Navigate to the URL and add/home to the end

#### To run the app with the Raspberry Pi 
15. SSH into pi `ssh pi@172.20.10.4` (Password: `heartagain`)
16. Start the background task 
`python3 manage.py readSensor`
17. Start the web app
`python3 manage.py runserver 172.20.10.4`
18. Navigate to link 172.20.10.4:8000/home/


To start background task, `tmux` and to disconnect `Ctrl + b` then to reattach `tmux a` to create a new window `Ctrl %` then to switch between windows `Ctrl ARROW_OF_CHOICE`

#### Loading fake data into database for testing
1. Load fake AEG data
`python3 loadAEGData.py`
2. Load fake ECG data 
`python3 loadFakeData.py`

### Dependencies
* PostgreSQL
* Redis
* Django
* Django Channels
* Chart.js

### ToDo List
* Update BPM calculation in readSensor.py
* Integrate the use of all sensors and reading from them
* Update logic for the search tool 
* Display all historical data based on search criteria-> ECG, temperature, flow and pressure
* Create Docker container for the application to run in to avoid missing dependencies and wrong versioning
* Enable sign in features



