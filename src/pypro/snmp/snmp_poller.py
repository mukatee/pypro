__author__ = 'teemu kanstren'

import time
from pysnmp.entity.rfc3413.oneliner import cmdgen

class SNMPPoller:
    def __init__(self, oid, snmp, loggers):
        self.oid = oid
        self.snmp = snmp
        self.loggers = loggers

    def poll(self):
        oid = self.oid
        error_indication, error_status, error_index, var_binds = self.snmp.getCmd(
            cmdgen.CommunityData(oid.community),
            cmdgen.UdpTransportTarget((oid.ip, oid.port)), oid.oid,
            lookupNames=True, lookupValues=True
        )

        epoch = int(time.time())
        # Check for errors and print out results
        if error_indication:
            for logger in self.loggers:
                logger.error(epoch, "failed to poll oid "+oid.oid+" from "+oid.target()+" : "+str(error_indication))
        elif error_status:
            for logger in self.loggers:
                logger.error(epoch, "failed to poll oid "+oid.oid+" from "+oid.target()+" : "+str(error_status))
        else:
            for name, val in var_binds:
                for logger in self.loggers:
                    logger.value(epoch, oid, val.prettyPrint())
        pass
