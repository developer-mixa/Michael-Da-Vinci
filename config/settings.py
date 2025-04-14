from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_WEBHOOK_URL: str

    RABBIT_HOST: str = 'rabbitmq'
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

    MINIO_USER: str
    MINIO_PASSWORD: str
    MINIO_HOST: str

    SERVER_PORT: int

    USER_REGISTRATION_QUEUE_TEMPLATE: str = 'user_registration.{user_id}'

    REGISTRATION_EXCHANGE_NAME: str = 'registration_exchange'
    ACQUAINTANCE_EXCHANGE_NAME: str = 'acquaintance_exchange'
    UPDATE_USER_EXCHANGE_NAME: str = 'update_user_exchange'


    REGISTRATION_QUEUE_NAME: str = 'registration_queue'
    ACQUAINTANCE_QUEUE_NAME: str = 'acquaintance_queue'
    ACQUAINTANCE_LIKE_QUEUE_NAME: str = 'acquaintance_like_queue'
    UPDATE_USER_QUEUE_NAME: str = 'update_user_queue'
    LIKES_QUEUE_NAME: str = 'likes'

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DBNAME}"

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASSWORD}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"

    class Config:
        env_file = ".env"


settings = Settings()