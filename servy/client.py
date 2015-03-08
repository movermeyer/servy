from __future__ import absolute_import

import os
import urllib2

import servy.proto as proto
import servy.exc as exc

class Service(object):
    def __init__(self, service, url, proc=None):
        self.__service = service
        self.__url = url
        self.__proc = proc

    def __getattr__(self, name):
        if self.__proc:
            proc = '{}.{}'.format(self.__proc, name)
        else:
            proc = name
        return Service(self.__service, self.__url, proc)

    def __call__(self, *args, **kw):
        url = os.path.join(*(c or '' for c in (self.__url, self.__service)))
        payload = proto.Request.encode(self.__proc, args, kw)
        try:
            request = urllib2.urlopen(url, payload)
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise exc.ServiceNotFound(self.__service)
            elif e.code == 501:
                raise exc.ProcedureNotFound(self.__proc)
            else:
                raise
        else:
            content = request.read()
            return proto.Response.decode(content)
