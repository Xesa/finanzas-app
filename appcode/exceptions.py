# 1. These custom exceptions allow to pass an exception until the API has to return a response,
#    which then can be converted to an HTTP response with the getError() method.
# 2. If we pass a message to the exception it will be included in the HTTP response,
#    but we can choose not to pass any message.
# 3. The error and the code will always be hard-coded in this module.
# 4. The function isException() simply checks if any object passed through it is an exception.

def isException(arg):
    return isinstance(arg, Exception)

class CustomException(Exception):
    def __init__(self, message=None, error=None, code=None):
        super().__init__(message)
        self.error = error if error is not None else None
        self.code = code if code is not None else None

    def getError(self):
        return f"{self.error}: {self.args[0]}" if self.args[0] is not None else self.error, self.code

class ValidationException(CustomException):
    def __init__(self, message=None):
        super().__init__(message, "Forbidden", 403)

class ParameterException(CustomException):
    def __init__(self, message=None):
        super().__init__(message, "Bad request", 400)



