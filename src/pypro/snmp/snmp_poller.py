__author__ = 'teemu kanstren'

import time
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pypro.snmp import config

class SNMPPoller:
    def __init__(self, oid, snmp, loggers):
        self.oid = oid
        self.snmp = snmp
        self.loggers = loggers

    def poll(self):
        oid = self.oid
#        error_indication, error_status, error_index, var_binds = None
        if config.SNMP_AUTH:
            user = config.SNMP_USER
            password = config.SNMP_PASS
            privacy_key = config.SNMP_PRIVKEY
            auth_proto = cmdgen.usmHMACMD5AuthProtocol
            if config.SNMP_AUTH_PROTO.lower() == "SHA".lower():
                auth_proto = cmdgen.usmHMACSHAAuthProtocol
            priv_proto = cmdgen.usmAesCfb128Protocol
            if config.SNMP_PRIV_PROTO.lower() == "DES":
                priv_proto = cmdgen.usmDESPrivProtocol
            error_indication, error_status, error_index, var_binds = \
                oid.measure_auth(self.snmp, user, password, privacy_key, auth_proto, priv_proto)
#            error_indication, error_status, error_index, var_binds = self.snmp.getCmd(
#                cmdgen.UsmUserData(user, authKey=password, privKey=privacy_key,
#                                   authProtocol=auth_proto, privProtocol=priv_proto),
#                cmdgen.UdpTransportTarget((oid.ip, oid.port)), oid.oid,
#                lookupNames=True, lookupValues=True
#            )
        else:
            error_indication, error_status, error_index, var_binds = oid.measure_base(self.snmp)
#            error_indication, error_status, error_index, var_binds = self.snmp.getCmd(
#                cmdgen.CommunityData(oid.community),
#                cmdgen.UdpTransportTarget((oid.ip, oid.port)), oid.oid_id,
#                lookupNames=True, lookupValues=True
#            )

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
                    logger.value(epoch, oid, val)
        pass
