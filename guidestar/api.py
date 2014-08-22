#!/usr/bin/env python
import json
import urllib

import requests
from requests.exceptions import RequestException, HTTPError

from guidestar.entities import Organization
from guidestar.exceptions import EXCEPTIONS_MAPPING, GuidestarError


class FilterBy(object):
    """ different filters used on search api endpoint

    """
    KEYWORD = 'keyword'
    EIN = 'ein'
    ZIP = 'zip'
    ORGANIZATION_NAME = 'organization_name'

    CHOICES = (KEYWORD, EIN, ZIP, ORGANIZATION_NAME, )


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

    def search(self, q, filter_by=FilterBy.KEYWORD, page=1, limit=10, url_path=None):
        if filter_by not in FilterBy.CHOICES:
            raise RuntimeError("not valid filter_by value")
        value = '%s:%s' % (filter_by, q)
        mapping = {
            'q': value,
            'p': page,
            'r': limit
        }
        url_path = url_path or 'search?%s'
        url = self._base_url + url_path % urllib.urlencode(mapping)
        response_json = self._do_request(url)
        return Organization.parse_list(response_json, limit, page)

    def advanced_search(self, q, filter_by=FilterBy.KEYWORD, page=1, limit=10):
        return self.search(q, filter_by=filter_by, page=page, limit=limit, url_path='advancedsearch?%s')

    def get_details(self, org_id):
        url = self._base_url + 'detail/%s' % org_id
        response_json = self._do_request(url)
        return Organization.parse(response_json)

    def _do_request(self, url):
        headers = {
            'X-Referring-Integrator': self._username
        }
        try:
            response = requests.get(url, headers=headers, auth=self._auth)
        except RequestException, ex:
            raise GuidestarError()
        else:
            try:
                response.raise_for_status()
            except HTTPError, ex:
                exception_class = EXCEPTIONS_MAPPING.get(ex.response.status_code, GuidestarError)
                raise exception_class(response=ex.response)
            else:
                response_json = json.loads(response.content)
        return response_json

