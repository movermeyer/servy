Basics
======

Client
------


Server
------

There is 2 ways to initialize :class:`servy.server.Server`:
#. Explicit - passing procedures by name
#. Implicit - decorating container

Server is based on two concepts:

Container

   Helper class that gives :class:`servy.server.Inspector`
   instruction to look for a procedures in this class. To provide flexibility
   every dict object is treated like a container.

Procedure

   Function or method.
