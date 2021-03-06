from __future__ import absolute_import

import servy.message
import servy.protocol.http as http
import servy.utils.dsntool as dsntool


class Client(object):
    PROTOCOL = http

    def __init__(self, dsn):
        self.__dsn = dsntool.DSN(dsn)

    def __getattr__(self, name):
        dsn = self.__dsn.copy()
        print dsn
        if dsn.path in ('', '/'):
            dsn.path = '/{}'.format(name)
        else:
            dsn.path = '{}.{}'.format(dsn.path, name)
        return Client(str(dsn))

    def __call__(self, *args, **kw):
        message = servy.message.Request.encode(args, kw)
        req = self.PROTOCOL.Request()
        req.connect(self.__dsn)
        content = req.send(message)
        return servy.message.Response.decode(content)
