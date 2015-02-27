from __future__ import absolute_import

import servy.client

service = servy.client.Service('processor', 'localhost', 8000)

def main():
    return service.process('anything')

if __name__ == '__main__':
    print main()
