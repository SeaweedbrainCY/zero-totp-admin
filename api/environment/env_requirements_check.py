
def test_conf(conf) -> bool:
    ## API
    assert isinstance(conf.api.port, int), "api.port is not an integer"
    assert isinstance(conf.api.jwt_secret, str), "api.jwt is not a string"
    assert len(conf.api.jwt_secret) >= 64, "api.jwt_secret must be at least 64 characters long"

    ## Environment
    assert conf.environment.type in ["local", "development", "production"], f"environment.type is not valid. Was expecting local, development or production, got {conf.environment.type}"

    # TODO: Add more checks here
