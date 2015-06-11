__author__ = 'teemu kanstren'

class OID:
    def __init__(self, oid, oid_name, community, ip, port, target_name):
        self.oid = oid
        self.oid_name = oid_name
        self.community = community
        self.ip = ip
        self.port = port
        self.target_name = target_name

    def target(self):
        return self.ip+":"+str(self.port)
