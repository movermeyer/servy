from __future__ import absolute_import

import servy.client

echo = servy.client.Service('echo', 'localhost', 8000)

def main():
    return echo.echo('anything')

if __name__ == '__main__':
    print main()
