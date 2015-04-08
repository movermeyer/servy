from __future__ import absolute_import

import io
import unittest
import urllib2

import mock

import servy.client
import servy.exc
import servy.proto


class Service(unittest.TestCase):
    def test_url(self):
        service = servy.client.Service('localhost', 'serv')
        self.assertEqual(service.url, 'http://localhost/serv')

    def test_client_init(self):
        client = servy.client.Client('localhost', 'serv')
        self.assertEqual(client._Client__service.url, 'http://localhost/serv')

    def test_client_host_with_port(self):
        client = servy.client.Client('localhost:80', 'serv')
        self.assertEqual(client._Client__service.url, 'http://localhost:80/serv')

    def test_client_unicode_values(self):
        client = servy.client.Client(u'localhost:80', u'serv')
        self.assertEqual(client._Client__service.url, 'http://localhost:80/serv')


class RemoteExecution(unittest.TestCase):
    def setUp(self):
        self.service = servy.client.Service('localhost', 'serv')
        self.client = servy.client.Client('localhost', self.service)

    def test_remote_execution(self):
        content = servy.proto.Response.encode('content')
        with mock.patch('servy.client.Service.read') as read:
            read.return_value = content
            self.assertEqual(self.client.fn(), servy.proto.Response.decode(content))
        message = servy.proto.Request.encode((), {})
        read.assert_called_once_with(message)

    def test_failed_remote_execution(self):
        with self.assertRaises(TypeError):
            self.client()

    def test_http_exception_404(self):
        with mock.patch('servy.client.Service.read') as read:
            read.side_effect = urllib2.HTTPError(self.service.url, 404, 'Not Found', [], io.StringIO())
            with self.assertRaises(servy.exc.ServiceNotFound):
                self.client.fn()

    def test_http_exception_503(self):
        with mock.patch('servy.client.Service.read') as read:
            fp = io.StringIO()
            fp.write(unicode(servy.proto.RemoteException.encode('traceback')))
            fp.seek(0)
            read.side_effect = urllib2.HTTPError(self.service.url, 503, 'Service Unavailable', [], fp)
            with self.assertRaises(servy.exc.RemoteException):
                self.client.fn()

    def test_http_exception_503_failed(self):
        with mock.patch('servy.client.Service.read') as read:
            read.side_effect = urllib2.HTTPError(self.service.url, 503, 'Service Unavailable', [], io.StringIO())
            with self.assertRaises(servy.exc.RemoteException):
                self.client.fn()

    def test_uncovered_http_exception(self):
        with mock.patch('servy.client.Service.read') as read:
            read.side_effect = urllib2.HTTPError(self.service.url, 600, 'Magic', [], io.StringIO())
            with self.assertRaises(urllib2.HTTPError):
                self.client.fn()
