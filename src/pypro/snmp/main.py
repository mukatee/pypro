__author__ = 'teemu kanstren'

from pysnmp.entity.rfc3413.oneliner import cmdgen

#resource OID's on linux: http://www.debianadmin.com/linux-snmp-oids-for-cpumemory-and-disk-statistics.html
#snmpwalk = get the whole subtree from given node
#snmpgetnext = get next for given value in tree. looping gives walk.

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('get_c'),
    cmdgen.UdpTransportTarget(('192.168.2.1', 161)),
    '1.3.6.1.4.1.2021.11.50.0',
    lookupNames=True, lookupValues=True
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print(errorStatus)
else:
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

