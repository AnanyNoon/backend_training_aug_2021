__all__ = ['engine', 'ctx', 'Context', 'DomainException', 'models', 'domain']


class DomainException(Exception):
    def __init__(self, message, *, context=None):
        self.message = message
        self.context = context or ctx.get()
        super().__init__(message)


from libutil import util

engine = util.get_engine('baz')

from libbaz.context import ctx, Context
from libbaz import models, domain

