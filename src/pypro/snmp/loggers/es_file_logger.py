__author__ = 'teemu kanstren'

import pypro.utils as utils
import pypro.snmp.config as config
from pypro.head_builder import HeadBuilder


class ESFileLogger:
    files = {}
    indices = {}

    def __init__(self):
        oids = config.SNMP_OIDS
        utils.check_dir()

        self.head = HeadBuilder("_index", "_type", "_id", config.ES_INDEX)

        self.event_id = 1
        self.event_log = open(utils.event_log + ".es", "w", encoding="utf-8")

        for oid in oids:
            file_name = utils.log_dir + "/" + oid._name() + "_log.es"
            log = open(file_name, "w", encoding="utf-8")
            self.files[oid.oid_id] = log
            self.indices[oid._name()] = 0

    def close(self):
        for file in self.files:
            file.close()
        self.event_log.close()

    def start(self, epoch):
        epoch *= 1000 #this converts it into milliseconds
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id), epoch) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "session_info" : "start"}'
        line = head + body
        self.event_log.write(line + "\n")
        self.event_log.flush()
        self.event_id += 1
        if config.PRINT_CONSOLE: print(line)

    def stop(self, epoch):
        epoch *= 1000
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id), epoch) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "session_info" : "stop"}'
        line = head + body
        self.event_log.write(line + "\n")
        self.event_log.flush()
        self.event_id += 1
        if config.PRINT_CONSOLE: print(line)

    def value(self, epoch, oid, value):
        epoch *= 1000
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        str_value = str(value)
        if not oid.numeric or not utils.is_number(str_value):
            str_value = '"'+str_value+'"'
#        else:
#            if not utils.is_number(str_value):
#                self.error(epoch, "Numeric OID "+oid.oid+" produced non-numeric value:"+str_value)
#                return
        head = '{"index" : ' + self.head.create(name, name + '_' + str(index), epoch) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "target" : "' + str(oid.target()) + '", ' + \
               '"target_name" : "' + str(oid.target_name) + '", "oid" : "' + str(oid.oid_id) + '", ' + \
               '"oid_name" : "' + str(oid.oid_name) + '", "value" : ' + str_value + '}'
        line = head + body
        log = self.files[oid.oid_id]
        log.write(line + "\n")
        log.flush()
        if config.PRINT_CONSOLE: print(line)

    def error(self, epoch, description):
        epoch *= 1000
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id), epoch) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "error" : "' + description + '"}'
        line = head + body
        self.event_log.write(line + "\n")
        self.event_log.flush()
        self.event_id += 1
        if config.PRINT_CONSOLE: print(line)
