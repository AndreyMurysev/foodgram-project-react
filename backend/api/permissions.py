from rest_framework.permissions import SAFE_METHODS, BasePermission


class EditAuthorAndAdminOrReadAll(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_superuser)
