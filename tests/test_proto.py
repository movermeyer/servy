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
        self.assertEqual(content, self.message)

    def test_decode(self):
        self.assertEqual(servy.proto.Response.decode(self.message), 'content')


class RequestProto(unittest.TestCase):
    def setUp(self):
        self.message = json.dumps({
            'message': 'request',
            'content': {
                'proc': 'proc',
                'args': (),
                'kw': {},
            },
        })

    def test_base_class(self):
        self.assertTrue(issubclass(servy.proto.Request, servy.proto.Message))

    def test_encode(self):
        content = servy.proto.Request.encode('proc', (), {})
        self.assertEqual(content, self.message)

    def test_decode(self):
        self.assertEqual(
            servy.proto.Request.decode(self.message),
            ('proc', [], {}),
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
        self.assertEqual(content, self.message)

    def test_decode(self):
        self.assertEqual(servy.proto.RemoteException.decode(self.message), 'traceback')
