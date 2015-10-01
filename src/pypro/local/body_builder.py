__author__ = 'teemu kanstren'

import time

import pypro.local.config as config


def session_info():
    now = int(time.time()) * 1000
    body = '{"description" : "started ('+ config.SESSION_NAME + ')"}'
    return body

def cpu_sys(epoch, user_count, system_count, idle_count, percent):
    "CPU metrics at system level"
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "user_count" : ' + str(user_count) + ', ' +\
            '"system_count" : ' + str(system_count) + ', "idle_count" : ' + str(idle_count) + ', ' + \
            '"percent" : ' + str(percent) + '}'
    return body

def cpu_proc(epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
    "Logs CPU metrics at process level"
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "pid" : ' + str(pid) + ', "priority" : ' + str(priority) + ', '\
            '"context_switches" : ' + str(ctx_count) + ', "threads" : ' + str(n_threads) + ', ' + \
            '"cpu_user" : ' + str(cpu_user) + ', "cpu_system" : '+str(cpu_system) + ', "percent" : '+str(percent) + \
            ', "pname" : "' + pname + '"}'
    return body

def mem_sys(epoch, available, percent, used, free,
            swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
    "Logs memory metrics at system level"
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "available" : ' + str(available) + ', "percent" : ' + str(percent) + ', ' +\
            '"used" : ' + str(used) + ', "free" : ' + str(free) + ', "swap_total" : ' + str(swap_total) + ', ' + \
            '"swap_used" : ' + str(swap_used) + ', "swap_free" : ' + str(swap_free) + ', "swap_in" : ' + str(swap_in) + ', ' + \
            '"swap_out" : ' + str(swap_out) + ', "swap_percent" : '+str(swap_percent)+'}'
    return body

def mem_proc(epoch, pid, rss, vms, percent, pname):
    "Logs memory metrics at process level"
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "pid" : ' + str(pid) + ', "rss" : ' + str(rss) + ', '\
            '"vms" : ' + str(vms) + ', "percent" : ' + str(percent) + ', "pname" : "' + pname + '"}'
    return body

def io_sys(epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "bytes_sent" : ' + str(bytes_sent) + ', "bytes_recv" : ' + str(bytes_recv) + ', ' +\
            '"packets_sent" : ' + str(packets_sent) + ', "packets_received" : ' + str(packets_recv) + ', ' + \
            '"errors_in" : ' + str(errin) + ', "errors_out" : ' + str(errout) + ', "dropped_in" : ' + str(dropin) + ', ' + \
            '"dropped_out" : ' + str(dropout) +'}'
    return body

def proc_error(epoch, pid, name):
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "pid" : ' + str(pid) + ', "name" : "' + str(name)+'"}'
    return body

def proc_info(epoch, pid, name):
#    now = int(epoch) * 1000
    body = '{"time":'+str(epoch)+', "pid" : ' + str(pid) + ', "name" : "' + str(name)+'"}'
    return body

