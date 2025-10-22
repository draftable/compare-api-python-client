#!/usr/bin/env python
"""
If you've installed the Python Draftable API then execute like:

  DR_ACCOUNT=<your-account> DR_TOKEN=<your-token> python example/simple.py

If you're running from the git repo, then execute as below (setting PYTHONPATH):

  PYTHONPATH=. DR_ACCOUNT=<your-account> DR_TOKEN=<your-token> python example/simple.py

Replace "<your-account>" and "<your-token>" with values from your Draftable
account at https://api.draftable.com/account/credentials
"""
import json
import os
import sys
import time

import draftable

# From https://api.draftable.com/account/credentials under "Account ID"
account_id = os.environ.get("DR_ACCOUNT")
auth_token = os.environ.get("DR_TOKEN")
base_url = os.environ.get("DR_BASE_URL")  # Enterprise only

if not account_id or not auth_token:
    sys.stderr.write(
        "Provide both DR_ACCOUNT and DR_TOKEN environment variables\n"
    )
    sys.stderr.write(
        'See https://api.draftable.com/account/credentials under "Account ID"\n'
    )
    sys.exit(1)

if base_url and not base_url.endswith("/v1"):
    sys.stderr.write(
        f'Value for DR_BASE_URL is "{base_url}" but must end with "/v1"\n'
    )
    sys.exit(1)

draftable_client = draftable.Client(account_id, auth_token)
comparisons = draftable_client.comparisons

change_details = comparisons.change_details("vPwyZKAU")

for change in change_details.changes:
    if change.kind != "match":
        print(f"change.kind: {change.kind}, leftText: {change.leftText}, rightText: {change.rightText}")

print(change_details.to_dict())
print(json.dumps(change_details.to_dict()))
print(json.dumps(change_details.to_dict(), ensure_ascii=False))
