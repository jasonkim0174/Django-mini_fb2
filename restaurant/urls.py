## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app

urlpatterns = [
    path(r'/', views.main, name="main"),
    path(r'main', views.main, name="restaurant-main"),
    path(r'/restaurant-order', views.order, name="restaurant-order"),
    path(r'/restaurant-confirmation', views.confirmation, name="restaurant-confirmation"),
]