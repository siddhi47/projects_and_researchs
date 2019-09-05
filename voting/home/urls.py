from django.urls import path, include
from . import views

urlpatterns = [path('', views.index),
               path('register/',views.register),
               path('register/submit',  views.submit),
               path('login', views.loginView),
               path('vote', views.vote)
               ]
