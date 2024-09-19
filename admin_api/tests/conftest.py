from sqlalchemy import create_engine
from ..root.settings import Settings

import pytest
from unittest.mock import patch
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from root.utils.abstract_base import AbstractBase
from tests.conftest_utils.db_test_setup import SqlDbTestConnector
import asyncio
import logging

LOGGER = logging.getLogger(__name__)


base_pg_url = str(Settings().postgres_url).split("://")[1].split("/")[0]
pg_props = base_pg_url.split(":")
pg_username, pg_password = pg_props[0], pg_props[1].split("@")[0]
pg_host, pg_port = pg_props[1].split("@")[1], pg_props[-1]


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def db_connector():
    with SqlDbTestConnector(
        user=pg_username, password=pg_password, host=pg_host, port=pg_port
    ) as connector:
        yield connector


@pytest.fixture()
async def setup_test_db(db_connector):
    engine = create_engine(db_connector.get_sync_db_url(), echo=True)
    LOGGER.info("Creating tables...")
    AbstractBase.metadata.create_all(engine)

    LOGGER.info(db_connector.get_sync_db_url())

    engine = create_async_engine(url=db_connector.get_db_url(), echo=True)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(setup_test_db):
    async_session = async_sessionmaker(bind=setup_test_db, expire_on_commit=False)
    async with async_session() as session:

        with patch(
            "database.db_handlers.user_db_handler.async_session"
        ) as mock_session:
            mock_session.return_value = session
            with patch(
                "database.db_handlers.book_db_handler.async_session"
            ) as mock_session:
                mock_session.return_value = session
                yield
