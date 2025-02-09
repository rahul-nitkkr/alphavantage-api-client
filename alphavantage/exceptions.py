"""Exceptions for the Alpha Vantage API client."""

class AlphaVantageError(Exception):
    """Base exception for Alpha Vantage API errors."""
    pass

class APIKeyError(AlphaVantageError):
    """Raised when there are issues with the API key."""
    pass

class RateLimitError(AlphaVantageError):
    """Raised when API rate limits are exceeded."""
    pass

class InvalidParameterError(AlphaVantageError):
    """Raised when invalid parameters are provided."""
    pass

class APIError(AlphaVantageError):
    """Raised when the API returns an error."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}") 