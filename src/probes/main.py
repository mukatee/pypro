__author__ = 'teemu'

import time
import psutil
import os
import cpu_poller
import mem_poller
import io_poller
import utils

print_console = True
interval = 1

def run_poller():
    #int() converts argument to integer (string or float), in this case the float time
    epoch = int(time.time())
    cpu_poller.poll_system(epoch)
    mem_poller.poll_system(epoch)
    io_poller.poll_system(epoch)
    for proc in psutil.process_iter():
        check_info(epoch, proc)
        cpu_poller.poll_process(epoch, proc)
        mem_poller.poll_process(epoch, proc)


if __name__ == "__main__":
    while True:
        run_poller()
        time.sleep(interval)
