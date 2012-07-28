import os
import sys
import logging
from optparse import OptionParser

import tornado.ioloop

from tasker.config import init_config
from tasker.config import get_config
from tasker.log import init_logger
from tasker.api.taskHandler import TaskHandler


def run():
    config = get_config()
    app_list = []

    for task_type in config.task_types:
        # define for every task_type a taskHandler class
        clazz = type('{0}TaskHandler'.format(task_type.capitalize()),
            (TaskHandler,), {'task_type': task_type})
        app_list.append((r"/{0}".format(task_type), clazz))
        app_list.append((r"/{0}/([0-9]+)".format(task_type), clazz))

    application = tornado.web.Application(app_list)
    application.listen(config.api.port)
    tornado.ioloop.IOLoop.instance().start()


def main():
    parser = OptionParser()
    parser.add_option('-m', '--mode', default='development', help='development mode [development|production]')

    options, args = parser.parse_args()  # @UnusedVariable
    init_logger(options.mode)
    init_config(options.mode)

    log = logging.getLogger()
    log.info('start api')

    try:
        run()
    except KeyboardInterrupt:
        log.info('stopped api by KeyboardInterrupt')
        sys.exit(0)


if __name__ == '__main__':
    main()
