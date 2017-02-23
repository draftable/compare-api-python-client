from datetime import datetime
from . import timezone


_unix_epoch = datetime(1970,1,1, tzinfo=timezone.utc)


# A Python 2 compatible method for getting timestamps...

def aware_datetime_to_timestamp(dt):
    # type: (datetime) -> int
    return int((dt - _unix_epoch).total_seconds())
