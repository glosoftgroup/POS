from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        url(r'^$', views.perms, name='perms'),
        url(r'^add_group/$', views.create_group, name='add_group'),
        url(r'^group_assign_permission/$', views.group_assign_permission, name='group_assign_permission'),
        url(r'^get_group_users/$', views.get_group_users, name='get_group_users'),
        url(r'^group_edit/$', views.group_edit, name='group_edit'),
]

if settings.DEBUG:
    # urlpatterns += [ url(r'^static/(?P<path>.*)$', serve)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)