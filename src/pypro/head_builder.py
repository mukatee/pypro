__author__ = 'teemu kanstren'

class HeadBuilder:
    def __init__(self, index_tag, type_tag, id_tag, index_value):
        self.index_tag = index_tag
        self.type_tag = type_tag
        self.id_tag = id_tag
        self.index_value = index_value

    def create(self, type, id):
        line = '{"'+self.index_tag+'" : "'+self.index_value+'", "'+self.type_tag+'" : "'+type+'", "'+self.id_tag+'" : "'+id+'"}'
        return  line
