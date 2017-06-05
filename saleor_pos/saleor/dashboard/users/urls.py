from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from . import api
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        # url(r'^$', views.users, name='users'),
        url(r'^$', permission_required('userprofile.view_user', login_url='account_login')
            (views.users), name='users'),
        url(r'^add/$', permission_required('userprofile.add_user', login_url='account_login')
            (views.user_add), name='user-add'),
        # url(r'^add/$', views.user_add, name='user-add'),
        url(r'^user_process/$', views.user_process, name='user_process'),
        url(r'^detail/(?P<pk>[0-9]+)/$', views.user_detail, name='user-detail'),
        url(r'^delete/(?P<pk>[0-9]+)/$', views.user_delete, name='user-delete'),
        url(r'^edit/(?P<pk>[0-9]+)/$', views.user_edit, name='user-edit'),
        url(r'^user_update(?P<pk>[0-9]+)/$', views.user_update, name='user-update'),
        url(r'^user_assign_permission/$', views.user_assign_permission, name='user_assign_permission'),
        # url(r'^add/', permission_required('userprofile.add_user', login_url='account_login')(views.user_add)),
        
]

if settings.DEBUG:
    # urlpatterns += [ url(r'^static/(?P<path>.*)$', serve)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)