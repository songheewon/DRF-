from rest_framework import serializers
from .models import Product, Review
from django.utils import timezone


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["author", "content", "rating"]


class ProductSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    review_author = ReviewSerializer(read_only=True, source="review_set", many=True)
    is_active = serializers.BooleanField(default=True)

    def get_review(self, obj):
        reviews = list(obj.review_set.values())
        if len(reviews) == 0:
            return "리뷰 없음"
        return reviews[-1] # 최근 댓글 리턴


    average_review = serializers.SerializerMethodField()
    def get_average(self, obj):
        product_reviews = obj.review_set.values()
        rating_list = [review['rating'] for review in product_reviews]

        if len(rating_list) == 0:
            return "평점 없음"
            average_rating = "평점 없음"

        average_rating = round(sum(rating_list) / len(rating_list), 1)
        return average_rating

    def validate(self, data):
        method = self.context.get("request").method
        if method == "POST":
            if data.get("exposure_end") < timezone.now():
                raise serializers.ValidationError(
                    detail={"error": "상품 등록기간이 지났습니다."}
                )
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        product.description += f"  <{product.created_date} 에 등록된 상품>"
        product.save()
        return product

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if instance.updated == instance.created:
            instance.description = f"<{instance.updated} 에 수정됨> \n" + instance.description
            instance.save()
        else:
            update_desc = "\n".join(instance.description.split("\\n")[1:])
            updated = f"<{instance.updated} 에 수정됨>\n" + update_desc
            instance.description = updated
            instance.save()
        return instance

    class Meta:
        model = Product
        fields = "__all__"