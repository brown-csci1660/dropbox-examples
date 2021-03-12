# wschor, Spring 2021
"""
This file contains the dataserver API as well as the UUID memloc API. You should **not** modify this file.
"""

import uuid


class Memloc:
    """
    Implementation of client side memory location management using UUID.
    """
    def Make(self):
        """
        Get random memloc.

        Params: None
        Returns: memloc (bytes)
        """
        return uuid.uuid4().bytes


    def MakeFromBytes(self, bytes16):
        """
        Get specific memloc from 16 byte input

        Params: 16 bytes to convert to memloc
        Returns: memloc (bytes)
        """
        return uuid.UUID(bytes=bytes16).bytes


class Dataserver:
    """
    Dataserver implementation.
    """
    def __init__(self):
        self.data = {}



    def _validate(self, memloc):
        """
        Validates the format of a memloc. Not to be used externally.
        """
        if (not isinstance(memloc, bytes)) or (not len(memloc) == 16):
            print("ERROR: Memloc must be 16 bytes")
            raise Exception("InvalidMemloc")


    def Set(self, memloc, val):
        """
        Stores a value at a memory location.

        Params:
            > memloc - hex string, len 32
            > val    - bytes

        Returns: None
        """
        self._validate(memloc)
        if not isinstance(val, bytes):
            print(
                f"ERROR: Datasever can only store raw bytes! You gave val of type {type(val)}. Please serialize to bytes."
            )
            raise ValueError

        self.data[memloc] = val



    def Get(self, memloc):
        """
        Retrieves a value from a memory location.

        Params:
            > memloc - hex string, len 32

        Returns: (value, err) where err is not None and value is None if memloc is not being used.
        """
        self._validate(memloc)
        if memloc in self.data:
            return self.data[memloc], None
        else:
            return None, "ValDoesNotExist"


# tests and usage examples
if __name__ == "__main__":
    ml = Memloc()

    loc1 = ml.Make()
    print("random memloc:", loc1)

    loc2 = ml.MakeFromBytes(b"0000000000000000")
    print("Specific memloc in hex:", loc2)

    ds = Dataserver()

    ds.Set(loc1, "Here is some data".encode())
    ds.Set(loc2, "Here is some more data".encode())

    loc1_data, err = ds.Get(loc1)
    assert loc1_data.decode() == "Here is some data" and err is None

    loc2_data, err = ds.Get(loc2)
    assert loc2_data.decode() == "Here is some more data" and err is None

    print("-------------------")
    print("error testing:")
    try:
        ds.Set("invalid memloc", "valid data".encode())
    except Exception as e:
        print("exception raised correctly!\n")

    try:
        ds.Set(loc1, "invalid data")
    except Exception as e:
        print("exception raised correctly!\n")
