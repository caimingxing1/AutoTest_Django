from rest_framework.response import Response


# 需要传入的是序列化对象
class APIResponse(Response):
    def __init__(self, code=100, msg='成功', result=None, status=None, headers=None, content_type=None, **kwargs):
        dic = {
            'code': code,
            'msg': msg
        }
        if result:
            dic['data'] = result
        dic.update(kwargs)
        # 对象来调用对象的绑定方法，self会自动传值。
        super().__init__(data=dic, status=status, headers=headers, content_type=content_type)
        # 类来调用对象的绑定方法，这个方法就是一个普通函数有几个参数就要传几个参数。
        # Response.__init__(data=dic, status=status, headers=headers, content_type=content_type)
