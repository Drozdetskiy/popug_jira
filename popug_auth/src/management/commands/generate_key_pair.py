from conf import SecuritySettings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from popug_sdk.conf import settings


def generate_key_pair() -> None:
    security_settings: SecuritySettings = settings.security
    key = rsa.generate_private_key(
        public_exponent=security_settings.public_exponent,
        key_size=security_settings.key_size,
    )

    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )

    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
    )

    print(private_key)
    print(public_key)
