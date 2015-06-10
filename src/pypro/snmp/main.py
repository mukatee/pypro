__author__ = 'teemu kanstren'

import time

from pysnmp.entity.rfc3413.oneliner import cmdgen

import pypro.config as config
from pypro.snmp.loggers.es_network_logger import ESNetLogger
from pypro.snmp.loggers.es_file_logger import ESFileLogger
from pypro.snmp.loggers.csv_file_logger import CSVFileLogger
from pypro.snmp.loggers.mysql_logger import MySqlLogger


#resource OID's on linux: http://www.debianadmin.com/linux-snmp-oids-for-cpumemory-and-disk-statistics.html
#snmpwalk = get the whole subtree from given node
#snmpgetnext = get next for given value in tree. looping gives walk.

def init():
    global cmd_gen
    global loggers
    cmd_gen = cmdgen.CommandGenerator()
    loggers = []
    if (config.ES_FILE_ENABLED): loggers.append(ESFileLogger())
    if (config.ES_NW_ENABLED): loggers.append(ESNetLogger())
    if (config.MYSQL_ENABLED): loggers.append(MySqlLogger())
    if (config.CSV_ENABLED): loggers.append(CSVFileLogger())

    global pollers



def poll():
    for logger in loggers:
        logger.start()

    for poller in pollers:
        poller.poll(loggers)

    for logger in loggers:
        logger.commit()

def run_poller():
#    time_this("init:", init)
    init()
    while True:
        poll()
        time.sleep(config.INTERVAL)

if __name__ == "__main__":
    print ("start at:"+str(int(time.time())))
    run_poller()
