import os
import yaml
from types import DictType


class Config(dict):

    def __init__(self, **kwargs):
        for k in kwargs:
            if type(kwargs[k]) == DictType:
                kwargs[k] = Config(**kwargs[k])
        dict.__init__(self, kwargs)
        self.__dict__ = self

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self

__config__ = None


def init_config(mode):
    global __config__
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '{0}.config.yaml'.format(mode)))
    s = open(path).read()
    s = s.format(**os.environ)
    data = yaml.load(s)
    __config__ = Config(**data)

def get_config():
    return __config__
