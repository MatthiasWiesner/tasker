import logging
from datetime import datetime
from tasker.manager.taskResponse import TaskResponse
from tasker.manager.storage import Storage

log = logging.getLogger()


class TaskResponseStorage(Storage):
    """ this class is not *really* necessary, but makes the session handling easier """

    def get(self, taskResponse_id):
        taskResponse = self.session.query(TaskResponse).get(taskResponse_id)
        return taskResponse

    def get_by_task(self, task_id):
        taskResponseList = self.session.query(TaskResponse).filter(TaskResponse.task_id == task_id)
        return [taskResponse for taskResponse in taskResponseList]

    def save(self, task_id, endpoint):
        taskResponse = TaskResponse(task_id, endpoint)
        self.session.add(taskResponse)
        self.session.commit()
        return taskResponse

    def update(self, taskResponse):
        taskResponse.last_modified_time = datetime.now()
        self.session.add(taskResponse)
        self.session.commit()
        return taskResponse

    def delete(self, taskResponse_id):
        taskResponse = self.get(taskResponse_id)
        if not taskResponse:
            return
        self.session.delete(taskResponse)
        self.session.commit()
