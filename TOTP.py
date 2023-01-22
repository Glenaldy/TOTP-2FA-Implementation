import datetime
import hmac
import hashlib
import time
import struct
import pyotp


def main():
    userid = "GlenaldyCleversonSebastian"
    secret_suffix = ""
    shared_secret = "GlenaldyCleversonSebastian"

    timestep = 30
    T0 = 0
    # passwd = TOTP(shared_secret, 10, T0, timestep).zfill(10)

    print(datetime.datetime.now())
    print(TOTP(shared_secret, 6, T0, timestep))
    totp = pyotp.TOTP(shared_secret)
    print(totp.now())


def HOTP(K, C, digits):
    Key = K.encode()
    Counter = struct.pack(">Q", C)

    hmac_sha256 = hmac.new(Key, Counter, hashlib.sha512).hexdigest()

    print(hmac_sha256)
    return Truncate(hmac_sha256)[-digits:]


def Truncate(hmac_hash):
    offset = int(hmac_hash[-1], 16)
    binary = int(hmac_hash[(offset * 2):((offset*2)+8)], 16) & 0x7FFFFFFF

    return str(binary)


def TOTP(K, digits=10, timeref=0, timestep=30):
    C = int(time.time() - timeref) // timestep
    return HOTP(K, C, digits=digits)


if __name__ == "__main__":
    main()
