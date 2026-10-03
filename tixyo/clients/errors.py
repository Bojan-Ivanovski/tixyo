"""Common client errors."""


class ClientError(RuntimeError):
    """Base error for client failures."""


class ClientConfigurationError(ClientError):
    """Raised when client configuration is invalid."""


class ClientRequestError(ClientError):
    """Raised when a remote service rejects or cannot complete a request."""
