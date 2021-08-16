import logging
import os

import pytest
from jsql import sql

from tests import load_fixtures

logger = logging.getLogger(__name__)

@pytest.fixture()
def client():
    from fastapi.testclient import TestClient
    from appbar.web import app
    from noonutil.v1 import fastapiutil
    return fastapiutil.ClientProxy(TestClient(app))

@pytest.fixture(scope="session", autouse=True)
def engine_bar():
    from libutil import util
    engine = util.get_engine('bar')
    assert engine.url.database == f'bar'
    import libbar
    libbar.models.tables.create_all()
    return engine

@pytest.fixture(scope="session", autouse=True)
def engine_baz():
    from libutil import util
    engine = util.get_engine('baz')
    assert engine.url.database == f'baz'
    import libbaz
    libbaz.models.tables.create_all()
    return engine


