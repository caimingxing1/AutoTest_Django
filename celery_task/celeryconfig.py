# 带密码的写法
# 'redis://:1234567@192.168.0.105:6379/1'
broker_url = 'redis://192.168.0.105:6379/1'  # broker  任务队列
result_backend = 'redis://192.168.0.105:6379/2'  # 结构存储，执行完的结果存着
include = ['celery_task.task']
worker_prefetch_multiplier = 2
worker_concurrency = 2