__author__ = 'teemu kanstren'

import os
import unittest
import shutil

import pkg_resources

from pypro.local.loggers.csv_file_logger import CSVFileLogger
from pypro import utils
import pypro.tests.t_assert as t_assert

#weird regex syntax, pattern required, weird errors...

class TestCSVLogs(unittest.TestCase):
    def setUp(self):
        if os.path.exists(utils.log_dir):
            shutil.rmtree(utils.log_dir, ignore_errors=True)

    def test_cpu_sys_csv(self):
#        self.assertEqual("a", "b")
        csv = CSVFileLogger()
        csv.cpu_sys(0, 1, 1, 1, 1)
        csv.cpu_sys(1, 3, 2, 5, 6)
        csv.cpu_sys(3, 22, 99, 11, 4)
        csv.cpu_sys(5, 155, 122, 12, 22)
        csv.close()
        actual = open(utils.cpu_sys_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_cpu_sys.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertEqualLF(actual+"a", expected)

    def test_cpu_proc_csv(self):
        csv = CSVFileLogger()
        csv.cpu_proc(0, 1, 1, 1, 1, 1, 1, 1, "p1")
        csv.cpu_proc(0, 2, 1, 3, 4, 2, 3, 1, "p2")
        csv.cpu_proc(0, 3, 2, 122, 7, 5, 8, 11, "p3")
        csv.cpu_proc(10, 1, 1, 1, 1, 1, 1, 1, "p1")
        csv.cpu_proc(10, 2, 1, 3, 4, 2, 3, 1, "p2")
        csv.cpu_proc(10, 3, 2, 122, 7, 5, 8, 11, "p3")
        csv.cpu_proc(20, 1, 1, 5, 1, 4, 3, 2, "p1")
        csv.cpu_proc(20, 3, 2, 555, 7, 11, 55, 32, "p3")
        csv.close()
        actual = open(utils.cpu_proc_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_cpu_proc.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertMultiLineEqualLF(actual, expected)

    def test_mem_sys_csv(self):
        csv = CSVFileLogger()
        csv.mem_sys(0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        csv.mem_sys(10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
        csv.mem_sys(12, 34, 654, 24, 33, 23, 442, 1, 13, 21, 44)
        csv.mem_sys(15, 3445, 345, 345, 44, 745, 367, 32, 1111, 33, 55)
        csv.mem_sys(33, 33, 453, 998, 347, 976, 8544, 45, 5555, 66, 33)
        csv.close()
        actual = open(utils.mem_sys_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_mem_sys.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertEqualLF(actual, expected)

    def test_mem_proc_csv(self):
        csv = CSVFileLogger()
        csv.mem_proc(0, 1, 11, 15, 5, "p1")
        csv.mem_proc(0, 2, 1, 3, 2, "p2")
        csv.mem_proc(0, 5432, 21, 33, 9, "p3")
        csv.mem_proc(5, 1, 22, 11, 3, "p1")
        csv.mem_proc(5, 5432, 7, 55, 7, "p3")
        csv.mem_proc(66, 1, 11, 15, 5, "p1")
        csv.mem_proc(66, 2, 11, 0, 22, "p2")
        csv.mem_proc(66, 5432, 212, 334, 44, "p3")
        csv.close()
        actual = open(utils.mem_proc_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_mem_proc.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertMultiLineEqualLF(actual, expected)

    def test_io_sys_csv(self):
        csv = CSVFileLogger()
        csv.io_sys(11111, 22, 22, 34, 43, 11, 11, 5, 3)
        csv.io_sys(22222, 55, 23, 44, 34, 23, 17, 15, 4)
        csv.io_sys(22233, 65, 23, 777, 44, 28, 18, 35, 5)
        csv.io_sys(25555, 78, 44, 1911, 53, 99434, 43, 43, 21)
        csv.close()
        actual = open(utils.io_sys_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_io_sys.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertEqualLF(actual, expected)

    def test_proc_error_csv(self):
        csv = CSVFileLogger()
        csv.proc_error(11111, 22, "epic fail")
        csv.proc_error(11111, 9758, "fail")
        csv.proc_error(11112, 7364, "little fail")
        csv.close()
        actual = open(utils.event_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_events.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertEqualLF(actual, expected)

    def test_proc_info_csv(self):
        csv = CSVFileLogger()
        csv.proc_info(11111, 22, "proc1")
        csv.proc_info(11111, 9758, "proc2")
        csv.proc_info(11111, 7364, "proc4")
        csv.proc_info(11111, 3332, "proc3")
        csv.close()
        actual = open(utils.proc_info_log+".csv").read()
        expected = pkg_resources.resource_string(self.__module__, 'expected_proc_info.csv').decode('utf8')
        t_assert.equal(actual, expected)
#        self.assertEqualLF(actual, expected)
