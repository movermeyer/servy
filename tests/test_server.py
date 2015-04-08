from __future__ import absolute_import

import unittest

import servy.server


class Dummy(object):
    def fn(self):
        pass


class Service(servy.server.Service):
    def __call__(self):
        pass


class ServiceInspector(unittest.TestCase):
    def test_is_service(self):
        self.assertTrue(servy.server.ServiceInspector.is_service(lambda x: x))

    def test_is_service_for_method(self):
        self.assertTrue(servy.server.ServiceInspector.is_service(Dummy().fn))

    def test_is_service_for_callable_class_service(self):
        self.assertTrue(servy.server.ServiceInspector.is_service(Service()))

    def test_is_service_for_type(self):
        self.assertFalse(servy.server.ServiceInspector.is_service(dict))

    def test_is_service_for_int(self):
        self.assertFalse(servy.server.ServiceInspector.is_service(1))

    def test_is_service_for_string(self):
        self.assertFalse(servy.server.ServiceInspector.is_service("1"))

    def test_is_service_for_dummy_class(self):
        self.assertFalse(servy.server.ServiceInspector.is_service(Dummy))
