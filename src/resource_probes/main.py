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

#logger = ESNetLogger(True, "session2")
#logger1 = MySqlLogger()
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
    #int() converts argument to integer (string or float), in this case the float time
#    epoch = int(time.time())
    cpu_poller.poll()
    mem_poller.poll()
    io_poller.poll()

def run_poller():
    while True:
        poll()
        time.sleep(config.INTERVAL)

if __name__ == "__main__":
    print ("start at:"+str(int(time.time())))
    run_poller()
