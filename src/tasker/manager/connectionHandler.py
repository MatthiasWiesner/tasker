import logging
from pika import PlainCredentials
from pika import ConnectionParameters
from pika.adapters import BlockingConnection
from tasker.config import config

log = logging.getLogger()


class ConnectionHandler(object):

    def __init__(self, task_type):
        self.task_type = task_type
        cfg = config['manager']['message_queue']
        credentials = PlainCredentials(cfg['username'], cfg['password'])
        parameters = ConnectionParameters(
            host=cfg['host'],
            port=cfg['port'],
            virtual_host=cfg['virtual_host'],
            credentials=credentials)

        conn = BlockingConnection(parameters)
        self.channel = conn.channel()

        self.exchange = '{0}.{1}'.format(
            cfg['exchange'],
            self.task_type)

        log.info("declare_exchange")
        self.channel.exchange_declare(
            exchange=self.exchange,
            type="fanout",
            passive=False,
            durable=False,
            auto_delete=False)
