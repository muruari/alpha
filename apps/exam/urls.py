from django.conf.urls import url
from . import views

urlpatterns = [
   
    url(r'^$', views.registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_trip$', views.add_trip_page),
    url(r'^create_trip$', views.create_trip),
    url(r'^reserve_trip/(?P<id>\d+)$', views.reserve_trip),
    url(r'^remove_trip/(?P<id>\d+)$', views.remove_trip),
    url(r'^trip_info/(?P<id>\d+)$', views.trip_info),
    url(r'^dashboard$', views.dashboard)
       
]