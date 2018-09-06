# Dangit

Minesweeper clone for fun, and to demonstrate React & Django proficiency!

### Using the app

It's live at http://dangit-prod.herokuapp.com. Still some bugs.

### Exploring the code

This repo is organized as a Django app, with two apps in `account` and `minesweeper`, and then a client side React app sitting in `dangit-client`. The two communicate using a GraphQL API powered by Graphene. The key objects are:
 - `Board`, `GameType`, and `minesweeper.schema` implement the majority of the Minesweeper business logic.
 - `GameState` persists the game states in a Postgres database
 - `minesweeper.services.start_game` and `minesweeper.services.make_move` implement the major API calls in separate, testable functions decoupled from the API

Key design decisions on the server are:
 - Modeling minesweeper as several sets of positions: the set of mines, the list of opened cells, and the set of flags. I wanted to keep the code very understandable and I think set operations on these sets makes for crisp and performant logic.
 - Using all the stuff Django gives you like `auth.User`, `staticfiles`, etc, as it's professionally maintained and likely good enough for a long time
 - Storing sets as arrays in Postgres. Marshaling each member of a set into a row in the database would be slower to fetch, inefficient to store due to index bloat, and slower to deserialize. Postgres has a handy array column type that avoids having to store lists as CSVs or something like that which `django-contrib` supports just fine, so it seemed like a good option. In a data warehouse, I'd likely pick something different so that cross-cutting queries could be authored easily (what cell do most people click first? how many opens does it take to lose on average?), but, this system doesn't yet need to support those requirements.

As required, the list of mines for a game isn't revealed to the client while the game is underway so that a crafty coder couldn't cheat, but, the mine list is accessible via the API. The client side application is structured as a classic React app that uses Apollo to communicate with the server and cache data. The most important pieces of code here would be:
 - `Minefield` in the `play_game` folder which renders all the cells of a minesweeper game
 - `QuickQuery` and `QuickMutation` which are small but really useful Apollo wrappers for reducing boilerplate
 - `Root` which sets up the whole React context, kind of like a `settings.py`

 Key design decisions on the client are:
 - No fancy state management library is used to reduce dependencies and implicit happenings. I think React shines most when it is reacting to explicit things that you do.
 - Typescript compiled via Webpack is used instead of plain old JavaScript. I really like having the assurance that I am passing all the right props to components and that my callbacks are going to get what they ask for, and I think in bigger applications this kind of thing really shines when helping people onboard and maintain.
 - Everything that can be a component generally is, in the React way, like for example the data fetchers and the router.

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
 - [X] Implement hexagonal game
 - [x] Deploy via Heroku
 - [ ] Deploy via k8s
 - [ ] Implement real time game type
