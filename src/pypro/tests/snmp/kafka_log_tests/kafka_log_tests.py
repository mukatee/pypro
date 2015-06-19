__author__ = 'teemu kanstren'

import os
import unittest

import pkg_resources
from kafka.consumer.simple import SimpleConsumer
from kafka import KafkaClient

from pypro.snmp.loggers.kafka_logger import KafkaLogger
import pypro.snmp.config as config
import pypro.tests.t_assert as t_assert
from pypro.snmp.oid import OID

class TestKafkaLogs(unittest.TestCase):
    topic_index = 1

    @classmethod
    def setUpClass(cls):
        config.KAFKA_SERVER = os.environ["PYPRO_KAFKA_SERVER"]
        TestKafkaLogs.oid1 = OID("1.1.1.1.1", "test_oid1", "public", "127.0.0.1", 55, "test target 1", True)
        TestKafkaLogs.oid2 = OID("1.1.1.1.1.0", "test_oid2", "private", "127.0.0.1", 255, "test target 2", True)
        TestKafkaLogs.oid3 = OID("1.1.1.2.1", "test_oid3", "public", "127.0.0.1", 155, "test target 3", False)
        TestKafkaLogs.oid4 = OID("1.1.1.2.1.0", "test_oid4", "private", "127.0.0.1", 233, "test target 4", False)
        config.SNMP_OIDS.append(TestKafkaLogs.oid1)
        config.SNMP_OIDS.append(TestKafkaLogs.oid2)
        config.SNMP_OIDS.append(TestKafkaLogs.oid3)
        config.SNMP_OIDS.append(TestKafkaLogs.oid4)

    def setUp(self):
        config.KAFKA_TOPIC = "pypro_tests_" + str(self.topic_index)
        TestKafkaLogs.topic_index += 1

    def test_numeric_oid_kafka(self):
        kafka = KafkaLogger()
        kafka.start(0)
        kafka.value(0, TestKafkaLogs.oid1, 1)
        kafka.value(1, TestKafkaLogs.oid1, 5)
        kafka.value(1, TestKafkaLogs.oid2, 7)
        kafka.value(2, TestKafkaLogs.oid2, 9)
        kafka.value(2, TestKafkaLogs.oid1, 11)
        kafka.value(2, TestKafkaLogs.oid1, "bomb on this")
        kafka.value(2, TestKafkaLogs.oid1, 12)
        kafka.close()

        self.assert_kafka('expected_numeric.kafka')

    def test_string_oid_kafka(self):
        kafka = KafkaLogger()
        kafka.start(0)
        kafka.value(0, TestKafkaLogs.oid3, "omg its bob\n\ron the line")
        kafka.value(1, TestKafkaLogs.oid4, "now for bunnies..")
        kafka.value(1, TestKafkaLogs.oid3, "this is a test\nwith linefeed")
        kafka.value(2, TestKafkaLogs.oid4, "once upon a time")
        kafka.value(2, TestKafkaLogs.oid3, "hello")
        kafka.value(2, TestKafkaLogs.oid3, 11)
        kafka.value(2, TestKafkaLogs.oid3, "ok passed?")
        kafka.close()

        self.assert_kafka('expected_string.kafka')

    def test_mixed_oid_kafka(self):
        kafka = KafkaLogger()
        kafka.start(0)
        kafka.value(0, TestKafkaLogs.oid3, "omg its bob\n\ron the line")
        kafka.value(1, TestKafkaLogs.oid4, "now for bunnies..")
        kafka.value(0, TestKafkaLogs.oid1, 1)
        kafka.value(7, TestKafkaLogs.oid1, 5)
        kafka.value(8, TestKafkaLogs.oid2, 7)
        kafka.value(33, TestKafkaLogs.oid3, "this is a test\nwith linefeed")
        kafka.value(555, TestKafkaLogs.oid4, "once upon a time")
        kafka.value(333, TestKafkaLogs.oid3, "hello")
        kafka.value(8888, TestKafkaLogs.oid1, "bomb on this")
        kafka.value(11111, TestKafkaLogs.oid1, 12)
        kafka.value(42322, TestKafkaLogs.oid3, 11)
        kafka.value(111111, TestKafkaLogs.oid3, "ok passed?")
        kafka.value(11222, TestKafkaLogs.oid2, 9)
        kafka.value(2, TestKafkaLogs.oid1, 11)
        kafka.close()

        self.assert_kafka('expected_mixed.kafka')

    def test_error_kafka(self):
        kafka = KafkaLogger()

        kafka.error(11111, "epic fail")
        kafka.error(11111, "fail")
        kafka.error(11112, "little fail")

        self.assert_kafka('expected_errors.kafka')

    def assert_kafka(self, expected_file_name):
        #print("reading server "+config.KAFKA_SERVER+" on topic:"+config.KAFKA_TOPIC)
        kafka_client = KafkaClient(config.KAFKA_SERVER)
        #simpleconsumer takes its timeout in seconds... hence 1, allowing all messages to appear but not hanging too long
        consumer = SimpleConsumer(kafka_client, b"my_group", config.KAFKA_TOPIC.encode("utf8"),
                                      iter_timeout=1)
        #seek(1,0) means to start processing from the begining (the 0) but skip 1 message from this index  (the first msg)
        #we bypass the first message since it is just used to autostart the topic
        consumer.seek(1, 0)
        actual = ""
        for msg in consumer:
            #the linefeed at the end is not really needed but it makes for more readable error reports
            actual += msg.message.value.decode('utf8')+"\n"
        expected = pkg_resources.resource_string(__name__, expected_file_name).decode('utf8')
        t_assert.equal(actual, expected)
