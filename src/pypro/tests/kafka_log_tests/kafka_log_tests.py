__author__ = 'teemu kanstren'

import os
import unittest
from pypro.local.kafka_logger import KafkaLogger
from pypro.tests.kafka_log_tests.consumer_thread import ConsumerThread
import pypro.local.config as config
from kafka import KafkaConsumer
from kafka.consumer.simple import SimpleConsumer
from kafka import SimpleProducer, KafkaClient

class TestKafkaLogs(unittest.TestCase):
    topic_index = 1

    @classmethod
    def setUpClass(cls):
        config.KAFKA_SERVER = os.environ["PYPRO_KAFKA_SERVER"]

    #        for message in consumer:
    #            pass

    def setUp(self):
        config.KAFKA_TOPIC = "pypro_tests_" + str(self.topic_index)
#        self.thread = ConsumerThread(self.consumer)
        TestKafkaLogs.topic_index += 1

    def test_cpu_sys_kafka(self):
        kafka = KafkaLogger()
        kafka.cpu_sys(0, 1, 1, 1, 1)
        kafka.cpu_sys(1, 3, 2, 5, 6)
        kafka.cpu_sys(3, 22, 99, 11, 4)
        kafka.cpu_sys(5, 155, 122, 12, 22)
        kafka.close()

        print("reading server "+config.KAFKA_SERVER+" on topic:"+config.KAFKA_TOPIC)
        kafka_client = KafkaClient(config.KAFKA_SERVER)
        consumer = SimpleConsumer(kafka_client, b"my_group", config.KAFKA_TOPIC.encode("utf8"),
                                      iter_timeout=200)
        consumer.seek(0, 0)
        for msg in consumer:
            print("received:"+str(msg.message.value))
#            self.msgs.append(msg.value)
#        actual = len(self.thread.msgs)

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

    def test_mem_sys_es(self):
        kafka = KafkaLogger()
        kafka.mem_sys(0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        kafka.mem_sys(10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
        kafka.mem_sys(12, 34, 654, 24, 33, 23, 442, 1, 13, 21, 44)
        kafka.mem_sys(15, 3445, 345, 345, 44, 745, 367, 32, 1111, 33, 55)
        kafka.mem_sys(33, 33, 453, 998, 347, 976, 8544, 45, 5555, 66, 33)

    def test_mem_proc_es(self):
        kafka = KafkaLogger()
        kafka.mem_proc(0, 1, 11, 15, 5, "p1")
        kafka.mem_proc(0, 2, 1, 3, 2, "p2")
        kafka.mem_proc(0, 5432, 21, 33, 9, "p3")
        kafka.mem_proc(5, 1, 22, 11, 3, "p1")
        kafka.mem_proc(5, 5432, 7, 55, 7, "p3")
        kafka.mem_proc(66, 1, 11, 15, 5, "p1")
        kafka.mem_proc(66, 2, 11, 0, 22, "p2")
        kafka.mem_proc(66, 5432, 212, 334, 44, "p3")

    def test_io_sys_es(self):
        kafka = KafkaLogger()
        kafka.io_sys(11111, 22, 22, 34, 43, 11, 11, 5, 3)
        kafka.io_sys(22222, 55, 23, 44, 34, 23, 17, 15, 4)
        kafka.io_sys(22233, 65, 23, 777, 44, 28, 18, 35, 5)
        kafka.io_sys(25555, 78, 44, 1911, 53, 99434, 43, 43, 21)

    def test_proc_error_es(self):
        kafka = KafkaLogger()
        kafka.proc_error(11111, 22, "epic fail")
        kafka.proc_error(11111, 9758, "fail")
        kafka.proc_error(11112, 7364, "little fail")

    def test_proc_info_es(self):
        kafka = KafkaLogger()
        kafka.proc_info(11111, 22, "proc1")
        kafka.proc_info(11111, 9758, "proc2")
        kafka.proc_info(11111, 7364, "proc4")
        kafka.proc_info(11111, 3332, "proc3")


