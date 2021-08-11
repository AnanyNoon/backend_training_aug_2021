import logging

from fastapi import APIRouter

from libbaz import Context, domain
from libutil import util
from noonutil.v1 import fastapiutil

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post('/counter/get',
             summary='get counter',
             tags=['counter'])
def get_counter(msg: domain.counter.Counter):
    with Context.fastapi():
        return {"value": msg.get_counter()}

@router.post('/counter/increment',
             summary='increment counter by',
             tags=['counter'])
def increment_counter_by(msg: domain.counter.IncrementCounterBy):
    with Context.fastapi():
        return {"value": msg.increment_by()}