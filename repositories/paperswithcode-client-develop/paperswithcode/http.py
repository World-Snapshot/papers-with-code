import enum
from typing import Optional

import httpx

from paperswithcode import errors
from paperswithcode.models import Model


class AuthorizationMethod(enum.Enum):
    basic = "Basic"
    token = "Token"
    jwt = "JWT"


class HttpClient:
    """Generic requests handler.

    Handles retries and HTTP errors.
    """

    Authorization = AuthorizationMethod
    ERRORS = {
        401: "Unauthorized",
        403: "Forbidden!",
        404: "Not found.",
        409: "Conflict",
        429: "Under pressure! (Too many requests)",
        500: "You broke it!!!",
        502: "Server not reachable.",
        503: "Server under maintenance.",
    }

    def __init__(
        self,
        url: str,
        token: str = "",
        authorization_method: AuthorizationMethod = AuthorizationMethod.jwt,
        timeout: int = 10,
    ):
        """Initialize.

        Args:
            url: URL to the Traktor server.
            token: Traktor authentication token.
            authorization_method: Authorization method.
            timeout: Request timeout time.
        """
        self.url = url
        self.token = token
        self.authorization_method = authorization_method
        self.timeout = timeout

        # Setup headers
        self.headers = {"Content-Type": "application/json"}

        self.response = None

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, str]] = None,
        data: Optional[Model] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        """Request method.

        Request method handles all the url joining, header merging, logging and
        error handling.

        Args:
            method: Method for the request - GET or POST
            url: Partial url of the request. It is added to the base url
            headers: Dictionary of additional HTTP headers
            params: Dictionary of query parameters for the request
            data: A JSON serializable Python object to send in the body of the request.
                Used only in POST requests.
            timeout: How many seconds to wait for the server to send data before
                giving up.

        Returns:
            Deserialized json response.
        """
        headers = {**self.headers, **(headers or {})}

        # Set authorization token
        if self.token.strip() != "":
            headers["Authorization"] = f"{self.authorization_method.value} {self.token}"

        timeout = timeout or self.timeout

        try:
            with httpx.Client(base_url=self.url, headers=self.headers) as client:
                if method.lower() == "get":
                    self.response = client.get(
                        url=url,
                        headers=headers,
                        params=params,
                        timeout=timeout,
                    )
                elif method.lower() == "patch":
                    self.response = client.patch(
                        url=url,
                        headers=headers,
                        params=params,
                        data=({} if data is None else data.dict()),
                        timeout=timeout,
                    )
                elif method.lower() == "post":
                    self.response = client.post(
                        url=url,
                        headers=headers,
                        params=params,
                        data=({} if data is None else data.dict()),
                        timeout=timeout,
                    )
                elif method.lower() == "delete":
                    self.response = client.delete(
                        url=url,
                        headers=headers,
                        params=params,
                        timeout=timeout,
                    )
                else:
                    raise errors.HttpClientError(
                        f"Unsupported method: {method}", status_code=405
                    )
        except httpx.TimeoutException as e:
            # If request timed out, let upper level handle it they way it sees
            # fit one place might want to retry another might not.
            raise errors.HttpClientTimeout() from e

        except ConnectionError as e:
            raise errors.HttpClientError("Server not reachable.") from e

        except Exception as e:
            raise errors.HttpClientError(f"Unknown error. {e!r}") from e

        if 200 <= self.response.status_code <= 299:
            try:
                return self.response.json() if self.response.text else {}
            except Exception as e:
                raise errors.HttpClientError(
                    f"Error while parsing server response: {e!r}",
                    response=self.response,
                ) from e

        # Check rate limit
        limit = self.response.headers.get("X-Ratelimit-Limit", None)
        if limit is not None:
            remaining = self.response.headers["X-Ratelimit-Remaining"]
            reset = self.response.headers["X-Ratelimit-Reset"]
            retry = self.response.headers["X-Ratelimit-Retry"]

            if remaining == 0:
                raise errors.HttpRateLimitExceeded(
                    response=self.response,
                    limit=limit,
                    remaining=remaining,
                    reset=reset,
                    retry=retry,
                )

        # Try known error messages
        message = self.ERRORS.get(self.response.status_code, None)
        if message is not None:
            raise errors.HttpClientError(message, response=self.response)

        if self.response.status_code == 400:
            try:
                message = self.response.json()["error"]
            except Exception:
                message = "Bad Request."
            raise errors.HttpClientError(message, response=self.response)

        # Generalize unknown messages.
        try:
            message = self.response.json()["message"]
        except Exception:
            message = "Unknown error."
        raise errors.HttpClientError(message, response=self.response)

    def get(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        """Perform get request.

        Args:
            url: Partial url of the request. It is added to the base url
            headers: Dictionary of additional HTTP headers
            params: Dictionary of query parameters for the request
            timeout: How many seconds to wait for the server to send data before
                giving up.

        Returns:
            Deserialized json response.

        """
        return self.request(
            method="get",
            url=url,
            headers=headers,
            params=params,
            timeout=timeout,
        )

    def patch(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, str]] = None,
        data: Optional[Model] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        """Perform patch request.

        Args:
            url: Partial url of the request. It is added to the base url
            headers: Dictionary of additional HTTP headers
            params: Dictionary of query parameters for the request
            data: A JSON serializable Python object to send in the body of the request.
            timeout: How many seconds to wait for the server to send data before
                giving up.

        Returns:
            Deserialized json response.

        """
        return self.request(
            method="patch",
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )

    def post(
        self,
        url: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, str]] = None,
        data: Optional[Model] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        """Perform post request.

        Args:
            url: Partial url of the request. It is added to the base url
            headers: Dictionary of additional HTTP headers
            params: Dictionary of query parameters for the request
            data: A JSON serializable Python object to send in the body of the request.
            timeout: How many seconds to wait for the server to send
                data before giving up

        Returns:
            Deserialized json response.

        """
        return self.request(
            method="post",
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )

    def delete(
        self,
        url,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        """Perform delete request.

        Args:
            url: Partial url of the request. It is added to the base url
            headers: Dictionary of additional HTTP headers
            params: Dictionary of query parameters for the request
            timeout: How many seconds to wait for the server to send data before
                giving up

        Returns:
            Deserialized json response.
        """
        return self.request(
            method="delete",
            url=url,
            headers=headers,
            params=params,
            timeout=timeout,
        )
