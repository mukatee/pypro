__author__ = 'teemu kanstren'

import time

from pypro.snmp import config
import pypro.local.body_builder as bb
from pypro.head_builder import HeadBuilder


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
        epoch *= 1000 #this converts it into milliseconds
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "session_info" : "start"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.event_id += 1
        if config.PRINT_CONSOLE: print(msg)

    def stop(self, epoch):
        epoch *= 1000 #this converts it into milliseconds
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "session_info" : "stop"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.event_id += 1
        if config.PRINT_CONSOLE: print(msg)

    def value(self, epoch, oid, _value):
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        value = str(_value)
        if (not oid.numeric):
            value = '"'+value+'"'
        head = '{"index" : ' + self.head.create(name, name+'_' + str(index)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "target" : "' + str(oid.target()) + '", ' + \
               '"target_name" : "' + str(oid.target_name) + '", "oid" : "' + str(oid.oid) + '", ' + \
               '"oid_name" : "' + str(oid.oid_name) + '", "value" : ' + value + '}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        if config.PRINT_CONSOLE: print(msg)

    def error(self, epoch, description):
        epoch *= 1000 #this converts it into milliseconds
        head = '{"index" : ' + self.head.create('event', 'event_' + str(self.event_id)) + '}\n'
        body = '{"time" : ' + str(epoch) + ', "error" : "'+description+'"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.event_id += 1
        if config.PRINT_CONSOLE: print(msg)

