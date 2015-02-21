__author__ = 'teemu kanstren'

import psutil

class ProcPoller:
    info = {}
    errors = {}

    def __init__(self, loggers):
        self.loggers = loggers

    def check_info(self, epoch, proc):
        try:
            name = proc.name()
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            name = "?"
        if proc.pid in self.info:
            if self.info[proc.pid] == name:
                return
        self.info[proc.pid] = name
        for logger in self.loggers:
            logger.proc_info(epoch, proc.pid, name)

    def handle_process_poll_error(self, epoch, proc):
        try:
            name = proc.name()
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            name = "? ("+proc.pid+")"
        if proc.pid in self.errors:
            if self.errors[proc.pid] == name:
                return
        self.errors[proc.pid] = name
        for logger in self.loggers:
            logger.proc_error(epoch, proc.pid, name)
