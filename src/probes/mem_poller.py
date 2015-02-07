__author__ = 'teemu kanstren'

import psutil
import time
import os
import main
import utils

header = "time;available;percent;used;free"
utils.check_dir()
system_log = open(utils.log_dir+"mem-log-sys.csv", "w", encoding="utf-8")
process_log = open(utils.log_dir+"mem-log-proc.csv", "w", encoding="utf-8")

def println_s(str):
    "Print a line to console and to a file"
    system_log.write(str + "\n")
    system_log.flush()
    if main.print_console: print(str)

def println_p(str):
    "Print a line to console and to a file"
    process_log.write(str + "\n")
    process_log.flush()
    if main.print_console: print(str)

def poll_system(epoch):
    mem_info = psutil.virtual_memory()
    available = mem_info.available
    percent = mem_info.percent
    used = mem_info.used
    free = mem_info.free
    swap_info = psutil.swap_memory()
    swap_total = swap_info.total
    swap_used = swap_info.used
    swap_free = swap_info.free
    swap_in = swap_info.sin
    swap_out = swap_info.sout
    swap_prct = swap_info.percent
    println_s(str(epoch) + ";" + str(available) + ";" + str(percent) + ";" + str(used) + ";" + str(free) + ";" +
              str(swap_total) + ";" + str(swap_used) + ";" + str(swap_free) + ";" + str(swap_in) + ";" +
              str(swap_out) + ";" + str(swap_prct))

def poll_process(epoch, proc):
    try:
        pid = proc.pid
        mem_info = proc.memory_info()
        rss = mem_info.rss
        vms = mem_info.vms
        prct = proc.memory_percent()
        println_p(str(epoch) + ":" + str(pid) + ";" + str(rss) + ";" + str(vms) + ";" + str(prct))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # if the process has disappeared, we get an exception and ignore it
        # pass <- pass is NOP in Python
        main.handle_process_poll_error(epoch, proc)

def poll():
    # int() converts argument to integer (string or float), in this case the float time
    epoch = int(time.time())
    poll_system(epoch)

    for proc in psutil.process_iter():
        main.check_info(epoch, proc)
        poll_process(epoch, proc)

if __name__ == "__main__":
    println_s(header)
    while (True):
        poll()
        time.sleep(1)
    system_log.close()
