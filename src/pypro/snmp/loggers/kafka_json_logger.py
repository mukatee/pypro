__author__ = 'teemu kanstren'

import time

from pypro.snmp import config
from pypro.head_builder import HeadBuilder
from pypro import utils

class KafkaJsonLogger:
    indices = {}

    def __init__(self):
        from kafka import SimpleProducer, KafkaClient
        from kafka.common import LeaderNotAvailableError
        self.kafka_client = KafkaClient(config.KAFKA_SERVER)
        self.kafka = SimpleProducer(self.kafka_client)

        for oid in config.SNMP_OIDS:
            self.indices[oid._name()] = 0

        self.head = HeadBuilder("db", "type", "tom", config.DB_NAME)
        try:
            self.kafka.send_messages(config.KAFKA_TOPIC, b"creating topic")
        except LeaderNotAvailableError:
            time.sleep(1)

    def close(self):
        self.kafka.stop(0)
        self.kafka_client.close()

    def start(self, epoch):
        head = self.head.create('info', config.TOM, epoch)
        body = '{"description" : "started ('+ config.SESSION_NAME + ')"'+', "value" : '+str(config.SESSION_ID)+'}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        if config.PRINT_CONSOLE: print(msg)

    def stop(self, epoch):
        head = self.head.create('info', config.TOM, epoch)
        body = '{"description" : "stopped ('+ config.SESSION_NAME + ')"'+', "value" : '+str(config.SESSION_ID)+'}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        if config.PRINT_CONSOLE: print(msg)

    def value(self, epoch, oid, name, value):
#        name = oid._name()
        name = name.replace(' ', '_')
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        is_error = False
        str_value = str(value)
        if oid.numeric and not utils.is_number(str_value):
            is_error = True
        head = self.head.create(name, oid.target_name, epoch)
        body = '{"target" : "' + str(oid.target()) + '", ' + \
               '"oid" : "' + str(oid.oid_id)
        if is_error:
            body += '", "error" : "' + str_value + '"}'
        else:
            body += '", "value" : ' + str_value + '}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        if config.PRINT_CONSOLE: print(msg)

    def error(self, epoch, description):
        head = self.head.create('info', config.TOM, epoch)
        body = '{"error" : "'+ description + '"}'
        msg = '{"header": '+ head + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        if config.PRINT_CONSOLE: print(msg)

