import logging
from tasker.manager.task import Task
from tasker.manager.storage import Storage

log = logging.getLogger()


class TaskStorage(Storage):
    """ this class is not *really* necessary, but makes the session handling easier """

    def get(self, task_id):
        task = self.session.query(Task).get(task_id)
        return task

    def get_by_identifier(self, task_ident):
        task = self.session.query(Task).filter_by(identifier=task_ident).first()
        return task

    def save(self, identifier, task_type, payload='', endpoints=''):
        task = Task(identifier, task_type, payload, endpoints)
        self.session.add(task)
        self.session.commit()
        return task

    def update(self, task):
        self.session.add(task)
        self.session.commit()
        return task

    def delete(self, task_id):
        task = self.get(task_id)
        if not task:
            return
        self.session.delete(task)
        self.session.commit()
