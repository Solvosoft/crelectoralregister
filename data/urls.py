from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.getAllData, name='getAllData'),
    path('quantity/', views.getQuantityVoters, name='getQuantityVoters'),
]