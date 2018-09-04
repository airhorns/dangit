from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^.*$', views.index, name='index'),  # wildcard match to forward anything unrecognized on to the client side router
]
