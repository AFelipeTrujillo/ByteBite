import os
from dotenv import load_dotenv


class Settings:

    def __init__(self):
        load_dotenv()

        self.MONGO_URI = self._get_env("MONGO_URI", "mongodb://localhost:27017/")
        self.MONGO_DB_NAME = self._get_env("MONGO_DB_NAME", "bytebite_db")

    def _get_env(self, key: str, default: str = None) -> str:
        value = os.getenv(key=key, default=default)
        if value is None:
            raise ValueError(f"Missing mandatory environment variable: {key}")
        return value


settings = Settings()
