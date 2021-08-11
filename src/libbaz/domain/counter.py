from libutil import util
from libbaz import ctx
from jsql import sql

def increment(id_counter):
    return increment_by(id_counter, 1)

def decrement(id_counter):
    return increment_by(id_counter, -1)

def increment_by(id_counter, by=1):
    create_counter(id_counter)
    sql(ctx.conn, "UPDATE counter SET value = value + :by WHERE id_counter = :id_counter", id_counter=id_counter, by=by)
    return get_counter(id_counter)

def decrement_by(id_counter, by=1):
    return increment_by(id_counter, -1 * by)

def create_counter(id_counter):
    sql(ctx.conn, "INSERT IGNORE INTO counter (id_counter, value) VALUES(:id_counter, 0)", id_counter=id_counter)

def get_counter(id_counter):
    return sql(ctx.conn, "SELECT value FROM counter WHERE id_counter = :id_counter", id_counter=id_counter).scalar() or 0

def clear(id_counter):
    sql(ctx.conn, "UPDATE counter SET value = 0 WHERE id_counter = :id_counter", id_counter=id_counter)

class Counter(util.NoonBaseModel):
    # For exposing the counter via HTTP
    # with validation by pydantic
    id_counter: int

    def value(self):
        return sql(ctx.conn, "SELECT value FROM counter WHERE id_counter = :id_counter", id_counter=self.id_counter).scalar() or 0

    clear = util.bind(clear)

class IncrementCounterBy(util.NoonBaseModel):
    # For exposing the counter via HTTP
    # with validation by pydantic
    id_counter: int
    by: int = 1

Counter.bind(increment)
Counter.bind(get_counter)
IncrementCounterBy.bind(increment_by)

get_value = util.unbind(Counter.value, Counter)

