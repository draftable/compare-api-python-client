from __future__ import absolute_import

# noinspection PyUnresolvedReferences
from .client import Client, PRODUCTION_CLOUD_BASE_URL
from .endpoints.comparisons.identifier import generate_identifier
from .endpoints.comparisons.sides import make_side

__version__ = '1.1.0'

