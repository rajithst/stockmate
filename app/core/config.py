import os
from urllib.parse import quote_plus

from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    auth_secret_key: str = ""
    auth_algorithm: str = "HS256"
    auth_token_expire_minutes: int = 300

    # Google Cloud Pub/Sub settings
    gcp_project_id: str = ""
    pubsub_company_sync_topic: str = "company-sync"
    pubsub_enabled: bool = False

    # Cloud SQL settings (optional, for Cloud Run)
    cloud_sql_instance: str = ""

    @field_validator("db_user", "db_password", "db_name", "fmp_api_key")
    @classmethod
    def validate_required_fields(cls, v: str, info) -> str:
        if not v or v.strip() == "":
            raise ValueError(f"{info.field_name} is required and cannot be empty")
        return v

    @property
    def db_url(self) -> str:
        safe_password = quote_plus(self.db_password)

        # If running on Cloud Run with Cloud SQL Auth Proxy (Unix Socket)
        if self.cloud_sql_instance:
            return (
                f"mysql+pymysql://{self.db_user}:{safe_password}"
                f"@/{self.db_name}?unix_socket=/cloudsql/{self.cloud_sql_instance}"
            )

        # Standard TCP connection (Localhost or Private IP)
        return (
            f"mysql+pymysql://{self.db_user}:{safe_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        # Load from a specific file if ENV_FILE is set (e.g. /secrets/stockmate-setting)
        # Otherwise default to .env for local development
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
    )


try:
    config = Config()
except ValidationError as e:
    print(f"Configuration error: {e}")
    raise
