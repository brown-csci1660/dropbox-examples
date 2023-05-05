##
## test_examples.py - Examples for using stencil components and testing
## This file contains examples of how to use the Dataserver and
## Keyserver as well as how to serialize various types of data you may
## want to use in this project.
##
## As you think about building your implementation, skim over these
## examples for some ideas on how to represent you data.
##
## See the comments on individual tests for a description of what each
## test does.
##

import unittest
import string

import support.crypto as crypto
import support.util as util

from support.dataserver import Memloc, dataserver, memloc
from support.keyserver import keyserver

# Import your client
import client as c

import dataclasses
import dacite

# Use this in place of the above line to test using the reference client
#import dropbox_client_reference as c

def s_addr(s):
    return memloc.MakeFromBytes(crypto.Hash(s.encode("utf-8"))[:16])


class DataserverExamples(unittest.TestCase):

    # All data you encrypt/sign/store must be encoded as a bytes()
    # object.  Here are some examples of turning strings into bytes
    def test_bytes_strings(self):
        s = "Hello world!" # A string

        # In most cases, we operate on data as bytes, so need to encode
        s_bytes = s.encode("utf-8")
        assert(isinstance(s_bytes, bytes))

        s_check = s_bytes.decode("utf-8")
        assert(s == s_check)

    # Examples for working with memlocs
    def test_memlocs(self):
        # Random memloc
        m1 = memloc.Make()

        # Memloc with a constant address
        bs = b"abcdef0123456789"
        m2 = memloc.MakeFromBytes(bs)

        # Want to use a string as a key instead?
        # You can do this by hashing the string and then taking the
        # last 16 bytes, like this!
        # Note:  This is a GREAT place to make a helper function
        m3 = memloc.MakeFromBytes(crypto.Hash("{}@enc".format("alice").encode("utf-8"))[:16])
        #m3 = s_addr("{}@enc".format("alice")) # <---- *GREAT* place for a helper function!!!

        some_data = crypto.SecureRandom(20)
        dataserver.Set(m1, some_data)
        dataserver.Set(m2, some_data)
        dataserver.Set(m3, some_data)

    # Storing stuff in the dataserver:  the basic idea
    # All data stored must be a bytes() object.  What if you want to
    # store something else?  See the examples below!
    def test_dataserver_bytes(self):
        addr = s_addr("addr")
        some_data = crypto.SecureRandom(20)

        # Store it
        dataserver.Set(addr, some_data)

        # Get it back out and check the result
        check_data = dataserver.Get(addr)
        assert(some_data == check_data)

    # If we want to store a dictionary, we need to serialize it to
    # bytes() first.  The stencil provides two methods to serialize
    # to/from bytes() objects: util.ObjectToBytes and
    # util.ObjectFromBytes, which know how to serialize the following
    # types:  int, str, bool, dict, list, bytes
    # Here's an example for a dict.  For handling classes or more
    # complex types, keep reading.
    def test_serialization_dict(self):
        info = {
            "a": 1,
            "b": crypto.SecureRandom(10),
            "mems": [1, 2, 3, 4],
        }

        # Store it on the dataserver
        addr = s_addr("my_info")
        info_bytes = util.ObjectToBytes(info)             # Convert to bytes
        dataserver.Set(addr, info_bytes)

        # Now get it back out
        info_check_bytes = dataserver.Get(addr)
        info_check = util.BytesToObject(info_check_bytes) # Convert back to dict
        assert(info == info_check)

    # Here's an example for how to serialize a class with custom fields
    def test_serialization_class(self):
        class SomeThing:
            def __init__(self, key: bytes, members: set[int]):
                self.key = key
                self.members = members  # <--- This is a set, which is
                                        # also unsupported by ObjectToBytes!

            # How do we handle this?  We can make a helper function
            # like this, which converts this object into a dict and
            # then uses ObjectToBytes (and another one to convert back
            def to_bytes(self):
                return util.ObjectToBytes({
                    "key": self.key,
                    "members": list(self.members), # Convert set to a list
                })

            @classmethod
            def make_from_bytes(cls, b: bytes):
                d = util.BytesToObject(b)
                return SomeThing(key=d["key"],
                                            members=set(d["members"]))

        # ** Usage example **
        # Make an object and serialize it to bytes
        t = SomeThing(key=crypto.SecureRandom(10),
                                 members=set([1, 2, 3]))
        t_bytes = t.to_bytes()

        # Store it in the dataserver
        addr = s_addr("alice@thing")
        dataserver.Set(addr, t_bytes)

        # Now fetch it and turn it back into an object
        r_bytes = dataserver.Get(addr)
        r = SomeThing.make_from_bytes(r_bytes)

        assert(t.key == r.key)
        assert(t.members == r.members)

    # Here's an example of how to serialize/deserialize every other type you're likely
    # to need for this project
    def test_serialization_manytypes(self):
        class SomeThing:
            def __init__(self, key: bytes, members: set[int],
                         k_pub: crypto.AsmPublicKey, k_priv: crypto.AsmPrivateKey,
                         some_addr: bytes):
                self.key = key
                self.members = members
                self.k_pub = k_pub
                self.k_priv = k_priv
                self.some_addr = some_addr

            def to_bytes(self):
                return util.ObjectToBytes({
                    "key": self.key,
                    "members": list(self.members), # Convert set to a list
                    "k_pub": self.k_pub.__bytes__(),
                    "k_priv": self.k_priv.__bytes__(),
                    "some_addr": self.some_addr,
                })

            @classmethod
            def make_from_bytes(cls, b: bytes):
                d = util.BytesToObject(b)
                return SomeThing(key=d["key"],
                                 members=set(d["members"]),
                                 k_pub=crypto.AsmPublicKey.from_bytes(d["k_pub"]),
                                 k_priv=crypto.AsmPrivateKey.from_bytes(d["k_priv"]),
                                 some_addr=d["some_addr"])

        # Make an object and serialize it to bytes
        k_pub, k_priv = crypto.AsymmetricKeyGen()
        some_memloc = memloc.Make()
        t = SomeThing(key=crypto.SecureRandom(10),
                      members=set([1, 2, 3]),
                      k_pub=k_pub,
                      k_priv=k_priv,
                      some_addr=some_memloc)
        t_bytes = t.to_bytes()

        # Store it in the dataserver
        addr = s_addr("alice@thing")
        dataserver.Set(addr, t_bytes)

        # Now fetch it and turn it back into an object
        r_bytes = dataserver.Get(addr)
        r = SomeThing.make_from_bytes(r_bytes)

        assert(t.key == r.key)
        assert(t.members == r.members)
        assert(t.some_addr == r.some_addr)

        assert(isinstance(r.k_pub, crypto.AsmPublicKey))
        assert(t.k_pub == r.k_pub)

        assert(isinstance(r.k_priv, crypto.AsmPrivateKey))
        assert(t.k_priv == r.k_priv)


    # If you like dataclasses, here's an example using Python's dataclasses
    def test_serialization_dataclass(self):
        @dataclasses.dataclass
        class Thing:
            a: int
            b: list[int]
            c: dict[str, int]

            # NOTE: If you use any types other than: int, list, dict, str
            # you still need to write to_bytes, make_from_bytes as above!

        t = Thing(a=1, b=[1, 2, 3], c={"a": 1, "b": 2})
        t_dict = dataclasses.asdict(t)
        t_bytes = util.ObjectToBytes(t_dict)

        # Store it in the dataserver
        addr = s_addr("alice@thing")
        dataserver.Set(addr, t_bytes)

        # Now let's get it back out
        r_bytes = dataserver.Get(addr)
        r_dict = util.BytesToObject(r_bytes)
        r = dacite.from_dict(data_class=Thing, data=r_dict)

        assert(t == r)

### ** Examples for using the keyserver **
class KeyserverExamples(unittest.TestCase):

    def setUp(self):
        dataserver.Clear()
        keyserver.Clear()

    def test_keyserver(self):
        k_pub, k_priv = crypto.AsymmetricKeyGen()

        keyserver.Set("alice", k_pub)

        alice_kpub = keyserver.Get("alice")
        assert(k_pub == alice_kpub)

    def test_keyserver_replace(self):
        k1_pub, k1_priv = crypto.AsymmetricKeyGen()
        keyserver.Set("alice", k1_pub)

        # Attempts to set the same key again should fail
        # (also, here's an example to test for an exception)
        k2_pub, k2_priv = crypto.AsymmetricKeyGen()
        self.assertRaises(ValueError,
                          keyserver.Set, "alice", k2_pub) # Same as keyserver.Set("alice", k2_pub)


## **Examples for testing attacks**
class TestAttackExamples(unittest.TestCase):

    # Clear dataserver and keyserver between tests
    def setUp(self):
        dataserver.Clear()
        keyserver.Clear()


    # Clear dataserver and keyserver between tests
    def test_password_cleartext(self):

        #### Setup phase:  do some actions as a legitimate client
        c.create_user("a", "1234")
        user = c.authenticate_user("a", "1234")


        #### Attack phase:  act like adversary and do things client shouldn't_bytes

        # As the attacker, we can directly use methods provide by the
        # dataserver and keyserver, which mimics the attacker's
        # capabilities of being able to add/modify data
        # See "Threat model" section on Wiki for more info.

        # Let's try to change alice's password
        # Relies on us knowing something about how data is stored
        dataserver.Set(s_addr("a"), "oops".encode("utf-8"))

        #### Testing:  try to do some action as client or adversary to prove attack worked
        user2 = c.authenticate_user("a", "oops")

        # When you write your attack tests, you should instead
        # probably test to make sure the attack is NOT successful:
        # self.assertRaises(util.DropboxError, c.authenticate_user, "a", "oops")

        # Example 2:  Try to log in as if you were user (and it should fail)
        self.assertRaises(util.DropboxError, c.authenticate_user, "a", "1234")

    # What if we didn't know where the password was stored?  Or, what
    # if we wanted to change a lot of data?
    def test_bad_file_upload(self):
        ###### Setup Phase
        user = c.create_user("a", "1234")
        file_bytes = b"hello world!"
        user.upload_file("file", file_bytes)

        #### Attack phase

        # FOR TESTING/ATTACKS ONLY: The Keyserver and Dataserver have
        # a method GetMap() which iterates over all its contents
        for memloc, data in dataserver.GetMap().items():
            # Overwrite whatever's here with some zeroes (or anything you want
            dataserver.Set(memloc, bytes(b'0' * 16))

        #### Test phase
        check_bytes = user.download_file("file")
        #assert(file_bytes == check_bytes)



# Start the REPL if this file is launched as the main program
if __name__ == '__main__':
    util.start_repl(locals())
