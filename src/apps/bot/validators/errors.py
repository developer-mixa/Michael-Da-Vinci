class ValidationError(Exception):
    def __init__(self) -> None:
        super().__init__()


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