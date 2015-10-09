__author__ = 'teemu kanstren'

import time
import pkg_resources
import io

from pypro.snmp import config
from pypro import utils

import avro.schema
import avro.io

class KafkaAvroLogger:
    indices = {}

    def __init__(self):
        from kafka import SimpleProducer, KafkaClient
        from kafka.common import LeaderNotAvailableError
        self.kafka_client = KafkaClient(config.KAFKA_SERVER)
        self.kafka = SimpleProducer(self.kafka_client)
        schema_int_src = pkg_resources.resource_string("pypro.snmp", "pypro_snmp_int.avsc").decode('utf-8')
        schema_float_src = pkg_resources.resource_string("pypro.snmp", "pypro_snmp_float.avsc").decode('utf-8')
        schema_str_src = pkg_resources.resource_string("pypro.snmp", "pypro_snmp_str.avsc").decode('utf-8')
        self.schema_int = avro.schema.Parse(schema_int_src)
        self.schema_float = avro.schema.Parse(schema_float_src)
        self.schema_str = avro.schema.Parse(schema_str_src)

        for oid in config.SNMP_OIDS:
            self.indices[oid._name()] = 0

        try:
            #empty msg to ensure topic is created
            self.kafka.send_messages(config.KAFKA_TOPIC, (0).to_bytes(1, byteorder='big'))
        except LeaderNotAvailableError:
            time.sleep(1)

    def close(self):
        self.kafka.stop(0)
        self.kafka_client.close()

    def start(self, epoch):
        if config.PRINT_CONSOLE: print('starting session logging to kafka with avro')

    def stop(self, epoch):
        if config.PRINT_CONSOLE: print('stopping session logging to kafka with avro')

    def value(self, epoch, oid, name, value):
        name = oid._name()
        index = self.indices[name]
        index += 1
        self.indices[name] = index
        str_value = str(value)
        if oid.is_numeric() and not utils.is_number(str_value):
            self.error(epoch, "Invalid number, received:"+str_value)
            return

        value_int = None
        value_float = None
        value_str = None
        if oid.is_int(): value_int = int(value)
        elif oid.is_float(): value_float = float(value)
        else: value_str = str(value)

        writer = None
        id = None
        value = None
        if value_int is not None:
            writer = avro.io.DatumWriter(self.schema_int)
            id = config.AVRO_SCHEMA_INT_ID
            value = value_int
        if value_float is not None:
            writer = avro.io.DatumWriter(self.schema_float)
            id = config.AVRO_SCHEMA_FLOAT_ID
            value = value_float
        if value_str is not None:
            writer = avro.io.DatumWriter(self.schema_str)
            id = config.AVRO_SCHEMA_STR_ID
            value = value_str
        bytes_writer = io.BytesIO()
        id_bytes = (id).to_bytes(1, 'big')
        bytes_writer.write(id_bytes)
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write({"header": {"type": oid.oid_name, "tom": oid.target_name, "address": oid.ip, "oid": oid.oid_name, "time":epoch},
                       "body": {"value": value}
                       }, encoder)
        raw_bytes = bytes_writer.getvalue()
        self.kafka.send_messages(config.KAFKA_TOPIC, raw_bytes)
        if config.PRINT_CONSOLE: print(str(raw_bytes))

    def error(self, epoch, description):
        pass

