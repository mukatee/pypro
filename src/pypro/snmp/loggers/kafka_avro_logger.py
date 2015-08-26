__author__ = 'teemu kanstren'

import time
import pkg_resources
import io

from pypro.snmp import config
from pypro.head_builder import HeadBuilder
from pypro import utils

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

class KafkaAvroLogger:
    indices = {}

    def __init__(self):
        from kafka import SimpleProducer, KafkaClient
        from kafka.common import LeaderNotAvailableError
        self.kafka_client = KafkaClient(config.KAFKA_SERVER)
        self.kafka = SimpleProducer(self.kafka_client)
        schema_src = pkg_resources.resource_string("pypro.snmp", "pypro_snmp.avsc").decode('utf-8')
        self.schema = avro.schema.Parse(schema_src)

        for oid in config.SNMP_OIDS:
            self.indices[oid._name()] = 0

        try:
            self.kafka.send_messages(config.KAFKA_TOPIC, b"creating topic")
        except LeaderNotAvailableError:
            time.sleep(1)

    def close(self):
        self.kafka.stop(0)
        self.kafka_client.close()

    def start(self, epoch):
        if config.PRINT_CONSOLE: print('starting session logging to kafka with avro')

    def stop(self, epoch):
        if config.PRINT_CONSOLE: print('stopping session logging to kafka with avro')

    def value(self, epoch, oid, value):
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

        writer = avro.io.DatumWriter(self.schema)
        bytes_writer = io.BytesIO()
        id = config.AVRO_SCHEMA_ID
        id_bytes = (id).to_bytes(1, 'big')
        bytes_writer.write(id_bytes)
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write({"header": {"type": oid.oid_name, "tom": oid.target_name, "address": oid.ip, "oid": oid.oid_name, "time":epoch},
                       "body": {"value_int": value_int, "value_float": value_float, "value_string": value_str}
                       }, encoder)
        raw_bytes = bytes_writer.getvalue()
        self.kafka.send_messages(config.KAFKA_TOPIC, raw_bytes)
        if config.PRINT_CONSOLE: print(str(raw_bytes))

    def error(self, epoch, description):
        pass

