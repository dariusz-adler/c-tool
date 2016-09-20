from django.conf.urls import url
from . import views

app_name = 'error'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^sorting/(?P<column>.+)/(?P<direction>.+)$', views.sorting, name='sorting'),

    # /details/[error.id]
    url(r'^details/(?P<error_id>[0-9]+)/$', views.detail, name='detail'),

    #/add
    url(r'^add/$', views.add_error, name='add'),

    #/update/error.id
    url(r'^update/(?P<error_id>[0-9]+)/$', views.update_error, name='update'),

    #/advanced_search
    url(r'advanced_search/$', views.advanced_search, name='advanced_search'),

    #/login
    url(r'login/$', views.login_user, name='login_user'),
    url(r'logout/$', views.logout_user, name='logout_user'),

    url(r'index/$', views.index, name='index'),

	# /createcopy/[copy-id]
    url(r'^createcopy/(?P<error_id>[0-9]+)/$', views.create_copy, name='create_copy'),
]
