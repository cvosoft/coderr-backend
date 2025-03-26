from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.exceptions import APIException


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise CustomAuthenticationFailed()
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "PATCH":
            return bool(request.user == obj.user)
        return False


class CustomAuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'Nicht authentifiziert.'
    default_code = 'not_authenticated'
