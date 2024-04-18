from types import GeneratorType
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from tests.conftest import override_get_db


@patch('gymrat.db.db_setup.get_db', return_value=override_get_db())
def test_get_db(mock_get_db):
    # check if the function returns a generator
    db = mock_get_db()
    assert isinstance(db, GeneratorType)

    # check if the generator returns a session object
    session: Session = next(db)
    assert isinstance(session, Session)



