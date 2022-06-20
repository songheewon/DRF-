from rest_framework import serializers
from .models import Category, Article, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ["username", "contents"]


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    class Meta:
        model = Article
        fields = ["category", "title", "contents", "comment_set"]