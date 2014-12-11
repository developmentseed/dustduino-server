## Installation
Prequisites:
- Install and start [Postgres](http://www.postgresql.org/) with a [new database](http://www.postgresql.org/docs/current/static/manage-ag-createdb.html)
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

Create a database URL for the API (depends on your Postgres database)
```
export DATABASE_URL='postgres://{{username}}:{{password}}@localhost:5432/{{database}}'
```

Django database stuff?
```
python manage.py makemigrations
python manage.py syncdb
```

Start the server
```
foreman start
```
