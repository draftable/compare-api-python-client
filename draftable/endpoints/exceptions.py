from __future__ import absolute_import

try:
    # noinspection PyUnresolvedReferences
    from typing import Union
except ImportError:
    pass


class EndpointException(Exception):
    pass


class InvalidArgument(EndpointException):
    def __init__(self, argument_name, message):
        # type: (str, str) -> None
        super(InvalidArgument, self).__init__("An invalid value was received for `{argument}`: {message}".format(argument=argument_name, message=message))


class BadRequest(EndpointException):
    def __init__(self, status_code, response):
        # type: (int, Union[dict, list]) -> None
        self.status_code = status_code
        self.response = response
        super(BadRequest, self).__init__('Bad request: status={status}, response={response}'.format(status=status_code, response=response))
