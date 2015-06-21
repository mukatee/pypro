__author__ = 'teemu kanstren'

#http://www.mibdepot.com/cgi-bin/getmib3.cgi?i=1&n=UCD-SNMP-MIB&r=f5&f=UCD-SNMP-MIB&v=v2&t=tree

import pypro.snmp.config as config
from pypro.snmp.oid import OID
import pypro.snmp.main as main
from pypro.snmp.oids import *

config.SESSION_NAME = "session2"
config.ES_INDEX = "pypro-snmp"
config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = True
config.CSV_ENABLED = True
config.KAFKA_ENABLED = False
config.KAFKA_TOPIC = "session2"
config.KAFKA_SERVER = "192.168.2.153"
config.PRINT_CONSOLE = True
#raw user space cpu time
config.SNMP_OIDS.append(UserCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('1.3.6.1.4.1.2021.11.50.0', 'user cpu time', 'public', '192.168.2.1', 161, 'router', True))
#percentage of user space cpu time
config.SNMP_OIDS.append(UserCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.11.9.0', 'percentage user cpu time', 'public', '192.168.2.1', 161, 'router', True))
#raw system cpu time
config.SNMP_OIDS.append(SystemCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('1.3.6.1.4.1.2021.11.52.0', 'system cpu time', 'public', '192.168.2.1', 161, 'router', True))
#percentage of system time
config.SNMP_OIDS.append(SystemCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('1.3.6.1.4.1.2021.11.10.0', 'percentage system cpu time', 'public', '192.168.2.1', 161, 'router', True))
#raw idle cpu time
config.SNMP_OIDS.append(IdleCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.11.53.0', 'idle cpu time', 'public', '192.168.2.1', 161, 'router', True))
#percentage of idle time
config.SNMP_OIDS.append(IdleCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.11.11.0', 'percentage idle cpu time', 'public', '192.168.2.1', 161, 'router', True))
#total ram in system
config.SNMP_OIDS.append(RamTotal('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.4.5.0', 'total RAM available', 'public', '192.168.2.1', 161, 'router', True))
#total ram free
config.SNMP_OIDS.append(RamFree('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.4.11.0', 'total RAM free', 'public', '192.168.2.1', 161, 'router', True))
#available disk space, requires modifying snmp config on host
config.SNMP_OIDS.append(DiskTotal('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.9.1.7.1', 'available disk space', 'public', '192.168.2.1', 161, 'router', True))
#used disk space, requires modifying snmp.config on host
config.SNMP_OIDS.append(DiskUsed('public', '192.168.2.1', 161, 'router'))
#config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.9.1.8.1', 'used disk space', 'public', '192.168.2.1', 161, 'router', True))
#bytes in (network interface 1, the last number..)
config.SNMP_OIDS.append(BytesIn('public', '192.168.2.1', 161, 'router', 1))
#config.SNMP_OIDS.append(OID('.1.3.6.1.2.1.2.2.1.10.1', 'nw bytes in if 1', 'public', '192.168.2.1', 161, 'router', True))
#bytes out (network interface 1, the last number..)
config.SNMP_OIDS.append(BytesOut('public', '192.168.2.1', 161, 'router', 1))
#config.SNMP_OIDS.append(OID('.1.3.6.1.2.1.2.2.1.16.1', 'nw bytes out if 1', 'public', '192.168.2.1', 161, 'router', True))
#used memory. counted as total-available
config.SNMP_OIDS.append(RamUsed('public', '192.168.2.1', 161, 'router'))

main.run_poller()
