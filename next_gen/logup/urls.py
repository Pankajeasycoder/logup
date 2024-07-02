from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('index/',index, name="index"),
    path('login/',login_page, name="login"),
    path('register/',register, name="register"),
]