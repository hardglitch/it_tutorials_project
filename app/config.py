from environs import Env

env = Env()
try:
    env.read_env()
    PG_HOST: str = env.str("PG_HOST")
    PG_PORT: int = env.int("PG_PORT")
    PG_USER: str = env.str("PG_USER")
    PG_NAME: str = env.str("PG_NAME")
    PG_PASS: str = env.str("PG_PASS")

    REDIS_HOST: str = env.str("REDIS_HOST")
    REDIS_PORT: int = env.int("REDIS_PORT")
    REDIS_PASS: str = env.str("REDIS_PASS")

    SECRET_KEY: str = env.str("SECRET_KEY")

    # GOOGLE_OAUTH_CLIENT_ID: str = env.str("GOOGLE_OAUTH_CLIENT_ID")
    # GOOGLE_OAUTH_CLIENT_SECRET: str = env.str("GOOGLE_OAUTH_CLIENT_SECRET")

except Exception:
    raise
