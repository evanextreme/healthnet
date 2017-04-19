FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./trunk/requirements.txt ./
RUN pip install -r requirements.txt
ADD ./trunk ./
RUN python manage.py makemigrations 
RUN python manage.py migrate --run-syncdb
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
RUN python manage.py initadmin
