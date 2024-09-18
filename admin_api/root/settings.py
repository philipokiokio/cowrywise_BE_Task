from .utils.base_schemas import AbstractSettings
from pydantic.networks import PostgresDsn, AmqpDsn


class Settings(AbstractSettings):
    postgres_url: PostgresDsn
    db_migration_env: bool = False
    ampq_url: AmqpDsn


print(Settings())
