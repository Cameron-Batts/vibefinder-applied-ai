"""Exceptions that mark expected failures, so real bugs are never hidden."""


class ValidationError(Exception):
    """Raised when user input or catalog data is invalid."""


class VerificationError(Exception):
    """Raised when a recommendation result fails a runtime check."""
