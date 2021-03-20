import unittest
import string
import random

from client import *

import support.crypto as crypto
import support.util as util

from support.dataserver import Dataserver, Memloc
from support.keyserver import Keyserver

import support.dataserver as ds
import support.keyserver as ks


def new_config():
    """ call this function at the beginning of tests to spawn a new enviroment """
    ds.dataserver.data = {}
    ks.keyserver.data = {}


class ClientTests(unittest.TestCase):

    def test_create_user(self):
        """Checks user creation"""
        new_config()
        u = create_user("usr", "pswd")
        u2 = authenticate_user("usr", "pswd")
        
        self.assertEqual(vars(u), vars(u2))


    def test_upload(self):
        """Tests if uploading a file throws any errors"""
        new_config()
        u = create_user("usr", "pswd")
        u.upload_file("file1", b'testing data')

    def test_download(self):
        """Tests if a downloaded file has the correct data in it"""
        new_config()

        u = create_user("usr", "pswd")

        data_to_be_uploaded = b'testing data'

        u.upload_file("file1", data_to_be_uploaded)
        downloaded_data = u.download_file("file1")

        self.assertEqual(downloaded_data, data_to_be_uploaded)

      
    def test_share_and_download(self):
        """Simple test of sharing and downloading a shared file"""
        new_config()

        u1 = create_user("usr1", "pswd")
        u2 = create_user("usr2", "pswd")

        u1.upload_file("shared_file", b'shared data')
        u1.share_file("shared_file", "usr2")

        u2.recieve_file("shared_file", "usr1")
        down_data = u2.download_file("shared_file")

        self.assertEqual(down_data, b'shared data')
    
    def test_download_error(self):
      """Simple test that should throw an error"""
      new_config()
      u = create_user("usr", "pswd")
      # file1 does not exist. Note that the function has to be wrapped in a lambda function
      # when using AssertRaises
      self.assertRaises(util.DropboxError, lambda: u.download_file("file1"))


    def test_the_next_test(self):
          """
          Implement more tests by defining more functions like this one!
          Note that functions have to start with the word "test" to be recognized. 
          They can use a "self.Assert___" statement or can just run a series of commands. 
          If there is no Assert statment, then the test will fail if and only if an error is raised. 
          """
          self.assertTrue(True)


      

if __name__ == '__main__':
    unittest.main()
