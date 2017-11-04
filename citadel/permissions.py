from rest_framework import permissions


class HasGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        required_groups = getattr(view, 'required_groups', {})
        # Return True si alguno de los grupos del usuario estan en required_groups
        if request.user.is_superuser:
            return True

        return set(required_groups).intersection(user_groups)
