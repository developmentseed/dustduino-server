## Installation
Prequisites:
- Install and start Postgres with a new database
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
