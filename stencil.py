"""
This file contains the stencil for your implementation. You **should** modify this file.
"""

import support.crypto as crypto
import support.util as util

# Dataserver, Memloc, and Keyserver (note the capital letter)
# are classes that are used only for type annotations. You should
# not use these classes directly
from support.dataserver import Dataserver, Memloc
from support.keyserver import Keyserver

# dataserver, memloc, and keyserver are instances of the classes 
# with the capitalized version of the name. These are the instances 
# you should interact with! See the bottom of the file for examples. 
from support.dataserver import dataserver, memloc
from support.keyserver import keyserver


class User:
    # TODO: add arguments as needed to initialize the User
    def __init__(self, username: str, password: str):
        # We are storing the username and password here even though the client is stateless. 
        # Note that "stateless" does not mean that you cannot store any information. It means that
        # the client, if restarted, can pick up where it left off given just a username and password.
        # Storing the username and password (or information derived from the username and password) 
        # meets this requirement. 
        self.username = username
        self.password = password

    def upload_file(self, filename: str, data: bytes):
        """store data at filename. Preserve sharing, overwrite"""
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def download_file(self, filename: str):
        """download and return data at filename. Raise error if file does not exist or if integrity fails"""
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def append_file(self, filename: str, data: bytes):
        """add data to filename. Raise error if file does not exist or if there was malicious action"""
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def share_file(self, filename: str, recipient: str):
        """share the file with filename with the recipient. Raise an error if the recipient does not exist or if there was malicious action"""
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def recieve_file(self, filename: str, sender: str):
        """accepts a filrname and a sender and takes access of the file @ filename. Raise an error if the file cannot be recieved"""
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")

    def revoke_file(self, filename: str, old_recipient: str):
        """take access to filename away from old_recipient"""
        # TODO: Implement!
        raise util.DropboxError("Not Implemented")


def create_user(username: str, password: str) -> User:
    """
    Raise an error if: username is taken or empty or if password is empty.
    Otherwise, create and return a User.
    """
    # TODO: Implement!
    raise util.DropboxError("Not Implemented")


def authenticate_user(username: str, password: str) -> User:
    """
    Raise an error if: username does not exist, the password is invalid, or there is an integrity issue.
    Otherwise, return a User object.
    """
    # TODO: Implement!
    raise util.DropboxError("Not Implemented")


# Usage examples!
if __name__ == "__main__":  
    ## Storing a list
    loc = memloc.Make()
    l = ["this", "is", "a", "list", "of", "strings", "and", "nums:", 1, 2, 3]
    dataserver.Set(loc, util.obj_to_bytes(l))
    l_bytes, err = dataserver.Get(loc)
    l2 = util.bytes_to_obj(l_bytes)
    assert(l == l2)

    ## Storing a dict
    loc = memloc.Make()
    d = {"k1": "v1", "k2": 2, "k3": "v3"}
    dataserver.Set(loc, util.obj_to_bytes(d))
    d_bytes, err = dataserver.Get(loc)
    d2 = util.bytes_to_obj(d_bytes)
    assert(d == d2)

    ## Storing a complex, nested data structure    
    loc = memloc.Make()
    c = {
        "k1": [{"k2": 2, "k3": [1,2,3], "k4": {"k5": [4,5,6]}}, "string", 12345], 
        "k6": ["this", "is", "a", "list", "of", "strings"]
        }
    dataserver.Set(loc, util.obj_to_bytes(c))
    c_bytes, err = dataserver.Get(loc)
    c2 = util.bytes_to_obj(c_bytes)
    assert(c == c2)

    ## raising errors
    def test_username(username):
        if username == "iAmAEvilHacker":
            # any message can be passed to the error. The autograder will check if a DropBox error is raised
            # but will not look at the message contents. The message is only for your own debugging and stylistic purposes
            raise util.DropboxError("A hacker is trying to break in!!")
    
    ### uncomment this line to show the error being raised
    # test_username("iAmAEvilHacker")