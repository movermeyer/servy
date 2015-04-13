from __future__ import absolute_import

import json
import unittest

import servy.message


class ResponseProto(unittest.TestCase):
    def setUp(self):
        self.message = json.dumps({
            'message': 'response',
            'content': 'content',
        })

    def test_base_class(self):
        assert issubclass(servy.message.Response, servy.message.Message)

    def test_encode(self):
        content = servy.message.Response.encode('content')
        assert content == self.message

    def test_decode(self):
        assert servy.message.Response.decode(self.message) == 'content'


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
        assert issubclass(servy.message.Request, servy.message.Message)

    def test_encode(self):
        content = servy.message.Request.encode((), {})
        assert content == self.message

    def test_decode(self):
        assert servy.message.Request.decode(self.message) == ([], {})


class ExceptionProto(unittest.TestCase):
    def setUp(self):
        self.message = json.dumps({
            'message': 'exception',
            'content': 'traceback',
        })

    def test_base_class(self):
        assert issubclass(servy.message.RemoteException, servy.message.Message)

    def test_encode(self):
        content = servy.message.RemoteException.encode('traceback')
        assert content == self.message

    def test_decode(self):
        assert servy.message.RemoteException.decode(self.message) == 'traceback'
