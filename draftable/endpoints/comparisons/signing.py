from __future__ import absolute_import

import hashlib
import hmac
import json
from collections import OrderedDict


def get_viewer_url_signature(account_id, auth_token, identifier, valid_until_timestamp):
    # type: (str, str, str, int) -> str

    # First, we generate our policy, which is an object giving the account_id and identifier of the comparison, and the valid_until time as a timestamp.
    policy = OrderedDict(
        (
            ("account_id", str(account_id)),
            ("identifier", str(identifier)),
            ("valid_until", int(valid_until_timestamp)),
        )
    )

    # Next, we convert the policy to JSON. We've used an OrderedDict so the fields will be serialized in the correct order.
    # Note that we don't have any whitespace in our JSON, achieved by specifying the separators.
    json_policy = json.dumps(policy, separators=(",", ":"))

    # Finally, we compute a SHA-256 HMAC of the JSON policy, using our auth token as the secret key.
    # The API expects it to be hex-encoded.
    return hmac.new(
        key=auth_token.encode("utf-8"),
        msg=json_policy.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
