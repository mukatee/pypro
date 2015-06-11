__author__ = 'teemu kanstren'

class OID:
    def __init__(self, oid, oid_name, community, ip, port, target_name, numeric):
        self.oid = oid
        self.oid_name = oid_name
        self.community = community
        self.ip = ip
        self.port = port
        self.target_name = target_name
        self.numeric = numeric

    def target(self):
        return self.ip+":"+str(self.port)

    def _name(self):
        return self.oid_name.replace(' ', '_')