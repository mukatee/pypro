__author__ = 'teemu kanstren'

#http://www.mibdepot.com/cgi-bin/getmib3.cgi?i=1&n=UCD-SNMP-MIB&r=f5&f=UCD-SNMP-MIB&v=v2&t=tree

import pypro.snmp.config as config
from pypro.snmp.oids.oid import OID
from pypro.snmp.oids.oid import OID_Type
import pypro.snmp.main as main

config.SESSION_NAME = "session2"
config.ES_INDEX = "pypro-snmp"
config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = False
config.CSV_ENABLED = True
config.KAFKA_AVRO_ENABLED = True
config.KAFKA_TOPIC = "pypro"
config.KAFKA_SERVER = "localhost"
config.PRINT_CONSOLE = True
config.SNMP_AUTH = False

#example for querying whatever OID you like
config.SNMP_OIDS.append(OID('1.3.6.1.2.1.1.3.0', 'system uptime', 'public', '192.168.2.1', 161, 'router', OID_Type.int))
#following are examples of the buildin OID to query
#raw user space cpu time
config.SNMP_OIDS.append(UserCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
#percentage of user space cpu time
config.SNMP_OIDS.append(UserCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#raw system cpu time
config.SNMP_OIDS.append(SystemCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
#percentage of system time
config.SNMP_OIDS.append(SystemCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#raw idle cpu time
config.SNMP_OIDS.append(IdleCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
#percentage of idle time
config.SNMP_OIDS.append(IdleCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#total ram in system
config.SNMP_OIDS.append(RamTotal('public', '192.168.2.1', 161, 'router'))
#total ram free
config.SNMP_OIDS.append(RamFree('public', '192.168.2.1', 161, 'router'))
#available disk space, requires modifying snmp config on host
config.SNMP_OIDS.append(DiskTotal('public', '192.168.2.1', 161, 'router'))
#used disk space, requires modifying snmp.config on host
config.SNMP_OIDS.append(DiskUsed('public', '192.168.2.1', 161, 'router'))
#bytes in (network interface 1, the last number..)
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 1))
#bytes out (network interface 1, the last number..)
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 1))
#used memory. counted as total-available
config.SNMP_OIDS.append(RamUsed('public', '192.168.2.1', 161, 'router'))

main.run_poller()

#example getting bytes received for all interfaces
#snmpwalk -v2c -c public 192.168.2.1 1.3.6.1.2.1.31.1.1.1.6

#example getting bytes sent for all interfaces
#snmpwalk -v2c -c public 192.168.2.1 1.3.6.1.2.1.31.1.1.1.10

#example getting all interface names
#snmpwalk -v2c -c public 192.168.2.1 .1.3.6.1.2.1.2.2.1.2

