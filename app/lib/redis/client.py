import redis
from flask import current_app, g


class ClientOutsideFlask(Exception):
    pass


class RedisFlask:

    def connect(self, db=0) -> redis.Redis:
        try:
            current_app.logger.info('connecting to Redis')
            if 'redis' not in g:
                  g.redis: redis.Redis = redis.StrictRedis(
                      host=current_app.config['REDIS_HOST'],
                      port=6379,
                      db=0,
                      username=current_app.config['REDIS_USER'],
                      password=current_app.config['REDIS_PSWD'],
                      socket_timeout=None,
                      connection_pool=None,
                      charset='utf-8',
                      errors='strict',
                      unix_socket_path=None
                  )
        except RuntimeError:
            current_app.logger.info('attempting to call client outside of Flask')
            raise ClientOutsideFlask('run client inside Flask only')
        return g.redis

