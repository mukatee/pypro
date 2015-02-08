__author__ = 'teemu kanstren'

import psutil
import time
import main
from file_logger import file_logger

class cpu_poller:
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

    def __init__(self, *loggers):
        self.loggers = loggers

    def poll_system(self, epoch):
        cpu_times = psutil.cpu_times()
        user_cnt = cpu_times.user
        system_cnt = cpu_times.system
        idle_cnt = cpu_times.idle
        prct = psutil.cpu_percent(interval=main.interval)
        #TODO: per CPU prct
        for logger in self.loggers:
            logger.cpu_sys(epoch, user_cnt, system_cnt, idle_cnt, prct)

    def poll(self):
        #int() converts argument to integer (string or float), in this case the float time
        epoch = int(time.time())
        self.poll_system(epoch)

        for proc in psutil.process_iter():
            main.check_info(epoch, proc)
            self.poll_process(epoch, proc)

    def poll_process(self, epoch, proc):
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
            for logger in self.loggers:
                logger.cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            #if the process has disappeared, we get an exception and ignore it
            #pass <- pass is NOP in Python
            main.handle_process_poll_error(epoch, proc)

if __name__ == "__main__":
    file = file_logger()
    cpu_poller = cpu_poller(file)
    while (True):
        cpu_poller.poll()
        time.sleep(1)
    file.close()
