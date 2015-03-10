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
        service = servy.client.Service('serv', 'localhost')
        self.assertEqual(service.url, 'http://localhost/serv')

    def test_client_init(self):
        client = servy.client.Client({'name': 'serv', 'host': 'localhost'})
        self.assertEqual(client._Client__service.url, 'http://localhost/serv')


class RemoteExecution(unittest.TestCase):
    def setUp(self):
        self.service = servy.client.Service('serv', 'localhost')
        self.client = servy.client.Client(self.service)

    def test_remote_execution(self):
        content = servy.proto.Response.encode('content')
        with mock.patch('servy.client.Service.read') as read:
            read.return_value = content
            self.assertEqual(self.client.fn(), servy.proto.Response.decode(content))
        message = servy.proto.Request.encode('fn', (), {})
        read.assert_called_once_with(message)

    def test_failed_remote_execution(self):
        with self.assertRaises(TypeError):
            self.client()

    def test_http_exception_404(self):
        with mock.patch('servy.client.Service.read') as read:
            read.side_effect = urllib2.HTTPError(self.service.url, 404, 'Not Found', [], io.StringIO())
            with self.assertRaises(servy.exc.ServiceNotFound):
                self.client.fn()

    def test_http_exception_501(self):
        with mock.patch('servy.client.Service.read') as read:
            read.side_effect = urllib2.HTTPError(self.service.url, 501, 'Not Implemented', [], io.StringIO())
            with self.assertRaises(servy.exc.ProcedureNotFound):
                self.client.fn()
