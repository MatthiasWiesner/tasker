import os
import yaml
from logging.config import dictConfig


def init_logger(mode):
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '{0}.log.yaml'.format(mode)))
    f = open(path).read()
    config = yaml.load(f)
    dictConfig(config)


