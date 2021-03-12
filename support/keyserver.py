# wschor, Spring 2021
"""
This file contains the Keyserver API. You should **not** modify this file.
"""

from .crypto import AsmPublicKey

class Keyserver:
    """
    Keyserver implementation.
    """
    def __init__(self):
        self.data = {}

    def _validate(self, String, pk=None):
        """
        Validates inputs. Not to be used externally.
        """
        if not isinstance(String, str):
            print(f"ERROR: Keyserver tags must be strings, not {type(String)}")
            raise ValueError
        if pk:
            if not isinstance(pk, AsmPublicKey):
                print(
                    f"ERROR: Keyserver keys must of type asmPublicKey, not {type(pk)}"
                )
                raise ValueError


    def Set(self, String, pk):
        """
        Stores pubkey at a string.

        Params:
            > String - str
            > pk     - AsmPublicKey

        Returns: err, which is None iff Set succeeded
        """
        self._validate(String, pk=pk)
        if String in self.data:
            return "TagAlreadyTaken"

        self.data[String] = pk


    def Get(self, String):
        """
        Retrieves a pk from a String tag.

        Params:
            > String - str

        Returns: (pk, err) where err is not None and pk is None iff String is being used.
        """
        self._validate(String)
        if String in self.data:
            return self.data[String], None
        else:
            return None, "TagDoesNotExist"


# tests and usage examples
if __name__ == "__main__":
    from crypto import AsymmetricKeyGen

    ks = Keyserver()
    pk1, _ = AsymmetricKeyGen()
    pk2, _ = AsymmetricKeyGen()
    pk3, _ = AsymmetricKeyGen()

    err = ks.Set("pk1", pk1)
    assert err is None
    err = ks.Set("pk2", pk2)
    assert err is None

    pk1_copy, err = ks.Get("pk1")

    assert pk1 == pk1_copy

    err = ks.Set("pk1", pk3)
    assert err == "TagAlreadyTaken"

    print("Expecting error messages...")
    exceptionThrown = False
    try:
        ks.Set(1, pk2)
    except ValueError as e:
        exceptionThrown = True

    assert exceptionThrown

    exceptionThrown = False
    try:
        ks.Set("tag", 1)
    except ValueError as e:
        exceptionThrown = True

    assert exceptionThrown
    print("Success!")
