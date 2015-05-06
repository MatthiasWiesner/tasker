import os
import yaml
from types import DictType

config = None


def init_config(mode):
    global config
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '{0}.config.yaml'.format(mode)))
    s = open(path).read()
    s = s.format(**os.environ)
    config = yaml.safe_load(s)
