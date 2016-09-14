from django.conf.urls import url
from . import views

app_name = 'error'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #/error.id
    url(r'^(?P<error_id>[0-9]+)/$', views.detail, name='detail'),

    #/add
    url(r'^add/$', views.add_error, name='add'),

    #/update/error.id
    url(r'^update/(?P<error_id>[0-9]+)/$', views.update_error, name='update')
]
