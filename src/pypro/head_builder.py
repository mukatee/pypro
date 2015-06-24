__author__ = 'teemu kanstren'


class HeadBuilder:
    def __init__(self, index_tag, type_tag, id_tag, db_value):
        self.index_tag = index_tag
        self.type_tag = type_tag
        self.id_tag = id_tag
        self.db_value = db_value

    def create(self, type, id, epoch):
        line = '{"' + self.index_tag + '" : "' + self.db_value + '", "' + \
               self.type_tag + '" : "' + type + '", "' + self.id_tag + '" : "' + id + \
               '", "time" : ' + str(epoch) + '}'
        return line
