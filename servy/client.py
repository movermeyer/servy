from __future__ import absolute_import

import os
import urllib2

import servy.proto as proto


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
        payload = proto.Client.encode(self.__proc, args, kw)
        try:
            request = urllib2.urlopen(url, payload)
        except urllib2.HTTPError as e:
            if e.code == 404:
                raise NameError('service \'{}\' is not defined'.format(self.__service))
            if e.code == 501:
                raise AttributeError('\'{}\' service has no procedure \'{}\''.format(
                    self.__service,
                    self.__proc,
                ))
            else:
                raise
        content = request.read()
        return proto.Client.decode(content)
