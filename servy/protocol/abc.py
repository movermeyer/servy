class Request(object):
    def __init__(self):
        pass

    def connect(self, dsn):
        self.dsn = dsn

    def send(self, message):
        pass


class Reply(object):
    def __init__(self, server, addr=None):
        self.server = server
        self.bind(addr)

    def bind(self, addr):
        pass

    def recv(self, message):
        pass
