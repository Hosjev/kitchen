import asyncio
import base64
import aioredis
import redis


class ImageParserAsync:

    def __init__(self):
        self.name = 'parser'

    def imageKey(self):
        return 'cocktail#image#'

    async def base64decode(self, imgBytes):
        #current_app.logger.warning('En/Decoding image')
        return base64.b64encode(imgBytes).decode()

    async def getFromRedis(self, redis, drink):
        _imgBytes = redis.get(self.imageKey() + drink.split('.')[0])
        #current_app.logger.warning('return from Redis')
        if not _imgBytes: _imgBytes = 'default'
        return await self.base64decode(_imgBytes)

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


class ImageParserPipeline(ImageParserAsync):

    def _repl(self, drinks, encImages):
        for i, d in enumerate(drinks):
            drinks[i][4] = encImages[i]
        return drinks

    async def repl_decode(self, bytesImages):
        results = []
        tasks = []
        for image in bytesImages:
            tasks.append(self.base64decode(image, results))
        asyncio.gather(*tasks)
        return results

    def build_pipeline(self, redis, keys):
        bytesImages = []
        with redis.pipeline() as pipe:
            pipe.multi()
            for key in keys:
                pipe.get(self.imageKey() + key)
            bytesImages = pipe.execute()
        return bytesImages

    def run(self, redis, drinks):
        bytesImages = self.build_pipeline(redis, list(map(lambda x: x[4].split('.')[0], drinks)))
        bytesImages = asyncio.run(self.repl_decode())
        return self.replace([list(x) for x in drinks], bytesImages)
