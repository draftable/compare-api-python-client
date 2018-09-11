from datetime import datetime

from . import timezone


_unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)


# A Python 2 compatible method for getting timestamps...

def aware_datetime_to_timestamp(dt):
    # type: (datetime) -> int
    return int((dt - _unix_epoch).total_seconds())


def parse_datetime(iso_format_string):
    # type: (str) -> datetime
    try:
        return datetime.strptime(iso_format_string, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError:
        # Sometimes the datetime can be missing the milliseconds, in which case the strptime call fails.
        return datetime.strptime(iso_format_string, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)