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
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from ...userprofile.models import User

def perms(request):
    users = User.objects.all().order_by('id')
    permissions = Permission.objects.all()
    groups = Group.objects.all()
    try:
        first_group = Group.objects.filter()[:1].get()
        users_in_group = User.objects.filter(groups__id=first_group.id)
        return TemplateResponse(request, 'dashboard/permissions/list.html', 
        {'users':users, 'permissions':permissions, 'groups':groups, 'users_in_group':users_in_group})
    except: ObjectDoesNotExist
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
        last_id_group = Group.objects.latest('id')
        return JsonResponse({"id":last_id_group.id, "name":last_id_group.name})

@csrf_exempt
def group_assign_permission(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)
        group_has_permissions = group.permissions.all()
        login_status = request.POST.get('check_login')
        permission_list = request.POST.getlist('checklist[]')
        users_in_group = User.objects.filter(groups__name=group.name)
        if login_status == 'inactive':   
            users_loop(False, users_in_group)
            return HttpResponse('deactivated')
        else:
            if group_has_permissions in permission_list:
                not_in_group_permissions = list(set(permission_list) - set(group_has_permissions))
                group.permissions.add(*not_in_group_permissions)
                group.save()
                refine_users_permissions(users_in_group, permission_list)
                users_loop(True, users_in_group)
                return HttpResponse('permissions added')
            else:
                not_in_group_permissions = list(set(permission_list) - set(group_has_permissions))
                group.permissions.remove(*group_has_permissions)
                group.permissions.add(*not_in_group_permissions)
                group.save()
                for user in users_in_group:
                    user.user_permissions.remove(*group_has_permissions)
                    user.user_permissions.add(*not_in_group_permissions)
                    user.save()
                users_loop(True, users_in_group)
                return HttpResponse('permissions updated')

def refine_users_permissions(users_in_group, permission_list):
    for user in users_in_group:
        user_has_permissions = Permission.objects.filter(user=user)
        if user_has_permissions in permission_list:
            not_in_user_permissions = list(set(permission_list) - set(user_has_permissions))
            user.is_staff = True
            user.is_active = True
            user.user_permissions.add(*not_in_user_permissions)
            user.save()
        else:
            not_in_user_permissions = list(set(permission_list) - set(user_has_permissions))
            user.is_staff = True
            user.is_active = True
            user.user_permissions.remove(*user_has_permissions)
            user.user_permissions.add(*not_in_user_permissions)
            user.save()

def users_loop(status, users):
    for user in users:
        user.is_staff = status
        user.is_active = status
        user.save()

def get_group_users(request):
    if request.is_ajax() and request.method == 'POST': 
        group_id = request.POST.get('id')
        users = User.objects.filter(groups__id=group_id)
        html = render_to_string('dashboard/permissions/group_users.html', {'users':users})
        return HttpResponse(html)

def group_edit(request):
    group_id = request.POST.get('id')
    group = Group.objects.get(id=group_id)
    permissions = Permission.objects.all()
    group_permissions = Permission.objects.filter(group=group)
    ctx = {'group': group,'permissions':permissions, 'group_permissions':group_permissions}
    html = render_to_string('dashboard/permissions/group_permissions.html', ctx)
    return HttpResponse(html)

def group_delete(request, pk):
    group = Group.objects.get(id=pk)
    group_permissions = Permission.objects.filter(group=group)
    users_in_group = User.objects.filter(groups__name=group.name)
    if request.method == 'POST':
        group.permissions.remove(*group_permissions)
        for user in users_in_group:
            group.user_set.remove(user)
            user.user_permissions.remove(*group_permissions)
        group.delete()
        return HttpResponse('success')
    else:
        return HttpResponse('error deleting')