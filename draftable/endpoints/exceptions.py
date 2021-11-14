import functools

import requests

try:
    from typing import Union
except ImportError:
    pass


class EndpointException(Exception):
    pass


class InvalidPath(Exception):
    pass


class InvalidArgument(EndpointException):
    def __init__(self, argument_name, message):
        # type: (str, str) -> None
        super().__init__(
            f"An invalid value was received for `{argument_name}`: {message}"
        )


class BadRequest(EndpointException):
    def __init__(self, status_code, response):
        # type: (int, Union[dict, list]) -> None
        self.status_code = status_code
        self.response = response
        super().__init__(f"Bad request: status={status_code}, response={response}")


class NotFound(BadRequest):
    pass


def raise_for(ex):
    # type: (requests.exceptions.RequestException) -> None
    if isinstance(ex, requests.exceptions.HTTPError):
        try:
            if ex.response.status_code == 404:
                wrapper = NotFound(404, ex.response.json())
            else:
                wrapper = BadRequest(ex.response.status_code, ex.response.json())
        except Exception:
            # No JSON body? This shouldn't happen, but we'll rethrow anyway.
            wrapper = BadRequest(ex.response.status_code, ex.response)
    else:
        # An error in communication has occurred.
        wrapper = EndpointException(
            "Unable to connect to the API. This can occur when you attempt to upload files, "
            "but have invalid credentials - please check your credentials."
        )

    wrapper.__cause__ = ex
    raise wrapper


def handle_request_exception(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.RequestException as ex:
            raise_for(ex)

    return wrapper
