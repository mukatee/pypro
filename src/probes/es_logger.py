__author__ = 'teemu kanstren'

import utils

class ESLogger:
    def __init__(self, print_console, index):
        utils.check_dir()
        self.print_console = print_console
        self.index = index

        self.cpu_sys_id = 1
        self.cpu_system_log = open(utils.log_dir+"cpu-log-sys.es", "w", encoding="utf-8")
        self.cpu_proc_id = 1
        self.cpu_proc_log = open(utils.log_dir+"cpu-log-proc.es", "w", encoding="utf-8")

        self.mem_sys_id = 1
        self.mem_system_log = open(utils.log_dir+"mem-log-sys.es", "w", encoding="utf-8")
        self.mem_proc_id = 1
        self.mem_proc_log = open(utils.log_dir+"mem-log-proc.es", "w", encoding="utf-8")

        self.io_sys_id = 1
        self.io_system_log = open(utils.log_dir+"io-log-es.csv", "w", encoding="utf-8")

        self.proc_info_id = 1
        self.proc_info_log = open(utils.log_dir+"proc-log-info.es", "w", encoding="utf-8")
        self.proc_error_id = 1
        self.proc_error_log = open(utils.log_dir+"proc-log-errors.es", "w", encoding="utf-8")

    def close(self):
        self.cpu_system_log.close()
        self.cpu_proc_log.close()
        self.mem_system_log.close()
        self.mem_proc_log.close()
        self.io_system_log.close()
        self.proc_info_log.close()
        self.proc_error_log.close()

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        line = '{"index : { "_index", "'+self.index+'", "_type", "System CPU", "_id", "'+str(self.cpu_sys_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "user count": "' + str(user_count) + '", ' +\
                '"system count": "' + str(system_count) + '", "idle count": "' + str(idle_count) + '", ' + \
                '"percent": "' + str(percent) + '"}'
        self.cpu_sys_id += 1
        self.cpu_system_log.write(line + "\n")
        self.cpu_system_log.flush()
        if self.print_console: print(line)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system):
        "Logs CPU metrics at process level"
        line = '{"index : { "_index", "'+self.index+'", "_type", "Process CPU", "_id", "'+str(self.cpu_proc_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "pid": "' + str(pid) + ', "priority": "' + str(priority) + '", '\
                '"context switches": "' + str(ctx_count) + '", "threads": "' + str(n_threads) + '", ' + \
                '"cpu user": "' + str(cpu_user) + '", "cpu system": "'+str(cpu_system)+'"}'
        self.cpu_proc_id += 1
        self.cpu_proc_log.write(line + "\n")
        self.cpu_proc_log.flush()
        if self.print_console: print(line)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        line = '{"index : { "_index", "'+self.index+'", "_type", "System Memory", "_id", "'+str(self.mem_sys_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "available": "' + str(available) + ', "percent": "' + str(percent) + '", ' +\
                '"used": "' + str(used) + '", "free": "' + str(free) + '", "swap total": "' + str(swap_total) + '", ' + \
                '"swap used": "' + str(swap_used) + '", "swap free": "' + str(swap_free) + '", "swap in": "' + str(swap_in) + '", ' + \
                '"swap out": "' + str(swap_out) + '", "swap percent": "'+str(swap_percent)+'"}'
        self.mem_sys_id += 1
        self.mem_system_log.write(line + "\n")
        self.mem_system_log.flush()
        if self.print_console: print(line)

    def mem_proc(self, epoch, pid, rss, vms, percent):
        "Logs memory metrics at process level"
        line = '{"index : { "_index", "'+self.index+'", "_type", "Process Memory", "_id", "'+str(self.mem_proc_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "pid": "' + str(pid) + ', "rss": "' + str(rss) + '", '\
                '"vms": "' + str(vms) + '", "percent": "' + str(percent) + '"}'
        self.mem_proc_id += 1
        self.mem_proc_log.write(line + "\n")
        self.mem_proc_log.flush()
        if self.print_console: print(line)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        line = '{"index : { "_index", "'+self.index+'", "_type", "System IO", "_id", "'+str(self.io_sys_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "bytes sent": "' + str(bytes_sent) + ', "bytes recv": "' + str(bytes_recv) + '", ' +\
                '"packets sent": "' + str(packets_sent) + '", "packets received": "' + str(packets_recv) + '", ' + \
                '"errors in": "' + str(errin) + '", "errors out": "' + str(errout) + '", "dropped in": "' + str(dropin) + '", ' + \
                '"dropped out": "' + str(dropout) +'"}'
        self.io_sys_id += 1
        self.io_system_log.write(line + "\n")
        self.io_system_log.flush()
        if self.print_console: print(line)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = '{"index : { "_index", "'+self.index+'", "_type", "Process Errors", "_id", "'+str(self.proc_error_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "pid": "' + str(pid) + ', "name": "' + str(name)+'"}'
        self.proc_error_id += 1
        self.proc_error_log.write(line + "\n")
        self.proc_error_log.flush()
        if self.print_console: print(line)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = '{"index : { "_index", "'+self.index+'", "_type", "Process Info", "_id", "'+str(self.proc_info_id)+'"}}\n'
        line += '{"time": "'+str(epoch) + '", "pid": "' + str(pid) + ', "name": "' + str(name)+'"}'
        self.proc_info_id += 1
        self.proc_info_log.write(line + "\n")
        self.proc_info_log.flush()
        if self.print_console: print(line)
