from datetime import datetime, timedelta

from draftable.endpoints.validation import (
    validate_expires,
    validate_identifier,
    validate_valid_until,
)

from ...transport import RESTClient
from ...utilities import Url, aware_datetime_to_timestamp
from ..exceptions import handle_request_exception
from . import signing
from .comparison import Comparison, comparison_from_response
from .sides import FileSide, URLSide, data_from_side

try:
    from typing import List, Optional, Union
except ImportError:
    pass


class ComparisonsEndpoint(object):
    def __init__(self, client, base_url):
        # type: (RESTClient, Url) -> None
        self.__url = base_url / "comparisons"
        self.__client = client

    @property
    def account_id(self):
        # type: () -> str
        return self.__client.account_id

    @property
    def auth_token(self):
        # type: () -> str
        return self.__client.auth_token

    @handle_request_exception
    def all(self):
        # type: () -> List[Comparison]
        return list(
            map(comparison_from_response, self.__client.get(self.__url)["results"])
        )

    @handle_request_exception
    def get(self, identifier):
        # type: (str) -> Comparison
        identifier = validate_identifier(identifier)
        return comparison_from_response(self.__client.get(self.__url / identifier))

    @handle_request_exception
    def create(self, left, right, identifier=None, public=False, expires=None):
        # type: (Union[str, FileSide, URLSide], Union[str, FileSide, URLSide], Optional[str], bool, Optional[Union[datetime, timedelta]]) -> Comparison
        """Creates a new comparison with the Draftable API.

        :param left: a string representing URL or file path, *or* a Side object that includes file type code and display name.
        :param right: as for "left".
        :param identifier: The identifier to use for this comparison, or None to generate a new identifier
        :param public: True if this comparison should be public, or False if not
        :param expires: None for never expires, or a datetime/timedelta object
        :return: the newly created comparison
        """
        if identifier is not None:
            identifier = validate_identifier(identifier)
        if expires is not None:
            expires = validate_expires(expires)
        public = bool(public)

        data = {
            "identifier": identifier,
            "left": data_from_side("left", left),
            "right": data_from_side("right", right),
            "public": public,
            "expires": expires.isoformat() if expires is not None else None,
        }

        return comparison_from_response(self.__client.post(self.__url, data))

    @handle_request_exception
    def delete(self, identifier):
        # type: (str) -> None
        identifier = validate_identifier(identifier)
        self.__client.delete(self.__url / identifier)

    def public_viewer_url(self, identifier, wait=False):
        # type: (str, bool) -> str
        identifier = validate_identifier(identifier)
        return str(
            self.__url / "viewer" / self.account_id / identifier
            + ("?wait" if wait else "")
        )

    def signed_viewer_url(
        self, identifier, valid_until=timedelta(minutes=30), wait=False
    ):
        # type: (str, Union[datetime, timedelta], bool) -> str
        identifier = validate_identifier(identifier)

        valid_until_timestamp = aware_datetime_to_timestamp(
            validate_valid_until(valid_until)
        )

        signature = signing.get_viewer_url_signature(
            self.account_id, self.auth_token, identifier, valid_until_timestamp
        )

        param_wait = "&wait" if wait else ""
        params = f"?valid_until={valid_until_timestamp}&signature={signature}{param_wait}"

        return str(self.__url / "viewer" / self.account_id / identifier + params)
