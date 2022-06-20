from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import BasePermission
from datetime import datetime


class OldUser3days(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        join_date = user.join_date
        now = datetime.today()
        return now-join_date >= datetime.timedelta(days=3)


class OldUser7days(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        join_date = user.join_date
        now = datetime.today()
        return (user.is_admin or user) and now-join_date >= datetime.timedelta(days=7)


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET',)
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하기 위해 로그인 해주세요.",
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        if request.method=='GET':
            if user.is_authenticated and user.is_admin:
                return True

            elif user.is_authenticated and request.method in self.SAFE_METHODS:
                return True

            return False

        if request.method=='POST':
            if user.is_authenticated and user.is_admin:
                return True
            return bool(request.user and request.user.join_date < (datetime.today() - datetime.timedelta(days=3)))

