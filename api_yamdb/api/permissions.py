from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.admin
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return request.user.admin or request.user.is_superuser


class AllOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                and request.user.is_anonymous
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.admin
                or request.user.moderator
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.admin
                     or request.user.is_superuser)
                or request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)
