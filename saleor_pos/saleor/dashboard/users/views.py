from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required

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


@staff_member_required
@permission_required('userprofile.view_user', raise_exception=True)
def users(request):
	users = User.objects.all().order_by('id')
	return TemplateResponse(request, 'dashboard/users/users.html', {'users':users})

@staff_member_required
@permission_required('userprofile.add_user', raise_exception=True)
def user_add(request):
	permissions = Permission.objects.all()
	for permission in permissions:
		g_name = str(permission).split()
		gname1 = g_name[0]
		gname2 = g_name[2]
		gname3 = g_name[3]
		gname4 = g_name[4]
		gname5 = g_name[5]
		gname6 = g_name[6]
	return TemplateResponse(request, 'dashboard/users/add_user.html', 
		{'permissions':permissions, 'gname1':gname1, 'gname2':gname2, 'gname3':gname3,'gname4':gname4,'gname5':gname5,'gname6':gname6})

@staff_member_required
@csrf_exempt
def user_process(request):
	user = User.objects.all()
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		password = request.POST.get('password')
		encr_password = make_password(password)
		nid = request.POST.get('nid')
		mobile = request.POST.get('mobile')
		image= request.FILES.get('image')
		new_user = User(
			name = name,
			email = email,
			password = encr_password,
			nid = nid,
			mobile = mobile,
			image = image
		)
		new_user.save()
		last_id = User.objects.latest('id')
		return HttpResponse(last_id.id)

def user_detail(request, pk):
	user = get_object_or_404(User, pk=pk)
	permissions = Permission.objects.filter(user=user)
	groups = user.groups.all()
	return TemplateResponse(request, 'dashboard/users/detail.html', {'user':user,'permissions':permissions,'groups':groups})

def user_delete(request, pk):
	user = get_object_or_404(User, pk=pk)
	if request.method == 'POST':
		user.delete()
		return HttpResponse('success')
def user_edit(request, pk):
	user = get_object_or_404(User, pk=pk)
	permissions = Permission.objects.all()
	user_permissions = Permission.objects.filter(user=user)
	ctx = {'user': user,'permissions':permissions, 'user_permissions':user_permissions}
	return TemplateResponse(request, 'dashboard/users/edit_user.html', ctx)

def user_update(request, pk):
	user = get_object_or_404(User, pk=pk)
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		password = request.POST.get('password')
		nid = request.POST.get('nid')
		mobile = request.POST.get('mobile')
		image= request.FILES.get('image')
		if password == user.password:
			encr_password = user.password
		else:
			encr_password = make_password(password)
		if image :
			user.name = name
			user.email = email
			user.password = encr_password
			user.nid = nid
			user.mobile = mobile
			user.image = image
			user.save()
			return HttpResponse("success with image")
		else:
			user.name = name
			user.email = email
			user.password = encr_password
			user.nid = nid
			user.mobile = mobile
			user.save()
			return HttpResponse("success without image")

@csrf_exempt
def user_assign_permission(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		user = get_object_or_404(User, pk=user_id)
		user_has_permissions = Permission.objects.filter(user=user)
		login_status = request.POST.get('check_login')
		permission_list = request.POST.getlist('checklist[]')
		if login_status == 'inactive':
			user.is_staff = False
			user.is_active = False
			user.user_permissions.remove(*user_has_permissions)
			user.save()
			return HttpResponse('deactivated')
		else:
			if user_has_permissions in permission_list:
				not_in_user_permissions = list(set(permission_list) - set(user_has_permissions))
				user.is_staff = True
				user.is_active = True
				user.user_permissions.add(*not_in_user_permissions)
				user.save()
				return HttpResponse('permissions added')
			else:
				not_in_user_permissions = list(set(permission_list) - set(user_has_permissions))
				user.is_staff = True
				user.is_active = True
				user.user_permissions.remove(*user_has_permissions)
				user.user_permissions.add(*not_in_user_permissions)
				user.save()
				return HttpResponse('permissions updated')



		