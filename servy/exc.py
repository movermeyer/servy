class BaseException(Exception):
    pass


class ServiceNotFound(BaseException):
    def __init__(self, service):
        self.service

    def __str__(self):
        return str(self.service)


class ProcedureNotFound(BaseException):
    def __init__(self, procedure):
        self.procedure = procedure

    def __str__(self):
        return str(self.procedure)
