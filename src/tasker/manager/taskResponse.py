import json
from datetime import datetime
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from tasker.manager.storage import Base

taskResponseStatus = ['CREATED', 'FINISHED']
taskResponseErrorCodes = {1: 'General error'}


class TaskResponse(Base):

    __tablename__ = 'task_response'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.id'))
    endpoint = Column(String(50))
    status = Column(Integer, default=0)
    errnr = Column(Integer, default=0)
    errmsg = Column(String(50))
    payload = Column(MEDIUMTEXT, default='')
    start_time = Column(DateTime, nullable=True)
    last_modified_time = Column(DateTime, nullable=True)

    def __init__(self, task_id, endpoint):
        self.task_id = task_id
        self.endpoint = endpoint
        self.status = taskResponseStatus.index('CREATED')
        self.start_time = datetime.now()

    def __repr__(self):
        return "<TaskResponse('{0}', '{1}', '{2}')>".format(self.id, self.task_id, self.start_time)

    def to_dict(self):
        try:
            payload = json.loads(self.payload)
        except ValueError:
            payload = None
        return dict(
            id=self.id,
            task_id=self.task_id,
            endpoint=self.endpoint,
            status=self.status,
            errnr=self.errnr,
            errmsg=self.errmsg,
            payload=payload,
            start_time=str(self.start_time),
            last_modified_time=str(self.last_modified_time)
        )
