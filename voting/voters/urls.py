from django.urls import path,re_path
from . import views

urlpatterns =[path('',views.voterHome),
              path('getBalance',views.getBalance),
              path('transfer',views.transfer),
              path('getBlock', views.getBlock),
              path('vote', views.vote),
            ]