from fastapi import HTTPException
import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def check_rate_limit(key: str, limit: int, window: int):
    current = redis_client.get(key)
    if current is None:
        redis_client.setex(key, window, 1)
    else:
        current = int(current)
        if current >= limit:
            raise HTTPException(
                status_code=429,
                detail="Çok fazla deneme yaptınız. Lütfen biraz bekleyin."
            )
        redis_client.incr(key)