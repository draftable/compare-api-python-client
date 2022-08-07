Draftable Compare API - Python Client Library
=============================================

[![pypi ver](https://img.shields.io/pypi/v/draftable-compare-api)](https://pypi.org/project/draftable-compare-api/)
[![pypi pyver](https://img.shields.io/pypi/pyversions/draftable-compare-api)](https://pypi.org/project/draftable-compare-api/)
[![pypi dlm](https://img.shields.io/pypi/dm/draftable-compare-api)](https://pypi.org/project/draftable-compare-api/)
[![license](https://img.shields.io/github/license/draftable/compare-api-python-client)](https://choosealicense.com/licenses/mit/)

[![travis](https://api.travis-ci.com/draftable/compare-api-python-client.svg?branch=stable)](https://app.travis-ci.com/github/draftable/compare-api-python-client)
[![codecov](https://codecov.io/gh/draftable/compare-api-python-client/branch/stable/graph/badge.svg)](https://codecov.io/gh/draftable/compare-api-python-client)
[![codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/draftable/compare-api-python-client)

A thin Python client for the [Draftable API](https://draftable.com/rest-api) which wraps all available endpoints and handles authentication and signing.

See the [full API documentation](https://api.draftable.com) for an introduction to the API, usage notes, and other reference material.

- [Requirements](#requirements)
- [Getting started](#getting-started)
- [CLI usage](#cli-usage)
- [API reference](#api-reference)
  - [Initializing the client](#initializing-the-client)
  - [Retrieving comparisons](#retrieving-comparisons)
  - [Deleting comparisons](#deleting-comparisons)
  - [Creating comparisons](#creating-comparisons)
  - [Displaying comparisons](#displaying-comparisons)
  - [Exporting comparisons](#exporting-comparisons)
  - [Utility functions](#utility-functions)
- [Other information](#other-information)
  - [Self-signed certificates](#self-signed-certificates)

Requirements
------------

- Operating system: Any maintained Linux, macOS, or Windows release
- Python runtime: Any [maintained version](https://devguide.python.org/#status-of-python-branches) (currently 3.7, 3.8, 3.9, or 3.10)

Getting started
---------------

- Create a free [API account](https://api.draftable.com)
- Retrieve your [credentials](https://api.draftable.com/account/credentials)
- Install the library

```sh
pip install draftable-compare-api
```

- Instantiate a client

```python
import draftable
client = draftable.Client('<yourAccountId>', '<yourAuthToken>')
comparisons = client.comparisons
```

- Start creating comparisons

```python
comparison = comparisons.create(
    'https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf',
    'https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf'
)
print("Comparison created: {}".format(comparison))

# Generate a signed viewer URL to access the private comparison. The expiry
# time defaults to 30 minutes if the valid_until parameter is not provided.
viewer_url = comparisons.signed_viewer_url(comparison.identifier)
print("Viewer URL (expires in 30 mins): {}".format(viewer_url))
```

CLI usage
---------

A helper utility, `dr-compare`, is included for interacting with the API from the command-line. After installing the library run `dr-compare` to view the built-in help.

The CLI tool will only be available in the environment under which the library is installed (e.g. a given *virtualenv*). To ensure it's accessible outside of any given environment install the library user or system-wide (e.g. `sudo pip install draftable-compare-api`).

API reference
-------------

- The handling of `datetime` objects is as follows:
  - Any _naive_ `datetime` objects provided in a method call are assumed to be in UTC time.
  - Returned `datetime` objects are always "_aware_" (include timezone information) and use UTC.

### Initializing the client

The package provides a module, `draftable`, which exports a class to create a `Client` for your API account.

`Client` provides a `comparisons` property which yields a `ComparisonsEndpoint` to manage the comparisons for your API account.

Creating a `Client` differs slightly based on the API endpoint being used:

```python
import draftable

# Draftable API (default endpoint)
account_id = '<yourAccountId>'  # Replace with your API credentials from:
auth_token = '<yourAuthToken>'  # https://api.draftable.com/account/credentials
client = draftable.Client(account_id, auth_token)
comparisons = client.comparisons

# Draftable API regional endpoint or Self-hosted
base_url = 'https://draftable.example.com/api/v1'  # Replace with the endpoint URL
account_id = '<yourAccountId>'  # Replace with your API credentials from the regional
auth_token = '<yourAuthToken>'  # Draftable API endpoint or your Self-hosted container
client = draftable.Client(account_id, auth_token, base_url)
comparisons = client.comparisons
```

For API Self-hosted you may need to [suppress TLS certificate validation](#self-signed-certificates) if the server is using a self-signed certificate (the default).

### Retrieving comparisons

Instances of the `ComparisonsEndpoint` class provide the following methods for retrieving comparisons:

- `all()`  
  Returns a `list` of all your comparisons, ordered from newest to oldest. This is potentially an expensive operation.
- `get(identifier: str)`  
  Returns the specified `Comparison` or raises a `NotFound` exception if the specified comparison identifier does not exist.

`Comparison` objects have the following properties:

- `identifier: str`  
  The unique identifier of the comparison
- `left: object` / `right: object`  
  Information about each side of the comparison
  - `file_type: str`  
    The file extension
  - `source_url: str` _(optional)_  
    The URL for the file if the original request was specified by URL, otherwise `None`
  - `display_name: str` _(optional)_  
    The display name for the file if given in the original request, otherwise `None`
- `public: bool`  
  Indicates if the comparison is public
- `creation_time: datetime`  
  Time in UTC when the comparison was created
- `expiry_time: datetime` _(optional)_  
  The expiry time if the comparison is set to expire, otherwise `None`
- `ready: bool`  
  Indicates if the comparison is ready to display

If a `Comparison` is _ready_ (i.e. it has been processed) it has the following additional properties:

- `ready_time: datetime`  
  Time in UTC the comparison became ready
- `failed: bool`  
  Indicates if comparison processing failed
- `error_message: str` _(only present if `failed`)_  
  Reason processing of the comparison failed

#### Example usage

```python
from draftable.endpoints import exceptions

identifier = '<identifier>'

try:
    comparison = comparisons.get(identifier)

    print("Comparison '{identifier}' ({visibility}) is {status}.".format(
        identifier = identifier,
        visibility = 'public' if comparison.public else 'private',
        status = 'ready' if comparison.ready else 'not ready'
    ))

    if comparison.ready:
        elapsed = comparison.ready_time - comparison.creation_time
        print("The comparison took {} seconds.".format(elapsed.total_seconds()))

        if comparison.failed:
            print("The comparison failed with error: {}".format(comparison.error_message))

except exceptions.NotFound:
    print("Comparison '{}' does not exist.".format(identifier))
```

### Deleting comparisons

Instances of the `ComparisonsEndpoint` class provide the following methods for deleting comparisons:

- `delete(identifier: str)`  
  Returns nothing on successfully deleting the specified comparison or raises a `NotFound` exception if no such comparison exists.

#### Example usage

```python
oldest_comparisons = comparisons.all()[-10:]
print("Deleting oldest {} comparisons ...".format(len(oldest_comparisons)))

for comparison in oldest_comparisons:
    comparisons.delete(comparison.identifier)
    print("Comparison '{}' deleted.".format(comparison.identifier))
```

### Creating comparisons

Instances of the `ComparisonsEndpoint` class provide the following methods for retrieving comparisons:

- `create(left: ComparisonSide, right: ComparisonSide, identifier: str = None, public: bool = False, expires: datetime | timedelta = None)`  
  Returns a `Comparison` representing the newly created comparison.

`create` accepts the following arguments:

- `left` / `right`  
  Describes the left and right files (see following section)
- `identifier` _(optional)_  
  Identifier to use for the comparison:
  - If specified, the identifier must be unique (i.e. not already be in use)
  - If unspecified or `None`, the API will automatically generate a unique identifier
- `public` _(optional)_  
  Specifies the comparison visibility:
  - If `False` or unspecified authentication is required to view the comparison
  - If `True` the comparison can be accessed by anyone with knowledge of the URL
- `expires` _(optional)_  
  Time at which the comparison will be deleted:
  - Must be specified as a `datetime` or a `timedelta` (UTC if naive)
  - If specified, the provided expiry time must be UTC and in the future
  - If unspecified or `None`, the comparison will never expire (but may be explicitly deleted)

The following exceptions may be raised:

- `BadRequest`  
  The request could not be processed (e.g. `identifier` already in use)
- `InvalidArgument`  
  Failure in parameter validation (e.g. `expires` is in the past)

#### Creating comparison sides

The `draftable` module provides the following static methods for creating comparison sides:

- `draftable.make_side(url_or_file_path: str, file_type: str = None, display_name: str = None)`  
  Returns a `ComparisonSide` for a file or URL by attempting to guess from the `url_or_file_path` parameter.

Alternatively, for explicitly creating a file or URL comparison side, the following static methods can be used:

- `draftable.endpoints.comparisons.sides.side_from_file(file: object, file_type: str, display_name: str = None)`  
  Returns a `ComparisonSide` for a locally accessible file.
- `draftable.endpoints.comparisons.sides.side_from_url(url: str, file_type: str, display_name: str = None)`  
  Returns a `ComparisonSide` for a remotely accessible file referenced by URL.

These methods accept the following arguments:

- `url_or_file_path` _(`make_side` only)_  
  The file or URL path for a comparison side
- `file` _(`side_from_file` only)_  
  A file object to be read and uploaded
  - The file must be opened for reading in _binary mode_
- `url` _(`side_from_url` only)_  
  The URL from which the server will download the file
- `file_type`  
  The type of file being submitted:
  - PDF: `pdf`
  - Word: `docx`, `docm`, `doc`, `rtf`
  - PowerPoint: `pptx`, `pptm`, `ppt`
  - Other: `txt`
- `display_name` _(optional)_  
  The name of the file shown in the comparison viewer

The following exceptions may be raised:

- `InvalidArgument`
  Failure in parameter validation (e.g. `file_type` is invalid, `url` is malformed, or `file` is not opened in _binary mode_)

The `make_side` method may additionally raise the following exceptions:

- `InvalidPath`  
  The provided path uses a file URI scheme (i.e. `file:`) but references a remote host or the file doesn't exist.
- `ValueError`  
  The provided path was not a URL or the file doesn't exist.

#### Example usage

```python
from datetime import timedelta

identifier = draftable.generate_identifier()

comparison = comparisons.create(
    identifier = identifier,

    left = draftable.make_side(
        'https://domain.com/left.pdf',
        file_type='pdf',
        display_name='Document.pdf'
    ),

    right = draftable.make_side(
        'path/to/right/file.docx',
        file_type='docx',
        display_name='Document (revised).docx'
    ),

    # Expire this comparison in 2 hours (default is no expiry)
    expires = timedelta(hours=2)
)
print("Created comparison: {}".format(comparison))
```

### Displaying comparisons

Instances of the `ComparisonsEndpoint` class provide the following methods for displaying comparisons:

- `public_viewer_url(identifier: str, wait: bool = False)`  
  Generates a public viewer URL for the specified comparison
- `signed_viewer_url(identifier: str, valid_until: datetime | timedelta = None, wait: bool = False)`  
  Generates a signed viewer URL for the specified comparison

Both methods use the following common parameters:

- `identifier`  
  Identifier of the comparison for which to generate a _viewer URL_
- `wait` _(optional)_  
  Specifies the behaviour of the viewer if the provided comparison does not exist
  - If `False` or unspecified, the viewer will show an error if the `identifier` does not exist
  - If `True`, the viewer will wait for a comparison with the provided `identifier` to exist  
    Note this will result in a perpetual loading animation if the `identifier` is never created

The `signed_viewer_url` method also supports the following parameters:

- `valid_until` _(optional)_  
  Time at which the URL will expire (no longer load)
  - Must be specified as a `datetime` or a `timedelta`
  - If specified, the provided expiry time must be UTC and in the future
  - If unspecified or `None`, the URL will be generated with the default 30 minute expiry

See the displaying comparisons section in the [API documentation](https://api.draftable.com) for additional details.

#### Example usage

```python
identifier = '<identifier>'

# Retrieve a signed viewer URL which is valid for 1 hour. The viewer will wait
# for the comparison to exist in the event processing has not yet completed.
viewer_url = comparisons.signed_viewer_url(identifier, timedelta(hours=1), wait=True)
print("Viewer URL (expires in 1 hour): {}".format(viewer_url))
```

### Exporting comparisons

To perform comparison exports retrieve an `ExportsEndpoint` instance via the `exports` property of your `Client` instance:

```python
exports = client.exports
```

#### Creating comparison exports

Instances of the `ExportsEndpoint` class provide the following methods for exporting comparisons:

- `create(comparison: Union[Comparison, str], kind: str = 'single_page')`  
  Returns a `Export` representing the newly created export.

`create` accepts the following arguments:

- `comparison`  
  The comparison to export provided as a `Comparison` instance or a comparison identifier
- `kind`  
  The type of export to perfom (see below)

The following export kinds are supported for the `kind` parameter:

- `single_page`  
  Exports only the right-side of the comparison with highlights and deletion markers
- `combined`  
  Exports both the left and right sides
- `left`  
  Export the left side only
- `right`  
  Exports the right side only

##### Example usage

```python
exports = client.exports

export = exports.create(comparison, kind='single_page')
```

#### Retrieving comparison exports

Instances of the `ExportsEndpoint` class provide the following methods for retrieving exports:

- `get(identifier: str)`  
  Returns the specified `Export` or raises a `NotFound` exception if the specified export identifier does not exist.

`Export` objects have the same properties as `Comparison` objects.

As with comparison requests, export requests need to be processed. Typically processing only takes a few seconds, but this can vary based on numerous factors (e.g. size of the documents being exported, number of changes in the comparison, etc ...). To determine if an export has been processed the `ready` property of the `Export` instance should be inspected and polling can be utilised to wait until the export has been completed.

##### Example usage

```python
import time

export = client.exports.create(comparison.identifier)

while not export.ready:
    time.sleep(1)
    export = client.exports.get(export.identifier)
    if export.ready:
        print(export.url)
```

### Utility functions

The `draftable` module provides the following static methods for generating comparison identifiers:

- `draftable.generate_identifier()`  
  Generates a random unique comparison identifier

Other information
-----------------

### Self-signed certificates

If connecting to an API Self-hosted endpoint which is using a self-signed certificate (the default) you will need to suppress certificate validation. This can be done by setting the `CURL_CA_BUNDLE` environment variable to an empty string. On Windows, this must be done from within the Python interpreter due to platform limitations.

See the below examples for different operating systems and shell environments. Note that all examples only set the variable for the running shell or Python interpreter and it will not persist. To persist the setting consult the documentation for your shell environment. This should be done with caution as this setting suppresses certificate validation for **all** connections made by the Python runtime!

#### Non-Windows environments (inc. WSL)

(ba)sh (Linux, macOS, WSL)

```sh
export CURL_CA_BUNDLE=0
```

PowerShell:

```posh
$env:CURL_CA_BUNDLE=0
```

#### Windows environments

Setting an environment variable to the empty string is not valid in Windows and is treated as equivalent to removing any existing environment variable of the same name. As such, suppressing certificate validation requires an alternate approach. The most straightforward is to set the environment variable from within Python, instead of before launch.

```python
import os

os.environ['CURL_CA_BUNDLE'] = ''
```

If your code spawns Python subprocesses they must separately modify their environment as the change will not be inherited as you'd normally expect.

#### All environments

Disabling certificate validation in production environments is strongly discouraged as it significantly lowers security. We only recommend setting this environment variable in development environments if configuring a CA signed certificate for API Self-hosted is not possible.
