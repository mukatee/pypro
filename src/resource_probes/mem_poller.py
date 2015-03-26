__author__ = 'teemu kanstren'

import psutil
import time

from resource_probes import config
from resource_probes.csv_file_logger import CSVFileLogger
from resource_probes.proc_poller import ProcPoller

class MemPoller:
    def __init__(self, proc_poller, loggers):
        self.loggers = loggers
        self.proc_poller = proc_poller

    def poll_system(self, epoch):
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
        for logger in self.loggers:
            logger.mem_sys(epoch, available, percent, used, free,
                           swap_total, swap_used, swap_free, swap_in, swap_out, swap_prct)

    def poll_process(self, epoch, proc):
        try:
            pid = proc.pid
            pname = self.proc_poller.get_name(proc)
            mem_info = proc.memory_info()
            rss = mem_info.rss
            vms = mem_info.vms
            prct = proc.memory_percent()

            for logger in self.loggers:
                logger.mem_proc(epoch, pid, rss, vms, prct, pname)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # if the process has disappeared, we get an exception and ignore it
            # pass <- pass is NOP in Python
            self.proc_poller.handle_process_poll_error(epoch, proc)

    def poll(self):
        # int() converts argument to integer (string or float), in this case the float time
        epoch = int(time.time())
        #TODO: remove this multiplier and do modifications in loggers
        self.poll_system(epoch)

        before = int(time.time() * 1000)

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

#        for proc in psutil.process_iter():
#            self.proc_poller.check_info(epoch, proc)
#            self.poll_process(epoch, proc)
        after = int(time.time() * 1000)
        diff = after-before
        #print("mem_p:"+str(diff))

if __name__ == "__main__":
    file = CSVFileLogger(True)
    mem_poller = MemPoller(ProcPoller(), file)
    while (True):
        mem_poller.poll()
        time.sleep(1)
    file.close()