from __future__ import absolute_import

import wsgiref.simple_server

import servy.server


class Parser(object):
    @classmethod
    def parse_details(cls, data):
        return data.get('details')


class Echo(object):

    parser = Parser()

    @classmethod
    def echo(cls, data):
        return 'echo: {}'.format(data)


server = servy.server.Server(
    echo=Echo
)


def main():
    httpd = wsgiref.simple_server.make_server('', 8000, server)
    httpd.serve_forever()

if __name__ == '__main__':
    main()
