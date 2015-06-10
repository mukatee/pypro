__author__ = 'teemu kanstren'

from pysnmp.entity.rfc3413.oneliner import cmdgen

class SNMPPoller:
    def __init__(self, oid, snmp):
        self.oid = oid
        self.snmp = snmp

    def poll(self, loggers):
        errorIndication, errorStatus, errorIndex, varBinds = self.snmp.getCmd(
            cmdgen.CommunityData('get_c'),
            cmdgen.UdpTransportTarget(('192.168.2.1', 161)),
            '1.3.6.1.4.1.2021.11.50.0',
            lookupNames=True, lookupValues=True
        )

        # Check for errors and print out results
        if errorIndication:
            print("ei:"+str(errorIndication))
        elif errorStatus:
            print("es:"+str(errorStatus))
        else:
            for name, val in varBinds:
                print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        pass
