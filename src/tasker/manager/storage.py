from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tasker.config import get_config

Base = declarative_base()


class Storage(object):

    def __init__(self):
        config = get_config()
        engine = create_engine(config.manager.db.uri, echo=config.manager.db.verbose)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()
