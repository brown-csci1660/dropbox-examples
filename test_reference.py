# test_reference.py
#
# This file imports the reference client and shows some example tests
# for how to use it.  You can add/extend these tests if you want to
# try things out to learn how the API works.
#
# Alternatively, to just try out using the reference in a Python
# shell, run:
# python3 test_reference.py
#
# This will import all of the libraries required and then start
# an interactive REPL.

import unittest
import string

import support.crypto as crypto
import support.util as util

from support.dataserver import dataserver, memloc
from support.keyserver import keyserver

# Import the REFERENCE client
import dropbox_client_reference as c


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        """
        This function is automatically called before every test is run. It
        clears the dataserver and keyserver to a clean state for each test case.
        """
        dataserver.Clear()
        keyserver.Clear()

    def test_create_user(self):
        """
        Checks user creation.
        """
        u = c.create_user("usr", "pswd")
        u2 = c.authenticate_user("usr", "pswd")

        self.assertEqual(vars(u), vars(u2))

    def test_upload(self):
        """
        Tests if uploading a file throws any errors.
        """
        u = c.create_user("usr", "pswd")
        u.upload_file("file1", b'testing data')

    def test_download(self):
        """
        Tests if a downloaded file has the correct data in it.
        """
        u = c.create_user("usr", "pswd")

        data_to_be_uploaded = b'testing data'

        u.upload_file("file1", data_to_be_uploaded)
        downloaded_data = u.download_file("file1")

        self.assertEqual(downloaded_data, data_to_be_uploaded)

    def test_share_and_download(self):
        """
        Simple test of sharing and downloading a shared file.
        """
        u1 = c.create_user("usr1", "pswd")
        u2 = c.create_user("usr2", "pswd")

        u1.upload_file("shared_file", b'shared data')
        u1.share_file("shared_file", "usr2")

        u2.receive_file("shared_file", "usr1")
        down_data = u2.download_file("shared_file")

        self.assertEqual(down_data, b'shared data')


# Start the REPL if this file is launched as the main program
if __name__ == "__main__":
    util.start_repl(locals())
