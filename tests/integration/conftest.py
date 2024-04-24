from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from core.utils import _create_user, _create_exercise, _create_workout
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
    db = _test_session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def valid_jwt_token() -> dict[str, str]:
    token = create_access_token("1")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def first_superuser(get_test_db):
    return _create_user(get_test_db, 'admin', 'admin@mail.com', 'admin', True, True)


@pytest.fixture
def first_inactive_superuser(get_test_db):
    return _create_user(get_test_db, 'admin', 'admin@mail.com', 'admin', False, True)


@pytest.fixture
def first_user(get_test_db):
    return _create_user(get_test_db, 'user1', 'user1@mail.com', '111', True, False)


@pytest.fixture
def first_inactive_user(get_test_db):
    return _create_user(get_test_db, 'user1', 'user1@mail.com', '111', False, False)


@pytest.fixture
def create_users(get_test_db):
    _create_user(get_test_db, 'test1', 'test1@mail.com', '111',
                 True, False)
    _create_user(get_test_db, 'test2', 'test2@mail.com', '111',
                 True, False)


@pytest.fixture
def create_exercises(get_test_db, first_user, first_superuser):
    _create_exercise(get_test_db, first_user, 'testex1', 'eq1', 'legs',
                     'weight', 'intermediate')
    _create_exercise(get_test_db, first_superuser, 'testex2', 'eq2', 'arms',
                     'weight', 'beginner')
    _create_exercise(get_test_db, first_user, 'testex3', 'eq3', 'core',
                     'weight', 'expert')


@pytest.fixture
def create_workout(get_test_db, first_user, first_superuser):
    _create_workout(get_test_db, first_user, 'workout1', expires='2024-05-29')
    _create_workout(get_test_db, first_superuser, 'workout2', expires='2024-06-29')
    _create_workout(get_test_db, first_user, 'workout3', 'description', '2024-05-29')
