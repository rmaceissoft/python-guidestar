#!/usr/bin/env python
import json
import urllib

import requests

from guidestar.entities import Organization


class Api(object):

    def __init__(self, username=None, password=None, sandbox=False):
        if sandbox:
            self._base_url = 'https://Sandboxdata.guidestar.org/v1/'
        else:
            self._base_url = 'https://data.guidestar.org/v1/'
        self._username = username
        self._password = password

    @property
    def _auth(self):
        return self._username, self._password

    def search(self, ein=None, zip=None, keyword=None):
        value = None
        if ein:
            value = 'ein:%s' % ein
        elif zip:
            value = 'zip:%s' % zip
        elif keyword:
            value = 'keyword:%s' % keyword
        if value:
            mapping = {'q': value}
        url = self._base_url + 'search?%s' % urllib.urlencode(mapping)
        response = requests.get(url, auth=self._auth)
        response_json = json.loads(response.content)
        return Organization.parse_list(response_json)

    def get_details(self, org_id):
        url = self._base_url + 'detail/%s' % org_id
        response = requests.get(url, auth=self._auth)
        response_json = json.loads(response.content)
        return Organization.parse(response_json)

