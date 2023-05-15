from django.db import models


# Create your models here.
# 性能测试计划
class PressurePlan(models.Model):
    # 计划名
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="计划名称")
    # 测试脚本
    # script = models.CharField(max_length=30, null=True, blank=True, verbose_name="压测脚本")
    # projectname
    project_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="项目名称")
    # 项目ID
    project_id = models.IntegerField(null=True, blank=True, verbose_name="项目ID")
    # 压测类型/压测计划
    pressure_type = models.CharField(max_length=1000, null=True, blank=True, default="[]", verbose_name="压测类型")
    # 计划描述
    plan_desc = models.CharField(max_length=100, null=True, blank=True, verbose_name="计划描述")

    def __str__(self):
        return self.name


class Tasks(models.Model):
    start_time = models.DateTimeField(null=True, verbose_name="创建的时间")
    status = models.CharField(max_length=10, null=True, blank=True, default='队列中')  # 队列中，压测中，已结束
    desc = models.CharField(max_length=300, null=True, blank=True, default='')
    project_id = models.IntegerField(default=0)
    project_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="项目名称")
    # 需要根据此任务ID获取任务的结果
    mq_id = models.CharField(max_length=64, null=True, blank=True, verbose_name="任务的ID")
    "celery -A celery_task worker -l info"


class DBScripts(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name="脚本名称")
    start_time = models.DateTimeField(null=True, verbose_name="创建的时间")
    desc = models.CharField(max_length=300, null=True, blank=True, default='')
    auther = models.CharField(max_length=30, null=True, blank=True, verbose_name="开发者")
    model = models.CharField(max_length=12, null=True, blank=True, verbose_name="脚本类型")
# class DB_Projects(models.Model):
#     name = models.CharField(max_length=30, null=True, blank=True, default='new project')
#     plan = models.CharField(max_length=1000, null=True, blank=True, default='[]')  # 压测计划，专用的关键字语法。（可保存成模版）
#     variable = models.CharField(max_length=1000, null=True, blank=True,
#                                 default='[]')  # 变量设置 [{"key":"a","value":1},{},{}]]
#
#     def __str__(self):
#         return self.name


# class DB_tasks(models.Model):
#     stime = models.CharField(max_length=30, null=True, blank=True, default='')
#     des = models.CharField(max_length=300, null=True, blank=True, default='')
#     project_id = models.IntegerField(default=0)
#     status = models.CharField(max_length=10, null=True, blank=True, default='队列中')  # 队列中 ， 压测中，已结束。
#     mq_id = models.IntegerField(default=0)
#     stop = models.BooleanField(default=False)  # 终止状态
#
#     all_times = models.CharField(max_length=5000, null=True, blank=True, default=[])
#     all_threads = models.CharField(max_length=5000, null=True, blank=True, default=[])
#     all_f = models.CharField(max_length=5000, null=True, blank=True, default=[])
#
#     jindu = models.IntegerField(default=0)  # 进度
#
#     def __str__(self):
#         return self.des
#
