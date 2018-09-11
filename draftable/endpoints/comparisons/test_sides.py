import os
from os.path import join, dirname, isfile, relpath

import pytest

from draftable.endpoints.exceptions import InvalidPath
from .sides import data_from_side, make_side, Side, FileSide, URLSide, guess_file_type_from_path

root_dir = dirname(dirname(dirname(dirname(__file__))))  # better with pathlib in Python 3.4+


def _get_test_file_path(p):
    # This would be easier with pathlib
    # return relpath(os.getcwd(), join('test-files', p))
    return join('test-files', p)


def test_file_code_guess():
    # main types
    assert guess_file_type_from_path('foo.pdf') == 'pdf'
    assert guess_file_type_from_path('foo.docx') == 'docx'
    assert guess_file_type_from_path('foo.doc') == 'doc'
    assert guess_file_type_from_path('foo.rtf') == 'rtf'
    assert guess_file_type_from_path('foo.pptx') == 'pptx'
    assert guess_file_type_from_path('foo.ppt') == 'ppt'

    # uppercase
    assert guess_file_type_from_path('foo.PDF') == 'pdf'
    assert guess_file_type_from_path('foo.DOCX') == 'docx'
    assert guess_file_type_from_path('foo.DOC') == 'doc'
    assert guess_file_type_from_path('foo.RTF') == 'rtf'
    assert guess_file_type_from_path('foo.PPTX') == 'pptx'
    assert guess_file_type_from_path('foo.PPT') == 'ppt'

    # stuff in the path
    assert guess_file_type_from_path('foo/bar.pdf') == 'pdf'
    assert guess_file_type_from_path('./foo/bar.pdf') == 'pdf'
    assert guess_file_type_from_path('../foo/bar.pdf') == 'pdf'
    assert guess_file_type_from_path('/foo/bar.pdf') == 'pdf'


def test_side_file_path():
    p = _get_test_file_path("hello.pdf")
    assert p == "test-files/hello.pdf"
    assert os.path.isfile(p)

    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, FileSide)
    assert r.file_type == "pdf"
    assert r.display_name == "hello.pdf"
    assert r.file.read() == open(p, 'rb').read()

    r = data_from_side('left', p)
    assert r['file_type'] == "pdf"
    assert r['display_name'] == "hello.pdf"


def test_side_bad_file_url():
    p = "file://server-name/" + _get_test_file_path("hello.pdf")
    assert p == "file://server-name/test-files/hello.pdf"

    with pytest.raises(InvalidPath):
        make_side(p)


def test_side_file_url():
    file_path = _get_test_file_path("hello.pdf")
    p = "file://" + root_dir + '/' + file_path

    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, FileSide)
    assert r.file_type == "pdf"
    assert r.display_name == "hello.pdf"
    assert r.file.read() == open(file_path, 'rb').read()

    r = data_from_side('left', p)
    assert r['file_type'] == "pdf"
    assert r['display_name'] == "hello.pdf"
    a, b, c = r['file']
    assert a == "left.pdf"
    assert b is not None  # an open File object
    assert c == 'application/octet-stream'


def test_side_http_url():
    p = "http://api.draftable.com/static/test-documents/code-of-conduct/left.rtf"
    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, URLSide)
    assert r.file_type == "rtf"
    assert r.display_name == "left.rtf"
    assert r.url == p

    r = data_from_side('left', p)
    assert r['file_type'] == "rtf"
    assert r['display_name'] == "left.rtf"
    assert r['source_url'] == p


def test_side_https_url():
    """Test that a URL starting with HTTPS works."""
    p = "https://api.draftable.com/static/test-documents/code-of-conduct/foo.docx"
    r = make_side(p)
    assert isinstance(r, Side)
    assert isinstance(r, URLSide)
    assert r.file_type == "docx"
    assert r.display_name == "foo.docx"
    assert r.url == p

    r = data_from_side('right', p)
    assert r['file_type'] == "docx"
    assert r['display_name'] == "foo.docx"
    assert r['source_url'] == p


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
