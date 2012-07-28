import time


def handle_task(task, taskResponse):
    """ do something with the task ... and return TaskResponse obj """
    time.sleep(5)
    # set errnr / errmsg
    taskResponse.errnr = 32
    taskResponse.errmsg = 'could not backup!'
    return taskResponse
