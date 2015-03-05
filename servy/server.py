from __future__ import absolute_import

import webob.exc
import webob.dec
import webob.response

import pickle


class Server(object):
    def __init__(self, **services):
        self.services = services

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
            procedure, args, kw = pickle.load(request.body_file)
        except:
            raise webob.exc.HTTPBadRequest

        for attr in procedure.split('.'):
            if not hasattr(service, attr):
                raise webob.exc.HTTPNotImplemented
            service = getattr(service, attr)

        content = service(*args, **kw)
        content = pickle.dumps(content)
        return webob.response.Response(content)
