import subprocess, threading, json, time, os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % 'Pressure')  # 引号中请输入您的setting父级目录名
django.setup()

from MyApp.models import *
import re
from random import randint

from faker import Faker

fake = Faker(locale='zh_CN')


def str_time_s():
    return str(time.time())[:10]


def str_time_ms():
    return str(time.time())[:14]


def str_time_μs():
    return str(time.time())


def data_file(row, index):  # 每个线程内有几个变量就执行几次
    content = df_content_list[row].replace('\n', '').split(' ')[index]
    try:
        content = eval(content)
    except:
        pass
    return content


def read_sp(sp, script_model):  # 每个线程执行一次
    old = {}
    if use_file:
        row = randint(0, len(df_content_list) - 1)

    for i in variable:
        old[i['key']] = eval(i['value'])

    if script_model == 'other':
        p_list = []
        params = [i for i in sp.split(' ') if i]
        for i in params:
            p_list.append('"' + repr(old[i]) + '"')
        end = ' '.join(p_list)

    elif script_model == 'python':
        p_list = []
        params = re.findall(r'\((.*?)\)', sp)[0].split(',')
        if params != ['']:
            for i in params:
                try:
                    eval(i)
                    p_list.append(repr(eval(i)))
                except:
                    p_list.append(repr(old[i]))

        end = sp.split('(')[0] + '(' + ','.join(p_list) + ')'

    return end


def play(mq):
    def doit_other(filepath, sp, tmp):
        sp = read_sp(sp, script_model)
        t1 = time.time()
        _bin = dz[script_name.split('.')[-1]]
        s = subprocess.call(_bin + ' ' + filepath + ' ' + sp + ' mqid=' + str(mq.id), shell=True)
        if s != 0:
            exec('round_f_%s["f"]+=1' % tmp)
        t2 = time.time()
        cha = int(t2 - t1)
        try:
            exec("round_times_%s[cha]+=1" % tmp)
        except:
            exec("round_times_%s[cha]=1" % tmp)

    def doit_python(filepath, sp, tmp):
        sp = read_sp(sp, script_model)
        t1 = time.time()
        try:
            exec('from scripts.python.%s import %s\n%s' % (script_name.split('.')[0], sp.split('(')[0], sp))
        except:
            exec('round_f_%s["f"]+=1' % tmp)

        t2 = time.time()
        cha = int(t2 - t1)
        try:
            exec("round_times_%s[cha]+=1" % tmp)
        except:
            exec("round_times_%s[cha]=1" % tmp)

    def doit_go(filepath, sp):
        print('go')

    def one_round(filepath, num, script_model, sp, pj):
        tmp = str(time.time()).replace('.', '')
        exec('global round_times_%s\nround_times_%s = {}' % (tmp, tmp))
        step_times.append(eval('round_times_%s' % tmp))
        exec('global round_f_%s\nround_f_%s = {"f":0}' % (tmp, tmp))
        step_f.append(eval('round_f_%s' % tmp))
        ts = []
        target = {"other": doit_other, "python": doit_python, "go": doit_go}[script_model]

        if pj:  # 是否要平均发出
            rest = 1 / (num - 1)  # *  *  *  *  *
        else:
            rest = 0

        for n in range(int(num)):
            t = threading.Thread(target=target, args=(filepath, sp, tmp))
            t.setDaemon(True)
            ts.append(t)
        for t in ts:
            t.start()
            time.sleep(rest)
        for t in ts:
            t.join()
        print('---结束了一轮压测---')

    dz = {"py": "python3", "java": "java", "php": "php"}  # 后缀对应自动命令字典，同学在自己公司自行添加
    message = json.loads(mq.message)
    task_id = message['task_id']
    task = DB_tasks.objects.filter(id=int(task_id))
    task.update(status='压测中')
    # ------
    project = DB_Projects.objects.filter(id=int(task[0].project_id))[0]
    plan = eval(project.plan)
    all_times = []
    all_threads = []
    all_f = []

    # 是否需要使用数据文件。
    global variable
    variable = eval(project.variable)  # [{"a":1},{"b":2},{}]
    global use_file
    use_file = False
    for v in variable:
        if v['value'][:9] == 'data_file':
            use_file = True
    if use_file:
        # 拿出文件数据
        file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data_files',
                                 'data_file_' + str(project.id))
        if os.path.exists(file_name):
            with open(file_name) as fp:
                global df_content_list
                df_content_list = fp.readlines()
                if len(df_content_list) == 0:
                    task.update(status='异常[文件内容为空]', all_times=all_times, all_threads=all_threads, all_f=all_f)
                    raise Exception('任务终止！文件内容为空！')
        else:
            task.update(status='异常[文件不存在]', all_times=all_times, all_threads=all_threads, all_f=all_f)
            raise Exception('任务终止！文件不存在！')

    all_steps = len(plan)
    over_steps = 0

    for step in plan:  # step = 阶段
        step_times = []
        step_threads = []
        step_f = []
        script_model = step["name"].split('/')[0]
        script_name = step["name"].split('/')[1]
        sp = step['sp']
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts', script_model,
                                script_name)
        trs = []

        pj = False
        if 's' in step['old_round']:
            pj = True

        step['old_round'] = step['old_round'].split('s')[0]

        if '+' in step['old_num']:  # 无限增压
            round = 100  # 安全阀
        elif '_' in step['old_num']:  # 瞬时增压
            round = int(step["old_round"]) * (step["old_num"].count('_') + 1)
        else:
            round = int(step["old_round"])  ################################################
        for r in range(round):  # round =5 ,r= 0,1,2,3,4

            if '/' in step["old_num"]:  # 阶梯增压
                mid = step["old_num"]  # 10/90
                num = int(mid.split('/')[0]) + (int(mid.split('/')[1]) - int(mid.split('/')[0])) / (round - 1) * r

            elif '+' in step["old_num"]:  # 无限增压
                mid = step["old_num"]  # 10+5
                num = int(int(mid.split('+')[0]) + int(step["old_round"]) * r)

            elif '_' in step["old_num"]:  # 瞬时增压
                mid = step["old_num"].split('_')
                num = int(mid[int(r / int(step["old_round"]))])
            else:
                num = int(step["old_num"])  #################################

            step_threads.append(num)
            tr = threading.Thread(target=one_round, args=(filepath, num, script_model, sp, pj))
            tr.setDaemon(True)
            trs.append(tr)
        for tr in trs:  # tr是轮
            # 路障
            now_task = DB_tasks.objects.filter(id=task_id)[0]
            if now_task.stop == True:
                break
            tr.start()
            time.sleep(1)
        for tr in trs:
            tr.join()
        print('-----------结束了一个阶段------------')
        all_times.append(step_times)
        all_threads.append(step_threads)
        all_f.append(step_f)
        over_steps += 1
        task.update(jindu=float(over_steps / all_steps) * 100)

    print('【整个压测任务结束】')

    # -------
    task.update(status='已结束', all_times=all_times, all_threads=all_threads, all_f=all_f)


if __name__ == "__main__":
    mq_id = sys.argv[1].split('=')[1]
    mq = DB_django_task_mq.objects.filter(id=int(mq_id))[0]
    play(mq)
