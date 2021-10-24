from .urls import Url


def test_basic_1():
    any_base_url = "https://api.test.com/v1"
    u = Url(any_base_url)
    assert str(u) == any_base_url
    assert str(u / "comparisons") == any_base_url + "/comparisons"
    assert str(u / "comparisons/1234") == any_base_url + "/comparisons/1234"
    assert str(u / "comparisons" / "1234") == any_base_url + "/comparisons/1234"

    # same but via `full`
    assert u.full == any_base_url
    assert (u / "comparisons").full == any_base_url + "/comparisons"


def test_basic_2():
    u = Url("")
    assert str(u) == ""
    assert str(u / "comparisons") == "/comparisons"
    assert str(u / "comparisons/1234") == "/comparisons/1234"
    assert str(u / "comparisons" / "1234") == "/comparisons/1234"


def test_plus_equals():
    base = "http://foo.bar"
    u = Url(base)
    assert str(u) == base
    assert str(u / "baz") == base + "/baz"

    assert str(u + "?blah") == base + "?blah"
    u += "?blob"
    assert str(u) == base + "?blob"

    u = Url(base) / "foo" + "?blob"
    assert str(u) == base + "/foo?blob"

    u = Url(base) / "foo" / "bar" + "?blob"
    assert str(u) == base + "/foo/bar?blob"
