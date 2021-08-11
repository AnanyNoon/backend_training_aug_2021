from libfoo import ctx, messages
from jsql import sql

def set_kv(msg: messages.SetKeyValRequest):
    sql(ctx.conn, '''
        INSERT INTO key_val (ns, k, v)
        VALUES (:ns, :key, :val)
        ON DUPLICATE KEY UPDATE v=VALUES(v)
    ''', **msg.dict())

def get_kv(msg: messages.GetKeyRequest):
    return sql(ctx.conn, 'SELECT v FROM key_val WHERE k=:key', **msg.dict()).scalar()

