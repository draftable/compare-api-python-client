from os.path import isfile, join
from pathlib import Path

import pytest

from draftable.endpoints.exceptions import InvalidPath

from .sides import (
    FileSide,
    Side,
    URLSide,
    data_from_side,
    guess_file_type_from_path,
    make_side,
)

root_dir = Path(__file__).parents[3]  # HACK


def _get_test_file_path(p):
    # This would be easier with pathlib
    # return relpath(os.getcwd(), join('test-files', p))
    return join("test-files", p)


def test_file_code_guess():
    # main types
    assert guess_file_type_from_path("foo.pdf") == "pdf"
    assert guess_file_type_from_path("foo.docx") == "docx"
    assert guess_file_type_from_path("foo.doc") == "doc"
    assert guess_file_type_from_path("foo.rtf") == "rtf"
    assert guess_file_type_from_path("foo.pptx") == "pptx"
    assert guess_file_type_from_path("foo.ppt") == "ppt"
    assert guess_file_type_from_path("foo.txt") == "txt"

    # uppercase
    assert guess_file_type_from_path("foo.PDF") == "pdf"
    assert guess_file_type_from_path("foo.DOCX") == "docx"
    assert guess_file_type_from_path("foo.DOC") == "doc"
    assert guess_file_type_from_path("foo.RTF") == "rtf"
    assert guess_file_type_from_path("foo.PPTX") == "pptx"
    assert guess_file_type_from_path("foo.PPT") == "ppt"
    assert guess_file_type_from_path("foo.TXT") == "txt"

    # stuff in the path
    assert guess_file_type_from_path(join("foo", "bar.pdf")) == "pdf"
    assert guess_file_type_from_path(join(".", "foo", "bar.pdf")) == "pdf"
    assert guess_file_type_from_path(join("..", "foo", "bar.pdf")) == "pdf"


def test_side_file_path():
    p = _get_test_file_path("hello.pdf")
    assert p == join("test-files", "hello.pdf")
    assert isfile(p)

    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, FileSide)
    assert r.file_type == "pdf"
    assert r.display_name == "hello.pdf"
    with open(p, "rb") as f:
        assert r.file.read() == f.read()

    r = data_from_side("left", p)
    assert r["file_type"] == "pdf"
    assert r["display_name"] == "hello.pdf"


def test_side_bad_file_url():
    p = join("file:", "server-name", _get_test_file_path("hello.pdf"))
    assert p == join("file:", "server-name", "test-files", "hello.pdf")

    with pytest.raises(InvalidPath):
        make_side(p)


def test_side_file_url():
    file_path = _get_test_file_path("hello.pdf")
    p = join("file:", root_dir, file_path)

    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, FileSide)
    assert r.file_type == "pdf"
    assert r.display_name == "hello.pdf"
    with open(file_path, "rb") as f:
        assert r.file.read() == f.read()

    r = data_from_side("left", p)
    assert r["file_type"] == "pdf"
    assert r["display_name"] == "hello.pdf"
    a, b, c = r["file"]
    assert a == "left.pdf"
    assert b is not None  # an open File object
    assert c == join("application", "octet-stream")


def test_side_http_url():
    p = "https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf"
    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, URLSide)
    assert r.file_type == "rtf"
    assert r.display_name == "left.rtf"
    assert r.url == p

    r = data_from_side("left", p)
    assert r["file_type"] == "rtf"
    assert r["display_name"] == "left.rtf"
    assert r["source_url"] == p


def test_side_https_url():
    """Test that a URL starting with HTTPS works."""
    p = "https://api.draftable.com/static/test-documents/code-of-conduct/foo.docx"
    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, URLSide)
    assert r.file_type == "docx"
    assert r.display_name == "foo.docx"
    assert r.url == p

    r = data_from_side("right", p)
    assert r["file_type"] == "docx"
    assert r["display_name"] == "foo.docx"
    assert r["source_url"] == p


def test_side_https_url_pdf_upper():
    p = "https://api.draftable.com/static/test-documents/code-of-conduct/right.PDF"
    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, URLSide)
    assert r.file_type == "pdf"
    assert r.display_name == "right.PDF"
    assert r.url == p


def test_side_https_url_query_string():
    p = "https://api.draftable.com/static/test-documents/code-of-conduct/right.docx?blah&blah"
    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, URLSide)
    assert r.file_type == "docx"
    assert r.display_name == "right.docx"
    assert r.url == p
