from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.startup_list, name='startup_list'),
    url(r'^create/$', views.get_startups, name='get_startups'),
    url(r'^gather/$', views.get_stacks, name='get_stacks'),
    url(r'^stack_list/$', views.stack_list, name='get_stacks'),
]