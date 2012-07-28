import time


def handle_task(task, taskResponse):
    """ do something with the task ... and return TaskResponse obj """
    time.sleep(20)
    taskResponse.payload = dict(yeah=1234123, yiya="yippie")
    # set errnr / errmsg
    return taskResponse
