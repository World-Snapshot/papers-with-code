__all__ = ["PapersWithCodeError"]

import enum
from typing import Optional

from httpx import Response
from pydantic import ValidationError as PydanticValidationError


class PapersWithCodeError(Exception):
    """Base class for all errors."""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}({self.message})"

    __repr__ = __str__


class InvalidConfiguration(PapersWithCodeError):
    class Op(str, enum.Enum):
        get = "getting"
        set = "setting"
        load = "loading"
        save = "saving"

    def __init__(
        self,
        message: Optional[str] = None,
        key: Optional[str] = None,
        value: Optional[str] = None,
        error: Optional[Exception] = None,
        operation: Op = Op.get,
    ):
        self.message = message
        self.key = key
        self.value = value
        self.error = error
        self.operation = operation
        if message is not None:
            super().__init__(message=message)
        else:
            error_msg = "" if error is None else f" {error}"
            if key is None:
                if value is None:
                    message = f"Configuration {operation} error.{error_msg}"
                else:
                    message = f"Invalid {operation} value '{value}'.{error_msg}"
            else:
                if value is None:
                    message = f"Error {operation} key='{key}'.{error_msg}"
                else:
                    message = (
                        f"Error {operation} key='{key}' value='{value}'." f"{error_msg}"
                    )
            super().__init__(message=message)


class ClientError(PapersWithCodeError):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message=message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.__class__.__name__}({self.status_code}: {self.message})"

    __repr__ = __str__


class ValidationError(ClientError):
    def __init__(self, error: PydanticValidationError):
        self.error = error
        super().__init__(message="Request validation error.", status_code=400)

    @property
    def errors(self):
        return self.error.errors()


class HttpClientError(ClientError):
    def __init__(
        self,
        message: str,
        response: Optional[Response] = None,
        status_code: int = 500,
    ):
        super().__init__(
            message=message,
            status_code=(status_code if response is None else response.status_code),
        )
        self.response = response

    @property
    def data(self) -> dict:
        if self.response is None:
            return {}
        return self.response.json()


class HttpClientTimeout(HttpClientError):
    """Http timeout error."""

    def __init__(self):
        super().__init__("Timeout exceeded")


class HttpRateLimitExceeded(HttpClientError):
    def __init__(self, response, limit, remaining, reset, retry):
        super().__init__("Rate limit exceeded.", response=response)
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.retry = retry

    def __str__(self):
        return (
            f"{self.__class__.__name__}(limit={self.limit}, "
            f"remaining={self.remaining}, reset={self.reset}s, "
            f"retry={self.retry}s)"
        )

    __repr__ = __str__


class SerializationError(ClientError):
    def __init__(self, errors):
        """Thrown when the client cannot serialize or deserialize an object.

        Args:
            errors: Dictionary of found errors
        """
        super().__init__("Serialization error.")
        self.errors = errors
