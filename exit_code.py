from enum import Enum


class ExitCode(Enum):
    EXIT_SUCCESS = 0
    WRONG_HELP_OPTIONS = 10
    WRONG_XML_FORMAT = 31
    WRONG_XML_STRUCTURE = 32
    INTERN_ERROR = 99
