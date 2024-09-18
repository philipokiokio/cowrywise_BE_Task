from .utils.base_schemas import AbstractSettings
from pydantic.networks import PostgresDsn, RedisDsn, AmqpDsn


class Settings(AbstractSettings):
    postgres_url: PostgresDsn
    redis_url: RedisDsn
    db_migration_env: bool = False
    ampq_url: AmqpDsn
