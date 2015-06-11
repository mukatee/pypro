__author__ = 'teemu kanstren'

import pypro.config as config
from pypro.snmp.oid import OID
import pypro.snmp.main as main

config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = True
#raw user space time
config.SNMP_OIDS.append(OID('1.3.6.1.4.1.2021.11.50.0', 'user cpu time', 'public', '192.168.2.1', 161, 'router', True))
main.run_poller()