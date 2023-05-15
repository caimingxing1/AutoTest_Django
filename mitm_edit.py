import json
import django
import os

from mitmproxy.http import Request, Response, HTTPFlow
from mitmproxy import http

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CmxAutoPlatform.settings.dev")
django.setup()


def request(flow: HTTPFlow):
    """
    在请求发送到服务器之前进行干预的脚本
    可以修改请求头/体、url等内容，用来欺骗服务器，还可以伪装成一个假服务器，直接给请求返回。
    :param flow:
    :return:
    """
    print(flow.request.headers)


def resoponse(flow: Response):
    """
    在请求发送到服务器后，服务器返回数据后进行干预的函数。
    修改的返回值/返回头/时间控制等
    :param flow:
    :return:
    """
    ...
