from __future__ import absolute_import

import mock
import unittest

import servy.client
import servy.proto


class RemoteExecution(unittest.TestCase):
    def setUp(self):
        self.service = servy.client.Service('serv', 'localhost')
        self.client = servy.client.Client(self.service)

    def test_remote_execution(self):
        content = servy.proto.Response.encode('content')
        with mock.patch('servy.client.Service.read') as read:
            read.return_value = content
            self.assertEqual(self.client(), servy.proto.Response.decode(content))
