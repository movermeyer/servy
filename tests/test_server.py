from __future__ import absolute_import

import unittest

import pytest
import webob
import webob.exc

import servy.server
import servy.message as message


def fn():
    pass


class Simple(object):
    @classmethod
    def fn():
        pass


class Complex(servy.server.Container):
    simple = Simple
    fn = fn


class ServerInitiation(unittest.TestCase):
    def test_explicit(self):
        server = servy.server.Server(
            fn=fn,
        )
        assert server.procedures == {
            'fn': fn,
        }

    def test_explicit_with_junk(self):
        server = servy.server.Server(
            junk=type,
        )
        assert server.procedures == {}

    def test_decorator_simple_container(self):
        Server = servy.server.Server(Simple)
        assert Server.procedures == {
            'fn': Simple.fn,
        }

    def test_decorator_simple_non_container(self):
        @servy.server.Server
        class Server(object):
            simple = Simple

        assert Server.procedures == {}

    def test_decorator_complex(self):
        @servy.server.Server
        class Server(object):
            c = Complex

        assert Server.procedures == {
            'c.fn': Complex.fn,
        }


@servy.server.Server
class RPC(object):
    NAME = 'rpc'

    @classmethod
    def proc(cls):
        return 'rpc'

    @classmethod
    def proc_ext(cls, prefix, suffix=None):
        suffix = suffix or ''
        return '{}_{}'.format(prefix, suffix)


class ProcedureCall(unittest.TestCase):
    def test_docs(self):
        request = webob.Request.blank('/')
        request.method = 'GET'

        response = RPC(request)
        assert response == 'proc\n    None\n\nproc_ext\n    None\n\n'

    def test_method_not_allowed(self):
        request = webob.Request.blank('/proc')
        request.method = 'PUT'

        with pytest.raises(webob.exc.HTTPMethodNotAllowed):
            RPC(request)

    def test_proc_not_found(self):
        request = webob.Request.blank('/not_found')
        request.method = 'POST'

        with pytest.raises(webob.exc.HTTPNotFound):
            RPC(request)

    def test_no_body(self):
        request = webob.Request.blank('/proc')
        request.method = 'POST'

        with pytest.raises(webob.exc.HTTPBadRequest):
            RPC(request)

    def test_call_without_args(self):
        request = webob.Request.blank('/proc')
        request.method = 'POST'
        request.body = message.Request.encode((), {})

        response = message.Response.decode(RPC(request))
        assert response == 'rpc'

    def test_call_with_args(self):
        request = webob.Request.blank('/proc_ext')
        request.method = 'POST'
        request.body = message.Request.encode(('O'), {'suffix': 'O'})

        response = message.Response.decode(RPC(request))
        assert response == 'O_O'
