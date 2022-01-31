import requests


class WebResource:

    def get_url(self, url):
        """Return the pure response for a synchronous http request"""
        resp = requests.get(url)
        resp.raise_for_status()
        return resp

    def json_data(self, resp):
        """Return the json response"""
        return resp.json()

    def resp_code(self, resp):
        """Return the status code of response"""
        return resp.status_code
