# Welcome to HealthNet!
HealthNet is a medical management platform designed for both practitioners and patients alike!
This project is a group effort created by SE Team 4, also known as "You Can't Tell Us What To Do!" over the course of a semester for RIT's Software Engineering 261 course.

# Installation
To install, simply follow the following steps in your command line enviornment

* Change to the root directory of the repository
* `python -m pip install -r pip-requirements.txt`
* `python manage.py migrate`

# Use
Now, just make a user and get set up!

* `python manage.py createsuperuser`
* Follow the steps displayed to create your user account
* `python manage.py runserver`

All set! As long as the server is running can access the administration page through localhost:8000/admin using the account you just created. Also, the website is accessible via localhost:8000!