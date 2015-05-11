
A REST API for DustDuino air quality sensors

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Deployment to Heroku

Use the heroku button above or manually create an app on heroku and deploy. For configuration purposes, the following table maps environment variables to their Django setting:

|Environment Variable                    |Django Setting              |Development Default          |Production Default
| -------------------------------------- | -------------------------- | --------------------------- | -----------------
|DJANGO_SECRET_KEY                       |SECRET_KEY                  |CHANGEME!!!                                    |raises error

## Installation on local machine

Create a virtual environment
```
virtualenv venv
source venv/bin/activate
```

Install the requirements
```
pip install -r requirements.txt
```

Initialize the database
```
python sensor_rest_api/manage.py syncdb
```

Start the server
```
python sensor_rest_api/manage.py runserver
```
