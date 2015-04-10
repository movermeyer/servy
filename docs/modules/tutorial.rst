Tutorial
========

Explicit Server Definition
--------------------------

The most simple way to define services is::

   def echo():
       pass

   server = servy.server.Server(
       echo=echo
   )


Implicit Server Definition
--------------------------

Server could be defined in more declarative way::

   @servy.server.Server
   class RPCServer(object):
       def echo(self):
           pass

All ``RPCServer`` callable attributes will be provided as services.

Simple Service
--------------

::

   class Logger(servy.server.Container):
       def __init__(self):
           self.logger = LoggerClass()
       def debug(self, message):
           self.logger.debug(message)

   @servy.server.Server
   class EchoServer(servy.server.Container):
       logger = Logger()

       @classmethod
       def echo(cls, message):
           return message
