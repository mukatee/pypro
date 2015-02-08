__author__ = 'teemu kanstren'

class proc_poller:
    info = {}
    errors = {}

    def __init__(self, *loggers):
        self.loggers = loggers

    def check_info(self, epoch, proc):
        if proc.pid in self.info:
            if self.info[proc.pid] == proc.name():
                return
        self.info[proc.pid] = proc.name()
        for logger in self.loggers:
            logger.proc_info(epoch, proc.pid, proc.name)

    def handle_process_poll_error(self, epoch, proc):
        if proc.pid in self.errors:
            if self.errors[proc.pid] == proc.name():
                return
        self.errors[proc.pid] = proc.name()
        for logger in self.loggers:
            logger.proc_error(epoch, proc.pid, proc.name())
