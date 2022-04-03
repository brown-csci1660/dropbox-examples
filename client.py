##
## client.py: Dropbox @ CSCI1660 (Spring 2022)
##
## This is the file where all of your code for your Dropbox client
## implementation must go.
##

## WARNING: You MUST NOT change these default imports. If you change the default
##          import statements in the stencil code, your implementation will be
##          rejected by the autograder. (Our autograder actually enforces this
##          this correctly, as opposed to the Crewmate Academy's autograder
##          from the Handin project!)

# Optional library containing some helpful string constants; not required to use
# this in your implementation. See https://docs.python.org/3/library/string.html
# for usage and documentation.
import string

# Imports the `crypto` and `util` libraries. See the Dropbox Wiki for usage and
# documentation.
import support.crypto as crypto
import support.util as util

# Imports the `dataserver`, `keyserver`, and `memloc` instances. See the Dropbox
# Wiki for usage and documentation.
from support.dataserver import dataserver, memloc
from support.keyserver import keyserver

# DO NOT EDIT ABOVE THIS LINE ##################################################

class User:
    def __init__(self) -> None:
        """
        Class constructor for the `User` class.

        You are free to add fields to the User class by changing the definition
        of this function.
        """
        pass

    def upload_file(self, filename: str, data: bytes) -> None:
        """
        The specification for this function is at:
        http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/storage/upload-file.html
        """
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def download_file(self, filename: str) -> bytes:
        """
        The specification for this function is at:
        http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/storage/download-file.html
        """
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def append_file(self, filename: str, data: bytes) -> None:
        """
        The specification for this function is at:
        http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/storage/append-file.html
        """
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def share_file(self, filename: str, recipient: str) -> None:
        """
        The specification for this function is at:
        http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/sharing/share-file.html
        """
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def receive_file(self, filename: str, sender: str) -> None:
        """
        The specification for this function is at:
        http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/sharing/receive-file.html
        """
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def revoke_file(self, filename: str, old_recipient: str) -> None:
        """
        The specification for this function is at:
        http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/sharing/revoke-file.html
        """
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

def create_user(username: str, password: str) -> User:
    """
    The specification for this function is at:
    http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/authentication/create-user.html
    """
    # TODO: Implement!
    raise util.DropboxError("Not Implemented")

def authenticate_user(username: str, password: str) -> User:
    """
    The specification for this function is at:
    http://cs.brown.edu/courses/csci1660/dropbox-wiki/client-api/authentication/authenticate-user.html
    """
    # TODO: Implement!
    raise util.DropboxError("Not Implemented")
