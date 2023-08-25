import os
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


redis_url = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"
redis = aioredis.from_url(redis_url, encoding="utf-8")

