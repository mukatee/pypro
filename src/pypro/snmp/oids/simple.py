__author__ = 'teemu kanstren'

from pypro.snmp.oid import OID


class UserCPUTimeRaw(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '1.3.6.1.4.1.2021.11.50.0', 'user cpu time', community, ip, port, target_name, True)

class UserCPUTimePrct(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.11.9.0', 'percentage user cpu time', community, ip, port, target_name, True)

class SystemCPUTimeRaw(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '1.3.6.1.4.1.2021.11.52.0', 'system cpu time', community, ip, port, target_name, True)

class SystemCPUTimePrct(OID):
    def __init__(self, community, ip, port, target_name):
        OID.__init__(self, '.1.3.6.1.4.1.2021.11.10.0', 'percentage system cpu time', community, ip, port, target_name, True)

class ProcessorLoad(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '.1.3.6.1.2.1.25.3.3.1.2.'+str(n), 'processor load '+str(n), community, ip, port, target_name, True)

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
        OID.__init__(self, '1.3.6.1.2.1.31.1.1.1.6.' + str(n), 'nw bytes in if ' + str(n), community, ip, port, target_name, True)

# bytes out for a network interface. parameter "n" defines interface number
class BytesOut(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '1.3.6.1.2.1.31.1.1.1.10.' + str(n), 'nw bytes out if ' + str(n), community, ip, port, target_name, True)

# discarded incoming packets for a network interface. parameter "n" defines interface number
class DiscardedIn(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '1.3.6.1.2.1.2.2.1.13.' + str(n), 'discarded packets in if ' + str(n), community, ip, port, target_name, True)

# discarded outgoing packets for a network interface. parameter "n" defines interface number
class DiscardedOut(OID):
    def __init__(self, community, ip, port, target_name, n):
        OID.__init__(self, '1.3.6.1.2.1.2.2.1.19.' + str(n), 'discarded packets out if ' + str(n), community, ip, port, target_name, True)

