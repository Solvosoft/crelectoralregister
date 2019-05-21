
from django.urls import path
from importcrdata import views

urlpatterns = [

    path('statistics/', views.Statistics.as_view(), name='statistics'),
    path('list/', views.PadronView.as_view(), name='padron'),
    path('listelector/', views.NewPerson.as_view(), name='listelector'),
    path('<str:cedula>/', views.ElectorInfoView.as_view(), name='elec'),


]