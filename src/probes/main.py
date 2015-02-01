__author__ = 'teemu'

import time
import psutil
import cpu_poller
import mem_poller
import io_poller

print_console = True
info = {}
errors = {}
interval = 1

proc_info_log = open("proc-log-info.csv", "w", encoding="utf-8")
proc_error_log = open("proc-log-errors.csv", "w", encoding="utf-8")

def println_p_err(str):
    "Print a line to console and to a file"
    proc_error_log.write(str + "\n")
    proc_error_log.flush()
    if print_console: print(str)

def println_p_info(str):
    "Print a line to console and to a file"
    proc_info_log.write(str + "\n")
    proc_info_log.flush()
    if print_console: print(str)

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

def check_info(epoch, proc):
    if proc.pid in info:
        if info[proc.pid] == proc.name():
            return
    info[proc.pid] = proc.name()
    println_p_info(str(epoch) + ": Process info " + str(proc.pid) + ": " + proc.name())

def handle_process_poll_error(epoch, proc):
        if proc.pid in errors:
            if errors[proc.pid] == proc.name():
                return
        errors[proc.pid] = proc.name()
        println_p_err(str(epoch) + ": Unable to poll process " + str(proc.pid) + ": " + proc.name())

if __name__ == "__main__":
    while True:
        run_poller()
        time.sleep(interval)
