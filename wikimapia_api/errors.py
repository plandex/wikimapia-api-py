
class Error(Exception): pass

class UnimplementedError(Error): pass

class RequestError(Error):
    def __init__(self, message, code):
        super(RequestError, self).__init__(message)
        self._code = code

    @property
    def code(self):
        return self._code

class FunctionNameError(RequestError): pass
