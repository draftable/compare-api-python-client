from __future__ import absolute_import

from ..urls import api_base_url


comparisons_url = '{base}/comparisons'.format(base=api_base_url)


def comparison_url_for(identifier):
    # type: (str) -> str
    return '{comparisons}/{identifier}'.format(comparisons=comparisons_url, identifier=identifier)


def viewer_url_for(account_id, identifier):
    # type: (str, str) -> str
    return '{comparisons}/viewer/{account_id}/{identifier}'.format(comparisons=comparisons_url, account_id=account_id, identifier=identifier)
