from __future__ import absolute_import

import servy.client

echo = servy.client.Service('echo', 'localhost', 8000)

def main():
    return echo.parser.parse_details({'details': 'anything1'})

if __name__ == '__main__':
    print main()
