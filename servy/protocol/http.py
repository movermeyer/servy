from __future__ import absolute_import


import urllib2
import urlparse


class Request(object):
    def __init__(self, dsn):
        self.dsn = dsn

    @property
    def url(self):
        url = {
            'scheme': 'http',
            'netloc': self.dsn.hostloc,
            'path': self.dsn.path,
            'params': '',
            'query': '',
            'fragment': '',
        }
        return urlparse.urlunparse(urlparse.ParseResult(**{k: v or '' for k, v in url.iteritems()}))

    def read(self, message):
        return urllib2.urlopen(self.url, message).read()
