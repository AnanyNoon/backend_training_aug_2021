import logging

from fastapi import APIRouter

from libfoo import Context, domain, messages
from libutil import util
from noonutil.v1 import fastapiutil
from appfoo.web import g

logger = logging.getLogger(__name__)
router = APIRouter()

def check_is_customer():
    if g.customer_code:
        return True
    return "You must be logged in"

is_customer = fastapiutil.create_auth_decorator(check_is_customer)



@router.post('/keyval/set',
             summary='set key val',
             tags=['keyval'])
@is_customer()
def set_key_val(msg: messages.SetKeyValRequest):
    with Context.fastapi():
        domain.keyval.set_kv(msg)
    return "ok"

@router.post('/keyval/get',
             response_model=messages.GetKeyResponse,
             summary='get key val',
             tags=['keyval'])
@is_customer()
def set_key_val(msg: messages.GetKeyRequest):
    with Context.fastapi():
        val = domain.keyval.get_kv(msg)
        return messages.GetKeyResponse(val=val)

