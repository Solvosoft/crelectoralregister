
from django.conf.urls import url
from importcrdata import views

urlpatterns = [
    url(r'^$', views.getTseData, name='index'),
    url('load/', views.loadDataView, name='loader'),
#    url('view-info', views.infoViewer, name='viewer')

]