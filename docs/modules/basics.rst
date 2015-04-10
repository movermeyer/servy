Basics
======

Client
------

Servy uses objects introspection to provide pythonic API for Services.

Server
------

Path of the HTTP request is name of the service to call. Service in terms of ``servy``
is callable object(function, method or class with defined ``__call__`` method and inherited
from :class:`servy.server.Service`). Service classes could also play roles of containers -
Service class is recursivly introspected for additional services and containers. Thus:
#. :class:`servy.server.Server` is a container for services and rpc handler.
#. :class:`servy.server.Service` is a base class for service and also container for additional
services

.. note::
   :class:`servy.server.Inspector` looks for a services in dicts, instances of
   :class:`servy.server.Service` and subclasses of :class:`servy.server.Service`.
