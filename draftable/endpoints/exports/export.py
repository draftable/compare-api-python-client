from .. import validation

try:
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
        include_cover_page,  # type: Optional[bool]
    ):
        self.__identifier = identifier
        self.__comparison = comparison
        self.__ready = ready
        self.__failed = failed
        self.__kind = validation.validate_export_kind(kind)
        self.__url = url
        self.__error_message = error_message
        self.__include_cover_page = include_cover_page

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

    @property
    def include_cover_page(self):
        # type: () -> Optional[bool]
        return self.__include_cover_page

    def __str__(self):
        # type: () -> str
        return (
            "Export("
            f"identifier={self.identifier!r}, "
            f"comparison_identifier={self.comparison_identifier!r}, "
            f"ready={self.ready!s}, "
            f"failed={self.failed!s}, "
            f"kind={self.kind!r}, "
            f"error_message={self.error_message!r}, "
            f"include_cover_page={self.include_cover_page!r}"
            ")"
        )

    def __repr__(self):
        # type: () -> str
        return (
            "Export("
            f"identifier={self.identifier!r}, "
            f"comparison_identifier={self.comparison_identifier!r}, "
            f"ready={self.ready!r}, "
            f"failed={self.failed!r}, "
            f"kind={self.kind!r}, "
            f"error_message={self.error_message!r}, "
            f"include_cover_page={self.include_cover_page!r}"
            ")"
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
        include_cover_page=data.get("include_cover_page"),
    )
