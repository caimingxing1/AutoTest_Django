from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str as smart_text
import jwt
from . import response
from user import models


# 定义响应jwt的数据格式
def jwt_response_payload_handler(token, user=None, request=None):
    dic = {
        'code': 100,
        'msg': "成功"
    }
    data = {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }
    dic['data'] = data
    return dic


# class MyJwtAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         jwt_value=request.META.get('HTTP_AUTHORIZATION')
#         if jwt_value:
#             try:
#             #jwt提供了通过三段token，取出payload的方法，并且有校验功能
#                 payload=jwt_decode_handler(jwt_value)
#             except jwt.ExpiredSignature:
#                 raise AuthenticationFailed('签名过期')
#             except jwt.InvalidTokenError:
#                 raise AuthenticationFailed('用户非法')
#             except Exception as e:
#                 # 所有异常都会走到这
#                 raise AuthenticationFailed(str(e))
#             # 因为payload就是用户信息的字典
#             print(payload)
#             # return payload, jwt_value
#             # 需要得到user对象，
#             # 第一种，去数据库查
#             # user=models.User.objects.get(pk=payload.get('user_id'))
#             # 第二种不查库
#             user=models.User(id=payload.get('user_id'),username=payload.get('username'))
#             return user,jwt_value
#         # 没有值，直接抛异常
#         raise AuthenticationFailed('您没有携带认证信息')


class MyJwtAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        # jwt_value = request.META.get('HTTP_AUTHORIZATION')
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        if smart_text(auth[0].lower()) == auth_header_prefix:
            if auth:
                jwt_value = auth[1]
                try:
                    # jwt提供了通过三段token，取出payload的方法，并且有校验功能
                    payload = jwt_decode_handler(jwt_value)
                except jwt.ExpiredSignature:
                    raise AuthenticationFailed('签名过期')
                except jwt.InvalidTokenError:
                    raise AuthenticationFailed('用户非法')
                except Exception as e:
                    # 所有异常都会走到这
                    raise AuthenticationFailed(str(e))
                user = self.authenticate_credentials(payload)
                return user, jwt_value
        # 没有值，直接抛异常
        raise AuthenticationFailed('您没有携带认证信息')













