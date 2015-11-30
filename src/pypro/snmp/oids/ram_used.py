__author__ = 'teemu kanstren'

from pysnmp.entity.rfc3413.oneliner import cmdgen

#ram used. a measure derived from reading two oid values, total ram in system and free ram in system.
class RamUsed:
    def __init__(self, community, ip, port, target_name):
        # sometimes the OID number sequence starts with "." which works to read it
        # but pysnmp returns the name without the first "." so have to use the same here as well for later comparison to work
        self.oid_total_id = '1.3.6.1.4.1.2021.4.5.0'
        self.oid_free_id = '1.3.6.1.4.1.2021.4.11.0'
        self.oid_name = 'used ram'
        self.community = community
        self.ip = ip
        self.port = port
        self.target_name = target_name
        self.oid_id = 'dm.ram.used'

    def target(self):
        return self.ip + ":" + str(self.port)

    def is_int(self):
        return True

    def is_float(self):
        return False

    def is_str(self):
        return False

    def _name(self):
        return self.oid_name.replace(' ', '_')

    def is_numeric(self):
        return True

    #for authenticated measurement polls
    def measure_auth(self, snmp, user, password, privacy_key, auth_proto, priv_proto):
        errorIndication, errorStatus, errorIndex, var_binds = snmp.getCmd(
            cmdgen.UsmUserData(user, authKey=password, privKey=privacy_key,
                               authProtocol=auth_proto, privProtocol=priv_proto),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            self.oid_total_id, #list of OID's to poll is here
            self.oid_free_id,
            lookupNames=True, lookupValues=True
        )
        return self.calc_used(errorIndication, errorStatus, errorIndex, var_binds)

    #for basic measurements with not authentication
    def measure_base(self, snmp):
        errorIndication, errorStatus, errorIndex, var_binds = snmp.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            self.oid_total_id, #list of OID's to poll is here
            self.oid_free_id)
        return self.calc_used(errorIndication, errorStatus, errorIndex, var_binds)

    def calc_used(self, errorIndication, errorStatus, errorIndex, var_binds):
        if errorIndication or errorStatus:
            return (errorIndication, errorStatus, errorIndex, [])
        for name, val in var_binds:
            #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
            pretty = str(name)
            if pretty == self.oid_total_id:
                total = val.prettyPrint() #here we pick up the total ram count in the system (oid 1)
            if pretty == self.oid_free_id:
                free = val.prettyPrint() #and here we pick up the free ram count in the system (oid 2)
        value = int(total) - int(free) #and calculate the derived measure (free ram count)
        return (errorIndication, errorStatus, errorIndex, [(self.oid_id, value)]) #finally return it in similar for to pysnmp
