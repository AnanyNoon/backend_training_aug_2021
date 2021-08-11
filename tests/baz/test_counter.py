from datetime import datetime
import pytest
from jsql import sql
from libbaz import Context, domain, ctx

def test_domain_pure_fn():
    with Context.service():
        assert domain.counter.get_counter(1) == 0
        assert domain.counter.increment(1) == 1
        assert domain.counter.increment(1) == 2
        assert domain.counter.increment(1) == 3
        assert domain.counter.decrement(1) == 2
        assert domain.counter.decrement(1) == 1
        assert domain.counter.decrement(1) == 0
        assert domain.counter.increment_by(1, 10) == 10
        assert domain.counter.decrement_by(1, 10) == 0

def test_domain_with_model_validation():
    with Context.service():
        counter = domain.counter.Counter(id_counter=1)
        assert counter.get_counter() == 0
        assert counter.increment() == 1
        assert counter.increment() == 2
        assert counter.increment() == 3

def test_exporting_function_from_model_to_module():
    with Context.service():
        counter = domain.counter.Counter(id_counter=1)
        sql(ctx.conn, "DELETE FROM counter")
        assert counter.value() == 0
        assert counter.increment() == 1
        assert counter.increment() == 2
        assert counter.value() == 2
        assert domain.counter.get_value(id_counter=1) == 2


def test_binding_func_to_model():
    with Context.service():
        counter = domain.counter.Counter(id_counter=1)
        sql(ctx.conn, "DELETE FROM counter")
        assert counter.value() == 0
        assert counter.increment() == 1
        assert counter.increment() == 2

        assert counter.value() == 2
        assert domain.counter.clear(id_counter=1) is None
        assert counter.value() == 0

        assert counter.increment() == 1
        assert counter.increment() == 2

        assert counter.value() == 2
        assert counter.clear() is None
        assert counter.value() == 0

def test_views(client):
    response = client.post(
        '/counter/get',
        json={
            "idCounter": 1,
        },
    )
    res = response.json()
    assert res['value'] == 0

    response = client.post(
        '/counter/increment',
        json={
            "idCounter": 1,
        },
    )
    res = response.json()
    assert res['value'] == 1

    response = client.post(
        '/counter/increment',
        json={
            "idCounter": 1,
            "by": -1
        },
    )
    res = response.json()
    assert res['value'] == 0


def test_wrong_request(client):
    response = client.post(
        '/counter/get',
        json={
            "something": "unrelated",
        },
        assert_status=400
    )