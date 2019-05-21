from django.urls import path
from django.conf.urls import url
from . import views
from data.models import Padron_electoral

app_name = 'data'

urlpatterns = [
    path('', views.listViewData.as_view(), name='getAllData'),
    path('statistics/', views.getQuantityVoters, name='getQuantityVoters'),
    path('filter/<search>', views.searchDetailView.as_view(), name='detailView'),
    path('distelec/', views.distelecListView.as_view(), name='distelec')
]
