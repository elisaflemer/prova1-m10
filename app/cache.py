import redis
import logging

LOGGER = logging.getLogger(__name__)

redis_client = redis.Redis(host='redis', port=6379, db=0)
LOGGER.info("Redis connected")
