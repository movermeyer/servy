from __future__ import absolute_import

import servy.client


scraper = servy.client.Client('localhost:8000')

def main():
    print scraper.echo.echo('11')
    # echo.shit()
    return scraper.echo.parser.parse_details({'details': 'anything1'})

if __name__ == '__main__':
    print main()
