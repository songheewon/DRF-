from .models import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from datetime import datetime


class OldUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        join_date = user.join_date
        now = datetime.today()
        return now-join_date >= datetime.timedelta(days=3)


class ArticleView(APIView):
    permission_classes = [IsAuthenticated, OldUser]

    def get(self, request):
        user = request.user
        articles = Article.objects.filter(user_id=user.id).values()
        titles=[]
        for article in articles:
            titles.append(article['title'])
        title_list_str=", ".join(titles)
        return Response({"title": title_list_str})

    def post(self, request):
        user = request.user
        title = request.data.get("title", "")
        category = request.data.get("category")
        contents = request.data.get("contents", "")

        if len(title)<=5:
            return Response({"message": "제목은 5글자보다 길어야합니다!"})
        if len(contents)<=20:
            return Response({"message": "내용은 20글자보다 길어야합니다!"})
        if category is None:
            return Response({"message": "카테고리를 선택해주세요!"})
        new_article = Article.objects.create(user=user, title=title, contents=contents)
        new_article.category.add(category)
        return Response({"message": "게시 성공!"})