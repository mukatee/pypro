__author__ = 'teemu kanstren'

import time
from elasticsearch import Elasticsearch
import pypro.local.config as config

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
                                sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=60)

    def close(self):
        pass

    def start(self): pass

    def commit(self): pass

    def session_info(self):
        now = int(time.time()) * 1000
        body = '{"description": "'+ config.SESSION_NAME + '", "start_time": ' + str(now) + '}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="session_info", id='session-'+str(now), body=body)
        if config.PRINT_CONSOLE: print(reply)

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "user_count": ' + str(user_count) + ', ' +\
                '"system_count": ' + str(system_count) + ', "idle_count": ' + str(idle_count) + ', ' + \
                '"percent": ' + str(percent) + '}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="system_cpu", id="cpu_sys_"+str(self.cpu_sys_id), body=body)
        self.cpu_sys_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
        "Logs CPU metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "priority": ' + str(priority) + ', '\
                '"context_switches": ' + str(ctx_count) + ', "threads": ' + str(n_threads) + ', ' + \
                '"cpu_user" : ' + str(cpu_user) + ', "cpu_system" : '+str(cpu_system) + ', "percent" : '+str(percent) + \
                ', "pname" : "' + pname + '"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="process_cpu", id="cpu_proc_"+str(self.cpu_proc_id), body=body)
        self.cpu_proc_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "available": ' + str(available) + ', "percent": ' + str(percent) + ', ' +\
                '"used": ' + str(used) + ', "free": ' + str(free) + ', "swap_total": ' + str(swap_total) + ', ' + \
                '"swap_used": ' + str(swap_used) + ', "swap_free": ' + str(swap_free) + ', "swap_in": ' + str(swap_in) + ', ' + \
                '"swap_out": ' + str(swap_out) + ', "swap_percent": '+str(swap_percent)+'}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="system_memory", id="mem_sys_"+str(self.mem_sys_id), body=body)
        self.mem_sys_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "rss": ' + str(rss) + ', '\
                '"vms": ' + str(vms) + ', "percent": ' + str(percent) + ', "pname" : "' + pname + '"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="process_memory", id="mem_proc_"+str(self.mem_proc_id), body=body)
        self.mem_proc_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "bytes_sent": ' + str(bytes_sent) + ', "bytes_recv": ' + str(bytes_recv) + ', ' +\
                '"packets_sent": ' + str(packets_sent) + ', "packets_received": ' + str(packets_recv) + ', ' + \
                '"errors_in": ' + str(errin) + ', "errors_out": ' + str(errout) + ', "dropped_in": ' + str(dropin) + ', ' + \
                '"dropped_out": ' + str(dropout) +'}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="system_io", id="io_sys_"+str(self.io_sys_id), body=body)
        self.io_sys_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def proc_error(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="event", id="proc_error_"+str(self.proc_error_id), body=body)
        self.proc_error_id += 1
        if config.PRINT_CONSOLE: print(reply)

    def proc_info(self, epoch, pid, name):
        "Print a line to console and to a file"
        epoch *= 1000 #this converts it into milliseconds
        body = '{"time": '+str(epoch) + ', "pid": ' + str(pid) + ', "name": "' + str(name)+'"}'
        reply = self.es.index(index=config.ES_INDEX, doc_type="process_info", id="proc_info_"+str(self.proc_info_id), body=body)
        self.proc_info_id += 1
        if config.PRINT_CONSOLE: print(reply)

