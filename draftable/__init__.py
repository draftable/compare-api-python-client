from .client import PRODUCTION_CLOUD_BASE_URL, Client
from .endpoints.comparisons.identifier import generate_identifier
from .endpoints.comparisons.sides import make_side

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("draftable-compare-api")
