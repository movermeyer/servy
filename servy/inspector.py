from __future__ import absolute_import

import inspect


class Container(object):
    pass


class Inspector(object):
    @staticmethod
    def is_procedure(obj):
        return (
            inspect.ismethod(obj) or
            inspect.isfunction(obj)
        )

    @staticmethod
    def is_container(obj):
        return (
            isinstance(obj, dict) or
            (inspect.isclass(obj) and issubclass(obj, Container)) or
            isinstance(obj, Container)
        )

    @staticmethod
    def get_public(items):
        return {k: v for k, v in items if (
            not (k.startswith('_') or k.startswith('__')) and
            k not in ('im_class', 'im_self', 'im_func')
        )}

    @classmethod
    def analyze(cls, obj):
        if isinstance(obj, dict):
            procedures = {k: v for k, v in obj.items() if cls.is_procedure(v)}.items()
            containers = {k: v for k, v in obj.items() if cls.is_container(v)}.items()
        else:
            procedures = inspect.getmembers(obj, cls.is_procedure)
            containers = inspect.getmembers(obj, cls.is_container)

        procedures = cls.get_public(procedures)
        containers = cls.get_public(containers)
        return containers, procedures

    @classmethod
    def find(cls, container):
        containers_tree, procedures_tree = cls.analyze(container)
        while containers_tree:
            for namespace in containers_tree.copy():
                container = containers_tree.pop(namespace)
                if namespace.count('.') > 3:
                    continue
                containers, procedures = cls.analyze(container)
                for procedure in procedures:
                    procedures_tree['{}.{}'.format(namespace, procedure)] = \
                        procedures[procedure]
                for container in containers:
                    containers_tree['{}.{}'.format(namespace, container)] = \
                        containers[container]

        return procedures_tree
