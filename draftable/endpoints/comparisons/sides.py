from os.path import basename, isfile, join, splitext

# urllib3 is a required dependency of requests
from urllib3.util import parse_url

from .. import validation
from ..exceptions import InvalidArgument, InvalidPath

try:
    from typing import Any, Optional, Union
except ImportError:
    pass


class Side(object):
    def __init__(self, file_type, display_name=None):
        # type: (str, Optional[str]) -> None
        self.__file_type = validation.validate_file_type(file_type)
        self.__display_name = None if display_name is None else str(display_name)

    @property
    def file_type(self):
        # type: () -> str
        return self.__file_type

    @property
    def display_name(self):
        # type: () -> Optional[str]
        return self.__display_name


class FileSide(Side):
    def __init__(self, file, file_type, display_name=None):
        # type: (Any, str, Optional[str]) -> None
        self.__file = validation.validate_file(file)
        super().__init__(file_type=file_type, display_name=display_name)

    @property
    def file(self):
        # type: () -> Any
        return self.__file

    def __str__(self):
        return f"File side: {self.__file} ({self.file_type}, '{self.display_name}')"


class URLSide(Side):
    def __init__(self, url, file_type, display_name=None):
        # type: (str, str, Optional[str]) -> None
        self.__url = validation.validate_url(url)
        super().__init__(file_type=file_type, display_name=display_name)

    @property
    def url(self):
        # type: () -> str
        return self.__url

    def __str__(self):
        return f"URL side: {self.__url} ({self.file_type}, '{self.display_name}')"


def data_from_side(side_name, side):
    # type: (str, Union[str, FileSide, URLSide]) -> dict
    """Given a side (which may be a string or Side object, return the data needed
    for a comparison POST request as a dictionary.
    """

    if isinstance(side, str):
        # User has provided a file path or URL.
        side = make_side(side)

    data = {
        "file_type": side.file_type,
    }

    if side.display_name:
        data["display_name"] = side.display_name
    if isinstance(side, URLSide):
        data["source_url"] = side.url
    else:
        assert isinstance(side, FileSide)
        data["file"] = (
            f"{side_name}.{side.file_type}",
            side.file,
            join("application", "octet-stream"),
        )
    return data


def side_from_url(url, file_type, display_name=None):
    # type: (str, str, Optional[str]) -> URLSide
    return URLSide(url, file_type, display_name)


def side_from_file(file_obj, file_type, display_name=None):
    # type: (Any, str, Optional[str]) -> FileSide
    return FileSide(file_obj, file_type, display_name)


def side_from_file_path(file_path, file_type=None, display_name=None):
    should_guess = file_type is None or file_type == "guess"
    if should_guess:
        file_type = guess_file_type_from_path(file_path)
    display_name = display_name or basename(file_path)

    # TODO: make sure this closes the file handle
    return FileSide(open(file_path, "rb"), file_type, display_name)


def make_side(url_or_file_path, file_type=None, display_name=None):
    # type: (str, Optional[str], Optional[str]) -> Side
    """
    Parsing the URL or file path and looking for the file extension is "ok"
    but works only based on human conventions. The more industrial strength
    approach is to read the beginning of the file or URL and determine the
    type unambiguously from the content.

    :param url_or_file_path: a URL or file path to compare.
    :param file_type: a string like "pdf", "docx", etc, or "guess" (or None) to detect.
    :return: a Side object
    """
    guess_type = file_type is None or file_type == "guess"

    if url_or_file_path.startswith("http"):
        url = parse_url(
            url_or_file_path
        )  # parse to get the path component on its own, without query string
        if guess_type:
            file_type = guess_file_type_from_path(url.path)
            if not file_type:
                raise InvalidArgument(
                    "file_type",
                    "Unable to infer file type from URL. `file_type` must be specified. This may require "
                    "passing a URLSide to comparisons.create rather than a string.",
                )
        display_name = display_name or basename(url.path)
        return URLSide(url.url, file_type, display_name)

    if url_or_file_path.startswith("file:"):
        url = parse_url(url_or_file_path)
        if url.host:
            raise InvalidPath(
                f"File url '{url_or_file_path}' must be local only, and not contain host name ('{url.host}')"
            )

        if not isfile(url.path):
            raise InvalidPath(
                f"File url '{url_or_file_path}' refers to file '{url.path}' but no such file exists"
            )

        return side_from_file_path(url.path, file_type, display_name)

    if isfile(url_or_file_path):
        return side_from_file_path(url_or_file_path, file_type, display_name)

    raise ValueError(
        f"Path is not a URL and not a file that exists: {url_or_file_path}"
    )


def guess_file_type_from_path(path):
    _, file_type = splitext(path)
    return file_type.strip(".").lower()


def guess_file_type_from_url(url):
    url = parse_url(
        url
    )  # parse to get the path component on its own, without query string
    file_type = guess_file_type_from_path(url.path)
    return file_type
