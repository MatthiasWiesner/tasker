import pickle
import logging
from tasker.manager.connectionHandler import ConnectionHandler
from tasker.manager.task import Task  # @UnusedImport

log = logging.getLogger()


class Producer(ConnectionHandler):

    def __init__(self, task_type, message):
        self.message = message
        super(Producer, self).__init__(task_type)

    def send_message(self):
        self.channel.basic_publish(
            body=self.message,
            exchange=self.exchange,
            routing_key="")
        log.info("channel.basic_publish to exchange: {0}".format(self.exchange))


def enqueue_task(task):
    message = pickle.dumps(task)
    connectionHandler = Producer(task.type, message)
    connectionHandler.send_message()
