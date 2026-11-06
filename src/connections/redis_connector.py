from redis.asyncio import Redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self) -> None:
        self.redis = await Redis(host=self.host, port=self.port)

    async def close(self) -> None:
        await self.redis.aclose()

    async def set(
        self,
        key: str,
        value: str | bytes | float,
        expire: int | None = None,
    ) -> bool:
        return await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)
