from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Config(BaseSettings):
    app_name: str = "StockMate"
    debug: bool = False

    db_user: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = ""
    fmp_api_key: str = ""
    openai_api_key: str = ""

    @property
    def db_url(self) -> str:
        safe_password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{safe_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

config = Config()
