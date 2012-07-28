import time
import json
import logging
import tornado.web
from tasker.manager.taskStorage import TaskStorage
from tasker.manager.taskResponseStorage import TaskResponseStorage
from tasker.manager.producer import enqueue_task
from tasker.manager.task import taskStatus
from tasker.config import get_config
log = logging.getLogger()


class TaskHandler(tornado.web.RequestHandler):

    def get(self, task_id):
        taskStorage = TaskStorage()
        taskResponseStorage = TaskResponseStorage()
        task = taskStorage.get(task_id)
        if task:
            taskResponseList = taskResponseStorage.get_by_task(task.id)
            log.info('get task: {0}'.format(task.to_dict()))
            result = dict(
                task=task.to_dict(),
                taskResponseList=[tr.to_dict() for tr in taskResponseList])
        else:
            result = None

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))

    def post(self):
        config = get_config()
        data = json.loads(self.request.body)
        if not data['identifier']:
            self.send_error(500)
        if not 'payload' in data:
            data['payload'] = ''
        if not 'endpoints' in data:
            data['endpoints'] = []
        data['task_type'] = self.task_type

        storage = TaskStorage()
        task = storage.save(
            data['identifier'],
            data['task_type'],
            json.dumps(data['payload']),
            json.dumps(data['endpoints']))
        enqueue_task(task)
        task.status = taskStatus.index('SENT')
        storage.update(task)

        if data['endpoints']:
            endpoint_set = set(data['endpoints'])
            taskResponseStorage = TaskResponseStorage()
            all_received = False
            for _i in range(config.api.wait_for_endpoints_timeout * 2):
                taskResponseList = taskResponseStorage.get_by_task(task.id)
                received_set = set([tr.endpoint for tr in taskResponseList])
                if endpoint_set.issubset(received_set):
                    all_received = True
                    break
                time.sleep(0.5)
            if not all_received:
                task.status = taskStatus.index('INCOMPLETE')
            else:
                task.status = taskStatus.index('DONE')
            storage.update(task)

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(task.to_dict()))
