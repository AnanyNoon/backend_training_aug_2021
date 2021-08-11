from eventpubsub import EventSubscriber
from noonutil.v1 import workerutil

consume_workers = workerutil.ThreadedWorkers()
subscriber = EventSubscriber('', consume_workers)

