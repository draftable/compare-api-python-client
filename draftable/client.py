from __future__ import absolute_import

from .endpoints import ComparisonsEndpoint


class Client(object):
    def __init__(self, account_id, auth_token):
        # type: (str, str) -> None
        self.__account_id = str(account_id)
        self.__auth_token = str(auth_token)

    @property
    def account_id(self):
        # type: () -> str
        return self.__account_id

    @property
    def auth_token(self):
        # type: () -> str
        return self.__auth_token

    @property
    def comparisons(self):
        # type: () -> ComparisonsEndpoint
        return ComparisonsEndpoint(self.account_id, self.auth_token)

    def __str__(self):
        # type: () -> str
        return 'Client(account_id={}, auth_token={})'.format(repr(self.account_id), repr(self.auth_token))

    def __repr__(self):
        # type: () -> str
        return 'Client(account_id={}, auth_token={})'.format(repr(self.account_id), repr(self.auth_token))
