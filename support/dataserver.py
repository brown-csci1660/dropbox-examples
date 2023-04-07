##
## dataserver.py - Dataserver Implementation
##
## This file contains the dataserver and memloc API.
##
## WARNING:  DO NOT MODIFY THIS FILE.  This file will be replaced
## with a different version in the autograder, so your changes will be
## overwritten.
##



import uuid

class Memloc:
    """
    Implementation of client side memory location management using UUID.
    """
    def Make(self) -> bytes:
        """
        Get random memloc.

        Params: None
        Returns: memloc (bytes)
        """
        return uuid.uuid4().bytes

    def MakeFromBytes(self, bytes16: bytes) -> bytes:
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
        self.data = {}  # type: dict[bytes, bytes]

    def _validate(self, memloc: bytes) -> None:
        """
        Validates the format of a memloc. Not to be used externally.
        """
        if (not isinstance(memloc, bytes)) or (not len(memloc) == 16):
            print("ERROR: Memloc must be a bytes() object of size 16 bytes")
            raise Exception("InvalidMemloc")

    def Set(self, memloc: bytes, val: bytes) -> None:
        """
        Stores a value at a memory location.

        Params:
            > memloc - bytes (16 bytes)
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

    def Get(self, memloc: bytes) -> bytes:
        """
        Retrieves a value from a memory location.

        Params:
            > memloc - bytes (16 bytes)

        Returns: val or raises ValueError
        """
        self._validate(memloc)
        if memloc in self.data:
            return self.data[memloc]
        else:
            raise ValueError("ValDoesNotExist")

    def Delete(self, memloc: bytes) -> None:
        """
        Delete a value from a memory location.

        Params:
            > memloc - bytes (16)

        Returns: None or raises ValueError
        """
        self._validate(memloc)
        if memloc in self.data:
            del self.data[memloc]
        else:
            raise ValueError("ValDoesNotExist")

    ##################################################################
    # NOTE: the following functions are provided for testing ONLY--you
    # can use them to test functionality or attacks, but you should
    # not use them in your client Implementation (ie, from client.py).
    ##################################################################

    def GetMap(self) -> dict:
        """
        Return the entire server contents as a dictionary.  You can


        Params: None
        Returns: dict
        """
        return self.data

    def Clear(self):
        """
        Delete the entire server contents
        """
        self.data = {}

dataserver = Dataserver()
memloc = Memloc()

# Here are some example usages and tests
if __name__ == "__main__":

    loc1 = memloc.Make()
    print("random memloc:", loc1)

    loc2 = memloc.MakeFromBytes(b"0000000000000000")
    print("Specific memloc in hex:", loc2)

    dataserver.Set(loc1, "Here is some data".encode())
    dataserver.Set(loc2, "Here is some more data".encode())

    loc1_data = dataserver.Get(loc1)
    assert loc1_data.decode() == "Here is some data"

    loc2_data = dataserver.Get(loc2)
    assert loc2_data.decode() == "Here is some more data"

    print("-------------------")
    print("error testing:")
    try:
        dataserver.Set("invalid memloc", "valid data".encode())
    except Exception as e:
        print("exception raised correctly!\n")

    try:
        dataserver.Set(loc1, "invalid data")
    except Exception as e:
        print("exception raised correctly!\n")
