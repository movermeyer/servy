class Request(object):
    def __init__(self):
        pass

    def connect(self, dsn):
        self.dsn = dsn

    def send(self, message):
        pass


class Reply(object):
    def __init__(self):
        pass

    def bind(self):
        pass

    def recv(self):
        pass
