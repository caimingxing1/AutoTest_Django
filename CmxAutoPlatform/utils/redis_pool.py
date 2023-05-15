# redis 连接池
import redis

# 造了一个池子，能放100个链接
# pool必须是单例
POOL = redis.ConnectionPool(host='192.168.0.105', port=6379, max_connections=100)


