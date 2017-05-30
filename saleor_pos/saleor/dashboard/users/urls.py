from django.conf.urls import url

from . import api
from . import views


urlpatterns = [
        url(r'^$', views.users, name='users'),
        url(r'^add/$', views.user_add, name='user-add'),
        url(r'^user_process/$', views.user_process, name='user_process'),
]
