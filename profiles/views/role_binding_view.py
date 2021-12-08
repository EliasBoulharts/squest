from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from guardian.shortcuts import get_objects_for_user

from profiles.models import UserRoleBinding, TeamRoleBinding, Team, Role


@login_required
def ajax_get_users_with_role(request):
    role_id = request.GET.get('role_id')
    content_type_id = request.GET.get('content_type_id')
    object_id = request.GET.get('object_id')
    bindings = UserRoleBinding.objects.filter(role__id=role_id, content_type__id=content_type_id, object_id=object_id)
    selected = [binding.user.id for binding in bindings]
    return render(request, 'profiles/role/users-dropdown-list.html',
                  {'users': User.objects.all(), 'selected': selected})

@login_required
def ajax_get_teams_with_role(request):
    role_id = request.GET.get('role_id')
    content_type_id = request.GET.get('content_type_id')
    object_id = request.GET.get('object_id')
    bindings = TeamRoleBinding.objects.filter(role__id=role_id, content_type__id=content_type_id, object_id=object_id)
    selected = [binding.user.id for binding in bindings]
    return render(request, 'profiles/role/teams-dropdown-list.html',
                  {'teams': Team.objects.all(), 'selected': selected})


def get_objects_of_user_from_content_type(user, content_type_id):
    content_type = ContentType.objects.get(id=content_type_id)
    return [(obj.id, obj.__str__) for obj in
            get_objects_for_user(user, f"{content_type.app_label}.change_{content_type.name}")]


def get_roles_from_content_type(content_type_id):
    content_type = ContentType.objects.get(id=content_type_id)
    return [(role.id, role.name) for role in Role.objects.filter(content_type=content_type)]