from __future__ import absolute_import

import servy.client

echo = servy.client.Client({'name': 'echo', 'host': 'localhost:8000'})


def main():
    print echo.echo('11')
    # echo.shit()
    return echo.parser.parse_details({'details': 'anything1'})

if __name__ == '__main__':
    print main()
