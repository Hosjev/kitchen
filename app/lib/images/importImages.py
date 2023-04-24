import os
import sys
import redis
from typing import List

def connect():
    return redis.StrictRedis(
        host='localhost',
        port=6379,
        db=0,
        password='',
        socket_timeout=None,
        connection_pool=None,
        charset='utf-8',
        errors='strict',
        unix_socket_path=None
    )

def generate_key(fileID: str) -> str:
    return f'cocktail#image#{fileID}'


def read_file(file: str) -> bin:
    return open(file, 'rb').read()


def runImagePipeline(directory: str) -> None:
    """Using a local source, read all images from
      directory arg, start a Redis pipeline, and
      dump images into Redis DB.

    Args:
        directory (str): directory hosting images
    """
    #directory = '/Users/wendiwhitsett/Scratch/kitchImages/'
    files: List = os.listdir(directory)

    r = connect()
    with r.pipeline() as pipe:
        pipe.multi()
        # muck thru array
        for file in files:
            pipe.set(generate_key(file.split('.')[0]), read_file(directory + file))
        pipe.execute()

if __name__ == "__main__":
    runImagePipeline(sys.argv[1])
