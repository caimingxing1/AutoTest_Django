"""CmxAutoPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from mock_service import urls as mockurl
from user import urls as userurl
from pressure import urls as pressureurl
from project import urls as projecturl
urlpatterns = [
    path('admin/', admin.site.urls),
    # 打开了media文件夹路径打开了
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIR_ROOT}),
    path('mockservice/', include(mockurl)),
    path('user/', include(userurl)),
    path('pressure/', include(pressureurl)),
    path('project', include(projecturl)),
]
