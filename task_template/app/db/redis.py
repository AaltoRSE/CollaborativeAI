import os
import redis

REDIS_HISTORY_DB = int(os.environ.get("REDIS_HISTORY_DB", "3"))

redis_host = os.environ.get("REDISHOST", "redis")
redis_port = os.environ.get("REDISPORT", "6379")
redis_password = os.environ.get("REDISPASSWORD", None)


redis_history_client = redis.StrictRedis(
    host=redis_host, port=int(redis_port), password=redis_password, db=REDIS_HISTORY_DB
)


def get_history_client():
    return redis_history_client 