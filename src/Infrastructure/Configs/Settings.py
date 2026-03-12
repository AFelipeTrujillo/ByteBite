import os
from dotenv import load_dotenv


class Settings:

    def __init__(self):
        load_dotenv()

        self.APP_NAME = self._get_env("APP_NAME", "ByteBite API")
        self.APP_DESCRIPTION = self._get_env("APP_DESCRIPTION", "Recipe Management and Weekly Shopping List Generator")
        self.APP_VERSION = self._get_env("APP_VERSION", "v1.0.2")
        self.MONGO_URI = self._get_env("MONGO_URI", "mongodb://localhost:27017/")
        self.MONGO_DB_NAME = self._get_env("MONGO_DB_NAME", "bytebite_db")
        self.JWT_SECRET: str = "tu_clave_secreta_super_segura"
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    def _get_env(self, key: str, default: str = None) -> str:
        value = os.getenv(key=key, default=default)
        if value is None:
            raise ValueError(f"Missing mandatory environment variable: {key}")
        return value


settings = Settings()
