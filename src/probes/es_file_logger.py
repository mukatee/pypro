__author__ = 'teemu kanstren'

import time
import utils
import config

class ESFileLogger:
    def __init__(self):
        utils.check_dir()

        self.session_log = open(utils.log_dir+"session-info-log.es", "w", encoding="utf-8")
        self.session_info()

        self.cpu_sys_id = 1
        self.cpu_system_log = open(utils.log_dir+"cpu-sys-log.es", "w", encoding="utf-8")
        self.cpu_proc_id = 1
        self.cpu_proc_log = open(utils.log_dir+"cpu-proc-log.es", "w", encoding="utf-8")

        self.mem_sys_id = 1
        self.mem_system_log = open(utils.log_dir+"mem-sys-log.es", "w", encoding="utf-8")
        self.mem_proc_id = 1
        self.mem_proc_log = open(utils.log_dir+"mem-proc-log.es", "w", encoding="utf-8")

        self.io_sys_id = 1
        self.io_system_log = open(utils.log_dir+"io-sys-log.es", "w", encoding="utf-8")

        self.proc_info_id = 1
        self.proc_info_log = open(utils.log_dir+"proc-info-log.es", "w", encoding="utf-8")
        self.event_id = 1
        self.event_log = open(utils.log_dir+"event-log.es", "w", encoding="utf-8")

    def close(self):
        self.cpu_system_log.close()
        self.cpu_proc_log.close()
        self.mem_system_log.close()
        self.mem_proc_log.close()
        self.io_system_log.close()
        self.proc_info_log.close()
        self.event_log.close()

    def session_info(self):
        now = time.time()
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "session_info", "_id": "session-'+str(now)+'"}}\n'
        line += '{"description": '+ config.SESSION_NAME + ', "start_time": ' + str(now) + '}'
        self.session_log.write(line + "\n")
        self.session_log.flush()

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "system_cpu", "_id": "cpu_sys_'+str(self.cpu_sys_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "user_count": ' + str(user_count) + ', ' +\
                '"system_count": ' + str(system_count) + ', "idle_count": ' + str(idle_count) + ', ' + \
                '"percent": ' + str(percent) + '}'
        self.cpu_sys_id += 1
        self.cpu_system_log.write(line + "\n")
        self.cpu_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent):
        "Logs CPU metrics at process level"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "process_cpu", "_id": "cpu_proc_'+str(self.cpu_proc_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "priority": ' + str(priority) + ', '\
                '"context_switches": ' + str(ctx_count) + ', "threads": ' + str(n_threads) + ', ' + \
                '"cpu_user": ' + str(cpu_user) + ', "cpu_system": '+str(cpu_system) + ', "percent": '+str(percent)+'}'
        self.cpu_proc_id += 1
        self.cpu_proc_log.write(line + "\n")
        self.cpu_proc_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "system_memory", "_id": "mem_sys_'+str(self.mem_sys_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "available": ' + str(available) + ', "percent": ' + str(percent) + ', ' +\
                '"used": ' + str(used) + ', "free": ' + str(free) + ', "swap_total": ' + str(swap_total) + ', ' + \
                '"swap_used": ' + str(swap_used) + ', "swap_free": ' + str(swap_free) + ', "swap_in": ' + str(swap_in) + ', ' + \
                '"swap_out": ' + str(swap_out) + ', "swap_percent": '+str(swap_percent)+'}'
        self.mem_sys_id += 1
        self.mem_system_log.write(line + "\n")
        self.mem_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def mem_proc(self, epoch, pid, rss, vms, percent):
        "Logs memory metrics at process level"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "process_memory", "_id": "mem_proc_'+str(self.mem_proc_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "rss": ' + str(rss) + ', '\
                '"vms": ' + str(vms) + ', "percent": ' + str(percent) + '}'
        self.mem_proc_id += 1
        self.mem_proc_log.write(line + "\n")
        self.mem_proc_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "system_io", "_id": "io_sys_'+str(self.io_sys_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "bytes_sent": ' + str(bytes_sent) + ', "bytes_recv": ' + str(bytes_recv) + ', ' +\
                '"packets_sent": ' + str(packets_sent) + ', "packets_received": ' + str(packets_recv) + ', ' + \
                '"errors_in": ' + str(errin) + ', "errors_out": ' + str(errout) + ', "dropped_in": ' + str(dropin) + ', ' + \
                '"dropped_out": ' + str(dropout) +'}'
        self.io_sys_id += 1
        self.io_system_log.write(line + "\n")
        self.io_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "event", "_id": "proc_error_'+str(self.event_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        self.event_id += 1
        self.event_log.write(line + "\n")
        self.event_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "process_info", "_id": "proc_info_'+str(self.proc_info_id)+'"}}\n'
        line += '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        self.proc_info_id += 1
        self.proc_info_log.write(line + "\n")
        self.proc_info_log.flush()
        if config.PRINT_CONSOLE: print(line)

