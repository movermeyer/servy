from __future__ import absolute_import

import servy.message
import servy.protocol.http as http
import servy.utils.dsntool as dsntool


class Client(object):
    PROTOCOL = http.Request

    def __init__(self, dsn):
        self.__dsn = dsntool.DSN(dsn)

    def __getattr__(self, name):
        dsn = self.__dsn.copy()
        if dsn.path == '/':
            dsn.path = '{}{}'.format(dsn.path, name)
        else:
            dsn.path = '{}.{}'.format(dsn.path, name)
        return Client(str(dsn))

    def __call__(self, *args, **kw):
        message = servy.message.Request.encode(args, kw)
        proto = self.PROTOCOL(self.__dsn)
        content = proto.read(message)
        return servy.message.Response.decode(content)
