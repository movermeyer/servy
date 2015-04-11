from __future__ import absolute_import

import json
import unittest

import servy.proto


class ResponseProto(unittest.TestCase):
    def setUp(self):
        self.message = json.dumps({
            'message': 'response',
            'content': 'content',
        })

    def test_base_class(self):
        self.assertTrue(issubclass(servy.proto.Response, servy.proto.Message))

    def test_encode(self):
        content = servy.proto.Response.encode('content')
        assert content == self.message

    def test_decode(self):
        assert servy.proto.Response.decode(self.message) == 'content'


class RequestProto(unittest.TestCase):
    def setUp(self):
        self.message = json.dumps({
            'message': 'request',
            'content': {
                'args': (),
                'kw': {},
            },
        })

    def test_base_class(self):
        self.assertTrue(issubclass(servy.proto.Request, servy.proto.Message))

    def test_encode(self):
        content = servy.proto.Request.encode((), {})
        assert content == self.message

    def test_decode(self):
        self.assertEqual(
            servy.proto.Request.decode(self.message),
            ([], {}),
        )


class ExceptionProto(unittest.TestCase):
    def setUp(self):
        self.message = json.dumps({
            'message': 'exception',
            'content': 'traceback',
        })

    def test_base_class(self):
        self.assertTrue(issubclass(servy.proto.RemoteException, servy.proto.Message))

    def test_encode(self):
        content = servy.proto.RemoteException.encode('traceback')
        assert content == self.message

    def test_decode(self):
        assert servy.proto.RemoteException.decode(self.message) == 'traceback'
