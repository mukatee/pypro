__author__ = 'teemu'

import time
from cpu_poller import CPUPoller
from mem_poller import MemPoller
from io_poller import IOPoller
from es_logger import ESLogger
from proc_poller import ProcPoller

interval = 1
es_logger = ESLogger(False, "session1")
proc_poller = ProcPoller(es_logger)
cpu_poller = CPUPoller(interval, proc_poller, es_logger)
mem_poller = MemPoller(proc_poller, es_logger)
io_poller = IOPoller(es_logger)

def run_poller():
    #int() converts argument to integer (string or float), in this case the float time
#    epoch = int(time.time())
    cpu_poller.poll()
    mem_poller.poll()
    io_poller.poll()

if __name__ == "__main__":
    while True:
        run_poller()
        time.sleep(interval)
