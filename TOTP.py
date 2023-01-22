# Mission/Task Description:
# * For the "password", provide an 10-digit time-based one time password conforming to RFC6238 TOTP.
#
# ** You have to read RFC6238 (and the errata too!) and get a correct one time password by yourself.
# ** TOTP's "Time Step X" is 30 seconds. "T0" is 0.
# ** Use HMAC-SHA-512 for the hash function, instead of the default HMAC-SHA-1.
# ** Token shared secret is the userid followed by ASCII string value "HDECHALLENGE003" (not including double quotations).
#
# *** For example, if the userid is "ninja@example.com", the token shared secret is "ninja@example.comHDECHALLENGE003".
# *** For example, if the userid is "ninjasamuraisumotorishogun@example.com", the token shared secret is "ninjasamuraisumotorishogun@example.comHDECHALLENGE003"
#

import datetime
import hmac
import hashlib
import time
import sys
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
    totp= pyotp.TOTP(shared_secret)
    print(totp.now())


def HOTP(K, C, digits=10):
    """HTOP:
    K is the shared key
    C is the counter value
    digits control the response length
    """
    K_bytes = K.encode()
    C_bytes = struct.pack(">Q", C)
    
    hmac_sha256 = hmac.new(key=K_bytes, msg=C_bytes,
                           digestmod=hashlib.sha1)
    print(hmac_sha256)
    a = Truncate(hmac_sha256)[-digits:]
    print(a)
    return a


def Truncate(hmac_hash):
    # """truncate sha512 value"""
    # offset = hmac_sha512[-1] & 0xf
    # print(offset)
    # # offset = int(hmac_sha512[-1], 16)
    # binary = int(hmac_sha512[(offset * 2):((offset*2)+8)], 16) & 0x7FFFFFFF
    digits = 6

    offset = hmac_hash[-1] & 0xf
    code = ((hmac_hash[offset] & 0x7f) << 24 |
            (hmac_hash[offset + 1] & 0xff) << 16 |
            (hmac_hash[offset + 2] & 0xff) << 8 |
            (hmac_hash[offset + 3] & 0xff))
    str_code = str(code % 10 ** digits)
    return str_code

# def SCRYPT(K):
#     return hashlib.scrypt("password".encode(), salt="glenaldy@mail.com".encode(), n = 2, r=1, p=2)

def TOTP(K, digits=10, timeref=0, timestep=30):
    """TOTP, time-based variant of HOTP
    digits control the response length
    the C in HOTP is replaced by ( (currentTime - timeref) / timestep )
    """
    C = int(time.time() - timeref) // timestep
    return HOTP(K, C, digits=digits)


if __name__ == "__main__":
    main()
