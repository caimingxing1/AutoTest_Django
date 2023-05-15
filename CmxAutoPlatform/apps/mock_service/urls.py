from django.contrib import admin
from django.urls import path, re_path, include
from mock_service import views

urlpatterns = [
    path('mock/', views.MockProjectViews.as_view()),
    path('mock/<int:pk>/', views.MockProjectView.as_view()),
    path('mock/unitlist/', views.MockUnitViews.as_view()),
    path('mock/unitlist/<int:pk>/', views.MockUnitView.as_view()),
    path('mock/service/', views.MitmProxyServe.as_view()),
]
