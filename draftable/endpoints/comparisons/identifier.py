import random
import string

# Constants for generating random unique (with high probability) identifiers:
_RANDOM_ID_LENGTH = 12
_RANDOM_ID_CHARSET = string.ascii_letters


def generate_identifier():
    # type: () -> str
    return "".join(
        random.choice(_RANDOM_ID_CHARSET) for _ in range(_RANDOM_ID_LENGTH)  # nosec
    )
