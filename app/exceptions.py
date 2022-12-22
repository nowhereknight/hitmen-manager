class ValidationError(ValueError):
    pass

class NotFoundError(ValueError):
    pass

class WrongPasswordError(ValueError):
    pass

class NotAllowedError(ValueError):
    pass

class ForbiddenError(ValueError):
    pass

class InvalidChangeError(ValueError):
    pass
