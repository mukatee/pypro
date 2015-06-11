__author__ = 'teemu kanstren'

import time

import pypro.utils as utils
import pypro.config as config


class CSVFileLogger:
    def __init__(self):
        utils.check_dir()

        self.session_info_log = open(utils.session_log+".csv", "w", encoding="utf-8")
        session_info_header = "time;description"
        now = int(time.time())
        self.session_info_log.write(session_info_header + "\n")
        self.session_info_log.write(str(now) + ";" + config.SESSION_NAME + "\n")
        self.session_info_log.flush()

        self.cpu_system_log = open(utils.cpu_sys_log+".csv", "w", encoding="utf-8")
        cpu_sys_header = "time;user;system;idle;percentage"
        self.cpu_system_log.write(cpu_sys_header + "\n")
        self.cpu_system_log.flush()

        self.cpu_proc_log = open(utils.cpu_proc_log+".csv", "w", encoding="utf-8")
        cpu_proc_header = "time;pid;priority;context-switches;n-of-threads;user;system;percent"
        self.cpu_proc_log.write(cpu_proc_header + "\n")
        self.cpu_proc_log.flush()

        self.mem_system_log = open(utils.mem_sys_log+".csv", "w", encoding="utf-8")
        mem_sys_header = "time;available;percentage;used;free;swap-total;swap-used;swap-free;swap-in;swap-out;swap-percentage"
        self.mem_system_log.write(mem_sys_header + "\n")
        self.mem_system_log.flush()

        self.mem_proc_log = open(utils.mem_proc_log+".csv", "w", encoding="utf-8")
        mem_proc_header = "time;pid;real-use;virtual-use;percentage"
        self.mem_proc_log.write(mem_proc_header + "\n")
        self.mem_proc_log.flush()

        self.io_system_log = open(utils.io_sys_log+".csv", "w", encoding="utf-8")
        io_sys_header = "time;bytes-sent;bytes-received;packets-sent;packets-received;errors-in;errors-out;dropped-in;dropped-out"
        self.io_system_log.write(io_sys_header + "\n")
        self.io_system_log.flush()

        self.proc_info_log = open(utils.proc_info_log+".csv", "w", encoding="utf-8")
        proc_info_header = "time;pid;name"
        self.proc_info_log.write(proc_info_header + "\n")
        self.proc_info_log.flush()

        self.event_log = open(utils.event_log+".csv", "w", encoding="utf-8")
        event_header = "time;type;pid;description"
        self.event_log.write(event_header + "\n")
        self.event_log.flush()

    def close(self):
        self.cpu_system_log.close()
        self.cpu_proc_log.close()
        self.mem_system_log.close()
        self.mem_proc_log.close()
        self.io_system_log.close()
        self.proc_info_log.close()
        self.event_log.close()
        self.session_info_log.close()

    def start(self): pass

    def commit(self): pass

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        line = str(epoch) + ";" + str(user_count) + ";" + str(system_count) + ";" + str(idle_count) + ";" + str(percent)
        self.cpu_system_log.write(line + "\n")
        self.cpu_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, cpu_percent, pname):
        "Logs CPU metrics at process level"
        line = str(epoch) + ";" + str(pid) + ";" + str(priority) + ";" + str(ctx_count) + ";" + \
            str(n_threads) + ";" + str(cpu_user) + ";" + str(cpu_system) + ";" + str(cpu_percent)
        self.cpu_proc_log.write(line + "\n")
        self.cpu_proc_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        line = str(epoch) + ";" + str(available) + ";" + str(percent) + ";" + str(used) + ";" + str(free) + ";" + \
                str(swap_total) + ";" + str(swap_used) + ";" + str(swap_free) + ";" + str(swap_in) + ";" + \
                str(swap_out) + ";" + str(swap_percent)
        self.mem_system_log.write(line + "\n")
        self.mem_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        line = str(epoch) + ";" + str(pid) + ";" + str(rss) + ";" + str(vms) + ";" + str(percent)
        self.mem_proc_log.write(line + "\n")
        self.mem_proc_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        line = str(epoch) + ";" + str(bytes_sent) + ";" + str(bytes_recv) + ";" + str(packets_sent) + ";" + \
                  str(packets_recv) + ";" + str(errin) + ";" + str(errout) + ";" + str(dropin) + ";" + str(dropout)
        self.io_system_log.write(line + "\n")
        self.io_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def proc_error(self, epoch, pid, description):
        "Print a line to console and to a file"
        line = str(epoch) + ";1;" + str(pid) + ";" + description
        self.event_log.write(line + "\n")
        self.event_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = str(epoch) + ";" + str(pid) + ";" + name
        self.proc_info_log.write(line + "\n")
        self.proc_info_log.flush()
        if config.PRINT_CONSOLE: print(line)
