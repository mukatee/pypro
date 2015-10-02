__author__ = 'teemu kanstren'

import time

from pysnmp.entity.rfc3413.oneliner import cmdgen

import pypro.snmp.config as config
from pypro.snmp.loggers.es_network_logger import ESNetLogger
from pypro.snmp.loggers.es_file_logger import ESFileLogger
from pypro.snmp.loggers.csv_logger import CSVFileLogger
from pypro.snmp.loggers.influx_logger import InFluxLogger
from pypro.snmp.loggers.kafka_json_logger import KafkaJsonLogger
from pypro.snmp.loggers.kafka_avro_logger import KafkaAvroLogger
from pypro.snmp.snmp_poller import SNMPPoller

#resource OID's on linux: http://www.debianadmin.com/linux-snmp-oids-for-cpumemory-and-disk-statistics.html
#also http://kaivanov.blogspot.fi/2012/02/linux-snmp-oids-for-cpumemory-and-disk.html
#snmpwalk = get the whole subtree from given node
#snmpgetnext = get next for given value in tree. looping gives walk.

def init():
#    global cmd_gen
    global loggers
#    global oids
    snmp = cmdgen.CommandGenerator()
    loggers = []
    oids = []
    if (config.ES_FILE_ENABLED): loggers.append(ESFileLogger())
    if (config.ES_NW_ENABLED): loggers.append(ESNetLogger())
    if (config.CSV_ENABLED): loggers.append(CSVFileLogger())
    if (config.INFLUX_ENABLED): loggers.append(InFluxLogger())
    if (config.KAFKA_JSON_ENABLED): loggers.append(KafkaJsonLogger())
    if (config.KAFKA_AVRO_ENABLED): loggers.append(KafkaAvroLogger())

    global pollers
    pollers = []
    for oid in config.SNMP_OIDS:
        pollers.append(SNMPPoller(oid, snmp, loggers))
    epoch = int(time.time()*1000)
    for logger in loggers:
        logger.start(epoch)

def poll():
    for poller in pollers:
        poller.poll()

def run_poller():
#    time_this("init:", init)
    init()
    while True:
        poll()
        time.sleep(config.INTERVAL)
    shutdown()

def shutdown():
    epoch = int(time.time())
    for logger in loggers:
        logger.stop(epoch)

if __name__ == "__main__":
    print ("start at:"+str(int(time.time())))
    run_poller()
