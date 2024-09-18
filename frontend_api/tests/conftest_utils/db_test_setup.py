import uuid
import psycopg2


class SqlDbTestConnector:
    """
    This class is used to create a temporary db for testing.
    We assume that a postgres docker build is running and exposed on port 6432.
    please pass respective param if diffirent from default.
    """

    def __init__(
        self,
        default_db: str = "postgres",
        user: str = "postgres",
        password: str = "password",
        host: str = "localhost",
        port: str = "6432",
        be_async: bool = True,
    ) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = f'A{str(uuid.uuid4()).replace("-", "")}Z'.lower()
        self.conn = psycopg2.connect(
            database=default_db, user=user, password=password, host=host, port=port
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        print(self.db_name)
        sql = f"""CREATE database {self.db_name};"""  # noqa: E703
        self.cursor.execute(sql)
        print("Database has been created successfully !!")
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{self.db_name}"
        if be_async:
            self.db_url = (
                f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{self.db_name}"
            )

    def get_db_url(self):
        return self.db_url

    def get_sync_db_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    def _drop_db(self):
        if not self.conn:
            self.conn = psycopg2.connect(
                database="postgres",
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )

        self.cursor = self.conn.cursor()

        sql = f"""DROP database {self.db_name} WITH (FORCE);"""  # noqa: E703
        self.cursor.execute(sql)
        print("Database has been dropped successfully !!")
        self.conn.close()
        self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._drop_db()
