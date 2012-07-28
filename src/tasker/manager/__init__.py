import os
import sys
import logging
from optparse import OptionParser
from traceback import format_exc
from tasker.config import init_config
from tasker.config import get_config
from tasker.log import init_logger
from tasker.manager.consumer import Consumer


def main():
    parser = OptionParser()
    parser.add_option('-e', '--endpoint', help='set endpoint')
    parser.add_option('-m', '--mode', default='development', help='run mode [development|production]')
    parser.add_option('-t', '--tasktype', default='worker', help='set task type')

    options, args = parser.parse_args()  # @UnusedVariable
    if not options.endpoint:
        parser.error('missing endpoint')
    init_logger(options.mode)
    init_config(options.mode)

    config = get_config()
    if not options.tasktype in config.task_types:
        parser.error("tasktype '{0}' is not in {1}".format(options.tasktype, str(config.task_types)))
        return

    config.endpoint = options.endpoint

    log = logging.getLogger()
    log.info('start consumer: {0}'.format(options.tasktype))

    connectionHandler = None
    try:
        connectionHandler = Consumer(options.tasktype)
        connectionHandler.consume()
    except KeyboardInterrupt:
        log.info('stopped consumer by KeyboardInterrupt')
        sys.exit(0)
    except Exception, e:
        log.error('An exception occured: {0} "{1}" {2}'.format(
            e.__class__.__name__,
            str(e),
            format_exc()))
    finally:
        if connectionHandler:
            connectionHandler.close()

if __name__ == '__main__':
    main()
