# Welcome to HealthNet!
HealthNet is a medical management platform designed for both practitioners and patients alike!
This project is a group effort created by SE Team 4, also known as "You Can't Tell Us What To Do!" over the course of a semester for RIT's Software Engineering 261 course.

# Installation (Native)
To install, simply follow the following steps in your command line enviornment

* Change to the root directory of the repository
* `python -m pip install -r requirements.txt`
* `python manage.py makemigrations`
* `python manage.py migrate --run-syncdb`

However, we now include a Dockerfile which should make setting up a container a snap! You can use this too instead of the above
* `docker build -t myhealth .`
* `docker run --name healthnet -p 8000:8000 -d myhealth`

# Use
Now, just make an admin user and get set up!

* `python manage.py createsuperuser`
* Follow the steps displayed to create your user account
* When you're done, it's time to run the server!
* `python manage.py runserver`

All set! As long as the server is running can access the administration page through localhost:8000/login using the account you just created. Also, the website is accessible via localhost:8000! Make sure to create hospitals and doctors after you log in, otherwise patients will not be able to register. 
