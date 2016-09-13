from django.conf.urls import url
from . import views

app_name = 'error'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sorting/(?P<column>.+)/$', views.sorting, name='sorting'),
    url(r'^(?P<error_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add_error, name='add'),
]
