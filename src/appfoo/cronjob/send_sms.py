import logging

from libutil import util

logger = logging.getLogger(__name__)
engine_foo = util.get_engine('foo')


def send_sms():
    pass


if __name__ == "__main__":
    logger.info("Cron job to send sms started")
    send_sms()
    logger.info("Cron job to send sms ended")
