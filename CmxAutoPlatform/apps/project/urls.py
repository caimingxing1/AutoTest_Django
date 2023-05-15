from django.urls import path

from project import views

urlpatterns = [
    path('/', views.Project.as_view()),
    path('/<int:pk>/', views.Project.as_view()),
    # path('mock/unitlist/', views.MockUnitViews.as_view()),
    # path('mock/unitlist/<int:pk>/', views.MockUnitView.as_view()),
    # path('mock/service/', views.MitmProxyServe.as_view()),
]