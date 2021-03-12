# wschor, Spring 2021
"""
This file contains some utility functions. You should **not** modify this file.
"""

import json
import base64

def print_bytes(b):
    """
    A helper function to print bytes as base64.
    """
    print(base64.b64encode(b).decode('utf-8'))

def bytes_to_b64(b):
    """
    A helper function that gives a base64 string representation of bytes
    """
    return base64.b64encode(b).decode()

def b64_to_bytes(b64):
    """
    A helper function that returns the bytes given by base64 string
    """
    return base64.b64decode(b64)

def __detect_tags(s):
    return s[:3] == "^^^" and s[-3:] == "$$$"

def _prepare_bytes(o):
    """
    A helper funtion for obj_to_bytes
    """
    if isinstance(o, dict):
        result = {}
        for key, value in o.items():
            if isinstance(key, bytes):

                key = "^^^" + bytes_to_b64(key) + "$$$"
            if isinstance(value, bytes):
                value = "^^^" + bytes_to_b64(value) + "$$$"
            elif isinstance(value, dict) or isinstance(value, list):
                value = _prepare_bytes(value)
            result[key] = value
        return result

    if isinstance(o, list):
        result = []
        for item in o:
            if isinstance(item, bytes):
                item = "^^^" + bytes_to_b64(item) + "$$$"
            elif isinstance(item, dict) or isinstance(item, list):
                item = _prepare_bytes(item)
            result.append(item)
        return result

    if isinstance(o, bytes):
        return "^^^" + bytes_to_b64(o) + "$$$"

    elif isinstance(o, (int, str, float, bool)) or o is None:
        return o
    else:
        print(f"ERROR: Unserializable type {type(o)} detected! Valid types are [dict, list, int, str, float, bool, NoneType]")
        raise ValueError

def _repair_bytes(o):
    """
    A helper funtion for obj_to_bytes
    """
    if isinstance(o, dict):
        result = {}
        for key, value in o.items():
            if isinstance(key, str):
                if __detect_tags(key):
                    key = b64_to_bytes(key[3:-3])
            if isinstance(value, str):
                if __detect_tags(value):
                    value = b64_to_bytes(value[3:-3])

            elif isinstance(value, dict) or isinstance(value, list):
                value = _repair_bytes(value)
            result[key] = value
        return result

    if isinstance(o, list):
        result = []
        for item in o:
            if isinstance(item, str):
                if __detect_tags(item):
                    item = b64_to_bytes(item[3:-3])
            elif isinstance(item, dict) or isinstance(item, list):
                item = _repair_bytes(item)
            result.append(item)
        return result

    if isinstance(o, str):
        if __detect_tags(o):
            return b64_to_bytes(o[3:-3])
        else:
            return o

    elif isinstance(o, (int, str, float, bool)) or o is None:
        return o
    else:
        print(f"ERROR: Undeserializable type {type(o)} detected! Valid types are [dict, list, int, str, float, bool, NoneType]")
        raise ValueError

def obj_to_bytes(o):
    """
    A helper function that will serialize objects to bytes using JSON.
    It can serialize arbitrary nestings of lists and dictionaries containing ints, floats, booleans, strs, Nones, and bytes.

    A note on bytes and strings:
    This function encodes all bytes as base64 strings in order to be json compliant.
    The complimentary function, bytes_to_obj, will decode everything it detects to be a base64 string
    back to bytes. If you store a base64 formatted string, it would also be decoded to bytes.

    To alleviate this, the base64 string are prefixed with "^^^" and suffixed with "$$$", and the function
    checks for those tags instead.

    In the (unlikely) event you store a string with this format it will be decoded to bytes!
    """
    o = _prepare_bytes(o)
    return json.dumps(o).encode()

def bytes_to_obj(b):
    """
    A helper function that will deserialize bytes to an object using JSON. See caveats in obj_to_bytes().
    """
    obj = json.loads(b.decode())
    return _repair_bytes(obj)



## Custom Exceptions
class DropboxError(Exception):
    def __init__(self, msg='DROPBOX ERROR', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
