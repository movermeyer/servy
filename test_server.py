from __future__ import absolute_import

import wsgiref.simple_server

import servy.server

class Service(object):
    @classmethod
    def process(cls, data):
        return 'result' + data


server = servy.server.Server(
    service=Service
)


def main():
    httpd = wsgiref.simple_server.make_server('', 8000, server.wsgi_app)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
