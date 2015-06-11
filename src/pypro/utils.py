__author__ = 'teemu kanstren'

import os

log_dir = "logs/"
session_log = log_dir+"session-info"
cpu_sys_log = log_dir+"cpu-log-sys"
cpu_proc_log = log_dir+"cpu-log-proc"
mem_sys_log = log_dir+"mem-log-sys"
mem_proc_log = log_dir+"mem-log-proc"
io_sys_log = log_dir+"io-log-sys"
event_log = log_dir+"event-log"
proc_info_log = log_dir+"proc-log-info"

def check_dir():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
