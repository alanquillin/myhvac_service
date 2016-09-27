import threading
import time


def spawn(*args, **kwargs):
    def _launch(func, *args, **kwargs):
        func(*args, **kwargs)
    t = threading.Thread(target=_launch, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
    return t


def kill(thread):
    thread.terminate()


def killall(threads):
    for t in threads:
        kill(t)


def join(thread):
    thread.join()


def joinall(threads):
    for t in threads:
        join(t)


sleep = time.sleep
