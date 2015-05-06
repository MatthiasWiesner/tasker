import logging
import json
import urllib2
from optparse import OptionParser
from sqlalchemy.engine import create_engine
from tasker.log import init_logger
from tasker.manager.storage import Base
# import modules with table definitions
import tasker.manager.taskResponse  # @UnusedImport
import tasker.manager.task  # @UnusedImport
from tasker.config import init_config

log = logging.getLogger()


class RequestWithMethod(urllib2.Request):
    def __init__(self, method, *args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return self._method


def initialize_db(config):
    log.info("initialize database")
    engine = create_engine(config['manager']['db']['uri'], echo=config['manager']['db']['verbose'])
    Base.metadata.drop_all(engine)
    log.info("dropped all tables")
    Base.metadata.create_all(engine)
    log.info("created all tables")


def initialize_rabbitmq(config):
    log.info("initialize rabbitmq")
    passmanager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passmanager.add_password(None, config['rabbitmq']['apiurl'], config['rabbitmq']['username'], config['rabbitmq']['password'])
    auth_handler = urllib2.HTTPBasicAuthHandler(passmanager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    # reset rabbit
    try:
        r = RequestWithMethod('DELETE', url='{0}/users/{1}'.format(config['rabbitmq']['apiurl'], config['manager']['message_queue']['username']))
        urllib2.urlopen(r)
        log.info("deleted rabbitmq user")
    except urllib2.HTTPError as e:
        if e.code != 404:
            raise e

    delete_list = [
        '{0}/exchanges/vhosts/{1}',
        '{0}/queues/vhost/{1}',
        '{0}/bindings/vhost/{1}',
        '{0}/vhosts/{1}'
    ]
    delete_list = map(lambda x: x.format(config['rabbitmq']['apiurl'], config['manager']['message_queue']['virtual_host']), delete_list)

    for url in delete_list:
        try:
            r = RequestWithMethod('DELETE', url)
            urllib2.urlopen(r)
            log.info('delete: ' + url)
        except urllib2.HTTPError as e:
            log.info('nothing to delete: ' + url)
            if e.code != 404:
                raise e

    # create vhost
    r = RequestWithMethod('PUT', url='{0}/vhosts/{1}'.format(config['rabbitmq']['apiurl'], config['manager']['message_queue']['virtual_host']))
    r.add_header('Content-Type', 'application/json')
    urllib2.urlopen(r)
    log.info("created vhost")

    # create user
    data = {"password": config['manager']['message_queue']['password'], "tags": ""}
    r = RequestWithMethod('PUT', url='{0}/users/{1}'.format(config['rabbitmq']['apiurl'], config['manager']['message_queue']['username']), data=json.dumps(data))
    r.add_header('Content-Type', 'application/json')
    urllib2.urlopen(r)
    log.info("created user")

    # set permissions
    data = {"configure": ".*", "write": ".*", "read": ".*"}
    r = RequestWithMethod('PUT', url='{0}/permissions/{1}/{2}'.format(
        config['rabbitmq']['apiurl'], config['manager']['message_queue']['virtual_host'], config['manager']['message_queue']['username']), data=json.dumps(data))
    r.add_header('Content-Type', 'application/json')
    urllib2.urlopen(r)
    log.info("set permissions")


def main():
    parser = OptionParser()
    parser.add_option('-m', '--mode', default='development', help='development mode [development|production]')
    parser.add_option('-d', '--database', action="store_true", default=False, help='initialize database')
    parser.add_option('-r', '--rabbitmq', action="store_true", default=False, help='initialize rabbitmq')

    options, args = parser.parse_args()  # @UnusedVariable
    init_logger(options.mode)
    init_config(options.mode)

    if not(options.database or options.rabbitmq):
        parser.error('You should initialize at least one of database or rabbitmq')

    log.info('initialize database, rabbitmq')

    from tasker.config import config

    if options.database:
        initialize_db(config)
    if options.rabbitmq:
        initialize_rabbitmq(config)
