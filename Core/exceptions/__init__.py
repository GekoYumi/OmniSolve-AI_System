"""Exception classes for OmniSolve."""
from .errors import (
    OmniSolveError,
    ConfigurationError,
    BrainConnectionError,
    BrainResponseError,
    CodeGenerationError,
    CodeValidationError,
    ParsingError,
    FileOperationError,
    ProjectError,
    RetryExhaustedError
)

__all__ = [
    'OmniSolveError',
    'ConfigurationError',
    'BrainConnectionError',
    'BrainResponseError',
    'CodeGenerationError',
    'CodeValidationError',
    'ParsingError',
    'FileOperationError',
    'ProjectError',
    'RetryExhaustedError'
]
