from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from gymrat.config import get_settings
from gymrat.db.db_setup import Base
from main import app
from security import create_access_token
from tests.conftest import engine, _test_session


@pytest.fixture(scope='function', autouse=True)
def set_up_and_tear_down():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception:
        print('Something went wrong')
        pass

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_settings():
    return get_settings('test')


@pytest.fixture
def subject():
    return 'user1'


@pytest.fixture
def expires_delta():
    return timedelta(minutes=30)


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def get_test_db(_test_session):
    db = _test_session
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def create_valid_jwt_token():
    token = create_access_token('111')
    return f'Bearer23 {token}'

