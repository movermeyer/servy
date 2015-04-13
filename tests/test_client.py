from __future__ import absolute_import

import io
import urllib2

import mock
import pytest

import servy.client
import servy.exc
import servy.message


@pytest.fixture
def service():
    return servy.client.Request('localhost', 'serv')


@pytest.fixture
def client(service):
    return servy.client.Client('localhost', service)


class TestRequest(object):
    def test_url(self):
        service = servy.client.Request('localhost', 'serv')
        assert service.url == 'http://localhost/serv'

    def test_client_init(self):
        client = servy.client.Client('localhost', 'serv')
        assert client._Client__service.url == 'http://localhost/serv'

    def test_client_host_with_port(self):
        client = servy.client.Client('localhost:80', 'serv')
        assert client._Client__service.url == 'http://localhost:80/serv'

    def test_client_unicode_values(self):
        client = servy.client.Client(u'localhost:80', u'serv')
        assert client._Client__service.url == 'http://localhost:80/serv'


class TestRemoteExecution(object):
    def test_remote_execution(self, client):
        content = servy.message.Response.encode('content')
        with mock.patch('servy.client.Request.read') as read:
            read.return_value = content
            assert client.fn() == servy.message.Response.decode(content)
        message = servy.message.Request.encode((), {})
        read.assert_called_once_with(message)

    def test_failed_remote_execution(self, client):
        with pytest.raises(TypeError):
            client()

    def test_http_exception_404(self, client, service):
        with mock.patch('servy.client.Request.read') as read:
            read.side_effect = urllib2.HTTPError(service.url, 404, 'Not Found', [], io.StringIO())
            with pytest.raises(servy.exc.ServiceNotFound):
                client.fn()

    def test_http_exception_503(self, client, service):
        with mock.patch('servy.client.Request.read') as read:
            fp = io.StringIO()
            fp.write(unicode(servy.message.RemoteException.encode('traceback')))
            fp.seek(0)
            read.side_effect = urllib2.HTTPError(service.url, 503, 'Service Unavailable', [], fp)
            with pytest.raises(servy.exc.RemoteException):
                client.fn()

    def test_http_exception_503_failed(self, client, service):
        with mock.patch('servy.client.Request.read') as read:
            read.side_effect = urllib2.HTTPError(service.url, 503, 'Service Unavailable', [], io.StringIO())
            with pytest.raises(servy.exc.RemoteException):
                client.fn()

    def test_uncovered_http_exception(self, client, service):
        with mock.patch('servy.client.Request.read') as read:
            read.side_effect = urllib2.HTTPError(service.url, 600, 'Magic', [], io.StringIO())
            with pytest.raises(urllib2.HTTPError):
                client.fn()
