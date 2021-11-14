from .endpoints import ComparisonsEndpoint, ExportsEndpoint
from .transport import RESTClient
from .utilities.urls import Url

try:
    from typing import Optional
except ImportError:
    pass


PRODUCTION_CLOUD_BASE_URL = "https://api.draftable.com/v1"


class Client(object):
    def __init__(self, account_id, auth_token, base_url=None):
        # type: (str, str, Optional[str]) -> None
        self.__client = RESTClient(account_id, auth_token)
        self.__base_url = Url(base_url or PRODUCTION_CLOUD_BASE_URL)
        self.comparisons = ComparisonsEndpoint(self.__client, self.__base_url)
        self.exports = ExportsEndpoint(self.__client, self.__base_url)

    @property
    def account_id(self):
        # type: () -> str
        return self.__client.account_id

    @property
    def auth_token(self):
        # type: () -> str
        return self.__client.auth_token

    @property
    def base_url(self):
        # type: () -> str
        return str(self.__base_url)

    @property
    def verify_ssl(self):
        # type: () -> bool
        return str(self.__client.verify_ssl)

    @verify_ssl.setter
    def verify_ssl(self, v):
        # type: (bool) -> None
        self.__client.verify_ssl = v

    def __repr__(self):
        # type: () -> str
        return (
            "Client("
            f"account_id={self.account_id!r}, "
            f"auth_token={self.auth_token!r}, "
            f"base_url={self.base_url!r}"
            ")"
        )


Client.__str__ = Client.__repr__
