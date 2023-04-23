import redis
from flask import current_app, g


class ClientOutsideFlask(Exception):
    pass


class RedisFlask:

    def connect(self, db=0) -> redis.Redis:
        try:
            current_app.logger.info('connecting to Redis')
            if 'redis' not in g:
                g.redis: redis.Redis = redis.Redis.from_url(
                  current_app.config['REDIS_URL'] + '/' + str(db)
                  )
        except RuntimeError:
            current_app.logger.info('attempting to call client outside of Flask')
            raise ClientOutsideFlask('run client inside Flask only')
        return g.redis


class RedisParser:

    def imageKey(self):
        return 'cocktail#image#'
