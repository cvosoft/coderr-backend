from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.exceptions import APIException


class IsAuthUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            raise CustomAuthenticationFailed()

        return True


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["PATCH", "DELETE"]:
            return bool(request.user == obj.reviewer)
        return False


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            raise CustomAuthenticationFailed()

        if not hasattr(user, 'profile') or user.profile.type != "customer":
            raise AuthenticationFailed("Nur Customer-User erlaubt.")

        return True


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            raise CustomAuthenticationFailed()

        if not hasattr(user, 'profile') or user.profile.type != "business":
            raise AuthenticationFailed("Nur Business-User erlaubt.")

        return True


class CustomAuthenticationFailed(APIException):
    status_code = 401
    default_detail = 'Nicht authentifiziert.'
    default_code = 'not_authenticated'
