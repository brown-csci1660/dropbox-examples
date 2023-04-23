##
## client.py - Dropbox client implementation
##

# ** Optional libraries, uncomment if you need them **
# Search "python <name> library" for documentation
#import string  # Python library with useful string constants
#import dacite  # Helpers for serializing dicts into dataclasses
#import pymerkle # Merkle tree implementation (CS1620/CS2660 only, but still optional)

## ** Support code libraries ****
# The following imports load our support code from the "support"
# directory.  See the Dropbox wiki for usage and documentation.
import support.crypto as crypto                   # Our crypto library
import support.util as util                       # Various helper functions

# These imports load instances of the dataserver, keyserver, and memloc classes
# to use in your client. See the Dropbox Wiki and setup guide for examples.
from support.dataserver import dataserver, memloc
from support.keyserver import keyserver

# **NOTE**:  If you want to use any additional libraries, please ask on Ed
# first.  You are NOT permitted to use any additional cryptographic functions
# other than those provided by crypto.py, or any filesystem/networking
# libraries.


def s_addr(s):
    return memloc.MakeFromBytes(crypto.Hash(s.encode("utf-8"))[:16])




class User:
    def __init__(self) -> None:
        pass

    def upload_file(self, filename: str, data: bytes) -> None:
        dataserver.Set(s_addr(filename), data)

    def download_file(self, filename: str) -> bytes:
        return dataserver.Get(s_addr(filename))

    def append_file(self, filename: str, data: bytes) -> None:
        # TODO: Implement
        raise util.DropboxError("Not Implemented")

    def share_file(self, filename: str, recipient: str) -> None:
        # TODO: Implement
        raise util.DropboxError("Not Implemented")

    def receive_file(self, filename: str, sender: str) -> None:
        # TODO: Implement
        raise util.DropboxError("Not Implemented")

    def revoke_file(self, filename: str, old_recipient: str) -> None:
        # TODO: Implement
        raise util.DropboxError("Not Implemented")

def create_user(username: str, password: str) -> User:
    info_addr = s_addr(username)
    dataserver.Set(info_addr, password.encode("utf-8"))

    return User() # Probably should do something else here...

def authenticate_user(username: str, password: str) -> User:
    info_addr = s_addr(username)
    password_bytes = dataserver.Get(info_addr)

    password_check = password_bytes.decode("utf-8")

    if password != password_check:  # Hmmm...
        raise util.DropboxError("Could not authenticate!")

    return User()
