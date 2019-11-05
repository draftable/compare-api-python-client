# Draftable Compare API - Python Client Library

This is a thin Python 2/3 client for Draftable's [document comparison API](https://draftable.com/comparison-api).
It wraps the available endpoints, and handles authentication and signing for you.
The library is [available on PyPI](https://pypi.python.org/pypi/draftable-compare-api) as `draftable-compare-api`.

See the [full API documentation](https://api.draftable.com) for an introduction to the API, usage notes, and other references.

### Getting started

- Sign up for free at [api.draftable.com](https://api.draftable.com) to get your credentials.

- `pip install draftable-compare-api`

- Instantiate a client:
    ```
    import draftable
    account_id = "your-account-id"  # Replace with your actual credentials from:
    auth_token = "your-auth-token"  # https://api.draftable.com/account/credentials
    client = draftable.Client(account_id, auth_token)
    ```

- Create a comparison:
    ```
    comparison = comparisons.create(
        'https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf',
        'https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf',
    )

    viewer_url = comparisons.signed_viewer_url(comparison.identifier, valid_until=timedelta(minutes=30))
    
    print("Comparison created:", comparison)
    print("Viewer URL (expires in 30 min):", viewer_url)
    ```

- The same, but with more control:

    ```
    comparison = comparisons.create(
        draftable.make_side('https://api.draftable.com/static/test-documents/code-of-conduct/left.rtf', file_type='rtf'),
        draftable.make_side('https://api.draftable.com/static/test-documents/code-of-conduct/right.pdf', file_type='pdf'),
    )
    ```
-----

# Client API

### Dependencies
The API requires the pypi ``requests`` and ``six`` packages.

### Design notes

- This library should be compatible with Python 2 and Python 3. Submit a Github issue if it doesn't work with your interpreter.
- This Python library always returns "aware" `datetime` objects, and assumes that any naive `datetime` objects given to it are in *UTC* time.
- The API is designed such that _requests should always succeed_, and _comparisons should always succeed_ in production.
    - Errors in making requests will only occur upon network failure, or when you provide invalid credentials or data.
    - Comparisons will only fail when the files are unreadable, or exceed your account's size limits.

### Initializing the client

The package `draftable-compare-api` installs a single module, `draftable`, which exports a single class, `draftable.Client`.

`Client(account_id: str, auth_token: str)` will construct an API client.
At present, `Client` has a single property, `comparisons`, that yields a `ComparisonsEndpoint` that manages the comparisons for your API account.

A client is set up as follows:

    import draftable
    account_id = "your-account-id"  # Replace with your actual credentials from:
    auth_token = "your-auth-token"  # https://api.draftable.com/account/credentials
    client = draftable.Client(account_id, auth_token)

To connect to a self-hosted Draftable installation, provide the base URL as the third parameter:

    base_url = "https://draftable.example.com/api/v1"  # replace this with the correct URL
    client = draftable.Client(account_id, auth_token, base_url)
    comparisons = client.comparisons


### Getting comparisons

`ComparisonsEndpoint` provides `all()` and `get(identifier: str)`.
- `all()` returns a `list` of _all your comparisons_, ordered from newest to oldest. This is a potentially expensive operation.
- `get(identifier: str)` returns a single `Comparison` object, or raises `comparisons.NotFound` if there isn't a comparison with that identifier.

###### Comparison objects

`Comparison` objects have the following properties:
- `identifier`: a `string` giving the identifier.
- `left`, `right`: objects giving information about each side, with properties:
    - `file_type`: the file extension.
    - `source_url`  _(optional)_: if the file was specified as a URL, this will be a string with the URL. Otherwise, `None`. 
    - `display_name` _(optional)_: the display name, if one was given. Otherwise, `None`.
- `public`: a `bool` giving whether the comparison is public, or requires authentication to view.
- `creation_time`: a UTC `datetime` giving when the comparison was created.
- `expiry_time` _(optional)_: if the comparison will expire, a UTC `datetime` giving the expiry time. Otherwise, `None`.
- `ready`: `bool` indicating whether the comparison is ready for display.

If a `Comparison` is `ready` (i.e. it has been processed and is ready for display), it will have the following additional properties:
- `ready_time`: UTC `datetime` giving the time the comparison became ready.
- `failed`: `bool` indicating whether the comparison succeeded or failed.
- `error_message` _(only present if `failed`)_: a string providing the developer with the reason the comparison failed.

###### Example usage
    
    from draftable.endpoints import exceptions
    
    identifier = '<identifier>' 
    
    try:
        comparison = comparisons.get(identifier)
        
        print("Comparison '{identifier}' ({publicOrPrivate}) is {readyOrNot}.".format(
            identifier = identifier,
            publicOrPrivate = 'public' if comparison.public else 'private',
            readyOrNot = 'ready' if comparison.ready else 'not ready',
        ))
    
        if comparison.ready:
            elapsed = comparison.ready_time - comparison.creation_time
            print("The comparison took {} seconds.".format(elapsed.total_seconds()))
            
            if comparison.failed:
                print("The comparison failed. Error message:\n" + comparison.error_message)
            
    except exceptions.NotFound:
        print("Comparison '{identifier}' doesn't exist.".format(identifier=identifier))


### Deleting comparisons

`ComparisonsEndpoint` provides `delete(identifier)`, which attempts to delete the comparison with that identifier.

It has no return value, and raises `comparisons.NotFound` if there isn't a comparison with that identifier. 

###### Example usage

    oldest_comparisons = comparisons.all()[-10:]
    
    print("Deleting oldest {} comparisons...".format(len(oldest_comparisons)));
    
    for comparison in oldest_comparisons:
        comparisons.delete(comparison.identifier)
        print("Deleted comparison '{}'.".format(comparison.identifier))

### Creating comparisons

`ComparisonsEndpoint` provides `create(left, right, [identifier], [public], [expires])`, which returns a `Comparison` object representing the newly created comparison.

###### Creation options

`create` accepts the following arguments:

- `left`, `right`: objects describing the left and right files, created using either `comparisons.side_from_file` or `comparisons.side_from_url` (see below)
- `identifier` _(optional)_: the identifier to use for the comparison.
    - If specified, the identifier can't clash with an existing comparison.
    - If left unspecified, the API will automatically generate one for you.
- `public` _(optional)_: whether the comparison is publicly accessible.
    - Defaults to `false`. If `true`, then the comparison viewer can be accessed by anyone, without authentication.
    - See the full API documentation for details.
- `expires` _(optional)_: a `timedelta` or a UTC `datetime`, specifying when the comparison will be automatically deleted.
    - If given, must be a positive `timedelta`, or a UTC `datetime` in the future.
    - Defaults to `None`, meaning the comparison will never expire.

The function `comparisons.side_from_url` accepts the following arguments:
- `url`: a fully qualified URL from which Draftable will download the file.
- `file_type`: the type of the file, specified by the file extension.
    - If you provide the incorrect file type, the comparison will fail.
- `display_name` _(optional)_: a name for the file, to be shown in the comparison.

The function `comparisons.side_from_file` accepts the following arguments:
- `file`: a file object to be read and uploaded. Ensure the file is opened for reading in _binary mode_.
- `file_type`: as before.
- `display_name` _(optional)_: as before.

###### Supported file types

The following file types are supported:
- PDF: `pdf`
- Word: `docx`, `docm`, `doc`, `rtf`
- PowerPoint: `pptx`, `pptm`, `ppt`

###### Exceptions

If you provide `comparisons.side_from_file` with an invalid `file_type`, or a `file` that isn't opened in _binary mode_, it will raise `comparisons.InvalidArgument`.

If you provide `comparisons.side_from_url` with an invalid `file_type` or a badly formatted `url`, it will raise `comparisons.InvalidArgument`.

Exceptions are raised by `create` in the following cases:
- If a parameter is invalid (e.g. `expires` is set to a time in the past), it will raise `comparisons.InvalidArgument`.
- If `identifier` is already in use by another comparison, `comparisons.BadRequest` is raised.
- If the API endpoint finds your request invalid for another reason, raises `comparisons.BadRequest`.


###### Example usage

    import draftable
    identifier = draftable.generate_identifier()  # Generates a unique identifier.

    comparison = comparisons.create(
    
        identifier = identifier,
        
        left = draftable.make_side('https://domain.com/left.pdf', file_type='pdf', display_name='document.pdf'),
        right = draftable.make_side('path/to/right/file.docx', file_type='docx', display_name='document (revised).docx'),
        
        # 'public' is omitted, because we only want to let authenticated users view the comparison.

        # Comparison expires 30 minutes into the future.
        expires = timedelta(minutes=30)

    )

    print("Created comparison:", comparison);

    # This generates a signed viewer URL that can be used to access the private comparison for the next 30 minutes.
    print("Viewer URL (expires in 30 min):", comparisons.signed_viewer_url(identifier));



### Displaying comparisons

Comparisons are displayed using a _viewer URL_. See the section on displaying comparisons in the [API documentation](https://api.draftable.com) for details.

Viewer URLs are generated with the following methods:

- `comparisons.public_viewer_url(identifier: str, wait: bool = False)`
    - Viewer URL for a public comparison with the given `identifier`.
    - `wait` is `false` by default, meaning the viewer will show an error if no such comparison exists.
    - If `wait` is `true`, the viewer will wait for a comparison with the given `identifier` to exist (potentially displaying a loading animation forever).

- `comparisons.signed_viewer_url(identifier: str, valid_until: datetime | timedelta = None, wait: bool = False)`
    - Gets a signed viewer URL for a comparison with the given `identifier`. (The signature is an HMAC based on your credentials.)
    - `valid_until` gives when the URL will expire. It's specified as a UTC `datetime`, or a `timedelta`.
        - If `valid_until` is `None`, the URL defaults to expiring 30 minutes in the future (more than enough time to load the page). 
    - Again, if `wait` is `true`, the viewer will wait for a comparison with the given `identifier` to exist.


###### Example usage

Somewhere in `tasks.py`:

    # Celery task for creating a comparison.
    # This will run on a background worker.
    
    @app.task
    def upload_comparison_in_background(identifier, left_file_path, right_url):
        comparisons.create(
            identifier = identifier,
            left = draftable.make_side(left_file_path, ...),
            right = draftable.make_side(right_url, ...),
        )

Then, in `compare.py`:

    from .tasks import upload_comparison_in_background
    
    identifier = draftable.generate_identifier()
    
    # Upload our request in the background with our Celery task.
    upload_comparison_in_background.delay(identifier, ...)
    
    # At some point, we'll have created the comparison. In the mean time, we'll immediately give the user a viewer URL.
    viewer_url = comparisons.signed_viewer_url(identifier, wait=true);
    
    # This URL is valid for 30 minutes, the default amount of time.
    print("Comparison is being created. View at:", viewer_url)

The comparison viewer will display a loading animation, waiting for the comparison to be created and processed.


### Utility methods

- `draftable.generate_identifier()` generates a random unique identifier for you to use.

-----

# Other information

### Python 2 and 3 compatibility

This package officially supports the latest releases of Python 2 and 3.

At the time of writing, `Python 2.7.13`, `Python 3.5.3`, and `Python 3.6.0` are known to be supported.

-----

That's it! Please report issues you encounter, and we'll work quickly to resolve them. Contact us at [support@draftable.com](mailto://support@draftable.com) if you need assistance.
