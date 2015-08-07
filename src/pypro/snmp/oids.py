__author__ = 'teemu kanstren'

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pypro.snmp.oid import OID


class UserCPUTimeRaw(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '1.3.6.1.4.1.2021.11.50.0', 'user cpu time', community, ip, port, target_name, True)


class UserCPUTimePrct(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '1.3.6.1.4.1.2021.11.9.0', 'percentage user cpu time', community, ip, port, target_name, True)


class SystemCPUTimeRaw(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '1.3.6.1.4.1.2021.11.52.0', 'system cpu time', community, ip, port, target_name, True)


class SystemCPUTimePrct(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '1.3.6.1.4.1.2021.11.10.0', 'percentage system cpu time', community, ip, port, target_name, True)


class IdleCPUTimeRaw(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.11.53.0', 'idle cpu time', community, ip, port, target_name, True)


class IdleCPUTimePrct(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.11.11.0', 'percentage idle cpu time', community, ip, port, target_name, True)


class RamTotal(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.4.5.0', 'total RAM', community, ip, port, target_name, True)


class RamFree(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.4.11.0', 'free RAM', community, ip, port, target_name, True)


# total available disk space, requires modifying snmp config on host
class DiskTotal(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.9.1.7.1', 'total disk space', community, ip, port, target_name, True)


# used disk space, requires modifying snmp.config on host
class DiskUsed(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.9.1.8.1', 'used disk space', community, ip, port, target_name, True)


# bytes in for a network interface. parameter "n" defines interface number
class BytesIn(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '.1.3.6.1.2.1.2.2.1.10.1.' + str(n), 'nw bytes in if ' + str(n), community, ip, port, target_name, True)


# bytes out for a network interface. parameter "n" defines interface number
class BytesOut(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '.1.3.6.1.2.1.2.2.1.16.1.' + str(n), 'nw bytes out if ' + str(n), community, ip, port, target_name, True)

# discarded incoming packets for a network interface. parameter "n" defines interface number
class DiscardedIn(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '1.3.6.1.2.1.2.2.1.13.' + str(n), 'discarded packets in if ' + str(n), community, ip, port, target_name, True)

# discarded outgoing packets for a network interface. parameter "n" defines interface number
class DiscardedOut(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '1.3.6.1.2.1.2.2.1.19.' + str(n), 'discarded packets out if ' + str(n), community, ip, port, target_name, True)

#ram used. a measure derived from reading two oid values, total ram in system and free ram in system.
class RamUsed:
    def __init__(self, community, ip, port, target_name):
        # sometimes the OID number sequence starts with "." which works to read it
        # but pysnmp returns the name without the first "." so have to that here as well for later comparison to work
        self.oid_total_id = '1.3.6.1.4.1.2021.4.5.0'
        self.oid_free_id = '1.3.6.1.4.1.2021.4.11.0'
        self.oid_name = 'used ram'
        self.community = community
        self.ip = ip
        self.port = port
        self.target_name = target_name
        self.numeric = True
        self.oid_id = 'used mem'

    def target(self):
        return self.ip + ":" + str(self.port)

    def _name(self):
        return self.oid_name.replace(' ', '_')

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
