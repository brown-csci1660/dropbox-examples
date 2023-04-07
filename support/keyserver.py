##
## keyserver.py - Keyserver Implementation
##
## This file contains the keyserver API.
##
## WARNING:  DO NOT MODIFY THIS FILE.  This file will be replaced
## with a different version in the autograder, so your changes will be
## overwritten.
##

from support.crypto import AsmPublicKey

class Keyserver:
    """
    Keyserver implementation.
    """
    def __init__(self):
        self.data = {}

    def _validate(self, identifier: str, pk=None) -> None:
        """
        Validates inputs. Not to be used externally.
        """
        if not isinstance(identifier, str):
            print(f"ERROR: Keyserver tags must be strings, not {type(identifier)}")
            raise ValueError
        if pk:
            if not isinstance(pk, AsmPublicKey):
                print(
                    f"ERROR: Keyserver keys must of type AsmPublicKey, not {type(pk)}"
                )
                raise ValueError

    def Set(self, identifier: str, pk: AsmPublicKey) -> None:
        """
        Stores pubkey at a string.

        Params:
            > String - str
            > pk     - AsmPublicKey

        Returns: None
        """
        self._validate(identifier, pk=pk)
        if identifier in self.data:
            raise ValueError("IdentifierAlreadyTaken")

        self.data[identifier] = pk

    def Get(self, identifier: str) -> bytes:
        """
        Retrieves a pk from a String tag.

        Params:
            > String - str

        Returns: public key or raises ValueError
        """
        self._validate(identifier)
        if identifier in self.data:
            return self.data[identifier]
        else:
            raise ValueError("IdentifierAlreadyTaken")

    def Delete(self, identifier: str) -> None:
        """
        Deletes a pk @ a String tag.

        Params:
            > String - str

        Returns: None or raises ValueError
        """
        self._validate(identifier)
        if identifier in self.data:
            del self.data[identifier]
        else:
            raise ValueError("IdentifierAlreadyTaken")

    ##################################################################
    # NOTE: the following functions are provided for testing ONLY--you
    # can use them to test functionality or attacks, but you should
    # not use them in your client Implementation (ie, from client.py).
    ##################################################################

    def GetMap(self) -> dict:
        """
        Return the entire server contents as a dictionary

        Params: None
        Returns: dict
        """
        return self.data

    def Clear(self):
        """
        Delete the entire server contents
        """
        self.data = {}

keyserver = Keyserver()

# tests and usage examples
if __name__ == "__main__":
    from support.crypto import AsymmetricKeyGen, SignatureKeyGen

    # keyserver = Keyserver()
    pk1, _ = AsymmetricKeyGen()
    pk2, _ = SignatureKeyGen()
    pk3, _ = AsymmetricKeyGen()

    keyserver.Set("pk1", pk1)
    keyserver.Set("pk2", pk2)

    pk1_copy = keyserver.Get("pk1")

    assert pk1 == pk1_copy

    exceptionThrown = False

    try:
        keyserver.Set("pk1", pk3)
    except ValueError as v:
        ## no error message in this case
         exceptionThrown = True

    assert exceptionThrown

    print("Expecting two error messages...")

    try:
        keyserver.Set(1, pk2)
    except ValueError as e:
        exceptionThrown = True

    assert exceptionThrown

    exceptionThrown = False
    try:
        keyserver.Set("tag", 1)
    except ValueError as e:
        exceptionThrown = True

    assert exceptionThrown
    print("Success!")
