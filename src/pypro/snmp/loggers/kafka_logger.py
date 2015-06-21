__author__ = 'teemu kanstren'

import time

from pypro.snmp import config
from pypro.head_builder import HeadBuilder
from pypro import utils

class KafkaLogger:
    indices = {}

    def __init__(self):
        from kafka import SimpleProducer, KafkaClient
        from kafka.common import LeaderNotAvailableError
        self.kafka_client = KafkaClient(config.KAFKA_SERVER)
        self.kafka = SimpleProducer(self.kafka_client)
        self.event_id = 1

        for oid in config.SNMP_OIDS:
            self.indices[oid._name()] = 0

        self.head = HeadBuilder("index", "doc_type", "id", config.ES_INDEX)
        try:
            self.kafka.send_messages(config.KAFKA_TOPIC, b"creating topic")
        except LeaderNotAvailableError:
            time.sleep(1)

    def close(self):
        self.kafka.stop(0)
        self.kafka_client.close()

    def start(self, epoch):
#        epoch *= 1000 #this converts it into milliseconds
        head = self.head.create('event', 'event_' + str(self.event_id))
        body = '{"start_time" : ' + str(epoch) + ', "session_info" : "start"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.event_id += 1
        if config.PRINT_CONSOLE: print(msg)

    def stop(self, epoch):
#        epoch *= 1000 #this converts it into milliseconds
        head = self.head.create('event', 'event_' + str(self.event_id))
        body = '{"time" : ' + str(epoch) + ', "session_info" : "stop"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.event_id += 1
        if config.PRINT_CONSOLE: print(msg)

    def value(self, epoch, oid, value):
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        is_str = False
        str_value = str(value)
        if not oid.numeric or not utils.is_number(str_value):
            is_str = True
#        head = self.head.create(name, name+'_' + str(index))
        head = self.head.create("measurement", name+'_' + str(index))
        body = '{"time" : ' + str(epoch) + ', "target" : "' + str(oid.target()) + '", ' + \
               '"target_name" : "' + str(oid.target_name) + '", "oid" : "' + str(oid.oid_id) + '", ' + \
               '"oid_name" : "' + str(oid.oid_name)
        if is_str:
            body += '", "str_value" : "' + str_value + '"}'
        else:
            body += '", "value" : ' + str_value + '}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        if config.PRINT_CONSOLE: print(msg)

    def error(self, epoch, description):
#        epoch *= 1000 #this converts it into milliseconds
        head = self.head.create('event', 'event_' + str(self.event_id))
        body = '{"time" : ' + str(epoch) + ', "error" : "'+description+'"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.event_id += 1
        if config.PRINT_CONSOLE: print(msg)

