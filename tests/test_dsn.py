import pytest

import servy.utils.dsntool as dsntool

class TestDSN(object):
    def test_parse(self):
        tests = [
            (
                'scheme://:password@host:1234/bar/che?option1=opt_val1&option2=opt_val2#anchor',
                {
                    'scheme': 'scheme',
                    'schemes': ['scheme'],
                    'username': '',
                    'password': 'password',
                    'netloc': ':password@host:1234',
                    'host': 'host',
                    'hostloc': 'host:1234',
                    'path': '/bar/che',
                    'paths': ['bar', 'che'],
                    'hostname': 'host',
                    'query': {'option1': 'opt_val1', 'option2': 'opt_val2'},
                    'fragment': 'anchor'
                }
            ),
            (
                'scheme://username@host:1234/bar/che?option1=opt_val1&option2=opt_val2#anchor',
                {
                    'scheme': 'scheme',
                    'schemes': ['scheme'],
                    'username': 'username',
                    'password': None,
                    'netloc': 'username@host:1234',
                    'host': 'host',
                    'hostloc': 'host:1234',
                    'path': '/bar/che',
                    'paths': ['bar', 'che'],
                    'hostname': 'host',
                    'query': {'option1': 'opt_val1', 'option2': 'opt_val2'},
                    'fragment': 'anchor'
                }
            ),
            (
                'scheme://username:password@host:1234/bar/che?option1=opt_val1&option2=opt_val2#anchor',
                {
                    'scheme': 'scheme',
                    'schemes': ['scheme'],
                    'username': 'username',
                    'password': 'password',
                    'netloc': 'username:password@host:1234',
                    'host': 'host',
                    'hostloc': 'host:1234',
                    'path': '/bar/che',
                    'paths': ['bar', 'che'],
                    'hostname': 'host',
                    'query': {'option1': 'opt_val1', 'option2': 'opt_val2'},
                    'fragment': 'anchor'
                }
            ),
            (
                'scheme://localhost',
                {
                    'scheme': 'scheme',
                    'schemes': ['scheme'],
                    'netloc': 'localhost',
                    'host': 'localhost',
                    'hostloc': 'localhost',
                    'path': '',
                    'paths': [],
                    'hostname': 'localhost',
                    'query': {}
                }
            ),
            (
                'scheme1+scheme2://username:password@host.com:9000/?opt=opt_val1&opt=opt_val2#anchor',
                {
                    'scheme': 'scheme1+scheme2',
                    'schemes': ['scheme1', 'scheme2'],
                    'username': 'username',
                    'password': 'password',
                    'netloc': 'username:password@host.com:9000',
                    'host': 'host.com',
                    'hostloc': 'host.com:9000',
                    'path': '/',
                    'paths': [],
                    'hostname': 'host.com',
                    'query': {'opt': ['opt_val1', 'opt_val2']},
                    'fragment': 'anchor'
                }
            ),
        ]

        for dsn, test_out in tests:
            r = dsntool.parse(dsn)
            for k, v in test_out.iteritems():
                assert v == getattr(r, k)

        with pytest.raises(AssertionError):
            r = dsntool.parse('//host.com:1234')

    def test_geturl(self):
        dsn = 'scheme://username:password@host:1234/bar/che?option1=opt_val1&option2=opt_val2#anchor'
        r = dsntool.parse(dsn)
        assert dsn == r.get_url()

    def test_unpack(self):
        dsn = 'scheme://username:password@host:1234/foo'
        dsn_test = {
            'scheme': 'scheme',
            'netloc': 'username:password@host:1234',
            'path': '/foo',
            'params': "",
            'query': {},
            'fragment': ''
        }
        scheme, netloc, path, params, query, fragment = dsntool.parse(dsn)
        assert 'scheme' == scheme
        assert 'username:password@host:1234' == netloc
        assert '/foo' == path
        assert '' == params
        assert {} == query
        assert '' == fragment

    def test___getitem__(self):
        dsn = 'scheme://username:password@host:1234/foo'
        r = dsntool.parse(dsn)
        assert 'scheme' == r[0]
        assert 'username:password@host:1234' == r[1]
        assert '/foo' == r[2]
        assert '' == r[3]
        assert {} == r[4]
        assert '' == r[5]

    def test_setdefault(self):
        dsn = 'scheme://username:password@host/foo'
        r = dsntool.parse(dsn)
        assert None == r.port

        r.set_default('port', 1234)
        assert 1234 == r.port

        r = dsntool.parse(dsn, port=1235)
        assert 1235 == r.port

