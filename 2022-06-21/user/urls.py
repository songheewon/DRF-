from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', views.UserApiView.as_view()),
    path('logout/', views.UserApiView.as_view()),
    path('<obj_id>/', views.UserView.as_view()),
]