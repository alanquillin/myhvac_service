import logging
import os
import eventlet
import eventlet.event
import eventlet.queue
import eventlet.semaphore
import eventlet.timeout
import eventlet.wsgi
from eventlet import websocket
import greenlet
import traceback


LOG = logging.getLogger(__name__)


getcurrent = eventlet.getcurrent
patch = eventlet.monkey_patch
sleep = eventlet.sleep
listen = eventlet.listen
connect = eventlet.connect


def spawn(*args, **kwargs):
    def _launch(func, *args, **kwargs):
        # Mimic gevent's default raise_error=False behaviour
        # by not propagating an exception to the joiner.
        try:
            func(*args, **kwargs)
        except TaskExit:
            pass
        except:
            # Log uncaught exception.
            # Note: this is an intentional divergence from gevent
            # behaviour; gevent silently ignores such exceptions.
            LOG.error('hub: uncaught exception: %s',
                      traceback.format_exc())

    return eventlet.spawn(_launch, *args, **kwargs)


def spawn_after(seconds, *args, **kwargs):
    def _launch(func, *args, **kwargs):
        # Mimic gevent's default raise_error=False behaviour
        # by not propagating an exception to the joiner.
        try:
            func(*args, **kwargs)
        except TaskExit:
            pass
        except:
            # Log uncaught exception.
            # Note: this is an intentional divergence from gevent
            # behaviour; gevent silently ignores such exceptions.
            LOG.error('hub: uncaught exception: %s',
                      traceback.format_exc())

    return eventlet.spawn_after(seconds, _launch, *args, **kwargs)


def kill(thread):
    thread.kill()


def joinall(threads):
    for t in threads:
        # This try-except is necessary when killing an inactive
        # greenthread.
        try:
            t.wait()
        except TaskExit:
            pass


Queue = eventlet.queue.LightQueue
QueueEmpty = eventlet.queue.Empty
Semaphore = eventlet.semaphore.Semaphore
BoundedSemaphore = eventlet.semaphore.BoundedSemaphore
TaskExit = greenlet.GreenletExit

WebSocketWSGI = websocket.WebSocketWSGI

Timeout = eventlet.timeout.Timeout

class Event(object):
    def __init__(self):
        self._ev = eventlet.event.Event()
        self._cond = False

    def _wait(self, timeout=None):
        while not self._cond:
            self._ev.wait()

    def _broadcast(self):
        self._ev.send()
        # Since eventlet Event doesn't allow multiple send() operations
        # on an event, re-create the underlying event.
        # Note: _ev.reset() is obsolete.
        self._ev = eventlet.event.Event()

    def is_set(self):
        return self._cond

    def set(self):
        self._cond = True
        self._broadcast()

    def clear(self):
        self._cond = False

    def wait(self, timeout=None):
        if timeout is None:
            self._wait()
        else:
            try:
                with Timeout(timeout):
                    self._wait()
            except Timeout:
                pass

        return self._cond