import requests


class PUBGRequestMixin:

    URL = 'https://api.playbattlegrounds.com/'

    def __init__(self, api_key, gzip=False):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key,
            'Accept': 'application/vnd.api+json'
        })
        if gzip:
            self.session.headers['Accept-Encoding'] = 'gzip'