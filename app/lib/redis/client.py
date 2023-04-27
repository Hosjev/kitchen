import redis
from flask import current_app, g


class ClientOutsideFlask(Exception):
    pass


class RedisFlask:

    def connect(self, db=0) -> redis.Redis:
        try:
            current_app.logger.info('connecting to Redis')
            if 'redis' not in g:
                g.redis: redis.Redis = redis.StrictRedis.from_url(current_app.config['REDIS_URL'])
        except RuntimeError:
            current_app.logger.info('attempting to call client outside of Flask')
            raise ClientOutsideFlask('run client inside Flask only')
        except Exception as err:
            current_app.logger.error(f'Redis connect failure: {err}')
        return g.redis

