from dangit.settings import *  # noqa
import django_heroku

DEBUG = False

django_heroku.settings(locals())
