__author__ = 'teemu kanstren'

import time

from elasticsearch import Elasticsearch

import pypro.local.config as config
import pypro.local.body_builder as bb


class ESNetLogger:
    def __init__(self):
        self.cpu_sys_id = 1
        self.cpu_proc_id = 1

        self.mem_sys_id = 1
        self.mem_proc_id = 1

        self.io_sys_id = 1

        self.proc_info_id = 1
        self.proc_error_id = 1

        self.es = Elasticsearch([config.ES_HOST+':'+str(config.ES_PORT)],
                                sniff_on_start=False, sniff_on_connection_fail=False, sniffer_timeout=60)

    def close(self):
        pass

    def start(self): pass

    def commit(self): pass

    def session_info(self):
        now = int(time.time()*1000)
        body = bb.session_info()
        reply = self.es.index(index=config.DB_NAME, doc_type="session_info", id='session-'+str(now), body=body)
        if config.PRINT_CONSOLE: print(reply)

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        body = bb.cpu_sys(epoch, user_count, system_count, idle_count, percent)
        reply = self.es.index(index=config.DB_NAME, doc_type="system_cpu", id="cpu_sys_"+str(self.cpu_sys_id), body=body)
        self.cpu_sys_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
        "Logs CPU metrics at process level"
        body = bb.cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname)
        reply = self.es.index(index=config.DB_NAME, doc_type="process_cpu", id="cpu_proc_"+str(self.cpu_proc_id), body=body)
        self.cpu_proc_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        body = bb.mem_sys(epoch, available, percent, used, free, swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent)
        reply = self.es.index(index=config.DB_NAME, doc_type="system_memory", id="mem_sys_"+str(self.mem_sys_id), body=body)
        self.mem_sys_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        body = bb.mem_proc(epoch, pid, rss, vms, percent, pname)
        reply = self.es.index(index=config.DB_NAME, doc_type="process_memory", id="mem_proc_"+str(self.mem_proc_id), body=body)
        self.mem_proc_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        body = bb.io_sys(epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)
        reply = self.es.index(index=config.DB_NAME, doc_type="system_io", id="io_sys_"+str(self.io_sys_id), body=body)
        self.io_sys_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        body = bb.proc_error(epoch, pid, name)
        reply = self.es.index(index=config.DB_NAME, doc_type="event", id="proc_error_"+str(self.proc_error_id), body=body)
        self.proc_error_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        body = bb.proc_info(epoch, pid, name)
        reply = self.es.index(index=config.DB_NAME, doc_type="process_info", id="proc_info_"+str(self.proc_info_id), body=body)
        self.proc_info_id += 1
        if config.PRINT_CONSOLE: print(reply)

