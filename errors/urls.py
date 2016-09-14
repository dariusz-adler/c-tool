from django.conf.urls import url
from . import views

app_name = 'error'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sorting/(?P<column>.+)/asc$', views.asc_sorting, name='asc_sorting'),
    url(r'^sorting/(?P<column>.+)/desc$', views.desc_sorting, name='desc_sorting'),
    url(r'^(?P<error_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add_error, name='add'),
]
