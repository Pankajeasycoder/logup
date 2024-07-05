from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('index/',index, name="index"),
    path('account/login/',login_page, name="login"),
    path('account/register/',register, name="register"),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("client/",Client_profile,name="client"),
    path("dealer/",Dearler_Profile,name="dealer"),







    

]