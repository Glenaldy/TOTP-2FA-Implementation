import pyotp
import qrcode


def generate_uri(key, name, issuer):
    return pyotp.totp.TOTP(key).provisioning_uri(
        name=name, issuer_name=issuer)


def generate_qr(uri, location):
    qrcode.make(uri).save(location)


def verify(key, code):
    totp = pyotp.TOTP(key)
    return totp.verify(code)


def generate_secret_key():
    return pyotp.random_base32()
