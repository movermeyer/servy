from __future__ import absolute_import

import pickle
import urllib2


class Proxy(object):
    def __init__(self, service, name):
        self._service = service
        self._name = name

    def __getattr__(self, name):
        name = '{}.{}'.format(self._name, name)
        return Proxy(self._service, name)

    def __call__(self, *args, **kw):
        payload = pickle.dumps((self._name, args, kw))
        request = urllib2.urlopen(self._service, payload)
        content = request.read()
        return pickle.loads(content)


class Service(object):
    def __init__(self, service, host, port):
        self._server = 'http://{host}:{port}/{service}'.format(
            host=host,
            port=port,
            service=service,
        )

    def __getattr__(self, name):
        return Proxy(self._server, name)

