from __future__ import absolute_import

from datetime import datetime
from .. import validation
from ...utilities.timestamp import parse_datetime

try:
    # noinspection PyUnresolvedReferences
    from typing import Optional
except ImportError:
    pass



class Export(object):
    def __init__(
        self,
        identifier,  # type: str
        comparison,  # type: str
        ready,  # type: bool
        failed,  # type: Optional[bool]
        kind,  # type: str
        url,  # type: Optional[str]
        error_message,  # type: Optional[str]
    ):
        self.__identifier = identifier
        self.__comparison = comparison
        self.__ready = ready
        self.__failed = failed
        self.__kind = validation.validate_export_kind(kind)
        self.__url = url
        self.__error_message = error_message

    @property
    def identifier(self):
        # type: () -> str
        return self.__identifier

    @property
    def comparison_identifier(self):
        # type: () -> str
        return self.__comparison

    @property
    def ready(self):
        # type: () -> bool
        return self.__ready

    @property
    def failed(self):
        # type: () -> Optional[bool]
        return self.__failed

    @property
    def kind(self):
        # type: () -> str
        return self.__kind

    @property
    def url(self):
        # type: () -> str
        return self.__url

    @property
    def error_message(self):
        # type: () -> Optional[str]
        return self.__error_message

    def __str__(self):
        # type: () -> str
        return "Export(identifier={}, comparison_identifier={}, ready={}, failed={}, kind={}, error_message={})".format(
            repr(self.identifier),
            repr(self.comparison_identifier),
            str(self.ready),
            str(self.failed),
            repr(self.kind),
            repr(self.error_message),
        )

    def __repr__(self):
        # type: () -> str
        return "Export(identifier={}, comparison_identifier={}, ready={}, failed={}, kind={}, error_message={})".format(
            repr(self.identifier),
            repr(self.comparison_identifier),
            repr(self.ready),
            repr(self.failed),
            repr(self.kind),
            repr(self.error_message),
        )

def export_from_response(data):
    # type: (dict) -> Export
    return Export(
        identifier=str(data["identifier"]),
        comparison=str(data["comparison"]),
        ready=data.get("ready"),
        failed=data.get("failed"),
        kind=data.get("kind"),
        url=str(data["url"]),
        error_message=data.get("error_message"),
    )
