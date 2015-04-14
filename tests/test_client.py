from __future__ import absolute_import

import io
import urllib2

import pytest
import mock

import servy.client
import servy.exc
import servy.message


@pytest.fixture
def client():
    return servy.client.Client('http://localhost/serv')


def test_client_getattr(client):
    assert str(client.fn._Client__dsn) == 'http://localhost/serv.fn'


def test_client_with_no_path():
    client = servy.client.Client('http://localhost/')
    assert str(client.fn._Client__dsn) == 'http://localhost/fn'


class TestRemoteExecution(object):
    def test_remote_execution(self, client):
        content = servy.message.Response.encode('content')
        with mock.patch('servy.client.Client.PROTOCOL.read') as read:
            read.return_value = content
            assert client.fn() == servy.message.Response.decode(content)
        message = servy.message.Request.encode((), {})
        read.assert_called_once_with(message)

    def test_http_exception_404(self, client):
        with mock.patch('servy.protocol.http.urllib2.urlopen') as read:
            read.side_effect = urllib2.HTTPError(str(client.dsn), 404, 'Not Found', [], io.StringIO())
            with pytest.raises(servy.exc.ServiceNotFound):
                client.fn()

    def test_http_exception_503(self, client):
        with mock.patch('servy.protocol.http.urllib2.urlopen') as read:
            fp = io.StringIO()
            fp.write(unicode(servy.message.RemoteException.encode('traceback')))
            fp.seek(0)
            read.side_effect = urllib2.HTTPError(str(client.dsn), 503, 'Service Unavailable', [], fp)
            with pytest.raises(servy.exc.RemoteException):
                client.fn()

    def test_http_exception_503_failed(self, client):
        with mock.patch('servy.protocol.http.urllib2.urlopen') as read:
            read.side_effect = urllib2.HTTPError(str(client.dsn), 503, 'Service Unavailable', [], io.StringIO())
            with pytest.raises(servy.exc.RemoteException):
                client.fn()

    def test_uncovered_http_exception(self, client):
        with mock.patch('servy.protocol.http.urllib2.urlopen') as read:
            read.side_effect = urllib2.HTTPError(str(client.dsn), 600, 'Magic', [], io.StringIO())
            with pytest.raises(urllib2.HTTPError):
                client.fn()
