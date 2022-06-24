from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request):
        user = request.user
        serialized_user_data = UserSerializer(user).data
        return Response(serialized_user_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user_serializer = UserSerializer(data=data, context={"request": request})
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True, context={"request": request})
        user_serializer.is_valid()
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        return Response({"message": "delete method!!"})


class UserApiView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})

        login(request, user)
        return Response({"message": "로그인 성공!!"})

    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!!"})