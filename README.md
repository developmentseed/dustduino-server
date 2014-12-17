## Installation

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Prequisites:
- Install and start [Postgres](http://www.postgresql.org/) with a [new user](http://www.postgresql.org/docs/9.3/static/app-createuser.html) and [new database](http://www.postgresql.org/docs/current/static/manage-ag-createdb.html)
- Install [Foreman](https://github.com/ddollar/foreman)
- Clone the repo

Create a virtual environment
```
virtualenv venv
source venv/bin/activate
```

Install the requirements 
```
pip install -r requirements.txt
```

Create a secret key
```
export DJANGO_SECRET_KEY=`python -c 'import random; import string; print "".join([random.SystemRandom().choice(string.digits + string.letters + string.punctuation) for i in range(100)])'`
```

Create a database URL for the API (depends on your Postgres database)
```
export DATABASE_URL='postgres://{{username}}:{{password}}@localhost:5432/{{database}}'
```

Initialize the database
```
python manage.py syncdb
```

Start the server
```
foreman start
```
