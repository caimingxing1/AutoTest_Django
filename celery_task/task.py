import os
import subprocess
import threading
import time
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CmxAutoPlatform.settings.dev")
django.setup()
from pressure import models
from celery_task.celery import app
from random import randint
from faker import Faker

fake = Faker(locale='zh_CN')
from CmxAutoPlatform.apps.pressure.scripts_file.python import p


@app.task
def add(x, y):
    return x, y


@app.task
def start_tasks(id):
    task = models.Tasks.objects.filter(id=id)
    task.update(status='压测中')
    # ========
    time.sleep(30)
    task.update(status='压测完成')
    return 123


def str_time_s():
    return str(time.time())[:10]


def str_time_ms():
    return str(time.time())[:14]


def str_time_μs():
    return str(time.time())


# def data_file(row, index):  # 每个线程内有几个变量就执行几次
#     content = df_content_list[row].replace('\n', '').split(' ')[index]
#     try:
#         content = eval(content)
#     except:
#         pass
#     return content


def play():
    def run_other(filepath, mq):
        print('other')
        subprocess.call('python3 ' + filepath + ' mqid=' + str(mq.id), shell=True)

    def run_python(filepath):
        print('python')
        from pressure.scripts_file.python.p import t

    def run_script(filepath):
        # subprocess.call('python3 ' + filepath, shell=True)
        print("我是执行脚本")

    # 每轮执行的并发数函数
    def one_round(filepath, num: int):
        concurrence_thread = []
        for concurrence in range(num):
            th = threading.Thread(target=run_script, args=(filepath,))
            th.setDaemon(True)
            concurrence_thread.append(th)
        for th in concurrence_thread:
            th.start()
        for th in concurrence_thread:
            th.join()
        print("==========结束了一轮压测==========")

    ## 三种测试计划
    # 0-10-2  执行第0个脚本，10个并发数量，执行两轮
    # "0-10-5,1-5-5"  两个阶段
    project_plan = "0-10-5,1-5-5"
    project_plan = "0-1/5-5"
    steps = project_plan.split(',')
    for step in steps:
        porject_script = int(step.split('-')[0])  # 并发的脚本
        plan_cunrrence_num = int(step.split('-')[1])  # 并发数量
        scripts_path = ''  # 脚本地址
        # 定义plan_round 的最大值,根据不同的参数获取不同的轮数
        if '+' in step:  # 无限增压
            plan_round = 100  # 安全阀
        elif '_' in step:  # 瞬时增压
            plan_round = step.split('-'[2]) * (step.count('_') + 1)
        else:
            plan_round = int(step.split('-')[2])  # 轮数

        # 首先是要并发轮数
        round_thred = []
        for round in range(plan_round):
            if '/' in step:
                # 阶梯增压
                mid = step.split('-')[1]  # 10/90
                # start_num = int(mid.split('/')[0])
                plan_cunrrence_num = (int(mid.split('/')[1]) - int(mid.split('/')[0])) * round
            elif '+' in step:
                mid = step.split('-')[1]
                plan_cunrrence_num = int(int(mid.split('-')[0]) + int(mid.split('+')[1]) * round)
            elif "_" in step:  # 瞬时增压
                mid = step.split('-')[1]
                mid = mid.split('_')
            else:
                # 常亮压测
                plan_cunrrence_num = int(step.split('-')[1])  # 并发数量
            t = threading.Thread(target=one_round, args=(scripts_path, plan_cunrrence_num))
            t.setDaemon(True)  # 设置为守护线程
            round_thred.append(t)

        for t in round_thred:
            t.start()
            time.sleep(1)

        for t in round_thred:
            t.join()
