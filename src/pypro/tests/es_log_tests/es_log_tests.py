__author__ = 'teemu kanstren'

import os
import unittest
import shutil
import pkg_resources
import pypro.local.utils as utils
from pypro.local.es_file_logger import ESFileLogger
import pypro.local.config as config

#weird regex syntax, pattern required, weird errors...

class TestESLogs(unittest.TestCase):
    def setUp(self):
        if os.path.exists(utils.log_dir):
            shutil.rmtree(utils.log_dir, ignore_errors=True)

    def test_cpu_sys_es(self):
        es = ESFileLogger()
        es.cpu_sys(0, 1, 1, 1, 1)
        es.cpu_sys(1, 3, 2, 5, 6)
        es.cpu_sys(3, 22, 99, 11, 4)
        es.cpu_sys(5, 155, 122, 12, 22)
        es.close()
        actual = open(utils.cpu_sys_log+".es").read()
        expected = pkg_resources.resource_string(__name__, 'expected_cpu_sys.es').decode('utf8')
        self.assertEqualLF(actual, expected)

    def test_cpu_proc_es(self):
        es = ESFileLogger()
        es.cpu_proc(0, 1, 1, 1, 1, 1, 1, 1, "p1")
        es.cpu_proc(0, 2, 1, 3, 4, 2, 3, 1, "p2")
        es.cpu_proc(0, 3, 2, 122, 7, 5, 8, 11, "p3")
        es.cpu_proc(10, 1, 1, 1, 1, 1, 1, 1, "p1")
        es.cpu_proc(10, 2, 1, 3, 4, 2, 3, 1, "p2")
        es.cpu_proc(10, 3, 2, 122, 7, 5, 8, 11, "p3")
        es.cpu_proc(20, 1, 1, 5, 1, 4, 3, 2, "p1")
        es.cpu_proc(20, 3, 2, 555, 7, 11, 55, 32, "p3")
        es.close()
        actual = open(utils.cpu_proc_log+".es").read()
        expected = pkg_resources.resource_string('pypro.tests.es_log_tests', 'expected_cpu_proc.es').decode('utf8')
#        print(self.unify_line_separators(actual))
#        print(self.unify_line_separators(expected))
        self.assertMultiLineEqualLF(actual, expected)

    def test_mem_sys_es(self):
        es = ESFileLogger()
        es.mem_sys(0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        es.mem_sys(10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
        es.mem_sys(12, 34, 654, 24, 33, 23, 442, 1, 13, 21, 44)
        es.mem_sys(15, 3445, 345, 345, 44, 745, 367, 32, 1111, 33, 55)
        es.mem_sys(33, 33, 453, 998, 347, 976, 8544, 45, 5555, 66, 33)
        es.close()
        actual = open(utils.mem_sys_log+".es").read()
        expected = pkg_resources.resource_string('pypro.tests.es_log_tests', 'expected_mem_sys.es').decode('utf8')
        self.assertEqualLF(actual, expected)

    def test_mem_proc_es(self):
        es = ESFileLogger()
        es.mem_proc(0, 1, 11, 15, 5, "p1")
        es.mem_proc(0, 2, 1, 3, 2, "p2")
        es.mem_proc(0, 5432, 21, 33, 9, "p3")
        es.mem_proc(5, 1, 22, 11, 3, "p1")
        es.mem_proc(5, 5432, 7, 55, 7, "p3")
        es.mem_proc(66, 1, 11, 15, 5, "p1")
        es.mem_proc(66, 2, 11, 0, 22, "p2")
        es.mem_proc(66, 5432, 212, 334, 44, "p3")
        es.close()
        actual = open(utils.mem_proc_log+".es").read()
        expected = pkg_resources.resource_string('pypro.tests.es_log_tests', 'expected_mem_proc.es').decode('utf8')
        self.assertMultiLineEqualLF(actual, expected)

    def test_io_sys_es(self):
        es = ESFileLogger()
        es.io_sys(11111, 22, 22, 34, 43, 11, 11, 5, 3)
        es.io_sys(22222, 55, 23, 44, 34, 23, 17, 15, 4)
        es.io_sys(22233, 65, 23, 777, 44, 28, 18, 35, 5)
        es.io_sys(25555, 78, 44, 1911, 53, 99434, 43, 43, 21)
        es.close()
        actual = open(utils.io_sys_log+".es").read()
        expected = pkg_resources.resource_string('pypro.tests.es_log_tests', 'expected_io_sys.es').decode('utf8')
        self.assertEqualLF(actual, expected)

    def test_proc_error_es(self):
        es = ESFileLogger()
        es.proc_error(11111, 22, "epic fail")
        es.proc_error(11111, 9758, "fail")
        es.proc_error(11112, 7364, "little fail")
        es.close()
        actual = open(utils.proc_error_log+".es").read()
        expected = pkg_resources.resource_string('pypro.tests.es_log_tests', 'expected_events.es').decode('utf8')
        self.assertEqualLF(actual, expected)

    def test_proc_info_es(self):
        es = ESFileLogger()
        es.proc_info(11111, 22, "proc1")
        es.proc_info(11111, 9758, "proc2")
        es.proc_info(11111, 7364, "proc4")
        es.proc_info(11111, 3332, "proc3")
        es.close()
        actual = open(utils.proc_info_log+".es").read()
        expected = pkg_resources.resource_string('pypro.tests.es_log_tests', 'expected_proc_info.es').decode('utf8')
        self.assertEqualLF(actual, expected)

    def assertEqualLF(self, actual, expected):
        actual = self.unify_line_separators(actual)
        expected = self.unify_line_separators(expected)
        self.assertEqual(expected, actual)

    def unify_line_separators(self, line):
        line = line.replace("\r\n", "\n")
        line = line.replace("\r", "\n")
        return line

    def assertMultiLineEqualLF(self, actual, expected):
        actual = self.unify_line_separators(actual)
        expected = self.unify_line_separators(expected)
        self.assertMultiLineEqual(expected, actual)
