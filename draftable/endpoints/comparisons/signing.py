import hashlib
import hmac
import json
from collections import OrderedDict


def get_viewer_url_signature(account_id, auth_token, identifier, valid_until_timestamp):
    # type: (str, str, str, int) -> str

    # Generate the signing policy. The usage of an OrderedDict is important to ensure
    # the fields are serialized in the correct order.
    policy = OrderedDict(
        (
            ("account_id", str(account_id)),
            ("identifier", str(identifier)),
            ("valid_until", int(valid_until_timestamp)),
        )
    )

    # Serialize the signing policy to JSON. Specifying the separators ensures removal of
    # all whitespace.
    json_policy = json.dumps(policy, separators=(",", ":"))

    # Compute a SHA-256 HMAC of the signing policy using the client's authentication
    # token as the secret key. The API expects the HMAC to be hex-encoded.
    return hmac.new(
        key=auth_token.encode("utf-8"),
        msg=json_policy.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
