from django.urls import path

from pressure import views

urlpatterns = [
    path('plan/', views.PressuerPlans.as_view()),
    path('plan/<int:pk>/', views.PressurePlan.as_view()),
    path('tasks/', views.Tasks.as_view()),
    path('task/<int:pk>/', views.TaskSingle.as_view()),
    path('scripts/', views.ScriptsViews.as_view()),
    path('scripts/<int:pk>/', views.ScriptsView.as_view())
    # path('mock/unitlist/', views.MockUnitViews.as_view()),
    # path('mock/unitlist/<int:pk>/', views.MockUnitView.as_view()),
    # path('mock/service/', views.MitmProxyServe.as_view()),
]
