from __future__ import absolute_import


import urllib2
import urlparse

import servy.exc


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
        try:
            content = urllib2.urlopen(self.url, message).read()
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise servy.exc.ServiceNotFound(self.dsn.path)
            elif e.code == 503:
                message = e.read()
                try:
                    tb = servy.message.RemoteException.decode(message)
                except (ValueError, TypeError):
                    tb = ''
                raise servy.exc.RemoteException(tb)
            else:
                raise
        else:
            return content
