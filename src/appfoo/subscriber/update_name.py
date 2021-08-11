import logging

from . import subscriber
from libutil import util

logger = logging.getLogger(__name__)
engine_foo = util.get_engine('foo')


@subscriber.subscribe('foo_name_changed~foo', log_message=True)
def process_foo_name_changed(payload):
    assert payload['pk'], 'unable to find pk'
    id_foo = payload['pk']
    # do something with id_foo
    logger.info(f'processed {id_foo}')
