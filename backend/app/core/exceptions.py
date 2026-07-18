"""Exceptions for MindMirror AI."""


class MindMirrorException(Exception):
    """Base exception for MindMirror AI."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AIServiceException(MindMirrorException):
    """Exception raised when AI service fails."""

    def __init__(self, message: str = "AI service unavailable"):
        super().__init__(message, status_code=503)


class ValidationException(MindMirrorException):
    """Exception raised when validation fails."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400)


class NotFoundException(MindMirrorException):
    """Exception raised when resource is not found."""

    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status_code=404)


class RateLimitException(MindMirrorException):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)
