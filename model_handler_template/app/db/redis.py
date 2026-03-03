import os
import redis

REDIS_SESSION_DB = 1
REDIS_MODEL_DB = 2

redis_host = os.environ.get("REDISHOST", "redis")
redis_port = os.environ.get("REDISPORT", "6379")
redis_password = os.environ.get("REDISPASSWORD", None)

redis_session_client = redis.StrictRedis(
    host=redis_host, port=int(redis_port), password=redis_password, db=REDIS_SESSION_DB
)

redis_model_client = redis.StrictRedis(
    host=redis_host, port=int(redis_port), password=redis_password, db=REDIS_MODEL_DB
)
