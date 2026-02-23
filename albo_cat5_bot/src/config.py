from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    user_agent: str = Field(
        default="AlboCat5ResearchBot/1.0 (+compliance-first outreach discovery)"
    )
    request_delay_seconds: float = 2.0
    timeout_seconds: float = 20.0
    save_raw_html: bool = False
    output_dir: str = "output"


settings = Settings()
