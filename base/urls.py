from django.urls import path, include
from .views import *
from django.contrib import admin

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('main/', main, name="main"),
    path('logout/', logoutView, name="logoutView"),
    path('chat/', chat, name="chat")
    #path('', views.register)
]
