__author__ = 'teemu kanstren'

import time

from elasticsearch import Elasticsearch

import pypro.snmp.config as config
import pypro.local.body_builder as bb


class ESNetLogger:
    indices = {}

    def __init__(self):
        self.event_id = 1

        self.es = Elasticsearch([config.ES_HOST+':'+str(config.ES_PORT)],
                                sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=60)
        for oid in config.SNMP_OIDS:
            self.indices[oid._name()] = 0

    def close(self):
        #todo: check is es needs closing
        pass

    def start(self, epoch):
        body = '{"time" : ' + str(epoch) + ', "session_info" : "start"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id='event_' + str(self.event_id), body=body)
        if config.PRINT_CONSOLE: print(reply)

    def stop(self, epoch):
        body = '{"time" : ' + str(epoch) + ', "session_info" : "stop"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id='event_' + str(self.event_id), body=body)
        if config.PRINT_CONSOLE: print(reply)

    def value(self, epoch, oid, _value):
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        value = str(_value)
        if (not oid.numeric):
            value = '"'+value+'"'
        body = '{"time" : ' + str(epoch) + ', "target" : "' + str(oid.target()) + '", ' + \
               '"target_name" : "' + str(oid.target_name) + '", "oid" : "' + str(oid.oid) + '", ' + \
               '"oid_name" : "' + str(oid.oid_name) + '", "value" : ' + value + '}'
        reply = self.es.index(index=config.ES_INDEX, doc_type=name, id=name + '_' + str(index), body=body)
        if config.PRINT_CONSOLE: print(reply)

    def error(self, epoch, description):
        body = '{"time" : ' + str(epoch) + ', "error" : "' + description + '"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id='event_' + str(self.event_id), body=body)
        if config.PRINT_CONSOLE: print(reply)
