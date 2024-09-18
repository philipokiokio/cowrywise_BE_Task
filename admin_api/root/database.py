from alembic import command
from alembic.config import Config
from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from root.settings import Settings
from root.utils.abstract_base import AbstractBase

settings = Settings()
engine = create_async_engine(url=str(settings.postgres_url))

async_session = async_sessionmaker(engine, expire_on_commit=False)


def create_migration():
    if settings.db_migration_env:
        # Initialize Alembic configuration
        alembic_ini_path = "alembic.ini"
        alembic_config = Config(alembic_ini_path)

        metadata = MetaData()
        postgres_url = str(settings.postgres_url).split("//")

        metadata.reflect(
            bind=create_engine(
                url=f"postgresql://{postgres_url[-1]}",
            )
        )

        existing_tables = set(metadata.tables.keys())
        defined_tables = set(AbstractBase.metadata.tables.keys())

        changed_columns = []
        table_names = []
        print("New tables found:", list(defined_tables - existing_tables))
        new_table = list(defined_tables - existing_tables)

        message = "_".join(new_table)
        if list(defined_tables - existing_tables):

            # Generate migration script
            command.revision(config=alembic_config, autogenerate=True, message=message)
            command.upgrade(alembic_config, "head")
        else:

            for table_name, table in AbstractBase.metadata.tables.items():
                existing_columns = {
                    c.name: c for c in inspect(metadata.tables[table_name]).c
                }
                defined_columns = {c.name: c for c in table.c}

                # Check for changes in columns
                for column_name, column in defined_columns.items():
                    if column_name not in existing_columns or not isinstance(
                        existing_columns[column_name].type, type(column.type)
                    ):
                        table_names.append(table_name)
                        changed_columns.append(column_name)
                        print(changed_columns)

        if changed_columns:
            message = (
                f"Columns changed in table { '_'.join(table_names)}:"
                f" {', '.join(changed_columns)}"
            )

            # Generate migration script
            command.revision(config=alembic_config, autogenerate=True, message=message)
            command.upgrade(alembic_config, "head")
        else:
            print("No new changes found.")
