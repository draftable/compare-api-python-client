from datetime import datetime

from ...utilities.timestamp import parse_datetime

try:
    from typing import Optional
except ImportError:
    pass


class ComparisonSide(object):
    def __init__(self, file_type, source_url, display_name):
        # type: (str, Optional[str], Optional[str]) -> None
        self.__file_type = file_type
        self.__source_url = source_url
        self.__display_name = display_name

    @property
    def file_type(self):
        # type: () -> str
        return self.__file_type

    @property
    def source_url(self):
        # type: () -> Optional[str]
        return self.__source_url

    @property
    def display_name(self):
        # type: () -> Optional[str]
        return self.__display_name

    def __str__(self):
        # type: () -> str
        source_url = ""
        if self.source_url:
            source_url = f", source_url: {self.source_url!r}"

        display_name = ""
        if self.display_name:
            display_name = f", display_name: {self.display_name!r}"

        return f"{{file_type: {self.file_type!r}{source_url}{display_name}}}"

    def __repr__(self):
        # type: () -> str
        return (
            "ComparisonSide("
            f"file_type={self.file_type!r}, "
            f"source_url={self.source_url!r}, "
            f"display_name={self.display_name!r}"
            ")"
        )


class Comparison(object):
    _DATE_FORMAT_STR = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(
        self,
        identifier,  # type: str
        left,  # type: ComparisonSide
        right,  # type: ComparisonSide
        public,  # type: bool
        creation_time,  # type: datetime
        expiry_time,  # type: Optional[datetime]
        ready,  # type: bool
        ready_time,  # type: Optional[datetime]
        failed,  # type: Optional[bool]
        error_message,  # type: Optional[str]
    ):
        self.__identifier = identifier
        self.__left = left
        self.__right = right
        self.__creation_time = creation_time
        self.__public = public
        self.__expiry_time = expiry_time
        self.__ready = ready
        self.__ready_time = ready_time
        self.__failed = failed
        self.__error_message = error_message

    @property
    def identifier(self):
        # type: () -> str
        return self.__identifier

    @property
    def left(self):
        # type: () -> ComparisonSide
        return self.__left

    @property
    def right(self):
        # type: () -> ComparisonSide
        return self.__right

    @property
    def public(self):
        # type: () -> bool
        return self.__public

    @property
    def creation_time(self):
        # type: () -> datetime
        return self.__creation_time

    @property
    def expiry_time(self):
        # type: () -> Optional[datetime]
        return self.__expiry_time

    @property
    def ready(self):
        # type: () -> bool
        return self.__ready

    @property
    def ready_time(self):
        # type: () -> Optional[datetime]
        return self.__ready_time

    @property
    def failed(self):
        # type: () -> Optional[bool]
        return self.__failed

    @property
    def error_message(self):
        # type: () -> Optional[str]
        return self.__error_message

    def __str__(self):
        # type: () -> str

        creation_time_str = self.creation_time.strftime(self._DATE_FORMAT_STR)

        expiry_time_str = None
        if self.expiry_time:
            expiry_time_str = self.expiry_time.strftime(self._DATE_FORMAT_STR)

        ready_time_str = None
        if self.ready_time:
            ready_time_str = self.ready_time.strftime(self._DATE_FORMAT_STR)

        error_message_str = None
        if self.error_message is not None:
            error_message_str = f"<{len(self.error_message)} chars>"

        return (
            "Comparison("
            f"identifier={self.identifier!r}, "
            f"left={self.left!s}, "
            f"right={self.right!s}, "
            f"public={self.public!s}, "
            f"creation_time={creation_time_str}, "
            f"expiry_time={expiry_time_str}, "
            f"ready={self.ready!s}, "
            f"ready_time={ready_time_str}, "
            f"failed={self.failed!s}, "
            f"error_message={error_message_str}"
            ")"
        )

    def __repr__(self):
        # type: () -> str
        return (
            "Comparison("
            f"identifier={self.identifier!r}, "
            f"left={self.left!r}, "
            f"right={self.right!r}, "
            f"public={self.public!r}, "
            f"creation_time={self.creation_time!r}, "
            f"expiry_time={self.expiry_time!r}, "
            f"ready={self.ready!r}, "
            f"ready_time={self.ready_time!r}, "
            f"failed={self.failed!r}, "
            f"error_message={self.error_message!r}"
            ")"
        )


def _comparison_side_from_response(side_data):
    # type: (dict) -> ComparisonSide
    return ComparisonSide(
        file_type=str(side_data["file_type"]),
        source_url=side_data.get("source_url"),
        display_name=side_data.get("display_name"),
    )


def comparison_from_response(data):
    # type: (dict) -> Comparison
    return Comparison(
        identifier=str(data["identifier"]),
        left=_comparison_side_from_response(data["left"]),
        right=_comparison_side_from_response(data["right"]),
        public=data.get("public", False),
        creation_time=parse_datetime(data["creation_time"]),
        expiry_time=parse_datetime(data["expiry_time"])
        if "expiry_time" in data
        else None,
        ready=data.get("ready"),
        ready_time=parse_datetime(data["ready_time"]) if "ready_time" in data else None,
        failed=data.get("failed"),
        error_message=data.get("error_message"),
    )
