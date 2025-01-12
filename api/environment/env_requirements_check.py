import re


def test_conf(conf) -> bool:
    ## API
    assert isinstance(conf.api.port, int), "api.port is not an integer"
    assert isinstance(conf.api.jwt_secret, str), "api.jwt is not a string"
    assert len(conf.api.jwt_secret) >= 64, "api.jwt_secret must be at least 64 characters long"

    ## Environment
    assert conf.environment.type in ["local", "development", "production"], f"environment.type is not valid. Was expecting local, development or production, got {conf.environment.type}"

    ## Zero-TOTP
    assert re.match(r"^https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/[^\s]*)?$", conf.zero_totp.api_uri), "database.zero_totp_db_uri is not a valid URL"
    assert isinstance(conf.zero_totp.bypass_cert_verification, bool), "zero_totp.bypass_cert_verification is not a boolean"

    # TODO: Add more checks here
