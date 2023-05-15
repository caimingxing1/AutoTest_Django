import datetime
import os.path

from celery.app.control import Control
from rest_framework.views import APIView
from rest_framework.request import Request
from pressure import models
from pressure import ser
from CmxAutoPlatform.utils.response import APIResponse
from celery_task.task import start_tasks
from celery_task.celery import app
from celery.result import AsyncResult
from CmxAutoPlatform.settings import dev


# Create your views here.
class PressuerPlans(APIView):
    # 获取所有的压测计划
    def get(self, request: Request):
        plans = models.PressurePlan.objects.all()
        plans_ser = ser.PressurePlanSer(plans, many=True)
        return APIResponse(result=plans_ser.data)

    # 新增压测计划
    def post(self, request: Request):
        data = request.data
        # 反序列化
        ser_obj = ser.PressurePlanSer(data=data)
        if ser_obj.is_valid():
            ser_obj.save()
        return self.get(request)


class PressurePlan(APIView):
    # 获取单个压测计划详情
    def get(self, request: Request, pk):
        plan = models.PressurePlan.objects.filter(id=int(pk)).first()
        plans_ser = ser.PressurePlanSer(plan)
        data = plans_ser.data
        data['pressure_type'] = eval(data['pressure_type'])
        return APIResponse(result=data)

    def put(self, request: Request, pk):
        request_data = request.data
        request_data['pressure_type'] = str(request.data.get('pressure_type'))
        ser_obj = ser.PressurePlanSer(data=request_data)
        request_instance = models.PressurePlan.objects.filter(id=pk).first()
        if ser_obj.is_valid():
            ser_obj.update(instance=request_instance, validated_data=ser_obj.data)
        else:
            raise "不合法"
        return APIResponse()

    # 删除计划
    def delete(self, request: Request, pk):
        models.PressurePlan.objects.filter(id=pk).delete()
        return PressuerPlans().get(request)


class Tasks(APIView):
    # 获取所有的任务
    def get(self, request: Request):
        tasks_obj = models.Tasks.objects.all()
        tasks_ser = ser.TasksSer(tasks_obj, many=True)
        tasks_data = tasks_ser.data
        return APIResponse(result=tasks_data)

    # 启动任务
    def post(self, request: Request):
        data = request.data
        plan_id = data.get('id')
        plan_data = models.PressurePlan.objects.filter(id=plan_id).first()
        plan_data_ser = ser.PressurePlanSer(plan_data)
        plan_data = plan_data_ser.data

        task_data = {}
        task_data['start_time'] = datetime.datetime.now()
        task_data['desc'] = plan_data['plan_desc']
        task_data['project_id'] = plan_data['project_id']
        task_data['project_name'] = plan_data['project_name']

        ser_data = ser.TasksSer(data=task_data)
        if ser_data.is_valid():
            ren = ser_data.save()
            # 需要讲这个taskID加入到tasks数据库中
            # 执行一步任务
            taskId = start_tasks.delay(id=ren.id)
            task = models.Tasks.objects.filter(id=ren.id)
            task.update(mq_id=taskId)
        else:
            raise "不合法"
        return APIResponse()


class TaskSingle(APIView):
    def delete(self, request: Request, pk):
        # 要获取mq_id
        task_obj = models.Tasks.objects.filter(id=pk).first()
        try:
            # 判断当前任务的状态
            task = AsyncResult(task_obj.mq_id)
            print(task.status)
            # 终止任务
            celery_control = Control(app=app)
            celery_control.revoke(str(task_obj.mq_id), terminate=True)
        except Exception as e:
            print(e)
            pass
        return APIResponse()


class ScriptsViews(APIView):
    # 上传文件
    def post(self, request: Request):
        print(request.data)
        request_Data = request.data
        request_Data['name'] = str(request.data.get('file'))
        filename = request_Data['name']
        filemodel = request_Data['model']
        print(filename, filemodel)
        # request_Data.pop('file')
        request_ser = ser.ScriptsSer(data=request_Data)
        if request_ser.is_valid():
            scripts_file_path = os.path.join(dev.BASE_DIR, f'apps/pressure/scripts_file/{filemodel}/{filename}')
            fp = open(scripts_file_path, 'wb+')
            for i in request_Data['file'].chunks():
                fp.write(i)
            fp.close()
            request_ser.save()
        else:
            raise "校验失败"
        return APIResponse()

    def get(self, request: Request):
        scripts = models.DBScripts.objects.all()
        scripts_ser = ser.ScriptsSer(scripts, many=True)
        return APIResponse(result=scripts_ser.data)


class ScriptsView(APIView):
    def delete(self, request: Request, pk):
        # 删除数据库中的数据
        object = models.DBScripts.objects.filter(id=pk)
        script_model = object.first().model
        script_name = object.first().name
        scripts_file_path = os.path.join(dev.BASE_DIR, f'apps/pressure/scripts_file/{script_model}/{script_name}')
        # 删除文件
        if os.path.exists(scripts_file_path):
            os.remove(scripts_file_path)
        object.delete()
        return ScriptsViews().get(request)

# def test(self):
#     # Django缓存用法
#     # from django.core.cache import cache
#     # cache.set('name','user')
#     # 直接操作
#     from django_redis import get_redis_connection
#     conn = get_redis_connection('default')
