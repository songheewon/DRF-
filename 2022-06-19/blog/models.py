from django.db import models
from user.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=100)
    category = models.ManyToManyField(Category, related_name="articles")
    contents = models.TextField(max_length=256)

    def __str__(self):
        return f"{self.user.username} 님의 게시글"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField("댓글창", max_length=100)

    def __str__(self):
        return f"{self.user.username} 님의 댓글"