__author__ = 'teemu kanstren'

from elasticsearch import Elasticsearch
import json

import pypro.snmp.config as config
from pypro import utils

class ESNetLogger:
    indices = {}

    def __init__(self):
        self.event_id = 1

        self.es = Elasticsearch([config.ES_HOST+':'+str(config.ES_PORT)],
                                sniff_on_start=False, sniff_on_connection_fail=False, sniffer_timeout=60)
        for oid in config.SNMP_OIDS:
            self.indices[oid._name()] = 0

    def close(self):
        #todo: check is es needs closing
        pass

    def start(self, epoch):
        epoch *= 1000
        body = '{"time" : ' + str(epoch) + ', "session_info" : "start"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id='event_' + str(self.event_id), body=body)
        self.event_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def stop(self, epoch):
        epoch *= 1000
        body = '{"time" : ' + str(epoch) + ', "session_info" : "stop"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id='event_' + str(self.event_id), body=body)
        self.event_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def value(self, epoch, oid, value):
        epoch *= 1000
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        str_value = str(value)
        if not oid.numeric or not utils.is_number(str_value):
            str_value = json.dumps(str_value)
        body = '{"time" : ' + str(epoch) + ', "target" : "' + str(oid.target()) + '", ' + \
               '"target_name" : "' + str(oid.target_name) + '", "oid" : "' + str(oid.oid_id) + '", ' + \
               '"oid_name" : "' + str(oid.oid_name) + '", "value" : ' + str_value + '}'
        reply = self.es.index(index=config.ES_INDEX, doc_type=name, id=name + '_' + str(index), body=body)
        if config.PRINT_CONSOLE: print(reply)

    def error(self, epoch, description):
        body = '{"time" : ' + str(epoch) + ', "error" : "' + description + '"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id='event_' + str(self.event_id), body=body)
        self.event_id += 1
        if config.PRINT_CONSOLE: print(reply)
