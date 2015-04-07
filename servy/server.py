from __future__ import absolute_import

import sys
import traceback

import webob.exc
import webob.dec
import webob.response

import servy.proto as proto


class Server(object):
    def __init__(self, server=None, **services):
        self.services = services

        if server:
            self.services.update(server.__dict__)

    @webob.dec.wsgify
    def __call__(self, request):
        if request.method == 'POST':
            return self.rpc(request)
        raise webob.exc.HTTPMethodNotAllowed

    def rpc(self, request):
        service = request.path[1:]
        if service not in self.services:
            raise webob.exc.HTTPNotFound

        service = self.services[service]

        try:
            procedure, args, kw = proto.Request.decode(request.body)
        except:
            raise webob.exc.HTTPBadRequest

        for attr in procedure.split('.'):
            if not hasattr(service, attr):
                raise webob.exc.HTTPNotImplemented
            service = getattr(service, attr)

        if not callable(service):
            raise webob.exc.HTTPUnprocessableEntity

        try:
            content = service(*args, **kw)
        except Exception:
            tb = ''.join(traceback.format_exception(*sys.exc_info()))
            message = proto.RemoteException.encode(tb)
            raise webob.exc.HTTPServiceUnavailable(body=message)

        content = proto.Response.encode(content)
        return webob.response.Response(content)
