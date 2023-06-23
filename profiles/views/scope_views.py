from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe

from profiles.forms.scope_form import ScopeCreateRBACForm
from profiles.models import RBAC, Scope

from django.urls import reverse

from django.contrib.auth.models import User


def scope_rbac_create(request, scope_id):
    scope = get_object_or_404(Scope, id=scope_id)
    form = ScopeCreateRBACForm(request.POST or None, scope=scope)
    class_name = scope.get_object().__class__.__name__
    if form.is_valid():
        form.save()
        return redirect(scope.get_absolute_url())
    breadcrumbs = [
        {'text': class_name, 'url': reverse(f'profiles:{class_name.lower()}_list')},
        {'text': scope,
         'url': reverse(f'profiles:{class_name.lower()}_details', kwargs={"pk": scope.id})},
        {'text': f'Add RBAC', 'url': ""},
    ]
    context = {'form': form, 'object_name': "billing_group", 'breadcrumbs': breadcrumbs,
               'action': "edit"}
    return render(request, 'generics/generic_form.html', context)


def scope_rbac_delete(request, scope_id, rbac_id, user_id):
    scope = get_object_or_404(Scope, id=scope_id)
    rbac = get_object_or_404(RBAC, group_ptr=rbac_id)
    user = get_object_or_404(User, id=user_id)
    class_name = scope.get_object().__class__.__name__
    details = None
    if hasattr(scope, "organization"):
        team_name_list = RBAC.objects.filter(
            scope__in=scope.organization.teams.all(),
            user__id=user_id
        ).values_list("scope__name", flat=True)
        details = {
            'warning_sentence': 'Warning: User still in following Teams, it will be removed from them:',
            'details_list': [f"{team}," for team in team_name_list]
        } if team_name_list else None

    if request.method == 'POST':
        scope.remove_user_in_role(user, rbac.role.name)
        return redirect(scope.get_absolute_url())
    context = {
        'breadcrumbs': [
            {'text': class_name, 'url': reverse(f'profiles:{class_name.lower()}_list')},
            {'text': scope,
             'url': reverse(f'profiles:{class_name.lower()}_details', kwargs={"pk": scope.id})},
            {'text': "Role", 'url': ""},
            {'text': rbac.role, 'url': ""},
            {'text': user, 'url': ""},
        ],
        'action_url': reverse(f'profiles:scope_rbac_delete',
                              kwargs={"scope_id": scope.id, "rbac_id": rbac_id, "user_id": user_id}) + "#users",
        'confirm_text': mark_safe(f"Confirm to remove <strong>{user}</strong> from <strong>{rbac.role}</strong>?"),
        'button_text': 'Delete',
        'details': details
    }
    return render(request, 'generics/confirm-delete-template.html', context=context)