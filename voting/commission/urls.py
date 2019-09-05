from django.urls import path
from . import views
urlpatterns = [path('', views.commission),
               path('register', views.register),
               path('distribute', views.distribute),
               path('distribute/dist',views.dist),
               path('showTransactions',views.showTx),


]