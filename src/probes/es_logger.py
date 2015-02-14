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
        self.io_system_log = open(utils.log_dir+"io-log-sys.es", "w", encoding="utf-8")

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
        line = '{"index" : { "_index": "'+self.index+'", "_type": "system_cpu", "_id": "cpu_sys_'+str(self.cpu_sys_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "user_count": ' + str(user_count) + ', ' +\
                '"system_count": ' + str(system_count) + ', "idle_count": ' + str(idle_count) + ', ' + \
                '"percent": ' + str(percent) + '}'
        self.cpu_sys_id += 1
        self.cpu_system_log.write(line + "\n")
        self.cpu_system_log.flush()
        if self.print_console: print(line)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system):
        "Logs CPU metrics at process level"
        line = '{"index" : { "_index": "'+self.index+'", "_type": "process_cpu", "_id": "cpu_proc_'+str(self.cpu_proc_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "priority": ' + str(priority) + ', '\
                '"context_switches": ' + str(ctx_count) + ', "threads": ' + str(n_threads) + ', ' + \
                '"cpu_user": ' + str(cpu_user) + ', "cpu_system": '+str(cpu_system)+'}'
        self.cpu_proc_id += 1
        self.cpu_proc_log.write(line + "\n")
        self.cpu_proc_log.flush()
        if self.print_console: print(line)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        line = '{"index" : { "_index": "'+self.index+'", "_type": "system_memory", "_id": "mem_sys'+str(self.mem_sys_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "available": ' + str(available) + ', "percent": ' + str(percent) + ', ' +\
                '"used": ' + str(used) + ', "free": ' + str(free) + ', "swap_total": ' + str(swap_total) + ', ' + \
                '"swap_used": ' + str(swap_used) + ', "swap_free": ' + str(swap_free) + ', "swap_in": ' + str(swap_in) + ', ' + \
                '"swap_out": ' + str(swap_out) + ', "swap_percent": '+str(swap_percent)+'}'
        self.mem_sys_id += 1
        self.mem_system_log.write(line + "\n")
        self.mem_system_log.flush()
        if self.print_console: print(line)

    def mem_proc(self, epoch, pid, rss, vms, percent):
        "Logs memory metrics at process level"
        line = '{"index" : { "_index": "'+self.index+'", "_type": "process_memory", "_id": "mem_proc_'+str(self.mem_proc_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "rss": ' + str(rss) + ', '\
                '"vms": ' + str(vms) + ', "percent": ' + str(percent) + '}'
        self.mem_proc_id += 1
        self.mem_proc_log.write(line + "\n")
        self.mem_proc_log.flush()
        if self.print_console: print(line)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        line = '{"index" : { "_index": "'+self.index+'", "_type": "system_io", "_id": "io_sys_'+str(self.io_sys_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "bytes_sent": ' + str(bytes_sent) + ', "bytes_recv": ' + str(bytes_recv) + ', ' +\
                '"packets_sent": ' + str(packets_sent) + ', "packets_received": ' + str(packets_recv) + ', ' + \
                '"errors_in": ' + str(errin) + ', "errors_out": ' + str(errout) + ', "dropped_in": ' + str(dropin) + ', ' + \
                '"dropped_out": ' + str(dropout) +'}'
        self.io_sys_id += 1
        self.io_system_log.write(line + "\n")
        self.io_system_log.flush()
        if self.print_console: print(line)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = '{"index" : { "_index": "'+self.index+'", "_type": "process_errors", "_id": "proc_error_'+str(self.proc_error_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        self.proc_error_id += 1
        self.proc_error_log.write(line + "\n")
        self.proc_error_log.flush()
        if self.print_console: print(line)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = '{"index" : { "_index": "'+self.index+'", "_type": "process_info", "_id": "proc_info_'+str(self.proc_info_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        self.proc_info_id += 1
        self.proc_info_log.write(line + "\n")
        self.proc_info_log.flush()
        if self.print_console: print(line)
