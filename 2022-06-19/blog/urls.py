from django.urls import path
from blog import views

urlpatterns = [
    path('', views.ArticleView.as_view()),
]