from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from blog.models import Article


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


class UserArticleView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user
        articles = Article.objects.filter(user_id=user.id).values()
        titles=[]
        for article in articles:
            titles.append(article['title'])
        title_list_str=", ".join(titles)
        return Response({"title": title_list_str})