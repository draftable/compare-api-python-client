import json
from typing import Any, Dict, List, Optional, Tuple


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

    def to_dict(self):
        return {
            "left": self.__left,
            "top": self.__top,
            "right": self.__right,
            "bottom": self.__bottom,
        }

    def __repr__(self):
        return (
            "Rectangle("
            f"left={self.__left}, "
            f"top={self.__top}, "
            f"right={self.__right}, "
            f"bottom={self.__bottom})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return self.to_dict() == other.to_dict()
        return False


# Region class
class Region(object):
    def __init__(self, data: Dict[str, Any]):
        self.__pageIndex: Optional[int] = data.get("pageIndex", None)
        self.__rectangles: List[Optional[Rectangle]] = (
            [Rectangle(rect) for rect in data["rectangles"]]
            if "rectangles" in data and data["rectangles"] is not None
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

    def to_dict(self):
        return {
            "pageIndex": self.__pageIndex,
            "rectangles": [rect.to_dict() for rect in self.__rectangles],
        }

    def __repr__(self):
        return (
            "Region("
            f"pageIndex={self.__pageIndex}, "
            f"rectangles={self.__rectangles})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, Region):
            return self.to_dict() == other.to_dict()
        return False


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

    def to_dict(self):
        return {
            "color": self.__color,
            "font": self.__font,
            "emphasis": self.__emphasis,
            "size": self.__size,
        }

    def __repr__(self):
        return (
            "Style("
            f"color={self.__color}, "
            f"font={self.__font}, "
            f"emphasis={self.__emphasis}, "
            f"size={self.__size})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, Style):
            return self.to_dict() == other.to_dict()
        return False


# StylesInfo class
class StylesInfo(object):
    def __init__(self, data: Dict[str, Any]):
        self.__leftStyles: List[Optional[Style]] = (
            [Style(style) for style in data["leftStyles"]]
            if "leftStyles" in data and data["leftStyles"] is not None
            else []
        )
        self.__rightStyles: List[Optional[Style]] = (
            [Style(style) for style in data["rightStyles"]]
            if "rightStyles" in data and data["rightStyles"] is not None
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

    def to_dict(self):
        return {
            "leftStyles": [style.to_dict() for style in self.__leftStyles],
            "rightStyles": [style.to_dict() for style in self.__rightStyles],
            "leftStyleMap": self.__leftStyleMap,
            "rightStyleMap": self.__rightStyleMap,
        }

    def __repr__(self):
        return (
            "StylesInfo("
            f"leftStyles={self.__leftStyles}, "
            f"rightStyles={self.__rightStyles}, "
            f"leftStyleMap={self.__leftStyleMap}, "
            f"rightStyleMap={self.__rightStyleMap})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, StylesInfo):
            return self.to_dict() == other.to_dict()
        return False


# Deletion mark class
class DeletionMark(object):
    def __init__(self, data: Dict[str, Any]):
        self.__pageIndex: Optional[int] = data.get("pageIndex", None)
        self.__point: Optional[Tuple[int, int]] = data.get("point", None)

    @property
    def pageIndex(self):
        # type: () -> Optional[int]
        return self.__pageIndex

    @property
    def point(self):
        # type: () -> Optional[Tuple[int, int]]
        return self.__point

    def to_dict(self):
        return {"pageIndex": self.__pageIndex, "point": self.__point}

    def __repr__(self):
        return (
            "DeletionMark("
            f"pageIndex={self.__pageIndex}, "
            f"point={self.__point})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, DeletionMark):
            return self.to_dict() == other.to_dict()
        return False


# Change class
class Change(object):
    def __init__(self, data: Dict[str, Any]):
        self.__kind: Optional[str] = data.get("kind", None)
        self.__leftText: Optional[str] = data.get("leftText", None)
        self.__rightText: Optional[str] = data.get("rightText", None)
        self.__leftRegion: Optional[Region] = (
            Region(data["leftRegion"])
            if "leftRegion" in data and data["leftRegion"] is not None
            else None
        )
        self.__rightRegion: Optional[Region] = (
            Region(data["rightRegion"])
            if "rightRegion" in data and data["rightRegion"] is not None
            else None
        )
        self.__stylesInfo: Optional[StylesInfo] = (
            StylesInfo(data["stylesInfo"])
            if "stylesInfo" in data and data["stylesInfo"] is not None
            else None
        )
        self.__deletionMark = (
            DeletionMark(data.get("deletionMark"))
            if "deletionMark" in data and data["deletionMark"] is not None
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

    def to_dict(self):
        return {
            "kind": self.__kind,
            "leftText": self.__leftText,
            "rightText": self.__rightText,
            "leftRegion": (
                self.__leftRegion.to_dict() if self.__leftRegion else None
            ),
            "rightRegion": (
                self.__rightRegion.to_dict() if self.__rightRegion else None
            ),
            "stylesInfo": (
                self.__stylesInfo.to_dict() if self.__stylesInfo else None
            ),
            "deletionMark": (
                self.__deletionMark.to_dict() if self.__deletionMark else None
            ),
        }

    def __repr__(self):
        return (
            "Change("
            f"kind={self.__kind}, "
            f"leftText={self.__leftText}, "
            f"rightText={self.__rightText}, "
            f"leftRegion={self.__leftRegion}, "
            f"rightRegion={self.__rightRegion}, "
            f"stylesInfo={self.__stylesInfo}, "
            f"deletionMark={self.__deletionMark})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, Change):
            return self.to_dict() == other.to_dict()
        return False


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

    def to_dict(self):
        return {
            "pageCount": self.__pageCount,
            "characterCount": self.__characterCount,
            "wordCount": self.__wordCount,
        }

    def __repr__(self):
        return (
            "DocumentSummary("
            f"pageCount={self.__pageCount}, "
            f"characterCount={self.__characterCount}, "
            f"wordCount={self.__wordCount})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, DocumentSummary):
            return self.to_dict() == other.to_dict()
        return False


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

    def to_dict(self):
        return {
            "matches": self.__matches,
            "deletions": self.__deletions,
            "insertions": self.__insertions,
            "replacements": self.__replacements,
            "matchingWords": self.__matchingWords,
            "deletedLeftWords": self.__deletedLeftWords,
            "replacedLeftWords": self.__replacedLeftWords,
            "insertedRightWords": self.__insertedRightWords,
            "replacedRightWords": self.__replacedRightWords,
        }

    def __repr__(self):
        return (
            "ChangeSummary("
            f"matches={self.__matches}, "
            f"deletions={self.__deletions}, "
            f"insertions={self.__insertions}, "
            f"replacements={self.__replacements}, "
            f"matchingWords={self.__matchingWords}, "
            f"deletedLeftWords={self.__deletedLeftWords}, "
            f"replacedLeftWords={self.__replacedLeftWords}, "
            f"insertedRightWords={self.__insertedRightWords}, "
            f"replacedRightWords={self.__replacedRightWords})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, ChangeSummary):
            return self.to_dict() == other.to_dict()
        return False


# Summary class
class Summary(object):
    def __init__(self, data: Dict[str, Any]):
        self.__anyChanges: Optional[bool] = data.get("anyChanges", None)
        self.__anyMatches: Optional[bool] = data.get("anyMatches", None)
        self.__changeSummary: Optional[ChangeSummary] = (
            ChangeSummary(data["changeSummary"])
            if "changeSummary" in data and data["changeSummary"] is not None
            else None
        )
        self.__leftDocumentSummary: Optional[DocumentSummary] = (
            DocumentSummary(data["leftDocumentSummary"])
            if "leftDocumentSummary" in data
            and data["leftDocumentSummary"] is not None
            else None
        )
        self.__rightDocumentSummary: Optional[DocumentSummary] = (
            DocumentSummary(data["rightDocumentSummary"])
            if "rightDocumentSummary" in data
            and data["rightDocumentSummary"] is not None
            else None
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

    def to_dict(self):
        return {"anyChanges": self.__anyChanges}

    def __repr__(self):
        return (
            "Summary("
            f"anyChanges={self.__anyChanges}, "
            f"anyMatches={self.__anyMatches}, "
            f"changeSummary={self.__changeSummary}, "
            f"leftDocumentSummary={self.__leftDocumentSummary}, "
            f"rightDocumentSummary={self.__rightDocumentSummary})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, Summary):
            return self.to_dict() == other.to_dict()
        return False


# Root class representing the entire data structure
class ChangeDetails(object):

    def __init__(self, data: Dict[str, Any]):
        self.__changes: List[Optional[Change]] = (
            [Change(change) for change in data["changes"]]
            if "changes" in data and data["changes"] is not None
            else []
        )
        self.__summary: Optional[Summary] = (
            Summary(data["summary"])
            if "summary" in data and data["summary"] is not None
            else None
        )

    @property
    def changes(self):
        # type: () -> Optional[List[Change]]
        return self.__changes

    @property
    def summary(self):
        # type: () -> Optional[Summary]
        return self.__summary

    def to_dict(self):
        return {
            "changes": [change.to_dict() for change in self.__changes],
            "summary": (self.__summary.to_dict() if self.__summary else None),
        }

    def __repr__(self):
        return (
            "ChangeDetails("
            f"changes={self.__changes}, "
            f"summary={self.__summary})"
        )

    def __str__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if isinstance(other, ChangeDetails):
            return self.to_dict() == other.to_dict()
        return False


def change_details_from_response(data):
    # type: (dict) -> ChangeDetails
    return ChangeDetails(data)
