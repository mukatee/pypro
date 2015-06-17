__author__ = 'teemu kanstren'

import threading


class ConsumerThread(threading.Thread):
    def __init__(self, consumer):
        threading.Thread.__init__(self)
        self.consumer = consumer
#        self.expected_count = expected_count

    def run(self):
        self.msgs = []
        for msg in self.consumer:
            print("received:"+msg.value)
            self.msgs.append(msg.value)
        self.consumer.close()
