from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from project import models
from project import ser
from CmxAutoPlatform.utils.response import APIResponse


# Create your views here.
class Project(APIView):
    def get(self, request: Request):
        project_obj = models.Project.objects.all()
        ser_pro = ser.ProjectSer(project_obj, many=True)
        return APIResponse(result=ser_pro.data)
