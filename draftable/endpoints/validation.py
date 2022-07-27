from datetime import datetime, timedelta, timezone

import requests

from draftable.endpoints.exceptions import InvalidArgument

try:
    from typing import Any, Union
except ImportError:
    pass

_valid_identifier_characters = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._"
)

_MIN_ID_LENGTH = 1
_MAX_ID_LENGTH = 1024

_allowed_file_types = {
    # PDFs
    "pdf",
    # Word documents
    "docx",
    "docm",
    "doc",
    "rtf",
    # PowerPoint presentations
    "pptx",
    "pptm",
    "ppt",
    # Other
    "txt",
}

_allowed_kinds = ("single_page", "combined", "left", "right")


def validate_identifier(identifier):
    # type: (str) -> str
    if not identifier:
        raise InvalidArgument("identifier", "`identifier` cannot be empty.")
    if not isinstance(identifier, str):
        raise InvalidArgument(
            "identifier", "`identifier` must be a string (of type `str`)."
        )
    if not _MIN_ID_LENGTH <= len(identifier) <= _MAX_ID_LENGTH:
        raise InvalidArgument(
            "identifier",
            f"`identifier` must be between {_MIN_ID_LENGTH} and {_MAX_ID_LENGTH} characters long.",
        )
    if not all(c in _valid_identifier_characters for c in identifier):
        raise InvalidArgument(
            "identifier",
            '`identifier` must only contain ASCII letters, numbers, and the characters "-._".',
        )
    return identifier


def validate_file_type(file_type):
    # type: (str) -> str
    if not file_type:
        raise InvalidArgument("file_type", "`file_type` cannot be empty.")
    munged_file_type = str(file_type).lower()
    if munged_file_type not in _allowed_file_types:
        raise InvalidArgument("file_type", f'"{file_type}" is not a valid file type')
    return munged_file_type


def validate_file(file):
    # type: (Any) -> Any
    if not file:
        raise InvalidArgument("file", "`file` must be specified.")
    if any(not hasattr(file, attr) for attr in ("mode", "read")):
        raise InvalidArgument(
            "file",
            "the given object doesn't appear to be a file - it's missing properties a file object should have.",
        )
    if hasattr(file, "readable") and not file.readable():
        raise InvalidArgument("file", "`file.readable()` is False.")
    if "b" not in file.mode:
        raise InvalidArgument(
            "file",
            f"the given file doesn't appear to be open in binary mode. It's mode is '{file.mode}'.",
        )
    return file


def validate_url(url):
    # type: (str) -> str
    if not url:
        raise InvalidArgument("url", "`url` cannot be empty.")
    if not isinstance(url, str):
        raise InvalidArgument("url", "`url` must be a string (of type `str`).")
    if len(url) > 2048:
        raise InvalidArgument("url", "`url` must be no longer than 2048 characters.")
    try:
        scheme, netloc, _, _, _, _ = requests.utils.urlparse(url)
    except Exception as ex:
        wrapper = InvalidArgument("url", "the value could not be parsed as a URL.")
        wrapper.__cause__ = ex
        raise wrapper
    if scheme not in ("http", "https"):
        raise InvalidArgument("url", '`url` must have "http" or "https" as its scheme.')
    if not netloc:
        raise InvalidArgument("url", "the given URL is malformed.")
    return url


def _validate_datetime_or_timedelta(parameter_name, value):
    # type: (str, Union[datetime, timedelta]) -> datetime
    if isinstance(value, timedelta):
        if value.total_seconds() <= 0:
            raise InvalidArgument(
                parameter_name,
                f"if a timedelta, `{parameter_name}` must be positive, but it was zero or negative.",
            )
        return datetime.now(tz=timezone.utc) + value

    if not isinstance(value, datetime):
        raise InvalidArgument(
            parameter_name, f"`{parameter_name}` must be a datetime or a timedelta."
        )
    # Make the datetime aware, with UTC as its timezone. If it was naive, we assume it was in UTC time.
    if value.utcoffset() is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    # Now we can safely check if it's in the future.
    if value < datetime.now(tz=timezone.utc):
        raise InvalidArgument(
            parameter_name, f"`{parameter_name}` must be in the future."
        )

    return value


def validate_expires(expires):
    # type: (Union[datetime, timedelta]) -> datetime
    return _validate_datetime_or_timedelta("expires", expires)


def validate_valid_until(valid_until):
    # type: (Union[datetime, timedelta]) -> datetime
    return _validate_datetime_or_timedelta("valid_until", valid_until)


def validate_export_kind(kind):
    # type: (str) -> str
    if not kind:
        raise InvalidArgument("kind", "`kind` cannot be empty.")
    munged_kind = str(kind).lower()
    if munged_kind not in _allowed_kinds:
        raise InvalidArgument("kind", f'"{kind}" is not a valid file type')
    return munged_kind
