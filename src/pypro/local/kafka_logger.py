__author__ = 'teemu kanstren'

import time
from kafka import SimpleProducer, KafkaClient
from pypro.local import config

class KafkaLogger:
    def __init__(self):
        kafka_client = KafkaClient(config.KAFKA_HOST+":"+config.KAFKA_PORT)
        self.kafka = SimpleProducer(kafka_client)
        self.cpu_sys_id = 1
        self.cpu_proc_id = 1

        self.mem_sys_id = 1
        self.mem_proc_id = 1

        self.io_sys_id = 1

        self.proc_info_id = 1
        self.proc_error_id = 1

    def close(self):
        pass

    def start(self): pass

    def commit(self): pass

    def session_info(self):
        now = int(time.time()) * 1000
        body = '{"description": "'+ config.SESSION_NAME + '", "start_time": ' + str(now) + '}'
        header = '{"doc_type": "session_info", "id": "session-'+str(now)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "user_count": ' + str(user_count) + ', ' +\
                '"system_count": ' + str(system_count) + ', "idle_count": ' + str(idle_count) + ', ' + \
                '"percent": ' + str(percent) + '}'
        header = '{"doc_type": "system_cpu", "id": "cpu_sys_'+str(self.cpu_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.cpu_sys_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
        "Logs CPU metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "priority": ' + str(priority) + ', '\
                '"context_switches": ' + str(ctx_count) + ', "threads": ' + str(n_threads) + ', ' + \
                '"cpu_user" : ' + str(cpu_user) + ', "cpu_system" : '+str(cpu_system) + ', "percent" : '+str(percent) + \
                ', "pname" : "' + pname + '"}'
        header = '{"doc_type": "process_cpu", "id": "cpu_proc_'+str(self.cpu_proc_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.cpu_proc_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "available": ' + str(available) + ', "percent": ' + str(percent) + ', ' +\
                '"used": ' + str(used) + ', "free": ' + str(free) + ', "swap_total": ' + str(swap_total) + ', ' + \
                '"swap_used": ' + str(swap_used) + ', "swap_free": ' + str(swap_free) + ', "swap_in": ' + str(swap_in) + ', ' + \
                '"swap_out": ' + str(swap_out) + ', "swap_percent": '+str(swap_percent)+'}'
        header = '{"doc_type": "system_memory", "id": "mem_sys_'+str(self.mem_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.mem_sys_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "rss": ' + str(rss) + ', '\
                '"vms": ' + str(vms) + ', "percent": ' + str(percent) + ', "pname" : "' + pname + '"}'
        header = '{"doc_type": "process_memory", "id": "mem_proc_'+str(self.mem_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.mem_proc_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "bytes_sent": ' + str(bytes_sent) + ', "bytes_recv": ' + str(bytes_recv) + ', ' +\
                '"packets_sent": ' + str(packets_sent) + ', "packets_received": ' + str(packets_recv) + ', ' + \
                '"errors_in": ' + str(errin) + ', "errors_out": ' + str(errout) + ', "dropped_in": ' + str(dropin) + ', ' + \
                '"dropped_out": ' + str(dropout) +'}'
        header = '{"doc_type": "system_io", "id": "mem_proc_'+str(self.io_sys_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.io_sys_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        header = '{"doc_type": "event", "id": "proc_error_'+str(self.proc_error_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.proc_error_id += 1
#        if config.PRINT_CONSOLE: print(reply)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        header = '{"doc_type": "process_info", "id": ""proc_info_"'+str(self.proc_info_id)+'"'+'}'
        msg = '{"header": '+ header + ', "body":'+ body+'}'
        self.kafka.send_messages(config.KAFKA_TOPIC, msg)
        self.proc_info_id += 1
#        if config.PRINT_CONSOLE: print(reply)


# To send messages synchronously
kafka = KafkaClient("192.168.2.153:9092")
producer = SimpleProducer(kafka)

# Note that the application is responsible for encoding messages to type str
producer.send_messages("my-topic", b"some message")
producer.send_messages("my-topic", b"this method", b"is variadic")

# Send unicode message
producer.send_messages("my-topic", u'你怎么样?'.encode('utf-8'))

# To send messages asynchronously
# WARNING: current implementation does not guarantee message delivery on failure!
# messages can get dropped! Use at your own risk! Or help us improve with a PR!
producer = SimpleProducer(kafka, async=True)
producer.send_messages("my-topic", b"async message")

# To wait for acknowledgements
# ACK_AFTER_LOCAL_WRITE : server will wait till the data is written to
#                         a local log before sending response
# ACK_AFTER_CLUSTER_COMMIT : server will block until the message is committed
#                            by all in sync replicas before sending a response
producer = SimpleProducer(kafka, async=False,
                          req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
                          ack_timeout=2000)

response = producer.send_messages("my-topic", b"another message")

if response:
    print(response[0].error)
    print(response[0].offset)

# To send messages in batch. You can use any of the available
# producers for doing this. The following producer will collect
# messages in batch and send them to Kafka after 20 messages are
# collected or every 60 seconds
# Notes:
# * If the producer dies before the messages are sent, there will be losses
# * Call producer.stop() to send the messages and cleanup
producer = SimpleProducer(kafka, batch_send=True,
                          batch_send_every_n=20,
                          batch_send_every_t=60)