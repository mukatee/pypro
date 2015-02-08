__author__ = 'teemu'

import main
import utils

class file_logger:
    def __init__(self):
        utils.check_dir()
        self.cpu_system_log = open(utils.log_dir+"cpu-log-sys.csv", "w", encoding="utf-8")
        self.cpu_proc_log = open(utils.log_dir+"cpu-log-proc.csv", "w", encoding="utf-8")
        cpu_sys_header = "time;user;system;idle"
        self.cpu_system_log.write(cpu_sys_header + "\n")
        self.cpu_system_log.flush()

        self.mem_system_log = open(utils.log_dir+"mem-log-sys.csv", "w", encoding="utf-8")
        self.mem_proc_log = open(utils.log_dir+"mem-log-proc.csv", "w", encoding="utf-8")
        mem_sys_header = "time;available;percent;used;free"
        self.mem_system_log.write(mem_sys_header + "\n")
        self.mem_system_log.flush()

        self.io_system_log = open(utils.log_dir+"io-log-sys.csv", "w", encoding="utf-8")
        io_sys_header = "time;"
        self.io_system_log.write(io_sys_header + "\n")
        self.io_system_log.flush()

        self.proc_info_log = open(utils.log_dir+"proc-log-info.csv", "w", encoding="utf-8")
        self.proc_error_log = open(utils.log_dir+"proc-log-errors.csv", "w", encoding="utf-8")


    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        line = str(epoch) + ";" + str(user_count) + ";" + str(system_count) + ";" + str(idle_count) + ";" + str(percent)
        self.cpu_system_log.write(line + "\n")
        self.cpu_system_log.flush()
        if main.print_console: print(line)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system):
        "Logs CPU metrics at process level"
        line = str(epoch) + ": " + str(pid) + ";" + str(priority) + ";" + str(ctx_count) + ";" + \
            str(n_threads) + ";" + str(cpu_user) + ";" + str(cpu_system)
        self.cpu_proc_log.write(line + "\n")
        self.cpu_proc_log.flush()
        if main.print_console: print(line)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        line = str(epoch) + ";" + str(available) + ";" + str(percent) + ";" + str(used) + ";" + str(free) + ";" + \
                str(swap_total) + ";" + str(swap_used) + ";" + str(swap_free) + ";" + str(swap_in) + ";" + \
                str(swap_out) + ";" + str(swap_percent)
        self.mem_system_log.write(line + "\n")
        self.mem_system_log.flush()
        if main.print_console: print(line)

    def mem_proc(self, epoch, pid, rss, vms, percent):
        "Logs memory metrics at process level"
        line = str(epoch) + ":" + str(pid) + ";" + str(rss) + ";" + str(vms) + ";" + str(percent)
        self.mem_proc_log.write(line + "\n")
        self.mem_proc_log.flush()
        if main.print_console: print(line)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        line = str(epoch) + ";" + str(bytes_sent) + ";" + str(bytes_recv) + ";" + str(packets_sent) + ";" + \
                  str(packets_recv) + ";" + str(errin) + ";" + str(errout) + ";" + str(dropin) + ";" + str(dropout)
        self.io_system_log.write(line + "\n")
        self.io_system_log.flush()
        if main.print_console: print(line)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = str(epoch) + ";" + str(pid) + ";" + name
        self.proc_error_log.write(line + "\n")
        self.proc_error_log.flush()
        if print_console: print(line)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = str(epoch) + ";" + str(pid) + ";" + name
        self.proc_info_log.write(str + "\n")
        self.proc_info_log.flush()
        if print_console: print(str)
