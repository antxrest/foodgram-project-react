from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Разрешение для администратора, иначе только чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение для автора, иначе только чтение."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
