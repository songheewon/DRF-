from rest_framework import serializers
from .models import Category, Article, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ["user", "comment"]


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    get_categories = serializers.ListField(required=False)
    comment_set = CommentSerializer(many=True)

    def validate(self, data):
        categories = data.get("get_categories", [])

        if len(data.get("title", "")) < 5:
            raise serializers.ValidationError(
                detail={"error": "제목은 5글자 이상이어야 합니다."}
            )
        if len(data.get("content", "")) < 20:
            raise serializers.ValidationError(
                detail={"error": "내용은 20자 이상이어야 합니다."}
            )
        if not categories:
            raise serializers.ValidationError(
                detail={"error": "카테고리를 선택하지 않았습니다."}
            )
        for category_id in categories:
            if not Category.objects.filter(id=category_id).exists():
                raise serializers.ValidationError(
                    detail={"error": "잘못된 카테고리입니다."}
                )
        return data

    def create(self, validated_data):
        get_categorys = validated_data.pop("get_categories")
        my_article = Article.objects.create(**validated_data)
        my_article.category.add(*get_categorys)

        return my_article

    def update(self, instance, validated_data):
        get_categorys = validated_data.pop("get_categories")

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        instance.category.set(get_categorys)
        return instance

    class Meta:
        model = Article
        fields = ["category", "title", "content", "comments", "user", "get_categories"]
