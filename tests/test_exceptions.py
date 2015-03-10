from __future__ import absolute_import

import unittest

import servy.exc


class StringRepresentation(unittest.TestCase):
    def test_service_not_found_str_repr(self):
        exception = servy.exc.ServiceNotFound('serv')
        self.assertEqual(str(exception), 'serv')

    def test_procedure_not_found_str_repr(self):
        exception = servy.exc.ProcedureNotFound('serv')
        self.assertEqual(str(exception), 'serv')
