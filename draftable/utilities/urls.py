try:
    from typing import Union
except ImportError:
    pass


class Url(object):
    """A pathlib-like object for building URLs.

    Join URLs using '/', and append query string using '+':

        >>> from draftable.endpoints.urls import Url
        >>> u = Url("http://example.com/foo")
        >>> u.full
        'http://example.com/foo'
        >>> u / "bar"
        Url('http://example.com/foo/bar')
        >>> u / "bar" / "baz.pdf"
        Url('http://example.com/foo/bar/baz.pdf')
        >>> u / "bar" / "baz.pdf" + "?t=1234"
        Url('http://example.com/foo/bar/baz.pdf?t=1234')
    """

    def __init__(self, base_url, *parts):
        # type: (Union[str, Url], str) -> None
        self.__url = str(base_url) + self.to_append(
            *parts
        )  # the str(base_url) handles the case that `base_url` is already a Url

    def __str__(self):
        """Return this URL as a string."""
        return self.__url

    def __repr__(self):
        return f"Url({self.__url!r})"

    def __truediv__(self, key):
        """Append a single path item to this URL."""
        return Url(self.__url, key)

    def __add__(self, other):
        """Add directly to the URL. Suitable for appending query strings, for example."""
        return Url(self.__url + other)

    def __iadd__(self, other):
        self.__url += other
        return self

    def to_append(self, *parts):
        """Return the string of parts, joined by '/', if there are parts, or the empty string if no parts.

        The returned string is suitable for appending to a base URL.
        """
        return ("/" + "/".join(parts)) if parts else ""

    @property
    def full(self):
        return self.__url
