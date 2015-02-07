__author__ = 'teemu kanstren'

import psutil
import time
import main
import utils

header = "time;"
utils.check_dir()
system_log = open(utils.log_dir+"io-log-sys.csv", "w", encoding="utf-8")

def println_s(str):
    "Print a line to console and to a file"
    system_log.write(str + "\n")
    system_log.flush()
    if main.print_console: print(str)

def poll_system(epoch):
    #TODO: per NIC data
    net_counters = psutil.net_io_counters()
    bytes_sent = net_counters.bytes_sent
    bytes_recv = net_counters.bytes_recv
    packets_sent = net_counters.packets_sent
    packets_recv = net_counters.packets_recv
    errin = net_counters.errin
    errout = net_counters.errout
    dropin = net_counters.dropin
    dropout = net_counters.dropout
    println_s(str(epoch) + ";" + str(bytes_sent) + ";" + str(bytes_recv) + ";" + str(packets_sent) + ";" +
              str(packets_recv) + ";" + str(errin) + ";" + str(errout) + ";" + str(dropin) + ";" + str(dropout))

def poll():
    # int() converts argument to integer (string or float), in this case the float time
    epoch = int(time.time())
    poll_system(epoch)

if __name__ == "__main__":
    println_s(header)
    while (True):
        poll()
        time.sleep(1)
    system_log.close()
