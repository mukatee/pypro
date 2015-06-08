__author__ = 'teemu kanstren'

import time
import pypro.local.config as config

class MySqlLogger:
    insert_session = "INSERT INTO session_info (description, start_time) VALUES (%s, %s)"
    insert_cpu_sys = "INSERT INTO cpu_sys (session_id, rec_time, user_mode, kernel_mode, idle_mode, percent) " + \
                     "VALUES (%s, %s, %s, %s, %s, %s)"
    insert_cpu_proc = "INSERT INTO cpu_proc (session_id, rec_time, proc_id, priority, ctx_switches, threads, user_mode, kernel_mode, percent) " + \
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_mem_sys = "INSERT INTO mem_sys (session_id, rec_time, available, percent, used, free, " + \
                     "swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent) " + \
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_mem_proc = "INSERT INTO mem_proc (session_id, rec_time, proc_id, used, virtual, percent) " + \
                     "VALUES (%s, %s, %s, %s, %s, %s)"
    insert_io_sys = "INSERT INTO io_sys (session_id, rec_time, bytes_sent, bytes_received, packets_sent, packets_received, " + \
                     "errors_in, errors_out, dropped_in, dropped_out) " + \
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_proc_error = "INSERT INTO event_log (session_id, event_time, event_type, description) " + \
                     "VALUES (%s, %s, %s, %s)"
    insert_proc_info = "INSERT INTO proc_info (session_id, rec_time, proc_id, name) " + \
                     "VALUES (%s, %s, %s, %s)"

    def __init__(self):
        import mysql.connector
        self.conn = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PW,
                                      host=config.MYSQL_HOST,
                                      database=config.MYSQL_DB)
        self.cursor = self.conn.cursor(prepared=True)

        self.cursor.execute(self.insert_session, (config.SESSION_NAME, time.time()))
        self.conn.commit()
        self.session_id = self.cursor.lastrowid

    def close(self):
        self.conn.close()

    def start(self):
        self.conn.start_transaction()

    def commit(self):
        self.conn.commit()

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        self.cursor.execute(self.insert_cpu_sys, (self.session_id, epoch, user_count, system_count, idle_count, percent))

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, cpu_percent, pname):
        "Logs CPU metrics at process level"
        self.cursor.execute(self.insert_cpu_proc, (self.session_id, epoch, pid, priority, ctx_count, n_threads,
                                                   cpu_user, cpu_system, cpu_percent))

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        self.cursor.execute(self.insert_mem_sys, (self.session_id, epoch, available, percent, used, free,
                                                  swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent))

    def mem_proc(self, epoch, pid, rss, vms, percent, pname):
        "Logs memory metrics at process level"
        self.cursor.execute(self.insert_mem_proc, (self.session_id, epoch, pid, rss, vms, percent))

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Logs IO activity"
        self.cursor.execute(self.insert_io_sys, (self.session_id, epoch, bytes_sent, bytes_recv,
                                                   packets_sent, packets_recv,
                                                   errin, errout, dropin, dropout))

    def proc_error(self, epoch, pid, name):
        "Logs an error related to process polling"
        self.cursor.execute(self.insert_proc_error, (self.session_id, epoch, 1, name))

    def proc_info(self, epoch, pid, name):
        "Logs information on a process"
        self.cursor.execute(self.insert_proc_info, (self.session_id, epoch, pid, name))

    def now(self):
        "Gives current time in milliseconds"
        return str((int) (time.time() * 1000))

