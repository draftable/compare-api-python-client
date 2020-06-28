#!/usr/bin/env python
"""
If you've installed the Python Draftable API then execute like:

  DR_ACCOUNT=<your-account> DR_TOKEN=<your-token> python example/simple.py

If you're running from the git repo, then execute as below (setting PYTHONPATH):

  PYTHONPATH=. DR_ACCOUNT=<your-account> DR_TOKEN=<your-token> python example/simple.py

Replace "<your-account>" and "<your-token>" with values from your Draftable
account at https://api.draftable.com/account/credentials
"""
import os
import sys

import draftable

# From https://api.draftable.com/account/credentials under "Account ID"
account_id = os.environ.get("DR_ACCOUNT")
auth_token = os.environ.get("DR_TOKEN")
base_url = os.environ.get("DR_BASE_URL")  # Enterprise only

if not account_id or not auth_token:
    sys.stderr.write("Provide both DR_ACCOUNT and DR_TOKEN environment variables\n")
    sys.stderr.write(
        'See https://api.draftable.com/account/credentials under "Account ID"\n'
    )
    sys.exit(1)

if base_url and not base_url.endswith("/v1"):
    sys.stderr.write(
        'Value for DR_BASE_URL is "%s" but must end with "/v1"\n' % base_url
    )
    sys.exit(1)

draftable_client = draftable.Client(account_id, auth_token, base_url)
comparisons = draftable_client.comparisons

# Create a new comparison with existing sample files
comparison = comparisons.create(
    left="https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf",
    right="https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf",
    # Alternatively, be explicit about "type" (RTF, PDF, etc) and display name:
    #
    #   left=comparisons.side_from_url('https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf', 'rtf'),
    #   right=comparisons.side_from_url('https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf', 'pdf'),
)

print("Created comparison:\n  %s" % comparison)
print("  - Public URL: %s" % comparisons.public_viewer_url(comparison.identifier))
print("  - Signed URL: %s" % comparisons.signed_viewer_url(comparison.identifier))


# Alternatively, be explicit about "type" (RTF, PDF, etc) and display name:
comparison = comparisons.create(
    left=draftable.make_side(
        "https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf",
        "rtf",
    ),
    right=draftable.make_side(
        "https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf",
        "pdf",
    ),
)

print("\nCreated with make_side:\n  %s" % comparison)
print("  - Public URL: %s" % comparisons.public_viewer_url(comparison.identifier))
print("  - Signed URL: %s" % comparisons.signed_viewer_url(comparison.identifier))
