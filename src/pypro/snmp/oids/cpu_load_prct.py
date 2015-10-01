__author__ = 'teemu kanstren'

from pysnmp.entity.rfc3413.oneliner import cmdgen


#cpu load measures. a set of measures derived from reading several oid values, (system, user, nice, idle counters).
class CPULoadPrct:
    def __init__(self, community, ip, port, target_name):
        # sometimes the OID number sequence starts with "." which works to read it
        # but pysnmp returns the name without the first "." so have to that here as well for later comparison to work
        self.oid_raw_user_id = '1.3.6.1.4.1.2021.11.50.0'
        self.oid_raw_nice_id = '1.3.6.1.4.1.2021.11.51.0'
        self.oid_raw_system_id = '1.3.6.1.4.1.2021.11.52.0'
        self.oid_raw_idle_id = '1.3.6.1.4.1.2021.11.53.0'
        self.oid_raw_sirq_id = '1.3.6.1.4.1.2021.11.61.0'#softirq
        self.community = community
        self.ip = ip
        self.port = port
        self.target_name = target_name
        self.numeric = True
        self.oid_id = 'dm.cpu.prct'
        self.oid_name = 'cpu load prct'
        self.prev_system = None
        self.prev_user = None
        self.prev_idle = None

    def _name(self):
        return self.oid_name.replace(' ', '_')

    def target(self):
        return self.ip + ":" + str(self.port)

    # for authenticated measurement polls
    def measure_auth(self, snmp, user, password, privacy_key, auth_proto, priv_proto):
        errorIndication, errorStatus, errorIndex, var_binds = snmp.getCmd(
            cmdgen.UsmUserData(user, authKey=password, privKey=privacy_key,
                               authProtocol=auth_proto, privProtocol=priv_proto),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            self.oid_raw_system_id,  # list of OID's to poll is here
            self.oid_raw_user_id,
            self.oid_raw_nice_id,
            self.oid_raw_idle_id,
            self.oid_raw_sirq_id,
            lookupNames=True, lookupValues=True
        )
        return self.calc_prct(errorIndication, errorStatus, errorIndex, var_binds)

    # for basic measurements with no authentication
    def measure_base(self, snmp):
        errorIndication, errorStatus, errorIndex, var_binds = snmp.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.ip, self.port)),
            self.oid_raw_system_id,  # list of OID's to poll is here
            self.oid_raw_user_id,
            self.oid_raw_nice_id,
            self.oid_raw_sirq_id,
            self.oid_raw_idle_id)
        return self.calc_prct(errorIndication, errorStatus, errorIndex, var_binds)

    def calc_prct(self, errorIndication, errorStatus, errorIndex, var_binds):
        if errorIndication or errorStatus:
            return (errorIndication, errorStatus, errorIndex, [])
        for name, val in var_binds:
            # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
            pretty = str(name)
            if pretty == self.oid_raw_system_id:
                system_count = float(val.prettyPrint())  # here we pick up the system raw cpu load (oid 1)
            if pretty == self.oid_raw_user_id:
                user_count = float(val.prettyPrint())  # here we pick up the user raw cpu load (oid 2)
            if pretty == self.oid_raw_idle_id:
                idle_count = float(val.prettyPrint())  # here we pick up the idle raw cpu load (oid 3)
            if pretty == self.oid_raw_nice_id:
                nice_count = float(val.prettyPrint())  # here we pick up the idle raw cpu load (oid 3)
            if pretty == self.oid_raw_sirq_id:
                sirq_count = float(val.prettyPrint())  # here we pick up the idle raw cpu load (oid 3)
        if self.prev_system is None:
            self.prev_system = system_count
            self.prev_user = user_count
            self.prev_nice = nice_count
            self.prev_idle = idle_count
            self.prev_sirq = sirq_count
            return ('No previous value available, not counting CPU load percentages', errorStatus, errorIndex, [])
        system_diff = system_count - self.prev_system
        user_diff = user_count - self.prev_user
        idle_diff = idle_count - self.prev_idle
        nice_diff = nice_count - self.prev_nice
        sirq_diff = sirq_count - self.prev_sirq
        total_diff = system_diff + user_diff + idle_diff + nice_diff + sirq_diff
        if total_diff == 0:
            return ('No ticks passed, not counting CPU load percentages', errorStatus, errorIndex, [])  # finally return it in format similar to pysnmp
        system_prct = system_diff / total_diff * 100
        user_prct = user_diff / total_diff * 100
        idle_prct = idle_diff / total_diff * 100
        nice_prct = nice_diff / total_diff * 100
        sirq_prct = sirq_diff / total_diff * 100

        self.prev_system = system_count
        self.prev_user = user_count
        self.prev_nice = nice_count
        self.prev_idle = idle_count
        self.prev_sirq = sirq_count

        values = []
        values.append(('cpu system prct', system_prct))
        values.append(('cpu user prct', user_prct))
        values.append(('cpu idle prct', idle_prct))
        values.append(('cpu nice prct', nice_prct))
        values.append(('cpu sirq prct', sirq_prct))
        return (errorIndication, errorStatus, errorIndex, values)  # finally return it in format similar to pysnmp
