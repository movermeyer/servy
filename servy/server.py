from __future__ import absolute_import

import pickle
import pprint


class Server(object):
    def __init__(self, **services):
        self.services = services

    def serve(self, environ):
        content_length = int(environ['CONTENT_LENGTH'])
        content = environ['wsgi.input'].read(content_length)
        endpoint, args, kw = pickle.loads(content)
        name = environ['PATH_INFO'][1:]
        service = self.services[name]
        endpoint = self.get_endpoint(service, endpoint)
        result = endpoint(*args, **kw)
        return pickle.dumps(result)

    def get_endpoint(self, service, endpoint):
        for attr in endpoint.split('.'):
            service = getattr(service, attr)
        return service

    def wsgi_app(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]

        request_method = environ['REQUEST_METHOD']
        if request_method == 'POST':
            content = self.serve(environ)

        start_response(status, headers)
        return content
