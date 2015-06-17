__author__ = 'teemu kanstren'

import time

from pypro.local import config
import pypro.local.body_builder as bb
from pypro.head_builder import HeadBuilder


class KafkaLogger:
    def __init__(self):
        from kafka import SimpleProducer, KafkaClient
        from kafka.common import LeaderNotAvailableError
        self.kafka_client = KafkaClient(config.KAFKA_SERVER)
        self.kafka = SimpleProducer(self.kafka_client)
        self.cpu_sys_id = 1
        self.cpu_proc_id = 1

        self.mem_sys_id = 1
        self.mem_proc_id = 1

        self.io_sys_id = 1

        self.proc_info_id = 1
        self.proc_error_id = 1

        self.head = HeadBuilder("index", "doc_type", "id", config.ES_INDEX)
        try:
            self.kafka.send_messages(config.KAFKA_TOPIC, b"creating topic")
        except LeaderNotAvailableError:
            time.sleep(1)

    def close(self):
        self.kafka.stop(0)
        self.kafka_client.close()

    def start(self): pass

    def commit(self): pass

    def session_info(self):
        now = int(time.time()) * 1000
        body = bb.session_info()
        header = self.head.create('session_info', 'session-'+str(now))
#        header = '{"doc_type": "session_info", "id": "session-'+str(now)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.cpu_sys(epoch, user_count, system_count, idle_count, percent)
        header = self.head.create('system_cpu', 'cpu_sys_'+str(self.cpu_sys_id))
#        header = '{"doc_type": "system_cpu", "id": "cpu_sys_'+str(self.cpu_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
#        print("posting to server "+config.KAFKA_SERVER+" on topic:"+config.KAFKA_TOPIC)
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.cpu_sys_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
        "Logs CPU metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname)
        header = self.head.create('process_cpu', 'cpu_proc_'+str(self.cpu_proc_id))
#        header = '{"doc_type": "process_cpu", "id": "cpu_proc_'+str(self.cpu_proc_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.cpu_proc_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.mem_sys(epoch, available, percent, used, free, swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent)
        header = self.head.create('system_memory', 'mem_sys_'+str(self.mem_sys_id))
#        header = '{"doc_type": "system_memory", "id": "mem_sys_'+str(self.mem_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.mem_sys_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.mem_proc(epoch, pid, rss, vms, percent, pname)
        header = self.head.create('process_memory', 'mem_proc_'+str(self.mem_proc_id))
#        header = '{"doc_type": "process_memory", "id": "mem_proc_'+str(self.mem_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.mem_proc_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.io_sys(epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)
        header = self.head.create('system_io', 'io_sys_'+str(self.io_sys_id))
#        header = '{"doc_type": "system_io", "id": "mem_proc_'+str(self.io_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.io_sys_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.proc_error(epoch, pid, name)
        header = self.head.create('event', 'proc_error_'+str(self.proc_error_id))
#        header = '{"doc_type": "event", "id": "proc_error_'+str(self.proc_error_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.proc_error_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = bb.proc_info(epoch, pid, name)
        header = self.head.create('process_info', 'proc_info_'+str(self.proc_info_id))
#        header = '{"doc_type": "process_info", "id": ""proc_info_"'+str(self.proc_info_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg.encode("utf8"))
        self.proc_info_id += 1
#        if config.PRINT_CONSOLE: print(reply)

# from kafka import SimpleProducer, KafkaClient
#
# # To send messages synchronously
# kafka = KafkaClient("192.168.2.79:9092")
# producer = SimpleProducer(kafka)
#
# # Note that the application is responsible for encoding messages to type str
# producer.send_messages("my-topic", b"some message")
# producer.send_messages("my-topic", b"this method", b"is variadic")
#
# # Send unicode message
# producer.send_messages("my-topic", u'你怎么样?'.encode('utf-8'))
#
# # To send messages asynchronously
# # WARNING: current implementation does not guarantee message delivery on failure!
# # messages can get dropped! Use at your own risk! Or help us improve with a PR!
# producer = SimpleProducer(kafka, async=True)
# producer.send_messages("my-topic", b"async message")
#
# # To wait for acknowledgements
# # ACK_AFTER_LOCAL_WRITE : server will wait till the data is written to
# #                         a local log before sending response
# # ACK_AFTER_CLUSTER_COMMIT : server will block until the message is committed
# #                            by all in sync replicas before sending a response
# producer = SimpleProducer(kafka, async=False,
#                           req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
#                           ack_timeout=2000)
#
# response = producer.send_messages("my-topic", b"another message")
#
# if response:
#     print(response[0].error)
#     print(response[0].offset)
#
# # To send messages in batch. You can use any of the available
# # producers for doing this. The following producer will collect
# # messages in batch and send them to Kafka after 20 messages are
# # collected or every 60 seconds
# # Notes:
# # * If the producer dies before the messages are sent, there will be losses
# # * Call producer.stop() to send the messages and cleanup
# producer = SimpleProducer(kafka, batch_send=True,
#                           batch_send_every_n=20,
#                           batch_send_every_t=60)