import random
import string

# Constants for generating random unique (with high probability) identifiers:
_randomIdentifierLength = 12
_randomIdentifierCharset = string.ascii_letters


def generate_identifier():
    # type: () -> str
    return ''.join(random.choice(_randomIdentifierCharset) for _ in range(_randomIdentifierLength))
