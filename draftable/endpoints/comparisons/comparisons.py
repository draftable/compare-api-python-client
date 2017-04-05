from __future__ import absolute_import, unicode_literals

try:
    # noinspection PyUnresolvedReferences
    from typing import List, Union, Optional, Any
except ImportError:
    pass

from datetime import datetime, timedelta
import random
import requests.exceptions
from . import exceptions, validation, signing, urls
from .comparison import Comparison, comparison_from_response
from ...transport import RESTClient
from ...utilities import aware_datetime_to_timestamp


# Constants for generating random unique (with high probability) identifiers:
_randomIdentifierLength = 12
_randomIdentifierCharset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Side(object):
    def __init__(self, file_type, display_name = None):
        # type: (str, Optional[str]) -> None
        self.__file_type = validation.validate_file_type(file_type)
        self.__display_name = None if display_name is None else str(display_name)

    @property
    def file_type(self):
        # type: () -> str
        return self.__file_type

    @property
    def display_name(self):
        # type: () -> Optional[str]
        return self.__display_name


class FileSide(Side):
    # noinspection PyShadowingBuiltins
    def __init__(self, file, file_type, display_name = None):
        # type: (Any, str, Optional[str]) -> None
        self.__file = validation.validate_file(file)
        super(FileSide, self).__init__(file_type=file_type, display_name=display_name)

    @property
    def file(self):
        # type: () -> Any
        return self.__file


class URLSide(Side):
    def __init__(self, url, file_type, display_name = None):
        # type: (str, str, Optional[str]) -> None
        self.__url = validation.validate_url(url)
        super(URLSide, self).__init__(file_type=file_type, display_name=display_name)

    @property
    def url(self):
        # type: () -> str
        return self.__url


def data_from_side(side_name, side):
    # type: (str, Union[FileSide, URLSide]) -> dict
    data = {
        'file_type': side.file_type,
    }
    if side.display_name:
        data['display_name'] = side.display_name
    if isinstance(side, URLSide):
        data['source_url'] = side.url
    else:
        assert isinstance(side, FileSide)
        data['file'] = ("{}.{}".format(side_name, side.file_type), side.file, 'application/octet-stream')
    return data


class ComparisonsEndpoint(object):

    InvalidArgument = exceptions.InvalidArgument
    BadRequest = exceptions.BadRequest
    NotFound = exceptions.NotFound

    @staticmethod
    def side_from_url(url, file_type, display_name=None):
        # type: (str, str, Optional[str]) -> URLSide
        return URLSide(url, file_type, display_name)

    # noinspection PyShadowingBuiltins
    @staticmethod
    def side_from_file(file, file_type, display_name=None):
        # type: (Any, str, Optional[str]) -> FileSide
        return FileSide(file, file_type, display_name)

    def __init__(self, account_id, auth_token):
        # type: (str, str) -> None
        self.__account_id = str(account_id)
        self.__auth_token = str(auth_token)
        self.__client = RESTClient(self.__account_id, self.__auth_token)

    def all(self):
        # type: () -> List[Comparison]
        try:
            return list(map(comparison_from_response, self.__client.get(urls.comparisons_url)['results']))
        except requests.exceptions.HTTPError as ex:
            exceptions.raise_for(ex)

    def get(self, identifier):
        # type: (str) -> Comparison
        identifier = validation.validate_identifier(identifier)
        try:
            return comparison_from_response(self.__client.get(urls.comparison_url_for(identifier)))
        except requests.exceptions.HTTPError as ex:
            exceptions.raise_for(ex)

    def create(self, left, right, identifier=None, public=False, expires=None):
        # type: (Union[FileSide, URLSide], Union[FileSide, URLSide], Optional[str], bool, Optional[Union[datetime, timedelta]]) -> Comparison
        if identifier is not None:
            identifier = validation.validate_identifier(identifier)
        if expires is not None:
            expires = validation.validate_expires(expires)
        public = bool(public)

        data = {
            'identifier': identifier,
            'left': data_from_side('left', left),
            'right': data_from_side('right', right),
            'public': public,
            'expires': expires.isoformat() if expires is not None else None,
        }

        try:
            return comparison_from_response(self.__client.post(urls.comparisons_url, data))
        except requests.exceptions.HTTPError as ex:
            exceptions.raise_for(ex)

    def delete(self, identifier):
        # type: (str) -> None
        identifier = validation.validate_identifier(identifier)
        try:
            self.__client.delete(urls.comparison_url_for(identifier))
        except requests.exceptions.HTTPError as ex:
            exceptions.raise_for(ex)

    def public_viewer_url(self, identifier, wait=False):
        # type: (str, bool) -> str
        identifier = validation.validate_identifier(identifier)
        return urls.viewer_url_for(self.__account_id, identifier) + ('?wait' if wait else '')

    def signed_viewer_url(self, identifier, valid_until=timedelta(minutes=30), wait=False):
        # type: (str, Union[datetime, timedelta], bool) -> str
        identifier = validation.validate_identifier(identifier)
        valid_until_timestamp = aware_datetime_to_timestamp(validation.validate_valid_until(valid_until))
        signature = signing.get_viewer_url_signature(self.__account_id, self.__auth_token, identifier, valid_until_timestamp)

        return '{viewer_url}?valid_until={valid_until}&signature={signature}{wait}'.format(
            viewer_url=urls.viewer_url_for(self.__account_id, identifier),
            valid_until=valid_until_timestamp,
            signature=signature,
            wait='&wait' if wait else '',
        )

    @staticmethod
    def generate_identifier():
        # type: () -> str
        return ''.join(random.choice(_randomIdentifierCharset) for _ in range(_randomIdentifierLength))
