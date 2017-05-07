# Welcome to HealthNet!
HealthNet is a medical management platform designed for both practitioners and patients alike!
This project is a group effort created by SE Team 4, also known as "You Can't Tell Us What To Do!" over the course of a semester for RIT's Software Engineering 261 course.

# Installation (Native)
To install, simply follow the following steps in your command line enviornment

* Change to the root directory of the repository
* `python -m pip install -r requirements.txt`
* `python manage.py makemigrations`
* `python manage.py migrate --run-syncdb`


# Configure

If you are running this off your own server, natively, we recommend editing the settings.py file located in the HealthNet directory, in order to configure the SMTP server and address to send notification emails from.

# Use
Now, just make an admin user and get set up!

* `python manage.py initadmin`
Automatically creates an admin account for you! The default username is "root" and the default password is "admin".
* `python manage.py runserver`

All set! As long as the server is running can access the administration page through localhost:8000/login using the account you just created. Also, the website is accessible via localhost:8000! Make sure to create hospitals and doctors after you log in, otherwise patients will not be able to register.


# Admin Funtime!

* `python manage.py runtests`
Allows you to run our unit tests and check the stability of the system.
* `python manage.py initsampledb`
Initializes a sample database complete with one of everything. User accounts are "spidey", "mj", and "dococ", with their passwords all being "qwertyuiop".

# Docker, for the weird people
However, we now have a docker container which should make setting up your system a snap! (Pun not intended, we don't have a Snap package)

* `docker pull evanextreme/healthnet`
* `docker run --name healthnet -p 8000:8000 -d healthnet`
The docker container automatically comes with the admin initialized, and a sample database created. Fun!
