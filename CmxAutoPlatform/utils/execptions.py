from rest_framework.views import exception_handler
# from CmxAutoPlatform.utils import response
from .response import APIResponse
from .logger import log


def common_execption_handler(exc, context):
    log.error("view是:%s，错误是%s" % (context['view'].__class__.__name__, str(exc)))
    # context['view']是TextView的对象，想拿出这个对象对应的类名
    print(context['view'].__class__.__name__)
    ret = exception_handler(exc, context)  # 是Respons对象，它内部有个data
    if not ret:  # dir内置处理不了，丢给Django的，我们自己来处理。
        # 可以加好多逻辑，更加具体的捕获异常
        return APIResponse(code=0, msg='error', result=str(exc))
    else:
        return APIResponse(code=0, msg='error', result=ret.data)
