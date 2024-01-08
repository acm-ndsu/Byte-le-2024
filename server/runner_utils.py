from queue import Queue


def worker_main(jobqueue: Queue):
    while not jobqueue.empty():
        job_func = jobqueue.get()
        job_func[0](*job_func[1:])
        jobqueue.task_done()
