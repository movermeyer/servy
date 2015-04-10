from __future__ import absolute_import

import unittest

import servy.server


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
        self.assertEqual(server.procedures, {
            'fn': fn,
        })

    def test_explicit_with_junk(self):
        server = servy.server.Server(
            junk=type,
        )
        self.assertEqual(server.procedures, {})

    def test_decorator_simple_container(self):
        Server = servy.server.Server(Simple)
        self.assertEqual(Server.procedures, {
            'fn': Simple.fn,
        })

    def test_decorator_simple_non_container(self):
        @servy.server.Server
        class Server(object):
            simple = Simple

        self.assertEqual(Server.procedures, {})
