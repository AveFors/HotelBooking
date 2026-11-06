from connections.redis_connector import RedisManager
from config import settings

redis = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
