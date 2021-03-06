class CannotDeactivateYourselfException(Exception):
    """
    Raised when an admin user attempts to deactivate or unstaff themself.
    """


class CannotDeleteYourselfException(Exception):
    """
    Raised when an admin user attempts to delete themself.
    """


class UserDoesNotExistException(Exception):
    """
    Raised when a delete or update operation is attempted on an unknown user.
    """


class InvalidSortDirectionException(Exception):
    """
    Raised when an invalid sort direction is provided.
    """


class InvalidSortAttributeException(Exception):
    """
    Raised when a sort is requested for an invalid or non-existent field.
    """
