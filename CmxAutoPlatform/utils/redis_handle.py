from redis import Redis
from CmxAutoPlatform.utils.redis_pool import POOL

r = Redis(connection_pool=POOL)
name = r.get('name')
print(name)
