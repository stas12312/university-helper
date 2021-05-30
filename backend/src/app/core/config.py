from typing import Optional, Any

from pydantic import BaseSettings, AnyHttpUrl, validator, EmailStr


class Settings(BaseSettings):
    SECRET_KEY: str  # = secrets.token_urlsafe(32)
    START_BALANCE: int = 100
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    API_V1_STR: str = '/api/v1'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SYNC_SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f'postgresql+asyncpg://{values.get("POSTGRES_USER")}:{values.get("POSTGRES_PASSWORD")}' \
               f'@{values.get("POSTGRES_SERVER")}/{values.get("POSTGRES_DB")}'

    @validator("SYNC_SQLALCHEMY_DATABASE_URI", pre=True)
    def sync_assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f'postgresql://{values.get("POSTGRES_USER")}:{values.get("POSTGRES_PASSWORD")}' \
               f'@{values.get("POSTGRES_SERVER")}/{values.get("POSTGRES_DB")}'

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/src/app/email-templates/"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        case_sensitive = True


settings = Settings()
