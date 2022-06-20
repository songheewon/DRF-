from rest_framework import serializers
from .models import User, UserProfile
from blog.serializers import ArticleSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["description", "nickname", "age", "hobby"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    article_set = ArticleSerializer(many=True)

    class Meta:
        model = User
        fields = ["username", "email", "fullname", "userprofile", "article_set"]