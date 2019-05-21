from django.conf.urls import url
from django.urls import path
from importcrdata import views

app_name = 'importcrdata'
urlpatterns = [
    url(r'^$', views.PadronView.as_view(), name='index'),
    url(r'estadisticas/$', views.StatisticsView.as_view(), name='estadisticas'),
    url(r'padron/agregar_persona/$', views.PersonCreateView.as_view(), name="agregar-persona"),
    url(r'estadisticas/provincia_ajax/$', views.ProvinciaAjaxView.as_view(), name='provincia-data'),
    url(r'estadisticas/canton_ajax/$', views.CantonAjaxView.as_view(), name='canton-data'),
    url(r'estadisticas/distrito_ajax/$', views.DistritoAjaxView.as_view(), name='distrito-data'),
    path('<int:cedula>/', views.PadronDetailView.as_view(), name="detalle"),

    # url('deco', views.testDecorator, name='deco'),

]
