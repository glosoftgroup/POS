from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from passlib.hash import pbkdf2_sha256

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from ...userprofile.models import Staff

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
def users(request):
  return TemplateResponse(request, 'dashboard/users/users.html', {})

@staff_member_required
def user_add(request):
  return TemplateResponse(request, 'dashboard/users/add_user.html', {})

@staff_member_required
@csrf_exempt
def user_process(request):
    user = Staff.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        encr_password = pbkdf2_sha256.encrypt(password, rounds=1000,salt_size=32)
        nid = request.POST.get('nid')
        mobile = request.POST.get('mobile')
        image= request.FILES.get('image')
        new_user = Staff(
            name = name,
            email = email,
            password = encr_password,
            nid = nid,
            mobile = mobile,
            image = image
        )
        new_user.save()
        return HttpResponse("success")