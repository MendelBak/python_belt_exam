from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^show$', views.show),
    url(r'^travels$', views.travels),
    url(r'^new_trip$', views.new_trip),
    url(r'^create_trip$', views.create_trip),
    url(r'^join/(?P<travel_id>\d+)$', views.join),
    url(r'^destination/(?P<travel_id>\d+)$', views.destination),
    url(r'^logout$', views.logout),
    url(r'^(?P<user_id>\d+)/destroy$', views.destroy),
]