""" Synchronous API call """
import requests
import json


class WebResource:
    def __init__(self, url):
        self.url = url

    def get_url(self):
        self.resp = requests.get(self.url)

    def json_data(self):
        return self.resp.json()

    def resp_code(self):
        return self.resp.status_code
