__author__ = 'teemu kanstren'

import os
import unittest

import pkg_resources
from kafka.consumer.simple import SimpleConsumer
from kafka import KafkaClient

from pypro.local.loggers import KafkaLogger
import pypro.config as config
import pypro.tests.t_assert as t_assert


class TestKafkaLogs(unittest.TestCase):
    topic_index = 1

    @classmethod
    def setUpClass(cls):
        config.KAFKA_SERVER = os.environ["PYPRO_KAFKA_SERVER"]

    def setUp(self):
        config.KAFKA_TOPIC = "pypro_tests_" + str(self.topic_index)
        TestKafkaLogs.topic_index += 1

    def test_cpu_sys_kafka(self):
        kafka = KafkaLogger()
        kafka.cpu_sys(0, 1, 1, 1, 1)
        kafka.cpu_sys(1, 3, 2, 5, 6)
        kafka.cpu_sys(3, 22, 99, 11, 4)
        kafka.cpu_sys(5, 155, 122, 12, 22)
        kafka.close()

        self.assert_kafka('expected_cpu_sys.kafka')

    def test_cpu_proc_kafka(self):
        kafka = KafkaLogger()
        kafka.cpu_proc(0, 1, 1, 1, 1, 1, 1, 1, "p1")
        kafka.cpu_proc(0, 2, 1, 3, 4, 2, 3, 1, "p2")
        kafka.cpu_proc(0, 3, 2, 122, 7, 5, 8, 11, "p3")
        kafka.cpu_proc(10, 1, 1, 1, 1, 1, 1, 1, "p1")
        kafka.cpu_proc(10, 2, 1, 3, 4, 2, 3, 1, "p2")
        kafka.cpu_proc(10, 3, 2, 122, 7, 5, 8, 11, "p3")
        kafka.cpu_proc(20, 1, 1, 5, 1, 4, 3, 2, "p1")
        kafka.cpu_proc(20, 3, 2, 555, 7, 11, 55, 32, "p3")

        self.assert_kafka('expected_cpu_proc.kafka')

    def test_mem_sys_kafka(self):
        kafka = KafkaLogger()
        kafka.mem_sys(0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        kafka.mem_sys(10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
        kafka.mem_sys(12, 34, 654, 24, 33, 23, 442, 1, 13, 21, 44)
        kafka.mem_sys(15, 3445, 345, 345, 44, 745, 367, 32, 1111, 33, 55)
        kafka.mem_sys(33, 33, 453, 998, 347, 976, 8544, 45, 5555, 66, 33)

        self.assert_kafka('expected_mem_sys.kafka')

    def test_mem_proc_kafka(self):
        kafka = KafkaLogger()
        kafka.mem_proc(0, 1, 11, 15, 5, "p1")
        kafka.mem_proc(0, 2, 1, 3, 2, "p2")
        kafka.mem_proc(0, 5432, 21, 33, 9, "p3")
        kafka.mem_proc(5, 1, 22, 11, 3, "p1")
        kafka.mem_proc(5, 5432, 7, 55, 7, "p3")
        kafka.mem_proc(66, 1, 11, 15, 5, "p1")
        kafka.mem_proc(66, 2, 11, 0, 22, "p2")
        kafka.mem_proc(66, 5432, 212, 334, 44, "p3")

        self.assert_kafka('expected_mem_proc.kafka')

    def test_io_sys_kafka(self):
        kafka = KafkaLogger()
        kafka.io_sys(11111, 22, 22, 34, 43, 11, 11, 5, 3)
        kafka.io_sys(22222, 55, 23, 44, 34, 23, 17, 15, 4)
        kafka.io_sys(22233, 65, 23, 777, 44, 28, 18, 35, 5)
        kafka.io_sys(25555, 78, 44, 1911, 53, 99434, 43, 43, 21)

        self.assert_kafka('expected_io_sys.kafka')

    def test_proc_error_kafka(self):
        kafka = KafkaLogger()
        kafka.proc_error(11111, 22, "epic fail")
        kafka.proc_error(11111, 9758, "fail")
        kafka.proc_error(11112, 7364, "little fail")

        self.assert_kafka('expected_events.kafka')

    def test_proc_info_kafka(self):
        kafka = KafkaLogger()
        kafka.proc_info(11111, 22, "proc1")
        kafka.proc_info(11111, 9758, "proc2")
        kafka.proc_info(11111, 7364, "proc4")
        kafka.proc_info(11111, 3332, "proc3")

        self.assert_kafka('expected_proc_info.kafka')

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
