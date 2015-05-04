__author__ = 'teemu kanstren'

from pypro.local import config
import psutil

class ProcPoller:
    #key = name, value = pid
    name_to_pid = {}
    #key = pid, value = name
    pid_to_name = {}
    processes = {}
    pids = []
    errors = {}

    def __init__(self, loggers):
        self.loggers = loggers

    def check_processes(self, epoch):
    #checks all processes to poll if the pid is already stored and name is known
    #if pid is stored and name matches, does nothing
    #if pid is stored and name does not match, replaces name mapping with new one
    #if pid is not stored, reads the name and creates the mapping
        self.name_to_pid = {}
        for pid in config.PROCESS_LIST:
            if isinstance(pid, int):
                proc = psutil.Process(pid)
                self.name_to_pid[self.get_name(proc)] = []
                self.check_info(epoch, proc)
                continue
            if pid == "-": return
            if pid == "*":
                for proc in psutil.process_iter():
                    self.name_to_pid[self.get_name(proc)] = []
                    self.check_info(epoch, proc)
                return
            self.name_to_pid[pid] = []
            for proc in psutil.process_iter():
                if self.get_name(proc) == pid:
                    self.check_info(epoch, proc)

    def get_processes(self, pid):
        procs = []
        if isinstance(pid, int):
            if pid in self.processes:
                procs.append(self.processes[pid])
            else:
                procs.append(psutil.Process(pid))
        else:
            if pid in self.name_to_pid:
                for i_pid in self.name_to_pid[pid]:
                    if i_pid in self.processes:
                        procs.append(self.processes[i_pid])
                    else:
                        procs.append(psutil.Process(i_pid))
#                    proc = psutil.Process(i_pid)
#                    procs.append(proc)
        return procs

    def get_name(self, proc):
        try:
            name = proc.name()
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            name = "? ("+str(proc.pid)+")"
        return name

    def check_info(self, epoch, proc):
        name = self.get_name(proc)
        pid = proc.pid

        self.name_to_pid[name].append(pid)

        if pid in self.pid_to_name:
            if self.pid_to_name[pid] == name:
                return
        self.pid_to_name[pid] = name
        self.processes[pid] = proc
        for logger in self.loggers:
            logger.proc_info(epoch, pid, name)

    def handle_process_poll_error(self, epoch, proc):
        name = self.get_name(proc)
        if proc.pid in self.errors:
            if self.errors[proc.pid] == name:
                return
        self.errors[proc.pid] = name
        for logger in self.loggers:
            logger.proc_error(epoch, proc.pid, name)
