Tutorial
========

Functional Server Definition
----------------------------

The most simple way to define services is::

   server = servy.server.Server(
       echo=Echo
   )

.. note::

   There is no introspection for ``Echo`` server, thus ``Echo`` class should be callable.
   To see more flexible way to define service take a look on Class-based Server Definition.

Class-based Server Definition
-----------------------------

Server could be defined in more declarative way::

   @servy.server.Server
   class RPCServer(object):
       echo = Echo

All ``RPCServer`` callable attributes will be provided as services.

Simple Service
--------------

::

   @servy.server.Server
   class EchoServer(object):
       @classmethod
       def echo(cls, message):
           return message
