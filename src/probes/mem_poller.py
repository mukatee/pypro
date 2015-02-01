__author__ = 'teemu kanstren'

import psutil
import time
import main

header = "time;available;percent;used;free"
system_log = open("mem-log-sys.csv", "w", encoding="utf-8")
process_log = open("mem-log-proc.csv", "w", encoding="utf-8")

def println_s(str):
    "Print a line to console and to a file"
    system_log.write(str+"\n")
    system_log.flush()
    if main.print_console: print(str)

def println_p(str):
    "Print a line to console and to a file"
    process_log.write(str+"\n")
    process_log.flush()
    if main.print_console: print(str)

def poll_system(epoch):
    mem_info = psutil.virtual_memory()
    available = mem_info.available
    percent = mem_info.percent
    used = mem_info.used
    free = mem_info.free
    println_s(str(epoch)+";"+str(available)+";"+str(percent)+";"+str(used)+";"+str(free))

def poll_process(epoch, proc):
    try:
        pid = proc.pid
        mem_info = proc.memory_info()
        rss = mem_info.rss
        vms = mem_info.vms
        prct = proc.memory_percent()
        println_p(str(epoch) + ":" + str(pid) +";"+str(rss)+";"+str(vms)+";"+str(prct))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        #if the process has disappeared, we get an exception and ignore it
        #pass <- pass is NOP in Python
        main.handle_process_poll_error(epoch, proc)

def poll():
    #int() converts argument to integer (string or float), in this case the float time
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
