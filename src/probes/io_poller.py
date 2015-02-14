__author__ = 'teemu kanstren'

import psutil
import time
from file_logger import FileLogger

class IOPoller:
    def __init__(self, *loggers):
        self.loggers = loggers

    def poll_system(self, epoch):
        #TODO: per NIC data
        net_counters = psutil.net_io_counters()
        bytes_sent = net_counters.bytes_sent
        bytes_recv = net_counters.bytes_recv
        packets_sent = net_counters.packets_sent
        packets_recv = net_counters.packets_recv
        errin = net_counters.errin
        errout = net_counters.errout
        dropin = net_counters.dropin
        dropout = net_counters.dropout
        for logger in self.loggers:
            logger.io_sys(epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)

    def poll(self):
        # int() converts argument to integer (string or float), in this case the float time
        epoch = int(time.time())
        epoch *= 1000
        self.poll_system(epoch)

if __name__ == "__main__":
    file = FileLogger(True)
    io_poller = IOPoller(file)
    while (True):
        io_poller.poll()
        time.sleep(1)
    file.close()