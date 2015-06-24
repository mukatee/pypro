__author__ = 'teemu kanstren'

import time
import os
import unittest
import shutil
import inspect
from elasticsearch import Elasticsearch
import pkg_resources

from pypro.local.loggers.es_network_logger import ESNetLogger
from pypro import utils
import pypro.tests.t_assert as t_assert
import pypro.local.config as config

#weird regex syntax, pattern required, weird errors...

#es = Elasticsearch()
#config.ES_INDEX = "pypro_tests"
#data = es.search(index=config.ES_INDEX)
#items = data["hits"]["hits"]
#print(str(items[0]["_source"]["bytes_sent"]))
#        data = self.es.get(config.ES_INDEX, doc_type="system_cpu")
#print(str(data))

class TestESLogs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config.DB_NAME = "pypro_tests"
        config.PRINT_CONSOLE = False

    def setUp(self):
        if os.path.exists(utils.log_dir):
            shutil.rmtree(utils.log_dir, ignore_errors=True)
        self.es = Elasticsearch()
        self.es.delete_by_query(config.DB_NAME, body='{"query":{"match_all":{}}}', ignore=[404])

    def test_cpu_sys_es(self):
        log = ESNetLogger()
        log.cpu_sys(0, 1, 1, 1, 1)
        log.cpu_sys(1, 3, 2, 5, 6)
        log.cpu_sys(3, 22, 99, 11, 4)
        log.cpu_sys(5, 155, 122, 12, 22)
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(4, len(items), "number of cpu sys items logged")
        self.assert_cpu_sys(items[0]["_source"], 0, 1, 1, 1, 1)
        self.assert_cpu_sys(items[1]["_source"], 1, 3, 2, 5, 6)
        self.assert_cpu_sys(items[2]["_source"], 3, 22, 99, 11, 4)
        self.assert_cpu_sys(items[3]["_source"], 5, 155, 122, 12, 22)

    def assert_cpu_sys(self, item, time, user_count, system_count, idle_count, percent):
        self.assertEqual(5, len(item), "number of properties for a cpu sys item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['percent'], percent)
        self.assertEqual(item['idle_count'], idle_count)
        self.assertEqual(item['system_count'], system_count)
        self.assertEqual(item['user_count'], user_count)

    def test_cpu_proc_es(self):
        log = ESNetLogger()
        log.cpu_proc(0, 1, 1, 1, 1, 1, 1, 1, "p1")
        log.cpu_proc(1, 2, 1, 3, 4, 2, 3, 1, "p2")
        log.cpu_proc(2, 3, 2, 122, 7, 5, 8, 11, "p3")
        log.cpu_proc(10, 1, 1, 1, 1, 1, 1, 1, "p1")
        log.cpu_proc(11, 2, 1, 3, 4, 2, 3, 1, "p2")
        log.cpu_proc(12, 3, 2, 122, 7, 5, 8, 11, "p3")
        log.cpu_proc(20, 1, 1, 5, 1, 4, 3, 2, "p1")
        log.cpu_proc(21, 3, 2, 555, 7, 11, 55, 32, "p3")
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(8, len(items), "number of cpu proc items logged")
#        print(str(items[0]["_source"]))
        self.assert_cpu_proc(items[0]["_source"], 0, 1, 1, 1, 1, 1, 1, 1, "p1")
        self.assert_cpu_proc(items[1]["_source"], 1, 2, 1, 3, 4, 2, 3, 1, "p2")
        self.assert_cpu_proc(items[2]["_source"], 2, 3, 2, 122, 7, 5, 8, 11, "p3")
        self.assert_cpu_proc(items[3]["_source"], 10, 1, 1, 1, 1, 1, 1, 1, "p1")
        self.assert_cpu_proc(items[4]["_source"], 11, 2, 1, 3, 4, 2, 3, 1, "p2")
        self.assert_cpu_proc(items[5]["_source"], 12, 3, 2, 122, 7, 5, 8, 11, "p3")
        self.assert_cpu_proc(items[6]["_source"], 20, 1, 1, 5, 1, 4, 3, 2, "p1")
        self.assert_cpu_proc(items[7]["_source"], 21, 3, 2, 555, 7, 11, 55, 32, "p3")

    def assert_cpu_proc(self, item, time, pid, priority, ctx_count, n_threads, cpu_user, cpu_system, percent, pname):
        self.assertEqual(9, len(item), "number of properties for a cpu sys item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['pid'], pid)
        self.assertEqual(item['priority'], priority)
        self.assertEqual(item['context_switches'], ctx_count)
        self.assertEqual(item['threads'], n_threads)
        self.assertEqual(item['cpu_user'], cpu_user)
        self.assertEqual(item['cpu_system'], cpu_system)
        self.assertEqual(item['percent'], percent)
        self.assertEqual(item['pname'], pname)
        # args = locals().copy()
        # del args["self"]
        # del args["item"]
        # expected_len = len(args) #reduce self and item
        # actual_len = len(item)
        # self.assertEqual(expected_len, actual_len, "number of properties for a cpu proc")
        # for arg in args:
        #     value = args[arg]
        #     if arg == "time":
        #         value *= 1000
        #     self.assertEqual(item[arg], value)

    def test_mem_sys_es(self):
        log = ESNetLogger()
        log.mem_sys(0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        log.mem_sys(10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
        log.mem_sys(12, 34, 654, 24, 33, 23, 442, 1, 13, 21, 44)
        log.mem_sys(15, 3445, 345, 345, 44, 745, 367, 32, 1111, 33, 55)
        log.mem_sys(33, 33, 453, 998, 347, 976, 8544, 45, 5555, 66, 33)
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(5, len(items), "number of mem sys items logged")
        self.assert_mem_sys(items[0]["_source"], 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        self.assert_mem_sys(items[1]["_source"], 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
        self.assert_mem_sys(items[2]["_source"], 12, 34, 654, 24, 33, 23, 442, 1, 13, 21, 44)
        self.assert_mem_sys(items[3]["_source"], 15, 3445, 345, 345, 44, 745, 367, 32, 1111, 33, 55)
        self.assert_mem_sys(items[4]["_source"], 33, 33, 453, 998, 347, 976, 8544, 45, 5555, 66, 33)

    def assert_mem_sys(self, item, time, available, percent, used, free,
                swap_total, swap_used, swap_free, swap_in, swap_out, swap_percent):
        self.assertEqual(11, len(item), "number of properties for a mem sys item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['available'], available)
        self.assertEqual(item['percent'], percent)
        self.assertEqual(item['used'], used)
        self.assertEqual(item['free'], free)
        self.assertEqual(item['swap_total'], swap_total)
        self.assertEqual(item['swap_used'], swap_used)
        self.assertEqual(item['swap_free'], swap_free)
        self.assertEqual(item['swap_in'], swap_in)
        self.assertEqual(item['swap_out'], swap_out)
        self.assertEqual(item['swap_percent'], swap_percent)

    def test_mem_proc_es(self):
        log = ESNetLogger()
        log.mem_proc(0, 1, 11, 15, 5, "p1")
        log.mem_proc(1, 2, 1, 3, 2, "p2")
        log.mem_proc(2, 5432, 21, 33, 9, "p3")
        log.mem_proc(5, 1, 22, 11, 3, "p1")
        log.mem_proc(6, 5432, 7, 55, 7, "p3")
        log.mem_proc(66, 1, 11, 15, 5, "p1")
        log.mem_proc(67, 2, 11, 0, 22, "p2")
        log.mem_proc(68, 5432, 212, 334, 44, "p3")
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(8, len(items), "number of mem proc items logged")
#        print(str(items[0]["_source"]))
        self.assert_mem_proc(items[0]["_source"], 0, 1, 11, 15, 5, "p1")
        self.assert_mem_proc(items[1]["_source"], 1, 2, 1, 3, 2, "p2")
        self.assert_mem_proc(items[2]["_source"], 2, 5432, 21, 33, 9, "p3")
        self.assert_mem_proc(items[3]["_source"], 5, 1, 22, 11, 3, "p1")
        self.assert_mem_proc(items[4]["_source"], 6, 5432, 7, 55, 7, "p3")
        self.assert_mem_proc(items[5]["_source"], 66, 1, 11, 15, 5, "p1")
        self.assert_mem_proc(items[6]["_source"], 67, 2, 11, 0, 22, "p2")
        self.assert_mem_proc(items[7]["_source"], 68, 5432, 212, 334, 44, "p3")

    def assert_mem_proc(self, item, time, pid, rss, vms, percent, pname):
        self.assertEqual(6, len(item), "number of properties for a mem proc item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['pid'], pid)
        self.assertEqual(item['rss'], rss)
        self.assertEqual(item['vms'], vms)
        self.assertEqual(item['percent'], percent)
        self.assertEqual(item['pname'], pname)

    def test_io_sys_es(self):
        log = ESNetLogger()
        log.io_sys(11111, 22, 22, 34, 43, 11, 11, 5, 3)
        log.io_sys(22222, 55, 23, 44, 34, 23, 17, 15, 4)
        log.io_sys(22233, 65, 23, 777, 44, 28, 18, 35, 5)
        log.io_sys(25555, 78, 44, 1911, 53, 99434, 43, 43, 21)
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(4, len(items), "number of mem sys items logged")
#        print(str(items[0]["_source"]))
        self.assert_io_sys(items[0]["_source"], 11111, 22, 22, 34, 43, 11, 11, 5, 3)
        self.assert_io_sys(items[1]["_source"], 22222, 55, 23, 44, 34, 23, 17, 15, 4)
        self.assert_io_sys(items[2]["_source"], 22233, 65, 23, 777, 44, 28, 18, 35, 5)
        self.assert_io_sys(items[3]["_source"], 25555, 78, 44, 1911, 53, 99434, 43, 43, 21)

    def assert_io_sys(self, item, time, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout):
        self.assertEqual(9, len(item), "number of properties for a mem proc item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['bytes_sent'], bytes_sent)
        self.assertEqual(item['bytes_recv'], bytes_recv)
        self.assertEqual(item['packets_sent'], packets_sent)
        self.assertEqual(item['packets_received'], packets_recv)
        self.assertEqual(item['errors_in'], errin)
        self.assertEqual(item['errors_out'], errout)
        self.assertEqual(item['dropped_in'], dropin)
        self.assertEqual(item['dropped_out'], dropout)

    def test_proc_error_es(self):
        log = ESNetLogger()
        log.proc_error(11111, 22, "epic fail")
        log.proc_error(11112, 9758, "fail")
        log.proc_error(11113, 7364, "little fail")
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(3, len(items), "number of mem sys items logged")
#        print(str(items[0]["_source"]))
        self.assert_proc_error(items[0]["_source"], 11111, 22, "epic fail")
        self.assert_proc_error(items[1]["_source"], 11112, 9758, "fail")
        self.assert_proc_error(items[2]["_source"], 11113, 7364, "little fail")

    def assert_proc_error(self, item, time, pid, name):
        self.assertEqual(3, len(item), "number of properties for a proc error item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['pid'], pid)
        self.assertEqual(item['name'], name)

    def test_proc_info_es(self):
        log = ESNetLogger()
        log.proc_info(11111, 22, "proc1")
        log.proc_info(11111, 9758, "proc2")
        log.proc_info(11111, 7364, "proc4")
        log.proc_info(11111, 3332, "proc3")
        log.close()
        time.sleep(1)
        data = self.es.search(index=config.DB_NAME, body='{"query":{"match_all":{}}, "sort": { "pid": { "order": "asc" }}}')
        items = data["hits"]["hits"]
        self.assertEqual(4, len(items), "number of mem sys items logged")
#        print(str(items[0]["_source"]))
        self.assert_proc_error(items[0]["_source"], 11111, 22, "proc1")
        self.assert_proc_error(items[1]["_source"], 11111, 3332, "proc3")
        self.assert_proc_error(items[2]["_source"], 11111, 7364, "proc4")
        self.assert_proc_error(items[3]["_source"], 11111, 9758, "proc2")

    def assert_proc_info(self, item, time, pid, name):
        self.assertEqual(3, len(item), "number of properties for a proc info item")
        self.assertEqual(item['time'], time)
        self.assertEqual(item['pid'], pid)
        self.assertEqual(item['name'], name)

