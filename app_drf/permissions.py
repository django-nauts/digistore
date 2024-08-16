from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            # Readonly access to all users
            request.method in SAFE_METHODS and
            request.user or
            # superuser has access to all methods
            request.user and
            request.user.is_superuser
        )


class IsSuperUserOrStaffReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            # get access to authors readonly
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_staff or
            # superuser has access to all methods
            request.user and
            request.user.is_superuser
        )


class IsStaffOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            # all users have access to readonly methods(GET, HEAD, OPTION)
            request.method in SAFE_METHODS or
            # Staff has access to all methods
            request.user and request.user.is_staff)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser or obj.author == request.user)


class IsUserOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser or obj.user == request.user)
