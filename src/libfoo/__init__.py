__all__ = ['engine', 'ctx', 'Context', 'DomainException', 'models', 'domain', 'messages']

class DomainException(Exception):
    def __init__(self, message, *, context=None):
        self.message = message
        self.context = context or ctx.get()
        super().__init__(message)


from libutil import util

engine = util.get_engine('foo')

from libfoo.context import ctx, Context
from libfoo import models, domain, messages

