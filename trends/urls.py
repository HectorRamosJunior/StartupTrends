from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.startup_list, name='startup_list'),
    url(r'^create/$', views.get_startups, name='get_startups'),
]