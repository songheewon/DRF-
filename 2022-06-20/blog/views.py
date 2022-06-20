from .models import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from DRF.permissions import IsAdminOrIsAuthenticatedReadOnly, OldUser7days


class ArticleView(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly, OldUser7days]

    def get(self, request):
        user = request.user
        articles = Article.objects.filter(user_id=user.id, post_end_date__gt=datetime.today()).order_by('-post_date')
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