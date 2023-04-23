import asyncio
import base64
import aioredis
import redis


class ImageParser:

    def __init__(self):
        self.name = 'parser'

    def imageKey(self):
        return 'cocktail#image#'

    async def base64encode(self, imgBytes):
        return base64.b64encode(imgBytes).decode()

    async def getFromRedis(self, redis, drink):
        _imgBytes = redis.get(self.imageKey() + drink.split('.')[0])
        if not _imgBytes: _imgBytes = 'default'
        return await self.base64encode(_imgBytes)

    async def process_drink(self, redis, index, drink, _processed):
        _processed[index] += list(drink[:4])
        _processed[index].append(await self.getFromRedis(redis, drink[4]))
        _processed[index] += list(drink[5:])

    async def getAllImages(self, redis: redis.Redis, drinks: list) -> list:
        tasks = []
        _processed_drinks = [list() for _ in range(len(drinks))]
        for index, drink in enumerate(drinks):
            tasks.append(self.process_drink(redis, index, drink, _processed_drinks))
        await asyncio.gather(*tasks)
        return _processed_drinks
