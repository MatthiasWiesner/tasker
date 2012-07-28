import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from tasker.manager.storage import Base

taskStatus = ['CREATED', 'SENT', 'DONE', 'INCOMPLETE']


class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(50))
    type = Column(String(20))
    status = Column(Integer, default=0)
    payload = Column(MEDIUMTEXT)
    endpoints = Column(MEDIUMTEXT)
    start_time = Column(DateTime, nullable=True)

    def __init__(self, identifier, task_type, payload='', endpoints=''):
        self.identifier = identifier
        self.type = task_type
        self.payload = str(payload)
        self.endpoints = endpoints
        self.status = taskStatus.index('CREATED')
        self.start_time = datetime.now()

    def __repr__(self):
        return "<Task('{0}', '{1}', '{2}', '{3}', '{4}')>".format(self.id, self.identifier, self.type, taskStatus[self.status], self.start_time)

    def to_dict(self):
        return dict(
            id=self.id,
            identifier=self.identifier,
            type=self.type,
            status=taskStatus[self.status],
            start_time=str(self.start_time),
            endpoints=json.loads(self.endpoints),
            payload=json.loads(self.payload)
        )
