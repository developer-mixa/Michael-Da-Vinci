"""Domain-level exceptions (no framework dependencies)."""


class DomainError(Exception):
    """Base class for all domain errors."""


# --- User errors ---

class NonRegisteredError(DomainError):
    """User with given telegram_id not found."""


class ProfileMustBeActivatedError(DomainError):
    """User profile must be activated to perform this action."""


class AlreadyRegisteredError(DomainError):
    """User is already registered."""


# --- Validation errors ---

class ValidationError(DomainError):
    """Base validation error."""


class NameCanContainLettersError(ValidationError):
    pass


class TooLongNameError(ValidationError):
    pass


class TooShortNameError(ValidationError):
    pass


class NameCannotContainSpacesError(ValidationError):
    pass


class NameBeginCannotBeLowercaseError(ValidationError):
    pass


class WrongAgeFormatError(ValidationError):
    pass

