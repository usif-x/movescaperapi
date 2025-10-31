class Settings:
    DEBUG: bool = True
    TESTING: bool = False
    TIMEOUT: int = 10


def get_settings():
    return Settings()


class ArabSeedEndpoints:
    URL: str = "https://a.asd.homes"
    HOME = "/main0"
    FILMS = "/movies/"
    NETFLIX_FILMS = "/category/netfilx/افلام-netfilx/"


def get_arabseed_endpoints():
    return ArabSeedEndpoints()
