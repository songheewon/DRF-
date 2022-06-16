from django.urls import path
from user import views

urlpatterns = [
    path('', views.UserArticleView.as_view()),
    path('login/', views.UserApiView.as_view()),
    path('logout/', views.UserApiView.as_view()),
]