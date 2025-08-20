import json
from .changes import Change, DeletionMark, ChangeDetails


class TestDeletionMarkSerialization:
    """Test that DeletionMark objects are properly serialized in Change.to_dict()"""

    def test_deletion_mark_serialization(self):
        """Test that DeletionMark objects are properly serialized in Change.to_dict()"""

        # Create test data with a DeletionMark
        change_data = {
            "kind": "deletion",
            "leftText": "Some deleted text",
            "rightText": None,
            "leftRegion": None,
            "rightRegion": None,
            "stylesInfo": None,
            "deletionMark": {"pageIndex": 1, "point": [100, 200]},
        }

        # Create Change object
        change = Change(change_data)

        # Convert to dict (this should not raise a TypeError)
        result_dict = change.to_dict()

        # Verify the result can be JSON serialized
        json_str = json.dumps(result_dict)

        # Verify the structure is correct
        assert result_dict["deletionMark"]["pageIndex"] == 1
        assert result_dict["deletionMark"]["point"] == [100, 200]

        # Verify we can round-trip through JSON
        parsed_back = json.loads(json_str)
        assert parsed_back["deletionMark"]["pageIndex"] == 1
        assert parsed_back["deletionMark"]["point"] == [100, 200]

    def test_deletion_mark_none(self):
        """Test that None deletionMark is handled correctly"""

        change_data = {
            "kind": "insertion",
            "leftText": None,
            "rightText": "Some new text",
            "leftRegion": None,
            "rightRegion": None,
            "stylesInfo": None,
            "deletionMark": None,
        }

        change = Change(change_data)
        result_dict = change.to_dict()

        # Should be serializable and deletionMark should be None
        json.dumps(result_dict)
        assert result_dict["deletionMark"] is None

    def test_deletion_mark_missing(self):
        """Test that missing deletionMark is handled correctly"""

        change_data = {
            "kind": "modification",
            "leftText": "Old text",
            "rightText": "New text",
            "leftRegion": None,
            "rightRegion": None,
            "stylesInfo": None,
            # deletionMark is missing entirely
        }

        change = Change(change_data)
        result_dict = change.to_dict()

        # Should be serializable and deletionMark should be None
        json.dumps(result_dict)
        assert result_dict["deletionMark"] is None

    def test_change_details_with_deletion_marks(self):
        """Test that Changes with DeletionMarks can be serialized"""

        change_details_data = {
            "changes": [
                {
                    "kind": "deletion",
                    "leftText": "Deleted text",
                    "rightText": None,
                    "deletionMark": {"pageIndex": 0, "point": [50, 100]},
                },
                {
                    "kind": "insertion",
                    "leftText": None,
                    "rightText": "Added text",
                    "deletionMark": None,
                },
            ],
            "summary": {"anyChanges": True},
        }

        # Create ChangeDetails object
        change_details = ChangeDetails(change_details_data)

        # Convert to dict (this should not raise a TypeError)
        result_dict = change_details.to_dict()

        # Verify the result can be JSON serialized
        json.dumps(result_dict)

        # Verify structure is correct
        assert len(result_dict["changes"]) == 2
        assert result_dict["changes"][0]["deletionMark"]["pageIndex"] == 0
        assert result_dict["changes"][0]["deletionMark"]["point"] == [50, 100]
        assert result_dict["changes"][1]["deletionMark"] is None

    def test_deletion_mark_direct_serialization(self):
        """Test that DeletionMark objects can be directly serialized"""

        deletion_mark_data = {"pageIndex": 2, "point": [150, 250]}

        deletion_mark = DeletionMark(deletion_mark_data)

        # Test to_dict method
        result_dict = deletion_mark.to_dict()
        assert result_dict["pageIndex"] == 2
        assert result_dict["point"] == [150, 250]

        # Test JSON serialization
        json_str = json.dumps(result_dict)
        parsed_back = json.loads(json_str)
        assert parsed_back["pageIndex"] == 2
        assert parsed_back["point"] == [150, 250]

    def test_change_with_complex_nested_data(self):
        """Test serialization of Change with multiple nested objects including DeletionMark"""

        change_data = {
            "kind": "replacement",
            "leftText": "Old text",
            "rightText": "New text",
            "leftRegion": {
                "pageIndex": 0,
                "rectangles": [{"left": 10, "top": 20, "right": 100, "bottom": 50}],
            },
            "rightRegion": {
                "pageIndex": 0,
                "rectangles": [{"left": 10, "top": 20, "right": 120, "bottom": 50}],
            },
            "stylesInfo": {
                "leftStyles": [{"color": "red", "font": "Arial", "size": 12}],
                "rightStyles": [{"color": "blue", "font": "Arial", "size": 12}],
                "leftStyleMap": "style1",
                "rightStyleMap": "style2",
            },
            "deletionMark": {"pageIndex": 0, "point": [75, 35]},
        }

        change = Change(change_data)
        result_dict = change.to_dict()

        # Should be fully serializable
        json.dumps(result_dict)

        # Verify all nested structures are properly serialized
        assert result_dict["deletionMark"]["pageIndex"] == 0
        assert result_dict["deletionMark"]["point"] == [75, 35]
        assert result_dict["leftRegion"]["pageIndex"] == 0
        assert len(result_dict["leftRegion"]["rectangles"]) == 1
        assert result_dict["stylesInfo"]["leftStyleMap"] == "style1"

    def test_nonascii_serialization(self):
        """Test that non-ASCII characters are properly serialized in str(Change)"""

        # Create test data with a DeletionMark
        change_data = {
            "kind": "replacement",
            "leftText": "café",
            "rightText": "áéíóú",
            "leftRegion": None,
            "rightRegion": None,
            "stylesInfo": None,
        }

        # Create Change object
        changes = ChangeDetails({"changes": [change_data]})

        # Verify the result can be JSON serialized
        json_str = str(changes)
        
        assert "café" in json_str
        assert "áéíóú" in json_str
                            