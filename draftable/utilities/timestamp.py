from datetime import datetime, timezone


def aware_datetime_to_timestamp(dt):  # pylint: disable=invalid-name
    # type: (datetime) -> int
    return int(dt.timestamp())


def parse_datetime(iso_format_string):
    # type: (str) -> datetime
    try:
        return datetime.strptime(iso_format_string, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        # Sometimes the datetime can be missing the microseconds
        return datetime.strptime(iso_format_string, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
