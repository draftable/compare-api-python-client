import json

try:
    from typing import Any, Dict, List, Optional, Tuple  # noqa F401
except ImportError:
    pass


# Rectangle class
class Rectangle(object):
    def __init__(self, data: Dict[str, Any]):
        self.__left: Optional[float] = data.get("left", None)
        self.__top: Optional[float] = data.get("top", None)
        self.__right: Optional[float] = data.get("right", None)
        self.__bottom: Optional[float] = data.get("bottom", None)

    @property
    def left(self):
        # type: () -> Optional[float]
        return self.__left

    @property
    def top(self):
        # type: () -> Optional[float]
        return self.__top

    @property
    def right(self):
        # type: () -> Optional[float]
        return self.__right

    @property
    def bottom(self):
        # type: () -> Optional[float]
        return self.__bottom

    def __repr__(self):
        return (
            "Rectangle("
            f"{self.__left}, "
            f"{self.__top}, "
            f"{self.__right}, "
            f"{self.__bottom})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# Region class
class Region(object):
    def __init__(self, data: Dict[str, Any]):
        self.__pageIndex: Optional[int] = data.get("pageIndex", None)
        self.__rectangles: List[Optional[Rectangle]] = (
            [Rectangle(rect) for rect in data["rectangles"]]
            if "rectangles" in data
            else []
        )

    @property
    def pageIndex(self):
        # type: () -> Optional[int]
        return self.__pageIndex

    @property
    def rectangles(self):
        # type: () -> List[Optional[Rectangle]]
        return self.__rectangles

    def __repr__(self):
        return "Region(" f"{self.__pageIndex}, " f"{self.__rectangles})"

    def __str__(self):
        return json.dumps(self.__dict__)


# Style class
class Style(object):
    def __init__(self, data: Dict[str, Any]):
        self.__color: Optional[str] = data.get("color", None)
        self.__font: Optional[str] = data.get("font", None)
        self.__emphasis: Optional[str] = data.get("emphasis", None)
        self.__size: Optional[int] = data.get("size", None)

    @property
    def color(self):
        # type: () -> Optional[str]
        return self.__color

    @property
    def font(self):
        # type: () -> Optional[str]
        return self.__font

    @property
    def emphasis(self):
        # type: () -> Optional[str]
        return self.__emphasis

    @property
    def size(self):
        # type: () -> Optional[int]
        return self.__size

    def __repr__(self):
        return (
            "Style("
            f"{self.__color}, "
            f"{self.__font}, "
            f"{self.__emphasis}, "
            f"{self.__size})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# StylesInfo class
class StylesInfo(object):
    def __init__(self, data: Dict[str, Any]):
        self.__leftStyles: List[Optional[Style]] = (
            [Style(style) for style in data["leftStyles"]]
            if "leftStyles" in data
            else []
        )
        self.__rightStyles: List[Optional[Style]] = (
            [Style(style) for style in data["rightStyles"]]
            if "rightStyles" in data
            else []
        )
        self.__leftStyleMap: Optional[str] = data.get("leftStyleMap", None)
        self.__rightStyleMap: Optional[str] = data.get("rightStyleMap", None)

    @property
    def leftStyles(self):
        # type: () -> List[Optional[Style]]
        return self.__leftStyles

    @property
    def rightStyles(self):
        # type: () -> List[Optional[Style]]
        return self.__rightStyles

    @property
    def leftStyleMap(self):
        # type: () -> Optional[str]
        return self.__leftStyleMap

    @property
    def rightStyleMap(self):
        # type: () -> Optional[str]
        return self.__rightStyleMap

    def __repr__(self):
        return (
            "StylesInfo("
            f"{self.__leftStyles}, "
            f"{self.__rightStyles}, "
            f"{self.__leftStyleMap}, "
            f"{self.__rightStyleMap})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# Change class
class Change(object):
    def __init__(self, data: Dict[str, Any]):
        self.__kind: Optional[str] = data.get("kind", None)
        self.__leftText: Optional[str] = data.get("leftText", None)
        self.__rightText: Optional[str] = data.get("rightText", None)
        self.__leftRegion: Optional[Region] = (
            Region(data["leftRegion"]) if "leftRegion" in data else None
        )
        self.__rightRegion: Optional[Region] = (
            Region(data["rightRegion"]) if "rightRegion" in data else None
        )
        self.__stylesInfo: Optional[StylesInfo] = (
            StylesInfo(data["stylesInfo"]) if "stylesInfo" in data else None
        )
        deletion = data.get("deletionMark")
        self.__deletionMark = (
            (
                deletion.get("pageIndex", None),
                tuple(deletion.get("point", None)),
            )
            if deletion
            else None
        )

    @property
    def kind(self):
        # type: () -> Optional[str]
        return self.__kind

    @property
    def leftText(self):
        # type: () -> Optional[str]
        return self.__leftText

    @property
    def rightText(self):
        # type: () -> Optional[str]
        return self.__rightText

    @property
    def leftRegion(self):
        # type: () -> Optional[Region]
        return self.__leftRegion

    @property
    def rightRegion(self):
        # type: () -> Optional[Region]
        return self.__rightRegion

    @property
    def stylesInfo(self):
        # type: () -> Optional[StylesInfo]
        return self.__stylesInfo

    @property
    def deletionMark(self):
        # type: () -> Optional[Tuple[int, Tuple[int, int]]]
        return self.__deletionMark

    def __repr__(self):
        return (
            "Change("
            f"{self.__kind}, "
            f"{self.__leftText}, "
            f"{self.__rightText}, "
            f"{self.__leftRegion}, "
            f"{self.__rightRegion}, "
            f"{self.__stylesInfo}, "
            f"{self.__deletionMark})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# DocumentSummary class
class DocumentSummary(object):
    def __init__(self, data: Dict[str, Any]):
        self.__pageCount: Optional[int] = data.get("pageCount", None)
        self.__characterCount: Optional[int] = data.get("characterCount", None)
        self.__wordCount: Optional[int] = data.get("wordCount", None)

    @property
    def pageCount(self):
        # type: () -> Optional[int]
        return self.__pageCount

    @property
    def characterCount(self):
        # type: () -> Optional[int]
        return self.__characterCount

    @property
    def wordCount(self):
        # type: () -> Optional[int]
        return self.__wordCount

    def __repr__(self):
        return (
            "DocumentSummary("
            f"{self.__pageCount}, "
            f"{self.__characterCount}, "
            f"{self.__wordCount})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# ChangeSummary class
class ChangeSummary(object):
    def __init__(self, data: Dict[str, Any]):
        self.__matches: Optional[int] = data.get("matches", None)
        self.__deletions: Optional[int] = data.get("deletions", None)
        self.__insertions: Optional[int] = data.get("insertions", None)
        self.__replacements: Optional[int] = data.get("replacements", None)
        self.__matchingWords: Optional[int] = data.get("matchingWords", None)
        self.__deletedLeftWords: Optional[int] = data.get(
            "deletedLeftWords", None
        )
        self.__replacedLeftWords: Optional[int] = data.get(
            "replacedLeftWords", None
        )
        self.__insertedRightWords: Optional[int] = data.get(
            "insertedRightWords", None
        )
        self.__replacedRightWords: Optional[int] = data.get(
            "replacedRightWords", None
        )

    @property
    def matches(self):
        # type: () -> Optional[int]
        return self.__matches

    @property
    def deletions(self):
        # type: () -> Optional[int]
        return self.__deletions

    @property
    def insertions(self):
        # type: () -> Optional[int]
        return self.__insertions

    @property
    def replacements(self):
        # type: () -> Optional[int]
        return self.__replacements

    @property
    def matchingWords(self):
        # type: () -> Optional[int]
        return self.__matchingWords

    @property
    def deletedLeftWords(self):
        # type: () -> Optional[int]
        return self.__deletedLeftWords

    @property
    def replacedLeftWords(self):
        # type: () -> Optional[int]
        return self.__replacedLeftWords

    @property
    def insertedRightWords(self):
        # type: () -> Optional[int]
        return self.__insertedRightWords

    @property
    def replacedRightWords(self):
        # type: () -> Optional[int]
        return self.__replacedRightWords

    def __repr__(self):
        return (
            "ChangeSummary("
            f"{self.__matches}, "
            f"{self.__deletions}, "
            f"{self.__insertions}, "
            f"{self.__replacements}, "
            f"{self.__matchingWords}, "
            f"{self.__deletedLeftWords}, "
            f"{self.__replacedLeftWords}, "
            f"{self.__insertedRightWords}, "
            f"{self.__replacedRightWords})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# Summary class
class Summary(object):
    def __init__(self, data: Dict[str, Any]):
        self.__anyChanges: Optional[bool] = data.get("anyChanges", None)
        self.__anyMatches: Optional[bool] = data.get("anyMatches", None)
        self.__changeSummary: Optional[ChangeSummary] = (
            ChangeSummary(data["changeSummary"])
            if "changeSummary" in data
            else None
        )
        self.__leftDocumentSummary: Optional[DocumentSummary] = (
            DocumentSummary(
                data["leftDocumentSummary"]
                if "leftDocumentSummary" in data
                else None
            )
        )
        self.__rightDocumentSummary: Optional[DocumentSummary] = (
            DocumentSummary(
                data["rightDocumentSummary"]
                if "rightDocumentSummary" in data
                else None
            )
        )

    @property
    def anyChanges(self):
        # type: () -> Optional[bool]
        return self.__anyChanges

    @property
    def anyMatches(self):
        # type: () -> Optional[bool]
        return self.__anyMatches

    @property
    def changeSummary(self):
        # type: () -> Optional[ChangeSummary]
        return self.__changeSummary

    @property
    def leftDocumentSummary(self):
        # type: () -> Optional[DocumentSummary]
        return self.__leftDocumentSummary

    @property
    def rightDocumentSummary(self):
        # type: () -> Optional[DocumentSummary]
        return self.__rightDocumentSummary

    def __repr__(self):
        return (
            "Summary("
            f"{self.__anyChanges}, "
            f"{self.__anyMatches}, "
            f"{self.__changeSummary}, "
            f"{self.__leftDocumentSummary}, "
            f"{self.__rightDocumentSummary})"
        )

    def __str__(self):
        return json.dumps(self.__dict__)


# Root class representing the entire data structure
class ChangeDetails(object):

    def __init__(self, data: Dict[str, Any]):
        self.__changes: List[Optional[Change]] = (
            [Change(change) for change in data["changes"]]
            if "changes" in data
            else []
        )
        self.__summary: Optional[Summary] = (
            Summary(data["summary"]) if "summary" in data else None
        )

    @property
    def changes(self):
        # type: () -> Optional[List[Change]]
        return self.__changes

    @property
    def summary(self):
        # type: () -> Optional[Summary]
        return self.__summary

    def __repr__(self):
        return f"ChangeDetails({self.__changes}, {self.__summary})"

    def __str__(self):
        return json.dumps(self.__dict__)


def change_details_from_response(data):
    # type: (dict) -> ChangeDetails
    return ChangeDetails(data)
