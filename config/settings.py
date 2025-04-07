from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_WEBHOOK_URL: str

    RABBIT_HOST: str = 'localhost' # rabbitmq
    RABBIT_PORT: int = 5672
    RABBIT_USER: str = 'guest'
    RABBIT_PASSWORD: str = 'guest'

    REDIS_HOST: str
    REDIS_PORT: str

    PG_USER: str
    PG_PASSWORD: str
    PG_DBNAME: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int

    SERVER_PORT: int

    USER_REGISTRATION_QUEUE_TEMPLATE: str = 'user_registration.{user_id}'
    REGISTRATION_EXCHANGE_NAME = 'registration_exchange'

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DBNAME}"

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"

    class Config:
        env_file = ".env"


settings = Settings()