import requests
import asyncio
import aiohttp

from aiohttp import ClientSession


class HTTPSync:

    def get_url(self, url):
        """Return the pure response for a synchronous http request"""
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp

    def json_data(self, resp):
        """Return the json response"""
        return resp.json()

    def resp_code(self, resp):
        """Return the status code of response"""
        return resp.status_code


class HTTPAsync:

    async def fetch(self, url: str, session: ClientSession, **kwargs):
        response = await session.request(method="GET", url = url, **kwargs)
        response.raise_for_status()
        data = await response.json()
        return data

    async def parse(self, url: str, **kwargs):
        try:
            data = await self.fetch(url, **kwargs)
        except (aiohttp.ClientError,
                aiohttp.http_exceptions.HttpProcessingError) as e:
            return e
        except Exception as e:
            return e
        return data

    async def single(self, url: str, res_list: list, **kwargs):
        result = await self.parse(url, **kwargs) # session buried
        if not result: return None
        res_list.append(result)

    async def bulk_get(self, urls: set, res: list):
        timeout = aiohttp.ClientTimeout(total=30)
        async with ClientSession(timeout=timeout) as session:
            tasks = []
            for url in urls:
                tasks.append(self.single(url, res, session=session))
            await asyncio.gather(*tasks)
