import httpx
import json
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self):
        self.base_url = settings.UPSTASH_REDIS_URL
        self.token = settings.UPSTASH_REDIS_TOKEN
        self.enabled = bool(self.base_url and self.token)

    async def get(self, key: str):
        if not self.enabled:
            return None
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{self.base_url}/get/{key}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    timeout=2.0,
                )
                data = r.json()
                return data.get("result")
        except Exception as e:
            logger.warning(f"Cache GET failed: {e}")
            return None

    async def set(self, key: str, value: str, ttl: int = 3600):
        if not self.enabled:
            return
        try:
            async with httpx.AsyncClient() as client:
                await client.get(
                    f"{self.base_url}/setex/{key}/{ttl}/{value}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    timeout=2.0,
                )
        except Exception as e:
            logger.warning(f"Cache SET failed: {e}")
