import logging
import os

import pytest
from jsql import sql

from tests import load_fixtures

logger = logging.getLogger(__name__)

@pytest.fixture()
def client():
    from fastapi.testclient import TestClient
    from appfoo.web import app
    from noonutil.v1 import fastapiutil
    return fastapiutil.ClientProxy(TestClient(app))

@pytest.fixture(scope="session", autouse=True)
def engine_foo():
    from libutil import util
    engine = util.get_engine('foo')
    assert engine.url.database == f'testfoo'
    import libfoo
    libfoo.models.tables.create_all()
    return engine

# Once for every test file, we rebuild the DB
# with fixtures
@pytest.fixture(scope="session", autouse=True)
def setup(engine_foo):
    import libfoo
    libfoo.models.tables.create_all()
    fixtures(engine_foo)

# This is done so that every test relies on the fact
# that the main fixtures are the only data it should
# expect on the DB
@pytest.fixture(autouse=True)
def clear_db(engine_foo):
    #sql(engine_foo, "TRUNCATE TABLE review")
    fixtures(engine_foo)

def fixtures(engine):
    from libfoo.models import tables
    load_fixtures.load_fixtures('/src/tests/foo/data/fixtures.toml', engine, tables)


