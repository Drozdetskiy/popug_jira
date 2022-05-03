from pydantic import (
    BaseModel,
    Field,
)

from popug_sdk.conf.auth import AuthSettings as BaseAuthSettings
from popug_sdk.conf.db import DatabaseSettings as BaseDatabaseSettings
from popug_sdk.conf.global_settings import Settings as BaseSettings
from popug_sdk.conf.redis import RedisSettings

PROGECT_NAME = "popug_auth"


class DatabaseSettings(BaseDatabaseSettings):
    database_name = f"{PROGECT_NAME}_db"


class AuthSettings(BaseAuthSettings):
    public_key: str = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDgGFoM/dQu1tf5xEvsfSVTU5ANRos87lmalgJ5CPB/wPED+mW0ZFjKycpInOtbUI9ZntvWGlFO1l/A6l6p9FaAa78HAp+YWYFRTRGoNaZSFw4VxvQ0i7ev6L+z8TzVaywRkXBVHYJvwQWAu+Noq1ED1AzE6QSGmq3S/Uo56cGFSKvKBc47IUyDUYYOyLOJGuownF7nBsBFi5wAsiw554JdNeMpha8kXRLHQrxHsYcz5+ysDfLqeT1TRtJ+avLXBzIw8Bpjqqr/tZWZVZ7g/LBfb31i11S7BxzSwndxLA9agQXCMMY78r3R/VZIj9BIO/vp3bAw60Mee7PaiMCZIgdR"  # noqa


class SecuritySettings(BaseModel):
    access_token_expiration: int = 3600  # 1 hour
    refresh_token_expiration: int = 86400  # 1 day
    secret_key: str = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDgGFoM/dQu1tf5\nxEvsfSVTU5ANRos87lmalgJ5CPB/wPED+mW0ZFjKycpInOtbUI9ZntvWGlFO1l/A\n6l6p9FaAa78HAp+YWYFRTRGoNaZSFw4VxvQ0i7ev6L+z8TzVaywRkXBVHYJvwQWA\nu+Noq1ED1AzE6QSGmq3S/Uo56cGFSKvKBc47IUyDUYYOyLOJGuownF7nBsBFi5wA\nsiw554JdNeMpha8kXRLHQrxHsYcz5+ysDfLqeT1TRtJ+avLXBzIw8Bpjqqr/tZWZ\nVZ7g/LBfb31i11S7BxzSwndxLA9agQXCMMY78r3R/VZIj9BIO/vp3bAw60Mee7Pa\niMCZIgdRAgMBAAECggEAH5/AIYI2jc+a1e/6KOr2N/6cXws7/gLC2VpfCfaVfenb\n+Uw+Swk4MJHufnXKju3c9PBCpMG9BKujAqXwavqEtIXABPy9SfIjmjYOjlbX3FDN\nl4wmjT3EU8o8N2gNRi7kHqyQFirea+fo32RkcLJwceJcVPNvRJGSgypkbazLtwOp\nLAxacRU/WazWf9pvjAWYqvRJ7AJkOOcs05Lh+EYmq2SN30ee/Wy5Urv0lWpEoT4H\nZinzepyqI0YL4lH7ugbzwewPbIcz8rLs7ynZAsK4TElkuWPZkRtu45aV4Ud7tCr6\ncoyjMSvGHr3sGLARVlljSB0ItcwpVjde7izEQw1f+QKBgQDjHL/wPTGMDirgCGWg\niq/f+Pzq7fOwv9j0xvg8pTvVtYZp2X6K+TmKLwhgV0QnUU/XPVNDincwCqXkhxih\n08e81UwtzR6CM1RgcYkmU0wmTlxm0Xkndb+9tVS9lW+IxZW4qZn7Ph/2Nxs5hyE7\nnGsFKjMDpeagrixHq/fHGQEj1QKBgQD8mVs5AY6xcXpnZK5olQISTGlwSIICme9V\n7AW1h/ZJsn0E+jvA+bI0QRxb36EmKGmzohgL2kuFn/ts7MPmlQjLyvKDLffkJ34T\nCYXMcvVA8wlKAOq5XHJ0sOjD5WoYOwXUU6RuvSLA5GMCbcASCXO4OBuybgNJz2nd\n7qlEBUCfjQKBgEszBcrCOFmrhz7PCPdzdHCwvO39BCeOHoROLXvHKlzE0lDSFzhk\n9Uxv7lIYExUBs3INeDhw7K4XmH5mzR0oRoacCbFQrb1myZV1gngSNLCqWaYhzf/m\n2SozlG+Bv4CGC+EtJzMtit+3t2gA+lwGmtkG9AVNNWQWx8qjglOGT/5RAoGACcg+\nmiSPTBvi66IghvhOTjsbUjfcoREpDaDIT9FmHlCFOu4d5klFN3TWDlDIwtuJzGUY\nnUzk49XgPMWmiIV5A7tmTOI42WMWJNKXleVVziAbWfxTGr6TyCUZvoxh4XJXtXNP\nyOIWOHYfx3ZMm+Y1zwqNOAm+otsfdHLLp1C0wfkCgYEAjPRLSoa0UEZPQDM6wwj8\n9fL+4hBcZm1IoLf5WB3F4s4svDzlMVLBsMMvAJoUbTHC5SxZhskj4ECePZZ3B8gL\nzTvwi3mjHXJClQMKz4k3DbVkzkbQxpK3iKFRmBtQ3dHl0SiuKzkli7XqC4YHe40D\nWydroLPu75CVBmh6b7HedNQ=\n-----END PRIVATE KEY-----\n"  # noqa
    algorithm: str = "RS256"

    auth_code_expiration: int = 60  # 1 minute

    public_exponent: int = 65537
    key_size: int = 2048


class Settings(BaseSettings):
    project: str = PROGECT_NAME
    use_https = False
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    redis: dict[str, RedisSettings] = Field(
        default_factory=lambda: {"default": RedisSettings()}
    )
    redirect_uris: list[str] = Field(default_factory=list)
    auth: AuthSettings = Field(default_factory=AuthSettings)
