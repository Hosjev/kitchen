""" Synchronous API call """
import requests
import json


class WebResource:

    def get_url(self, url):
        resp = requests.get(url)
        resp.raise_for_status()
        return resp

    def json_data(self, resp):
        return resp.json()

    def resp_code(self, resp):
        return resp.status_code
