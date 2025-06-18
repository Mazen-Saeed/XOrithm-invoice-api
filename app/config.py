from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # environment variables
    POSTGRE_URL:       str
    ER_CONVERSION_URL:  str
    ER_SUPPORTED_URL:   str

settings = Settings()
