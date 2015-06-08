__author__ = 'teemu kanstren'

import psutil
import time
import pypro.local.config as config
from pypro.local.proc_poller import ProcPoller
from pypro.local.csv_file_logger import CSVFileLogger
from pypro.local.es_file_logger import ESFileLogger

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

    def __init__(self, proc_poller, loggers):
        self.proc_poller = proc_poller
        self.loggers = loggers

    def poll_system(self, epoch):
        cpu_times = psutil.cpu_times()
        user_cnt = cpu_times.user
        system_cnt = cpu_times.system
        idle_cnt = cpu_times.idle
        prct = psutil.cpu_percent()
        #TODO: per CPU
        for logger in self.loggers:
            logger.cpu_sys(epoch, user_cnt, system_cnt, idle_cnt, prct)

    def poll(self):
        #int() converts argument to integer (string or float), in this case the float time
        epoch = int(time.time())
        self.poll_system(epoch)

        before = int(time.time()*1000)
        self.proc_poller.check_processes(epoch)
        for pid in config.PROCESS_LIST:
            if pid == "-": return
            if pid == "*":
                for proc in psutil.process_iter():
                    self.proc_poller.check_info(epoch, proc)
                    self.poll_process(epoch, proc)
                return
            processes = self.proc_poller.get_processes(pid)
#            print("got "+str(processes)+" for "+str(pid))
            for proc in processes:
                self.poll_process(epoch, proc)
        after = int(time.time()*1000)
        diff = after-before
        #print("cpu_p:"+str(diff))

    def poll_process(self, epoch, proc):
        try:
            pid = proc.pid
            pname = self.proc_poller.get_name(proc)
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
                logger.cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, cpu_percent, pname)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            #if the process has disappeared, we get an exception and ignore it
            #pass <- pass is NOP in Python
            self.proc_poller.handle_process_poll_error(epoch, proc)

if __name__ == "__main__":
    csv = CSVFileLogger()
    es = ESFileLogger()
    proc = ProcPoller(csv, es)
    cpu_poller = CPUPoller(proc, csv, es)
    while (True):
        cpu_poller.poll()
        time.sleep(config.INTERVAL)
    csv.close()
