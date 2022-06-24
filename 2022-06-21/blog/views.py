from .models import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from DRF.permissions import IsAdminOrIsAuthenticatedReadOnly
from rest_framework import status
from serializers import ArticleSerializer
from django.db.models import Q


class ArticleView(APIView):
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user
        articles = Article.objects.filter(
            Q(post_date__lte=datetime.today(), post_end_date__gte=datetime.today()) |
            Q(user=user)
        ).order_by('-post_date')

        return Response(ArticleSerializer(articles, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        article_serializer = ArticleSerializer(data=data, context={"request": request})

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)

        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, obj_id):
        article = Article.objects.get(id=obj_id)
        article_serializer = ArticleSerializer(article, data=request.data, partial=True, context={"request": request})
        article_serializer.is_valid(raise_exception=True)
        article_serializer.save()

        return Response(article_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        return Response({"message": "게시글 삭제"})