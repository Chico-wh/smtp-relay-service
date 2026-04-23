from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # SMTP Hostinger
    smtp_host: str = "smtp.hostinger.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_pass: str
    smtp_from: str = "no_reply@reuzz.online"
    smtp_from_name: str = "Allugi"

    # Segurança
    api_key: str  # chave que o Django vai mandar no header

    # Ambiente
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()