"""
This file contains the stencil for your implementation. You **should** modify this file.
"""

from support.crypto import *
from support.util import *
from support.dataserver import Dataserver, Memloc
from support.keyserver import Keyserver


def create_user(username, password, dataserver, keyserver, memloc_factory):
    """
    Raise an error if: username is taken or empty or if password is empty.
    Otherwise, create a user.
    """
    # TODO: Implement!
    raise DropboxError("Not Implemented")


def authenticate_user(username, password, dataserver, keyserver, memloc_factory):
    """
    Raise an error if: username does not exist, the password is invalid, or there is an integrity issue.
    Otherwise, return a User object.
    """
    # TODO: Implement!
    raise DropboxError("Not Implemented")


class User:
    # TODO: add arguments as needed to initialize the User
    def __init__(self, dataserver, keyserver, memloc_factory):
        # dataserver object
        self.dataserver = dataserver
        # keyserver object
        self.keyserver = keyserver
        # memloc_factory object
        self.memloc_factory = memloc_factory

    def upload_file(self, filename, data):
        """store data at filename. Preserve sharing, overwrite"""
        # TODO: Implement!
        raise DropboxError("Not Implemented")

    def download_file(self, filename):
        """download and return data at filename. Raise error if file does not exist or if integrity fails"""
        # TODO: Implement!
        raise DropboxError("Not Implemented")

    def append_file(self, filename, data):
        """add data to filename. Raise error if file does not exist or if there was malicious action"""
        # TODO: Implement!
        raise DropboxError("Not Implemented")

    def share_file(self, filename, recipient):
        """share the file with filename with the recipient"""
        # TODO: Implement!
        raise DropboxError("Not Implemented")

    def recieve_file(self, filename, sender, token):
        """accepts a token and takes access of the file @ filename"""
        # TODO: Implement!
        raise DropboxError("Not Implemented")

    def revoke_file(self, filename, old_recipient):
        """take access away from old_recipient"""
        # TODO: Implement!
        raise DropboxError("Not Implemented")
