__author__ = 'teemu'

import time
import resource_probes.config as config
from resource_probes.cpu_poller import CPUPoller
from resource_probes.mem_poller import MemPoller
from resource_probes.io_poller import IOPoller
from resource_probes.es_network_logger import ESNetLogger
from resource_probes.es_file_logger import ESFileLogger
from resource_probes.csv_file_logger import CSVFileLogger
from resource_probes.proc_poller import ProcPoller
from resource_probes.mysql_logger import MySqlLogger

def init():
    global loggers
    global proc_poller
    global cpu_poller
    global mem_poller
    global io_poller

    loggers = []
    if (config.ES_FILE_ENABLED): loggers.append(ESFileLogger())
    if (config.ES_NW_ENABLED): loggers.append(ESNetLogger())
    if (config.MYSQL_ENABLED): loggers.append(MySqlLogger())
    if (config.CSV_ENABLED): loggers.append(CSVFileLogger())
    proc_poller = ProcPoller(loggers)
    cpu_poller = CPUPoller(proc_poller, loggers)
    mem_poller = MemPoller(proc_poller, loggers)
    io_poller = IOPoller(loggers)

def poll():
    for logger in loggers:
        logger.start()
#    time_this("cpu:", cpu_poller.poll)
#    time_this("mem:", mem_poller.poll)
#    time_this("io:", io_poller.poll)
    cpu_poller.poll()
    mem_poller.poll()
    io_poller.poll()
    for logger in loggers:
        logger.commit()

def run_poller():
#    time_this("init:", init)
    init()
    while True:
        poll()
        time.sleep(config.INTERVAL)

def time_this(pre, f):
    "Runs parameter function f() and measures the time it takes"
    before = int(time.time()*1000)
    f()
    after = int(time.time()*1000)
    diff = after - before
    print(pre+str(diff))

if __name__ == "__main__":
    print ("start at:"+str(int(time.time())))
    run_poller()
