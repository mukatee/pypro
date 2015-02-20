__author__ = 'teemu'

import time
import config
from cpu_poller import CPUPoller
from mem_poller import MemPoller
from io_poller import IOPoller
from es_network_logger import ESNetLogger
from es_file_logger import ESFileLogger
from csv_file_logger import CSVFileLogger
from proc_poller import ProcPoller
from mysql_logger import MySqlLogger

#logger = ESNetLogger(True, "session2")
#logger1 = MySqlLogger()
logger1 = ESFileLogger()
logger2 = CSVFileLogger()
proc_poller = ProcPoller(logger1, logger2)
cpu_poller = CPUPoller(proc_poller, logger1, logger2)
mem_poller = MemPoller(proc_poller, logger1, logger2)
io_poller = IOPoller(logger1, logger2)

def run_poller():
    #int() converts argument to integer (string or float), in this case the float time
#    epoch = int(time.time())
    cpu_poller.poll()
    mem_poller.poll()
    io_poller.poll()

if __name__ == "__main__":
    print (time.time())
    while True:
        run_poller()
        time.sleep(config.INTERVAL)
