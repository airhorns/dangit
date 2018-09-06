# Dangit

Minesweeper clone for fun, and to demonstrate React & Django proficiency!

### Getting Set Up

- Install system dependencies:  `chromedriver` and `python` version 3.6.
- Run
```
$ pipenv install --dev && yarn
```
to install the python dependencies for the application.
- Run
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


### Todo list

 - [x] Classic game interface
 - [x] Save gamestate on server
 - [x] Fix auto open bug
 - [x] Fix flagged animation
 - [x] Display fun animation when game completes or fails & status on the game page
 - [X] Implement user login
 - [X] Implement user sign up
 - [X] Implement user homepage / game list
 - [ ] Implement user stats / leaderboards
 - [ ] Implement board generator that doesn't require guessing
 - [ ] Implement hexagonal game
 - [x] Deploy via Heroku
 - [ ] Deploy via k8s
 - [ ] Implement real time game type
