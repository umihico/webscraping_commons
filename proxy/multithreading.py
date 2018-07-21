import queue
from threading import Thread
from time import sleep, time
from tqdm import tqdm


def proxy_thread(proxy, job_queue, submit_queue):
    failed_sleep_time = 0
    while True:
        try:
            job = job_queue.get_nowait()
        except queue.Empty:
            sleep(failed_sleep_time)
        else:
            try:
                submit_queue.put(job(proxy))
                job_queue.task_done()
            except (Exception, ) as e:
                job_queue.put(job)
                failed_sleep_time += 10
                sleep(failed_sleep_time)
            else:
                failed_sleep_time = 0
        if job_queue.unfinished_tasks == 0:
            return


class ProxyJob():
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, proxy):
        return self.func(proxy, *self.args, **self.kwargs)


def multithreading(proxies, jobs):
    """"
    for example
    func,url,url2,url3=*job
    result=func(given_proxy,url,url2,url3)
    """
    job_queue = queue.LifoQueue()
    submit_queue = queue.Queue()
    for raw_job in jobs:
        # func,url=*raw_job
        job = ProxyJob(*raw_job)
        job_queue.put(job)
    proxy_threads = []
    for proxy in proxies:
        args = (proxy, job_queue, submit_queue)
        t = Thread(target=proxy_thread, args=(*args,))
        t.daemon = True
        t.start()
        proxy_threads.append(t)
    total_job_size = len(jobs)
    tqdm_ = tqdm(total=total_job_size)
    prev_finished_tasks = 0
    submitted_last_time = time()
    while True:
        finished_tasks = submit_queue.qsize()
        current_job_size = job_queue.qsize()
        if time() - submitted_last_time > 60:
            break
        if current_job_size == 0 and finished_tasks == total_job_size:
            break
        buf = finished_tasks - prev_finished_tasks
        tqdm_.update(buf)
        if buf > 0:
            submitted_last_time = time()
        prev_finished_tasks = finished_tasks
        print({"job": current_job_size, "done": finished_tasks})
        sleep(1)
    print("current_job_size.qsize() is 0")
    # for t in proxy_threads:
    #     t.join()
    result = []
    while True:
        try:
            res = submit_queue.get_nowait()
            print(res)
            result.append(res)
        except queue.Empty:
            return result
