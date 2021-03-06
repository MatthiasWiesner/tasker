import imp
import json
import pickle
import logging
from tasker.manager.connectionHandler import ConnectionHandler
from tasker.manager.taskStorage import TaskStorage
from tasker.manager.taskResponseStorage import TaskResponseStorage
from tasker.manager.task import Task  # @UnusedImport
from tasker.manager.task import taskStatus
import tasker.manager.handler
from tasker.manager.taskResponse import taskResponseStatus
from tasker.config import config

log = logging.getLogger()


class Consumer(ConnectionHandler):

    def __init__(self, task_type):
        super(Consumer, self).__init__(task_type)

    def consume(self):
        log.info('receive')

        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(
            exchange=self.exchange,
            queue=queue_name)

        self.channel.basic_consume(
            self.handle_delivery,
            queue=queue_name)

        self.channel.start_consuming()

    def handle_delivery(self, channel, method, header, body):
        try:
            task = pickle.loads(body)
        except KeyError:
            log.error('received body could not loaded')
            return
        finally:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

        # access task.id to check
        try:
            assert type(task) == Task
        except:
            log.error('received message is not a task')
            return
        taskStorage = TaskStorage()
        task = taskStorage.update(task)
        log.info('received message {0}'.format(task))

        taskResponseStorage = TaskResponseStorage()
        taskResponse = taskResponseStorage.save(task.id, config['endpoint'])

        # load and run handler module
        try:
            f, filename, description = imp.find_module(task.type, tasker.manager.handler.__path__)
        except ImportError:
            log.error('unknown tasktype')
            return
        handler = imp.load_module(task.type, f, filename, description)
        taskResponse = handler.handle_task(task, taskResponse)

        if taskResponse.payload:
            taskResponse.payload = json.dumps(taskResponse.payload)
        taskResponse.status = taskResponseStatus.index('FINISHED')
        taskResponseStorage.update(taskResponse)
        task = taskStorage.update(task)

        # update task status, if all endpoint are finished
        if task.endpoints and task.status == taskStatus.index('SENT'):
            endpoint_set = set(json.loads(task.endpoints))
            if self._endpoints_completed(endpoint_set, task):
                task.status = taskStatus.index('DONE')
                taskStorage.update(task)

    def close(self):
        self.channel.basic_cancel(consumer_tag="Consumer.{0}".format(self.exchange))
        self.channel.stop_consuming()

    def _endpoints_completed(self, endpoint_set, task):
        taskResponseStorage = TaskResponseStorage()
        taskResponseList = taskResponseStorage.get_by_task(task.id)
        received_set = set([tr.endpoint for tr in taskResponseList if tr.status == taskResponseStatus.index('FINISHED')])
        return endpoint_set.issubset(received_set)
