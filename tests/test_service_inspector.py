from __future__ import absolute_import

import unittest

import servy.server


class Dummy(object):
    def fn(self):
        pass


class Service(servy.server.Service):
    def __call__(self):
        pass


class ServiceDetection(unittest.TestCase):
    def test_lambda(self):
        self.assertTrue(servy.server.ServiceInspector.is_service(lambda x: x))

    def test_method(self):
        self.assertTrue(servy.server.ServiceInspector.is_service(Dummy().fn))

    def test_callable_class_service(self):
        self.assertTrue(servy.server.ServiceInspector.is_service(Service()))

    def test_type(self):
        self.assertFalse(servy.server.ServiceInspector.is_service(dict))

    def test_int(self):
        self.assertFalse(servy.server.ServiceInspector.is_service(1))

    def test_string(self):
        self.assertFalse(servy.server.ServiceInspector.is_service("1"))

    def test_dummy_class(self):
        self.assertFalse(servy.server.ServiceInspector.is_service(Dummy))


class ContainerDetection(unittest.TestCase):
    def test_dict(self):
        self.assertTrue(servy.server.ServiceInspector.is_container({}))

    def test_service_class(self):
        self.assertTrue(servy.server.ServiceInspector.is_container(Service))

    def test_service_class_instance(self):
        self.assertTrue(servy.server.ServiceInspector.is_container(Service()))

    def test_dummy_class(self):
        self.assertFalse(servy.server.ServiceInspector.is_container(Dummy))


class PublicMethodsDetection(unittest.TestCase):
    def test_double_underscores(self):
        items = {
            '__private': None,
        }
        self.assertEqual(
            servy.server.ServiceInspector.get_public(items.items()),
            {},
        )

    def test_single_underscores(self):
        items = {
            '_private': None,
        }
        self.assertEqual(
            servy.server.ServiceInspector.get_public(items.items()),
            {},
        )
