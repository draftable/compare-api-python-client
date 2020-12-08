from datetime import timedelta

from draftable import PRODUCTION_CLOUD_BASE_URL, Client
from draftable.endpoints.comparisons import signing
from draftable.endpoints.validation import validate_valid_until
from draftable.utilities import aware_datetime_to_timestamp


def test_basic_client_with_default_base_url():
    c = Client("a", "b")
    assert c.account_id == "a"
    assert c.auth_token == "b"
    assert c.base_url == PRODUCTION_CLOUD_BASE_URL


def test_basic_client_with_onprem_base_url():
    c = Client("aa", "bb", "https://draftable.corp.co/api/api/v1")
    assert c.account_id == "aa"
    assert c.auth_token == "bb"
    assert c.base_url == "https://draftable.corp.co/api/api/v1"


def test_comparison_viewer_url():
    """Test that URL generation works correctly.

    The "public" URL, i.e. without expiry and signature, has this form:
        <base_url>comparisons/viewer/<account>/<identifier>

    Where base_url is like this (not must end in '/v1' with no trailing slash):
        <scheme>://<host:port><prefix>/v1/

    e.g.:
        http://api.localhost:9123/v1/comparisons/viewer/RiWmsc-test/nVymKCCn

    The "limited" URL, i.e. has a signed expiry time, has this form:
        <base_url>comparisons/viewer/<account>/<identifier>?valid_until=<unix-epoch-time>&signature=<signature>

    """
    base_url = "https://dr.corp.co/api/v1"
    account_id = "aa"
    auth_token = "bb"
    identifier = "abc"

    c = Client(account_id, auth_token, base_url)

    assert c.comparisons.public_viewer_url(
        identifier
    ) == base_url + "/comparisons/viewer/%s/%s" % (account_id, identifier)
    assert c.comparisons.public_viewer_url(
        identifier, wait=True
    ) == base_url + "/comparisons/viewer/%s/%s?wait" % (account_id, identifier)

    when = validate_valid_until(timedelta(minutes=5))
    expires = aware_datetime_to_timestamp(when)
    signature = signing.get_viewer_url_signature(
        account_id, auth_token, identifier, expires
    )
    expected = base_url + "/comparisons/viewer/%s/%s?valid_until=%s&signature=%s" % (
        account_id,
        identifier,
        expires,
        signature,
    )

    assert c.comparisons.signed_viewer_url(identifier, when) == expected
    assert (
        c.comparisons.signed_viewer_url(identifier, when, wait=True)
        == expected + "&wait"
    )
