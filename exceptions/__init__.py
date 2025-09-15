"""
Custom exceptions for the Secretaria El Cano application.

This module defines custom exception classes used throughout the application
for better error handling and debugging.
"""


class SecretariaElCanoException(Exception):
    """Base exception class for the Secretaria El Cano application."""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DatabaseException(SecretariaElCanoException):
    """Exception raised for database-related errors."""
    pass


class AuthenticationException(SecretariaElCanoException):
    """Exception raised for authentication-related errors."""
    pass


class ValidationException(SecretariaElCanoException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, field: str = None, code: str = None):
        self.field = field
        super().__init__(message, code)


class FalleroNotFoundException(SecretariaElCanoException):
    """Exception raised when a fallero is not found."""
    pass


class UserNotFoundException(SecretariaElCanoException):
    """Exception raised when a user is not found."""
    pass


class DuplicateRecordException(SecretariaElCanoException):
    """Exception raised when trying to create a duplicate record."""
    pass