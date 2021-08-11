import logging
import time

from libutil import util
from . import workers

logger = logging.getLogger(__name__)
engine_foo = util.get_engine('foo')


def sync_foo():
    pass


@workers.register
def worker_sync_foo():
    logger.info("Worker sync_foo started")
    while True:
        sync_foo()
        time.sleep(60*30)
