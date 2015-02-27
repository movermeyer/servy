from __future__ import absolute_import

import pickle


class Server(object):
    def __init__(self, **services):
        self.services = services

    def wsgi_app(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]

        start_response(status, headers)

        return pickle.dumps('resp')
