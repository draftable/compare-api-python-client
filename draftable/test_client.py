import datetime
import os
from datetime import timedelta

import pytest
import requests

from draftable import PRODUCTION_CLOUD_BASE_URL, Client, generate_identifier, make_side
from draftable.endpoints.comparisons import signing
from draftable.endpoints.validation import validate_valid_until
from draftable.utilities import aware_datetime_to_timestamp


@pytest.fixture
def client():
    return Client(
        os.environ["DRAFTABLE_TEST_ACCOUNT_ID"], os.environ["DRAFTABLE_TEST_AUTH_TOKEN"]
    )


@pytest.fixture
def comparisons(client):
    return client.comparisons


@pytest.fixture
def exports(client):
    return client.exports


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

    assert (
        c.comparisons.public_viewer_url(identifier)
        == f"{base_url}/comparisons/viewer/{account_id}/{identifier}"
    )
    assert (
        c.comparisons.public_viewer_url(identifier, wait=True)
        == f"{base_url}/comparisons/viewer/{account_id}/{identifier}?wait"
    )

    when = validate_valid_until(timedelta(minutes=5))
    expires = aware_datetime_to_timestamp(when)

    signature = signing.get_viewer_url_signature(
        account_id, auth_token, identifier, expires
    )

    expected = (
        f"{base_url}/comparisons/viewer/{account_id}/{identifier}"
        f"?valid_until={expires}&signature={signature}"
    )

    assert c.comparisons.signed_viewer_url(identifier, when) == expected
    assert (
        c.comparisons.signed_viewer_url(identifier, when, wait=True)
        == f"{expected}&wait"
    )


def test_comparison_list(comparisons):
    comparisons.all()


def test_create_retrieve_export_delete(comparisons, exports):
    comparison = comparisons.create(
        left="https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf",
        right="https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf",
    )
    assert not comparison.ready, "We do not expect the comparison to be ready yet"
    assert not comparison.failed

    while True:
        comparison = comparisons.get(comparison.identifier)
        if comparison.ready:
            assert not comparison.failed
            break

    export = exports.create(comparison)
    while True:
        export = exports.get(export.identifier)
        if export.ready:
            assert not export.failed
            response = requests.get(export.url)
            assert response.ok
            break

    comparisons.delete(comparison.identifier)


def test_create_from_files(comparisons, exports):
    comparison = comparisons.create(
        left="test-files/hello.pdf",
        right="test-files/hello.pdf",
        expires=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    assert not comparison.failed


def test_create_from_files_txt(comparisons, exports):
    comparison = comparisons.create(
        left="test-files/hello-left.txt",
        right="test-files/hello-right.txt",
        expires=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    assert not comparison.failed


def test_create_with_sides(comparisons, exports):
    comparison = comparisons.create(
        left=make_side(
            "test-files/hello.pdf", file_type="pdf", display_name="Hello.pdf"
        ),
        right=make_side(
            "https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf",
            file_type="pdf",
            display_name="Right.pdf",
        ),
        identifier=generate_identifier(),
        expires=timedelta(hours=1),
    )
    assert not comparison.failed


def test_create_retrieve_export_coverpage(comparisons, exports):
    comparison = comparisons.create(
        left="test-files/hello-left.txt",
        right="test-files/hello-right.txt",
        expires=datetime.datetime.now() + datetime.timedelta(days=1),
    )
    assert not comparison.ready, "We do not expect the comparison to be ready yet"
    assert not comparison.failed

    while True:
        comparison = comparisons.get(comparison.identifier)
        if comparison.ready:
            assert not comparison.failed
            break

    export = exports.create(comparison, kind="combined", include_cover_page=True)
    while True:
        export = exports.get(export.identifier)
        if export.ready:
            assert not export.failed
            response = requests.get(export.url)
            assert response.ok
            break

    comparisons.delete(comparison.identifier)
