import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gymrat.config import get_settings
from gymrat.db.db_setup import get_db
from main import app

_test_settings = get_settings("test")

TEST_SQLALCHEMY_DATABASE_URL = (f"postgresql://{_test_settings.POSTGRES_USER}:{_test_settings.POSTGRES_PASSWORD}@"
                                f"{_test_settings.POSTGRES_HOST}:{_test_settings.POSTGRES_PORT}/{_test_settings.POSTGRES_DB}")


@pytest.fixture
def test_sqlalchemy_database_url():
    return TEST_SQLALCHEMY_DATABASE_URL


engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=False)


@pytest.fixture
def _engine():
    return engine


@pytest.fixture
def _test_session(_engine):
    return sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def override_get_db():
    db = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
