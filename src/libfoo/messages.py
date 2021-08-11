from datetime import datetime
from typing import List

from pydantic import validator, conint

from libutil import util


class SetKeyValRequest(util.NoonBaseModel):
    ns: str
    key: str
    val: str

    @validator('val')
    def must_less_than_1000_char(cls, val):
        if len(val) > 1000:
            raise ValueError('must be less than 1000 characters')
        return val

class GetKeyRequest(util.NoonBaseModel):
    ns: str
    key: str

class GetKeyResponse(util.NoonBaseModel):
    val: str


