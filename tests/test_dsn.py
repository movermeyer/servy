import pytest

import servy.utils.dsntool as dsntool

@pytest.fixture
def dsn_example():
    return [
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


@pytest.fixture
def sample_dsn():
    return 'scheme://username:password@host/foo'


class TestDSN(object):
    def test_DSN(self, dsn_example):
        for dsn, expected in dsn_example:
            r = dsntool.DSN(dsn)
            for k, v in expected.iteritems():
                assert v == getattr(r, k)

        with pytest.raises(AssertionError):
            r = dsntool.DSN('//host.com:1234')

    def test_geturl(self):
        dsn = 'scheme://username:password@host:1234/bar/che?option1=opt_val1&option2=opt_val2#anchor'
        r = dsntool.DSN(dsn)
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
        scheme, netloc, path, params, query, fragment = dsntool.DSN(dsn)
        assert scheme == 'scheme'
        assert netloc == 'username:password@host:1234'
        assert path == '/foo'
        assert params == ''
        assert query == {}
        assert fragment == ''

    def test_set_default_missed(self, sample_dsn):
        assert dsntool.DSN(sample_dsn).port == None

    def test_set_default_init(self, sample_dsn):
        assert dsntool.DSN(sample_dsn, port=1235).port == 1235

    def test_set_default_call(self, sample_dsn):
        r = dsntool.DSN(sample_dsn)
        r.set_default('port', 1234)
        assert r.port == 1234

    def test_field_update(self, sample_dsn):
        r = dsntool.DSN(sample_dsn)
        r.username = 'user'
        assert r.get_url() == 'scheme://user:password@host/foo'
