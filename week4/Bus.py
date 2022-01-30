from readerwriterlock import rwlock

class Bus:
    def __init__(self):
        self.message = None
        self.lock = rwlock.RWLockWriteD()

    def read(self):
        with self.lock.gen_rlock():
            msg = self.message
        return msg

    def write(self, msg):
        with self.lock.gen_wlock():
            self.message = msg