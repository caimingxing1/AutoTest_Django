from celery import Celery

# 带密码的写法
# 'redis://:1234567@192.168.0.105:6379/1'
broker = 'redis://192.168.0.105:6379/1'  # broker  任务队列
backend = 'redis://192.168.0.105:6379/2'  # 结构存储，执行完的结果存着

app = Celery(__name__, broker=broker, backend=backend)
# 需要用命令来执行
