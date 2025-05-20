from rest_framework import permissions


class CanEditOnlyUnprovedRecipes(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            not obj.public and
            not obj.admin_approved and
            obj.author == request.user
        )
