from __future__ import absolute_import

import sys
import traceback

import webob.exc
import webob.dec
import webob.response

import servy.inspector as inspector
import servy.message as message


class Server(object):
    def __init__(self, _container=None, **procedures):
        if _container:
            self.procedures = inspector.Inspector.find(_container)
        else:
            self.procedures = {}
            for name, proc in procedures.items():
                if not inspector.Inspector.is_procedure(proc):
                    continue
                self.procedures[name] = proc

    def __call__(self, request):
        procedure = request.path[1:]
        if procedure not in self.procedures:
            raise webob.exc.HTTPNotFound

        procedure = self.procedures[procedure]

        try:
            args, kw = message.Request.decode(request.body)
        except:
            raise webob.exc.HTTPBadRequest

        try:
            content = procedure(*args, **kw)
        except:
            tb = ''.join(traceback.format_exception(*sys.exc_info()))
            body = message.RemoteException.encode(tb)
            raise webob.exc.HTTPServiceUnavailable(body=body)

        return message.Response.encode(content)
