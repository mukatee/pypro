__author__ = 'teemu kanstren'

import psutil
import time
from proc_poller import ProcPoller
from file_logger import FileLogger
from es_logger import ESLogger

class CPUPoller:
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

    def __init__(self, interval, proc_poller, *loggers):
        self.proc_poller = proc_poller
        self.loggers = loggers
        self.interval = interval

    def poll_system(self, epoch):
        cpu_times = psutil.cpu_times()
        user_cnt = cpu_times.user
        system_cnt = cpu_times.system
        idle_cnt = cpu_times.idle
        prct = psutil.cpu_percent()
        #TODO: per CPU prct
        for logger in self.loggers:
            logger.cpu_sys(epoch, user_cnt, system_cnt, idle_cnt, prct)

    def poll(self):
        #int() converts argument to integer (string or float), in this case the float time
        epoch = int(time.time())
        epoch *= 1000 #this converts it into milliseconds
        self.poll_system(epoch)

        for proc in psutil.process_iter():
            self.proc_poller.check_info(epoch, proc)
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
            cpu_percent = proc.cpu_percent()
            for logger in self.loggers:
                logger.cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, cpu_percent)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            #if the process has disappeared, we get an exception and ignore it
            #pass <- pass is NOP in Python
            self.proc_poller.handle_process_poll_error(epoch, proc)

if __name__ == "__main__":
    file = FileLogger(True)
    es = ESLogger(False, "session1")
    proc = ProcPoller(file)
    cpu_poller = CPUPoller(1, proc, file, es)
    while (True):
        cpu_poller.poll()
        time.sleep(1)
    file.close()
