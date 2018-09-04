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
$ webpack
```
to bundle a new version of the client side code.

Run `bin/autolint` to automatically lint and conform all code to PEP8/ES6 standards via `autopep8` and `tslint`
