from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    openai_key: str
    groq_key: str
    hatchet_client_token: str
    hatchet_client_tls_strategy: str
