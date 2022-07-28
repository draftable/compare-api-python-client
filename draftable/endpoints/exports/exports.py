from ...transport import RESTClient
from ...utilities import Url
from ..comparisons.comparison import Comparison
from ..exceptions import handle_request_exception
from ..validation import validate_export_kind, validate_identifier
from .export import Export, export_from_response

try:
    from typing import Optional, Union
except ImportError:
    pass


class ExportsEndpoint(object):
    def __init__(self, client, base_url):
        # type: (RESTClient, Url) -> None
        self.__url = base_url / "exports"
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
    def get(self, identifier):
        # type: (str) -> Export
        identifier = validate_identifier(identifier)
        return export_from_response(self.__client.get(self.__url / identifier))

    @handle_request_exception
    def create(self, comparison, kind="single_page", include_cover_page=False):
        # type: (Union[str, Comparison], Optional[str], Optional[bool]) -> Export
        """Creates a new export with the Draftable API.

        :param comparison: comparison object to be exported, or the identifier of a comparison.
        :param comparison: as for "left".
        :return: the newly created export
        """
        if isinstance(comparison, str):
            comparison_identifier = validate_identifier(comparison)
        elif isinstance(comparison, Comparison):
            comparison_identifier = comparison.identifier
        else:
            raise TypeError(
                "Comparison must either be a comparison identifier or Comparison object"
            )

        kind = validate_export_kind(kind)
        data = {
            "comparison": comparison_identifier,
            "kind": kind,
            "include_cover_page": include_cover_page,
        }
        return export_from_response(self.__client.post(self.__url, data))
