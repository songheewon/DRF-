from django.db import models
from user.models import User as UserModel


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    category = models.ManyToManyField(Category, related_name="articles")
    contents = models.TextField(max_length=256)

    def __str__(self):
        return f"{self.user.username} 님의 게시글"