import requests

from ..utilities import Url

try:
    from typing import Any, Optional, Tuple, Union
except ImportError:
    pass


def _is_file(obj):
    # type: (Any) -> bool
    # This is how the requests library checks.
    return hasattr(obj, "__iter__") and not isinstance(obj, (str, list, tuple, dict))


def _is_file_tuple(obj):
    # type: (Any) -> bool
    return isinstance(obj, tuple) and any(map(_is_file, obj))


def _data_contains_file(data):
    # type: (Any) -> bool
    if isinstance(data, (list, tuple)):
        return any(map(_data_contains_file, data))

    if isinstance(data, dict):
        return any(map(_data_contains_file, data.values()))

    return _is_file(data)


# Flattens our nested form data, e.g. "right: {file_type: ...}" becomes "right.file_type = ...".
# Additionally, separates plain data from file objects.
# This lets us support uploading files "nested" in a subkey, by setting the key to e.g. "left.file".
# At least, Django Rest Framework is happy to receive data in this format.
def _flatten_form_data(initial_data):
    # type: (dict) -> Tuple[dict, dict]
    data = {}
    files = {}

    for key, value in initial_data.items():
        if isinstance(value, dict):
            flattened_data, flattened_files = _flatten_form_data(value)
            for sub_key, sub_value in flattened_data.items():
                data[f"{key}.{sub_key}"] = sub_value
            for sub_key, sub_file in flattened_files.items():
                files[f"{key}.{sub_key}"] = sub_file
        else:
            if _is_file(value) or _is_file_tuple(value):
                files[key] = value
            else:
                data[key] = value

    return data, files


class RESTClient(object):
    def __init__(self, account_id, auth_token):
        # type: (str, str) -> None
        self.__account_id = account_id
        self.__auth_token = auth_token
        self.verify_ssl = True

    @property
    def account_id(self):
        # type: () -> str
        return self.__account_id

    @property
    def auth_token(self):
        # type: () -> str
        return self.__auth_token

    def __auth(self, r):
        r.headers["Authorization"] = f"Token {self.__auth_token}"
        return r

    def get(self, url, parameters=None):
        # type: (Union[str, Url], Optional[dict]) -> Union[dict, list]
        response = requests.get(
            url, auth=self.__auth, params=parameters, verify=self.verify_ssl
        )
        response.raise_for_status()
        return response.json()

    def post(self, url, data):
        # type: (str, dict) -> Union[dict, list]
        if not _data_contains_file(data):
            response = requests.post(
                url, auth=self.__auth, json=data, verify=self.verify_ssl
            )
        else:
            data, files = _flatten_form_data(data)
            # Obscure issue:
            # When the request is bad (e.g. invalid authentication), requests throws a weird ConnectionError rather than a HTTPError. Only in this multipart case!
            # (It seems that when the request is bad, our API (via Django Rest Framework) may not wait for the full upload?)
            # Asking for JSON seems to help? But it fails with frequency ~30% when you give invalid credentials.
            # I don't have a good fix for this (yet!), so there's a note in the exception thrown in the weird case. ~ James (April 2017)
            response = requests.post(
                url,
                auth=self.__auth,
                data=data,
                files=files,
                headers={"Accept": "application/json"},
                verify=self.verify_ssl,
            )

        response.raise_for_status()
        return response.json()

    def delete(self, url):
        # type: (str) -> None
        response = requests.delete(url, auth=self.__auth, verify=self.verify_ssl)
        response.raise_for_status()
