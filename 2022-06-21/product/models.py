from django.db import models
from user.models import User
from datetime import timedelta, datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=70)
    thumbnail = models.ImageField("썸네일", upload_to='product/')
    description = models.TextField("설명", max_length=255, blank=True, null=True)
    created_date = models.DateTimeField("작성일", auto_now_add=True)
    exposure_start = models.DateTimeField("노출 시작일", default=datetime.now)
    exposure_end = models.DateTimeField("노출 종료일", default=datetime.now()+timedelta(days=6))
    price = models.CharField("가격", max_length=128, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} 님의 제품"


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField("내용", max_length=256)
    rating = models.IntegerField("평점", validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_date = models.DateField("작성일", auto_now_add=True)

    def __str__(self):
        return f"{self.product}상품 {self.author}님의 리뷰"