##
## crypto.py - Cryptographic API for Dropbox
##
## This file contains the crypto API.  All cryptographic operations in
## your project should be performed using only the functions in this
## file.
##
## WARNING:  DO NOT MODIFY THIS FILE.  This file will be replaced
## with a different version in the autograder, so your changes will be
## overwritten.
##


from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, hmac, serialization, constant_time
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from support.util import *

import base64
import os

def check_type(arg, corr_type, param_name: str, func_name: str) -> None:
    """
    A helper function for argument type checking.
    """
    if not isinstance(arg, corr_type):
        print(f"\nParameter \"{param_name}\" to {func_name} must of type {corr_type}!")
        print(f"Instead, it is: {type(arg)}\n")
        raise TypeError

class AsmPublicKey:
    """
    A wrapper around a public key. Allows for marshalling to and from bytes.
    Do not call this class construtor directly. Instead use AsymmetricKeyGen or SignatureKeyGen.
    """
    def __init__(self, libPubKey):
        self.libPubKey = libPubKey

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    @classmethod
    def from_bytes(cls, byte_repr):
        pub_key = serialization.load_pem_public_key(byte_repr)
        return cls(pub_key)

    def __str__(self):
        pem = self.libPubKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem.decode('utf-8')

    def __bytes__(self):
        pem = self.libPubKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem

class AsmPrivateKey:
    """
    A wrapper around a private key.
    Do not call this class construtor directly. Instead use AsymmetricKeyGen or SignatureKeyGen.
    """
    def __init__(self, libPrivKey):
        self.libPrivKey = libPrivKey

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    @classmethod
    def from_bytes(cls, byte_repr):
        private_key = serialization.load_pem_private_key(byte_repr, password=None)
        return cls(private_key)

    def __str__(self):
        pem = self.libPrivKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem.decode('utf-8')

    def __bytes__(self):
        pem = self.libPrivKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem

"""
These classes are wrappers around AsmPublicKey and AsmPrivateKey that
are used to make type checking easier for encryption and decryption
vs. signing and verifying.

Note that the underlying data is the same for both sets of keys (RSA
keypairs). These classes are only wrappers to help enforce that we
should not use the same keys for signing as we do for encryption.
"""
class AsymmetricEncryptKey(AsmPublicKey):
    pass
class AsymmetricDecryptKey(AsmPrivateKey):
    pass
class SignatureVerifyKey(AsmPublicKey):
    pass
class SignatureSignKey(AsmPrivateKey):
    pass

def AsymmetricKeyGen() -> tuple[AsymmetricEncryptKey, AsymmetricDecryptKey]:
    """
     Generates a public-key pair for asymmetric encryption purposes.

     Params: None
     Returns: (Public) Asymmetric Encryption Key, (Private) Asymmetric Decryption Key
    """
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()

    return AsymmetricEncryptKey(public_key), AsymmetricDecryptKey(private_key)

def AsymmetricEncrypt(EncryptionKey: AsymmetricEncryptKey, plaintext: bytes) -> bytes:
    """
     Using the public key, encrypt the plaintext
     Params:
        > PublicKey - AsmPublicKey
        > plaintext - bytes
     Returns: ciphertext bytes
    """
    check_type(EncryptionKey, AsymmetricEncryptKey, "EncryptionKey", "AsymmetricEncrypt")
    check_type(plaintext, bytes, "plaintext", "AsymmetricEncrypt")

    c_bytes = EncryptionKey.libPubKey.encrypt(plaintext, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA512()),
        algorithm=hashes.SHA512(),
        label=None
    ))
    return c_bytes

def AsymmetricDecrypt(DecryptionKey: AsymmetricDecryptKey, ciphertext: bytes) -> bytes:
    """
     Using the private key, decrypt the ciphertext
     Params:
        > PrivateKey - AsmPrivateKey
        > ciphertext - bytes
     Returns: paintext (bytes)
    """
    check_type(DecryptionKey, AsymmetricDecryptKey, "DecryptionKey", "AsymmetricDecrypt")
    check_type(ciphertext, bytes, "ciphertext", "AsymmetricDecrypt")

    plaintext = DecryptionKey.libPrivKey.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    )

    return plaintext

def SignatureKeyGen() -> tuple[SignatureVerifyKey, SignatureSignKey]:
    """
    Generates a public-key pair for digital signature purposes.
    Params: None
    Returns: (Public) Verifying Key, (Private) Signing Key
    """
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()

    return SignatureVerifyKey(public_key), SignatureSignKey(private_key)

def SignatureSign(SigningKey: SignatureSignKey, data: bytes) -> bytes:
    """
    Uses the private key key to sign the data.
    Params:
        > SigningKey - SignatureSignKey
        > data       - bytes

    Returns: signature (bytes)
    """
    check_type(SigningKey, SignatureSignKey, "SigningKey", "SignatureSign")
    check_type(data, bytes, "data", "SignatureSign")

    signature = SigningKey.libPrivKey.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA512()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA512()
    )
    return signature

def SignatureVerify(VerifyKey: SignatureVerifyKey, data: bytes, signature: bytes) -> bool:
    """
    Uses the public key key to verify that signature is a valid signature for message.
    Params:
        > PublicKey - AsmPublicKey
        > data      - bytes
        > signature - bytes

    Returns: boolean conditional on signature matches
    """
    check_type(VerifyKey, SignatureVerifyKey, "VerifyKey", "SignatureVerify")
    check_type(data, bytes, "data", "SignatureVerify")

    try:
        VerifyKey.libPubKey.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
    except Exception:
        return False

    return True

def Hash(data: bytes) -> bytes:
    """
    Computes a cryptographically secure hash of data.
    Params:
        > data - bytes

    Returns: the SHA512 hash of the input data (bytes)
    """
    check_type(data, bytes, "data", "Hash")

    digest = hashes.Hash(hashes.SHA512())
    digest.update(data)
    return digest.finalize()

def HMAC(key: bytes, data: bytes) -> bytes:
    """
    Compute a SHA-512 hash-based message authentication code (HMAC) of data.
    Returns an error if key is not 128 bits (16 bytes).

    You should use this function if you want a “keyed hash” instead of simply calling Hash
    on the concatenation of key and data, since in practical applications,
    doing a simple concatenation can allow the adversary to retrieve the full key.

    Params:
        > key  - bytes
        > data - bytes

    Returns: SHA-512 hash-based message authentication code (HMAC) of data (bytes)
    """
    check_type(data, bytes, "data", "Hash")
    check_type(key, bytes, "key", "Hash")

    h = hmac.HMAC(key, hashes.SHA512())
    h.update(data)
    return h.finalize()

def HMACEqual(hmac1: bytes, hmac2: bytes) -> bool:
    """
    Check if an HMAC is correct in constant time wrt the number of matching bytes.
    This is important to avoid timing attacks.

    Params:
        > hmac1 - bytes
        > hmac2 - bytes

    Returns: Boolean conditional on if hmacs match
    """
    check_type(hmac1, bytes, "hmac1", "HMACEqual")
    check_type(hmac2, bytes, "hmac2", "HMACEqual")

    return constant_time.bytes_eq(hmac1, hmac2)

def HashKDF(key: bytes, purpose: str) -> bytes:
    """
    Takes a key and a purpose and returns a new key.
    HashKDF is a keyed hash function that can generate multiple keys from a single key.
    This can simplify your key management schemes.

    Note that the "purpose" adds another input the the hash function such that the same password can produce
    more than one key.

    Params:
        > key - bytes
        > purpose - string

    Returns: new key (bytes)
    """

    check_type(key, bytes, "key", "HashKDF")
    check_type(purpose, str, "purpose", "HashKDF")

    hkdf = HKDF(
        algorithm=hashes.SHA512(),
        length=len(key),
        salt=None,
        info=purpose.encode(),
    )
    key = hkdf.derive(key)
    return key

def PasswordKDF(password: str, salt: bytes, keyLen: int) -> bytes:
    """
    Output some bytes that can be used as a symmetric key. The size of the output equals keyLen.
    A password-based key derivation function can be used to deterministically generate a cryptographic key
    from a password or passphrase.

    A password-based key derivation function is an appropriate way to derive a key from a password,
    if the password has at least a medium level of entropy (40 bits or so).

    Ideally, the salt should be different for each user or use of the function.
    Avoid using the same constant salt for everyone,
    as that may enable an attacker to create a single lookup table for reversing this function.

    Params:
        > password - string
        > salt - bytes
        > keyLen - int

    Returns: A key of length keyLen (bytes)
    """
    check_type(password, str, "password", "PasswordKDF")
    check_type(salt, bytes, "salt", "PasswordKDF")
    check_type(keyLen, int, "keyLen", "PasswordKDF")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=keyLen,
        salt=salt,
        iterations=1000,  # NOTE:  We have decreased this value for testing.
                          # A production version using PBKDF2 would use >= 10000
                          # iterations to increase the cost of generating hashes.
                          # Since we'll be generating a lot of hashes to create
                          # users in each test, we use a lower value now
                          # and could increase it when the client is ready
                          # for deployment to real users.
    )
    key = kdf.derive(password.encode())
    return key

def SymmetricEncrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """
    Encrypt the plaintext using AES-CBC mode with the provided key and IV.
    Pads plaintext using 128 bit blocks. Requires a valid size key.
    The ciphertext at the end will inlcude the IV as the last 16 bytes.

    Params:
        > key - bytes (128 bits)
        > iv  - bytes (128 bits)
        > plaintext - bytes

    Returns: A ciphertext using AES-CBC mode with the provided key and IV (bytes)
    """
    check_type(key, bytes, "key", "SymmetricEncrypt")
    check_type(iv, bytes, "iv", "SymmetricEncrypt")
    check_type(plaintext, bytes, "plaintext", "SymmetricEncrypt")

    if len(key) != 16:
        raise ValueError

    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext)
    padded_data += padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext + iv

def SymmetricDecrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypt the ciphertext using the key. The last 16 bytes of the ciphertext should be the IV.

    Params:
        > key        - bytes
        > iv         - bytes
        > ciphertext - bytes

    Returns: A plaintext, decrypted from the given ciphertext, key and iv (bytes).
             If the padding in wrong after decryption (which will happen if the wrong key is used),
             then the decryption will be returned with the incorrect padding.
    """
    check_type(key, bytes, "key", "symmetricDecrypt")
    check_type(ciphertext, bytes, "ciphertext", "symmetricDecrypt")

    iv = ciphertext[-16:]
    ciphertext = ciphertext[:-16]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    try:
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(plaintext)
        plaintext += unpadder.finalize()
    except:
        pass

    return plaintext

def SecureRandom(num_bytes: int) -> bytes:
    """
    Given a length, return that many randomly generated bytes. Can be used for an IV or symmetric key.

    Params:
        > num_bytes - int

    Returns: num_bytes random bytes
    """
    check_type(num_bytes, int, "num_bytes", "SecureRandom")
    return os.urandom(num_bytes)

if __name__ == '__main__':
    # generate keys
    pk, sk = AsymmetricKeyGen()

    # marshall keys to byte
    pk_bytes = bytes(pk)
    sk_bytes = bytes(sk)

    # generate key copies from bytes
    pk2 = AsymmetricEncryptKey.from_bytes(pk_bytes)
    sk2 = AsymmetricDecryptKey.from_bytes(sk_bytes)
    assert(pk == pk2)
    assert(sk == sk2)

    # encrypt the same message with the pub key and its copy
    cipher = AsymmetricEncrypt(pk, "CS1660".encode())
    cipher2 = AsymmetricEncrypt(pk2, "CS1660".encode())

    # decrypt with the non-matching sk to show they are the same
    plain = AsymmetricDecrypt(sk, cipher2)
    plain2 = AsymmetricDecrypt(sk2, cipher)

    assert(plain == plain2)

    # compute a signature
    verify_key, signing_key = SignatureKeyGen()
    data = "CS1660".encode()
    signature = SignatureSign(signing_key, data)
    verification = SignatureVerify(verify_key, data, signature)

    assert(verification == True)

    # compute a hash (SHA512)
    hash = Hash("CS1660".encode())
    assert(len(hash) == 64)

    # check HMACs
    hmac_val1 = HMAC("key".encode(), "data".encode())
    hmac_val2 = HMAC("key".encode(), "data".encode())
    HMACEqual(hmac_val1, hmac_val2)

    # check HashKDF
    hkdf1 = HashKDF("key".encode(), "CS1660")
    hkdf2 = HashKDF("key".encode(), "CS1660")
    assert(hkdf1 == hkdf2)

    # using different purposes causes different keys
    hkdf3 = HashKDF("key".encode(), "purpose #1")
    hkdf4 = HashKDF("key".encode(), "purpose #2")
    assert(hkdf3 != hkdf4)

    # check PasswordKDF
    password = "this is a long and secure password. Here are some symbols: @#$%^&^*%^%&"
    pkey = PasswordKDF(password, SecureRandom(16), 16)
    assert(len(pkey) == 16)

    # check symmetric encryption
    key = SecureRandom(16)
    iv = SecureRandom(16)
    plaintext = "CS1660 is the best class".encode()

    ciphertext = SymmetricEncrypt(key, iv, plaintext)
    plaintext2 = SymmetricDecrypt(key, ciphertext)
    assert(plaintext == plaintext2)
