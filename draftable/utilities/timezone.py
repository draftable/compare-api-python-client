from __future__ import absolute_import

try:
    # noinspection PyUnresolvedReferences
    from datetime import timezone

    utc = timezone.utc

except ImportError:

    # If we're in python 2, we need to implement our own tzinfo class in order to make datetimes be aware...

    from datetime import timedelta, tzinfo

    ZERO = timedelta(0)

    # A UTC class.

    class UTC(tzinfo):
        """UTC"""

        def utcoffset(self, dt):
            return ZERO

        def tzname(self, dt):
            return "UTC"

        def dst(self, dt):
            return ZERO

    utc = UTC()
