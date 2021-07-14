class UserValidationFailedException(Exception):
    """Error raised when rebuttal for specific debate fails to be recorded."""
    pass


class InvalidPermissionException(Exception):
    """Error raised when a user has no permission."""
    pass
