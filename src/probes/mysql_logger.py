__author__ = 'teemu kanstren'

import mysql.connector

class mysql_logger:
    def __init__(self):
        self.conn = mysql.connector.connect(user='pypro', password='omg-change-this-pw',
                                      host='localhost',
                                      database='pypro_db')

    def close(self):
        self.conn.close()

    def cpu_sys(self, epoch, user_count, system_count, idle_count, percent):
        "Logs CPU metrics at system level"
        pass

    def cpu_proc(self, epoch, pid, priority, ctx_count, n_threads, cpu_user, cpu_system):
        "Logs CPU metrics at process level"
        pass

    def mem_sys(self, epoch, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        "Logs memory metrics at system level"
        pass

    def mem_proc(self, epoch, pid, rss, vms, percent):
        "Logs memory metrics at process level"
        pass

    def io_sys(self, epoch, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        "Logs IO activity"
        pass

    def proc_error(self, epoch, pid, name):
        "Logs an error related to process polling"
        pass

    def proc_info(self, epoch, pid, name):
        "Logs information on a process"
        pass
