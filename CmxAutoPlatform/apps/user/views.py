from django.shortcuts import render
# Create your views here.
from CmxAutoPlatform.utils.response import APIResponse

from rest_framework.views import APIView


class UserInfo(APIView):
    # 获取用户的信息
    def get(self, request):
        user_info = {
            "roles": ['admin'],
            "introduction": 'I am a super administrator',
            "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            "name": 'Super Admin'
        }
        return APIResponse(result=user_info)

    # 修改用户的信息
    def post(self, request):
        ...
