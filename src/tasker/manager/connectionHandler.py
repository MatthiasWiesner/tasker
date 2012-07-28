import logging
from pika import PlainCredentials
from pika import ConnectionParameters
from pika.adapters import BlockingConnection
from tasker.config import get_config

log = logging.getLogger()


class ConnectionHandler(object):

    def __init__(self, task_type):
        self.task_type = task_type
        self.config = get_config()
        config = self.config.manager.message_queue
        credentials = PlainCredentials(config.username, config.password)
        parameters = ConnectionParameters(
            host=config.host,
            port=config.port,
            virtual_host=config.virtual_host,
            credentials=credentials)

        conn = BlockingConnection(parameters)
        self.channel = conn.channel()

        self.exchange = '{0}.{1}'.format(
            self.config.manager.message_queue.exchange,
            self.task_type)

        log.info("declare_exchange")
        self.channel.exchange_declare(
            exchange=self.exchange,
            type="fanout",
            passive=False,
            durable=False,
            auto_delete=False)
