import logging

from fastapi import APIRouter

from libbar import Context, domain
from libutil import util
from noonutil.v1 import fastapiutil

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post('/pastebin/create',
             summary='create pastebin',
             tags=['pastebin'])
def create_pastebin(msg: domain.pastebin.UploadPastebin):
    with Context.fastapi():
        return {"pastebin_code": msg.execute()}

@router.post('/pastebin/get',
             summary='get pastebin',
             tags=['pastebin'])
def get_pastebin(msg: domain.pastebin.GetPastebin):
    with Context.fastapi():
        return {'txt': msg.execute()}

@router.post('/pastebin/get_views',
             summary='get pastebin views',
             tags=['pastebin'])
def get_pastebin(msg: domain.pastebin.GetPastebinViews):
    with Context.fastapi():
        return {'views': msg.execute()}

