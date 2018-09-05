# Dangit

Minesweeper clone for fun, and to demonstrate React & Django proficiency!

### Getting Set Up

Run
```
$ pip install -r dev_requirements.txt && yarn
```
to install the dependencies for the application.

Run
```
$ python manage.py migrate
```
to set up the database to power the application.


### Developing

Run

```
$ python manage.py runserver
```

to run the Django development server.

Run
```
$ webpack  # add the --watch flag for automatic rebuilds
```
to bundle a new version of the client side code.

Run
```
$ python manage.py createsuperuser
```
to get an admin super user you can use to access the Django admin interface for your development environment.

Run `bin/autolint` to automatically lint and conform all code to PEP8/ES6 standards via `autopep8` and `tslint`
