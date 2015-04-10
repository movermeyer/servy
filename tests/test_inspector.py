from __future__ import absolute_import

import unittest

import servy.server


class Empty(object):
    pass


class Dummy(object):
    def fn(self):
        pass


class Map(object):
    m = {'fn': lambda x: x}


class Service(servy.server.Service):
    def __call__(self):
        pass

srv = Service()


class Inception(object):
    service = srv

    class A1(servy.server.Service):
        class A2(servy.server.Service):
            class A3(servy.server.Service):
                class A4(servy.server.Service):
                    class A5(servy.server.Service):
                        @classmethod
                        def fn(cls):
                            pass


class ServiceDetection(unittest.TestCase):
    def test_lambda(self):
        self.assertTrue(servy.server.Inspector.is_service(lambda x: x))

    def test_method(self):
        self.assertTrue(servy.server.Inspector.is_service(Dummy().fn))

    def test_callable_class_service(self):
        self.assertTrue(servy.server.Inspector.is_service(Service()))

    def test_type(self):
        self.assertFalse(servy.server.Inspector.is_service(dict))

    def test_int(self):
        self.assertFalse(servy.server.Inspector.is_service(1))

    def test_string(self):
        self.assertFalse(servy.server.Inspector.is_service("1"))

    def test_dummy_class(self):
        self.assertFalse(servy.server.Inspector.is_service(Dummy))


class ContainerDetection(unittest.TestCase):
    def test_dict(self):
        self.assertTrue(servy.server.Inspector.is_container({}))

    def test_service_class(self):
        self.assertTrue(servy.server.Inspector.is_container(Service))

    def test_service_class_instance(self):
        self.assertTrue(servy.server.Inspector.is_container(Service()))

    def test_dummy_class(self):
        self.assertFalse(servy.server.Inspector.is_container(Dummy))


class PublicMethodsDetection(unittest.TestCase):
    def test_double_underscores(self):
        items = {
            '__private': None,
        }
        self.assertEqual(
            servy.server.Inspector.get_public(items.items()),
            {},
        )

    def test_single_underscores(self):
        items = {
            '_private': None,
        }
        self.assertEqual(
            servy.server.Inspector.get_public(items.items()),
            {},
        )


class Analyze(unittest.TestCase):
    def test_dummy_object(self):
        containers, services = servy.server.Inspector.analyze(Dummy)
        self.assertEqual(containers, {})
        self.assertEqual(services, {'fn': Dummy.fn})

    def test_dummy_instance_object(self):
        dummy = Dummy()
        containers, services = servy.server.Inspector.analyze(dummy)
        self.assertEqual(containers, {})
        self.assertEqual(services, {'fn': dummy.fn})

    def test_empty_object(self):
        containers, services = servy.server.Inspector.analyze(Empty)
        self.assertEqual(containers, {})
        self.assertEqual(services, {})

    def test_map(self):
        containers, services = servy.server.Inspector.analyze(Map)
        self.assertEqual(containers, {'m': Map.m})
        self.assertEqual(services, {})

    def test_map_instance(self):
        m = Map()
        containers, services = servy.server.Inspector.analyze(m)
        self.assertEqual(containers, {'m': m.m})
        self.assertEqual(services, {})

    def test_dict(self):
        container = {'fn': lambda x: x}
        containers, services = servy.server.Inspector.analyze(container)
        self.assertEqual(containers, {})
        self.assertEqual(services, {'fn': container['fn']})


class ServiceFinder(unittest.TestCase):
    def test_dummy(self):
        services = servy.server.Inspector.find(Dummy)
        self.assertEqual(services, {'fn': Dummy.fn})

    def test_dummy_instance(self):
        dummy = Dummy()
        services = servy.server.Inspector.find(dummy)
        self.assertEqual(services, {'fn': dummy.fn})

    def test_empty(self):
        services = servy.server.Inspector.find(Empty)
        self.assertEqual(services, {})

    def test_map(self):
        services = servy.server.Inspector.find(Map)
        self.assertEqual(services, {'m.fn': Map.m['fn']})

    def test_service(self):
        services = servy.server.Inspector.find(Inception)
        self.assertEqual(services, {'service': srv})
