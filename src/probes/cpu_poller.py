__author__ = 'teemu kanstren'

import psutil
import time
import main

# process priority
trace_niceness = True
# number of threads per process
trace_threads = True
# cpu use percentage
trace_prct = True
# time in user space
trace_user = True
#time in kernel space
trace_system = True
header = "time;user;system;idle"

props = []

system_log = open("cpu-log-sys.csv", "w", encoding="utf-8")
proc_log = open("cpu-log-proc.csv", "w", encoding="utf-8")

def println_s(str):
    "Print a line to console and to a file"
    system_log.write(str + "\n")
    system_log.flush()
    if main.print_console: print(str)

def println_p(str):
    "Print a line to console and to a file"
    proc_log.write(str + "\n")
    proc_log.flush()
    if main.print_console: print(str)

def poll_system(epoch):
    cpu_times = psutil.cpu_times()
    user_cnt = cpu_times.user
    system_cnt = cpu_times.system
    idle_cnt = cpu_times.idle
    println_s(str(epoch) + ";" + str(user_cnt) + ";" + str(system_cnt) + ";" + str(idle_cnt))

def poll():
    #int() converts argument to integer (string or float), in this case the float time
    epoch = int(time.time())
    poll_system(epoch)

    for proc in psutil.process_iter():
        main.check_info(epoch, proc)
        poll_process(epoch, proc)

def poll_process(epoch, proc):
    try:
        pid = proc.pid
        priority = proc.nice()
        #status is a text indicator such as "running". ignoring for now.
        #        status = proc.status()
        ctx_switches = proc.num_ctx_switches()
        ctx_count = ctx_switches.voluntary + ctx_switches.involuntary
        n_threads = proc.num_threads()
        cpu_times = proc.cpu_times()
        cpu_user = cpu_times.user
        cpu_system = cpu_times.system
        println_p(
            str(epoch) + ": " + str(pid) + ";" + str(priority) + ";" + str(ctx_count) + ";" +
            str(n_threads) + ";" + str(cpu_user) + ";" + str(cpu_system)
        )
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        #if the process has disappeared, we get an exception and ignore it
        #pass <- pass is NOP in Python
        main.handle_process_poll_error(epoch, proc)

if __name__ == "__main__":
    #    f = open("perf-log.csv", "w", encoding="utf-8")
    println_s(header)
    while (True):
        poll()
        time.sleep(1)
    system_log.close()
    proc_log.close()

