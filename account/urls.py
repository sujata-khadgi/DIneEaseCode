
from django.urls import path
from .views import *

urlpatterns = [
    path('ho', home,name="home"),
    path('about', about,name="about"),
    path('register', register,name="register"),
    path('login', login,name="login"),
    path('logout', logout,name ="logout"),



   
]