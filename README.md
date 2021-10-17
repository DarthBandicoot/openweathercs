# openweathercs


My attempt at CyberSmart Tech test.

Key Features:

    Handles Multiple users Todo List, on first page you will either 
    enter new account information which adds a new user or you'll select your account
    and enter the pin code you chose for the todo list

    When adding a new task on save it will send a request to the api along with the 
    city name to retrieve the current temperature then saves it with the location.

    Each task in the todo list will have a colour coded background correlated
    to the current local temperature

    Once a Task status has been marked as Done it is no longer editable



# Setup

## Setup without Docker

    1. Check that the sqlite3 is uncommented in the settings file
    2. pip install -r requirements.txt
    3. python manage.py migrate
    4. python manage.py createsuperuser
    5. python manage.py add_locations


## Setup with Docker

    1. Uncomment the postgresql db settings, comment out the sql one
    2. run docker-compose up
    3. docker-compose exec openweathercs python manage.py migrate
    4. docker-compose exec openweathercs python manage.py createsuperuser
    5. docker-compose exec openweathercs python manage.py add_locations


### Bugs with the tech test

    1. When docker setup is ran currently, docker-compose up works and launches the db however I can't seem to open the
    application in my browser.
