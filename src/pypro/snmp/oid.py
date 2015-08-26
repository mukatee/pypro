__author__ = 'teemu kanstren'

from pysnmp.entity.rfc3413.oneliner import cmdgen
from enum import Enum

class OID:
    def __init__(self, oid_id, oid_name, community, ip, port, target_name, type):
        self.oid_id = oid_id
        self.oid_name = oid_name
        self.community = community
        self.ip = ip
        self.port = port
        self.target_name = target_name
        self.type = type

    def target(self):
        return self.ip+":"+str(self.port)

    def _name(self):
        return self.oid_name.replace(' ', '_')

    def is_int(self):
        return self.type == OID_Type.int

    def is_float(self):
        return self.type == OID_Type.float

    def is_str(self):
        return self.type == OID_Type.string

    def is_numeric(self):
        return self.type == OID_Type.int or self.type == OID_Type.float

    def measure_auth(self, snmp, user, password, privacy_key, auth_proto, priv_proto):
        return snmp.getCmd(
            cmdgen.UsmUserData(user, authKey=password, privKey=privacy_key,
                               authProtocol=auth_proto, privProtocol=priv_proto),
            cmdgen.UdpTransportTarget((self.ip, self.port)), self.oid_id,
            lookupNames=True, lookupValues=True
        )

    def measure_base(self, snmp):
        errorIndication, errorStatus, errorIndex, var_binds = snmp.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.ip, self.port)), self.oid_id,
            lookupNames=True, lookupValues=True
        )
        values = []
        for name, val in var_binds:
#            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
            values.append((name.prettyPrint(), val.prettyPrint()))
        return (errorIndication, errorStatus, errorIndex, values)

class OID_Type(Enum):
    int = 1
    float = 2
    string = 3
