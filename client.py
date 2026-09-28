"""CSP Channel Pipeline & Select Multiplexing Engine.
100% Python Standard Library.
"""

import collections

class CSPChannel:
    """Communicating Sequential Processes (CSP) Go-style channel."""
    def __init__(self, capacity=0):
        self.capacity = capacity
        self.queue = collections.deque()
        self.closed = False

    def send(self, val):
        if self.closed:
            raise RuntimeError("Cannot send to a closed channel")
        if self.capacity == 0:
            self.queue.append(val)
        elif len(self.queue) < self.capacity:
            self.queue.append(val)
            return True
        return False

    def recv(self):
        if self.queue:
            return self.queue.popleft(), True
        if self.closed:
            return None, False
        return None, None

    def close(self):
        self.closed = True

    @staticmethod
    def select(channels_to_read):
        for ch in channels_to_read:
            val, ok = ch.recv()
            if ok is not None:
                return ch, val, ok
        return None, None, None
