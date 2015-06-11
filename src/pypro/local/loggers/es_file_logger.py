__author__ = 'teemu kanstren'

import time

import pypro.utils as utils
import pypro.config as config
import pypro.local.body_builder as bb
from pypro.head_builder import HeadBuilder


class ESFileLogger:
    def __init__(self):
        utils.check_dir()

        self.head = HeadBuilder("_index", "_type", "_id", config.ES_INDEX)

        self.session_log = open(utils.session_log+".es", "w", encoding="utf-8")
        self.session_info()

        self.cpu_sys_id = 1
        self.cpu_system_log = open(utils.cpu_sys_log+".es", "w", encoding="utf-8")
        self.cpu_proc_id = 1
        self.cpu_proc_log = open(utils.cpu_proc_log+".es", "w", encoding="utf-8")

        self.mem_sys_id = 1
        self.mem_system_log = open(utils.mem_sys_log+".es", "w", encoding="utf-8")
        self.mem_proc_id = 1
        self.mem_proc_log = open(utils.mem_proc_log+".es", "w", encoding="utf-8")

        self.io_sys_id = 1
        self.io_system_log = open(utils.io_sys_log+".es", "w", encoding="utf-8")

        self.proc_info_id = 1
        self.proc_info_log = open(utils.proc_info_log+".es", "w", encoding="utf-8")
        self.event_id = 1
        self.event_log = open(utils.event_log+".es", "w", encoding="utf-8")

    def close(self):
        self.cpu_system_log.close()
        self.cpu_proc_log.close()
        self.mem_system_log.close()
        self.mem_proc_log.close()
        self.io_system_log.close()
        self.proc_info_log.close()
        self.event_log.close()

    def start(self): pass

    def commit(self): pass

    def session_info(self):
        now = int(time.time()) * 1000
        line = '{"index" : '+self.head.create('session_info', 'session-'+str(now))+'}\n'
#        line = '{"index" : { "_index" : "'+config.ES_INDEX+'", "_type" : "session_info", "_id" : "session-'+str(now)+'"}}\n'
        line += bb.session_info()
        self.session_log.write(line + "\n")
        self.session_log.flush()

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('system_cpu', 'cpu_sys_'+str(self.cpu_sys_id))+'}\n'
#        line = '{"index" : { "_index" : "'+config.ES_INDEX+'", "_type" : "system_cpu", "_id" : "cpu_sys_'+str(self.cpu_sys_id)+'"}}\n'
        line += bb.cpu_sys(epoch, user_count, system_count, idle_count, percent)
        self.cpu_sys_id += 1
        self.cpu_system_log.write(line + "\n")
        self.cpu_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
        "Logs CPU metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('process_cpu', 'cpu_proc_'+str(self.cpu_proc_id))+'}\n'
#        line = '{"index" : { "_index" : "'+config.ES_INDEX+'", "_type" : "process_cpu", "_id" : "cpu_proc_'+str(self.cpu_proc_id)+'"}}\n'
        line += bb.cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname)
        self.cpu_proc_id += 1
        self.cpu_proc_log.write(line + "\n")
        self.cpu_proc_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('system_memory', 'mem_sys_'+str(self.mem_sys_id))+'}\n'
#        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type" : "system_memory", "_id" : "mem_sys_'+str(self.mem_sys_id)+'"}}\n'
        line += bb.mem_sys(epoch, available, percent, used, free, swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent)
        self.mem_sys_id += 1
        self.mem_system_log.write(line + "\n")
        self.mem_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('process_memory', 'mem_proc_'+str(self.mem_proc_id))+'}\n'
#        line = '{"index" : { "_index": "'+config.ES_INDEX+'", "_type": "process_memory", "_id": "mem_proc_'+str(self.mem_proc_id)+'"}}\n'
        line += bb.mem_proc(epoch, pid, rss, vms, percent, pname)
        self.mem_proc_id += 1
        self.mem_proc_log.write(line + "\n")
        self.mem_proc_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('system_io', 'io_sys_'+str(self.io_sys_id))+'}\n'
#        line = '{"index" : { "_index" : "'+config.ES_INDEX+'", "_type" : "system_io", "_id" : "io_sys_'+str(self.io_sys_id)+'"}}\n'
        line += bb.io_sys(epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)
        self.io_sys_id += 1
        self.io_system_log.write(line + "\n")
        self.io_system_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('event', 'proc_error_'+str(self.event_id))+'}\n'
#        line = '{"index" : { "_index" : "'+config.ES_INDEX+'", "_type" : "event", "_id" : "proc_error_'+str(self.event_id)+'"}}\n'
        line += bb.proc_error(epoch, pid, name)
        self.event_id += 1
        self.event_log.write(line + "\n")
        self.event_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        line = '{"index" : '+self.head.create('process_info', 'proc_info_'+str(self.proc_info_id))+'}\n'
#        line = '{"index" : { "_index" : "'+config.ES_INDEX+'", "_type" : "process_info", "_id" : "proc_info_'+str(self.proc_info_id)+'"}}\n'
        line += bb.proc_info(epoch, pid, name)
        self.proc_info_id += 1
        self.proc_info_log.write(line + "\n")
        self.proc_info_log.flush()
        if config.PRINT_CONSOLE: print(line)

