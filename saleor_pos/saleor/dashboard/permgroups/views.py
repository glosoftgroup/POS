from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import is_safe_url
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from passlib.hash import pbkdf2_sha256

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from ...userprofile.models import User

#    : code to import groups and permissions
#    -------------------------------------
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from api.models import Project
#--- execution
# new_group, created = Group.objects.get_or_create(name='new_group')
# # Code to add permission to group ???
# ct = ContentType.objects.get_for_model(Project)

# # Now what - Say I want to add 'Can add project' permission to new_group?
# permission = Permission.objects.create(codename='can_add_project',
#                                    name='Can add project',
#                                    content_type=ct)
# new_group.permissions.add(permission)


def perms(request):
    users = User.objects.all().order_by('id')
    permissions = Permission.objects.all()
    groups = Group.objects.all()
    return TemplateResponse(request, 'dashboard/permissions/list.html', 
        {'users':users, 'permissions':permissions, 'groups':groups})

@csrf_exempt
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        users = request.POST.getlist('users[]')
        try:
            group = Group.objects.get(name=group_name)
            return HttpResponse('error')
        except: ObjectDoesNotExist
        group = Group.objects.create(name=group_name)
        group.user_set.add(*users)
        group.save()
        last_id = Group.objects.latest('id')
        return HttpResponse(last_id)

@csrf_exempt
def group_assign_permission(request):
    if request.method == 'POST':
        group_id = request.POST.get('user_id')
        group = Group.objects.get(id=group_id)
        group_has_permissions = group.permissions.all()
        login_status = request.POST.get('check_login')
        permission_list = request.POST.getlist('checklist[]')
        users_in_group = User.objects.filter(groups__name=group.name)
        if login_status == 'inactive':   
            users_loop(False)
            return HttpResponse('deactivated')
        else:
            if group_has_permissions in permission_list:
                not_in_group_permissions = list(set(permission_list) - set(group_has_permissions))
                group.permissions.add(*not_in_group_permissions)
                group.save()
                users_loop(True)
                return HttpResponse('permissions added')
            else:
                not_in_group_permissions = list(set(permission_list) - set(group_has_permissions))
                group.permissions.remove(*group_has_permissions)
                group.permissions.add(*not_in_group_permissions)
                group.save()
                users_loop(True)
                return HttpResponse('permissions updated')

def users_loop(status):
    for user in users_in_group:
        user.is_staff = status
        user.is_active = status
        user.save()