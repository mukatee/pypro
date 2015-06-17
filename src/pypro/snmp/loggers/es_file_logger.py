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
            self.files[oid.oid] = log
            self.indices[oid._name()] = 0

    def close(self):
        for file in self.files:
            file.close()
        self.event_log.close()

    def start(self, epoch):
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "session_info" : "start"}'
        line = head + body
        self.event_log.write(line + "\n")
        self.event_log.flush()
        self.event_id += 1
        if config.PRINT_CONSOLE: print(line)

    def stop(self, epoch):
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "session_info" : "stop"}'
        line = head + body
        self.event_log.write(line + "\n")
        self.event_log.flush()
        self.event_id += 1
        if config.PRINT_CONSOLE: print(line)

    def value(self, epoch, oid, _value):
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        value = str(_value)
        if (not oid.numeric):
            value = '"'+value+'"'
        head = '{"index" : ' + self.head.create(name, name + '_' + str(index)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "target" : "' + str(oid.target()) + '", ' + \
               '"target_name" : "' + str(oid.target_name) + '", "oid" : "' + str(oid.oid) + '", ' + \
               '"oid_name" : "' + str(oid.oid_name) + '", "value" : ' + value + '}'
        line = head + body
        log = self.files[oid.oid]
        log.write(line + "\n")
        log.flush()
        if config.PRINT_CONSOLE: print(line)

    def error(self, epoch, description):
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "error" : "' + description + '"}'
        line = head + body
        self.event_log.write(line + "\n")
        self.event_log.flush()
        self.event_id += 1
        if config.PRINT_CONSOLE: print(line)
