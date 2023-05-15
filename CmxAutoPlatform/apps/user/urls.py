from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from mock_service import urls as mockurl
from rest_framework_jwt.views import obtain_jwt_token
from user import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('info/', views.UserInfo.as_view()),
]
