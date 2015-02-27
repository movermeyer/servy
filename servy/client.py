from __future__ import absolute_import

import pickle
import urllib2


class Proxy(object):
    def __init__(self, server, name):
        self.server = server
        self.name = name

    def __call__(self, *args, **kw):
        payload = pickle.dumps((self.name, args, kw))
        request = urllib2.urlopen(self.server, payload)
        content = request.read()
        return pickle.loads(content)


class Client(object):
    def __init__(self, host, port):
        self._server = 'http://{host}:{port}'.format(
            host=host,
            port=port,
        )

    def __getattr__(self, name):
        return Proxy(self._server, name)

