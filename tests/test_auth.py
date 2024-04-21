import pytest
from sqlalchemy import insert, select

from tests.conftest import client, async_session_maker
from src.country.models import country

def test_get():

    assert 1 == 1