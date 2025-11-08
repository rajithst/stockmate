from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import ValidationError, field_validator
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

    # Authentication settings
    auth_secret_key: str = (
        "c2ec5943cf9a81b1e22f808a958ed1fac22b9f5f1dd92fef4e036e82226a0c18"
    )
    auth_algorithm: str = "HS256"
    auth_token_expire_minutes: int = 300

    @field_validator("db_user", "db_password", "db_name", "fmp_api_key")
    @classmethod
    def validate_required_fields(cls, v: str, info) -> str:
        if not v or v.strip() == "":
            raise ValueError(f"{info.field_name} is required and cannot be empty")
        return v

    @property
    def db_url(self) -> str:
        safe_password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{safe_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


try:
    config = Config()
except ValidationError as e:
    print(f"Configuration error: {e}")
    raise
