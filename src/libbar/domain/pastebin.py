from libutil import util
from libbar import ctx
from libbaz import Context as BazContext, domain as baz
from jsql import sql
import secrets
import pydantic


class UploadPastebin(util.NoonBaseModel):
    txt: str

    @pydantic.validator('txt')
    def must_less_than_1000_char(cls, txt):
        if len(txt) > 1000:
            raise ValueError('must be less than 1000 characters')
        return txt

    def execute(self):
        assert self.txt != 'illegal content', 'cant store illegal content'

        code = secrets.token_hex(16)
        sql(ctx.conn, '''
            INSERT INTO pastebin (code, txt)
            VALUES (:code, :txt)
        ''', code=code, **self.dict())
        return code


def get_pastebin(pastebin_code):
    return sql(ctx.conn, 'SELECT id_pastebin, txt FROM pastebin WHERE code=:pastebin_code', pastebin_code=pastebin_code).dict()


class GetPastebin(util.NoonBaseModel):
    # for exposure as an API
    pastebin_code: str

    def execute(self):
        pb = get_pastebin(self.pastebin_code)

        if not pb:
            return None

        # This accesses a different domain and
        # sets up its own DB connection etc.
        # The transaction running within this block
        # is completely unrelated to the transaction
        # (ctx.conn) running within get_pastebin(...)
        with BazContext.service():
            baz.counter.increment(pb['id_pastebin'])

        return pb['txt']

class GetPastebinViews(util.NoonBaseModel):
    # for exposure as an API
    pastebin_code: str

    def execute(self):
        pb = get_pastebin(self.pastebin_code)

        if not pb:
            return 0

        # This accesses a different domain and
        # sets up its own DB connection etc.
        # The transaction running within this block
        # is completely unrelated to the transaction
        # (ctx.conn) running within get_pastebin(...)
        with BazContext.service():
            return baz.counter.get_counter(id_counter=pb['id_pastebin'])

