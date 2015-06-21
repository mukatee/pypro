__author__ = 'teemu kanstren'

import time
import os
import unittest
import shutil
import inspect
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pkg_resources
from operator import itemgetter

from pypro.snmp.loggers.es_network_logger import ESNetLogger
from pypro import utils
import pypro.tests.t_assert as t_assert
import pypro.snmp.config as config
import pypro.tests.t_assert as t_assert
from pypro.snmp.oid import OID

#weird regex syntax, pattern required, weird errors...

#es = Elasticsearch()
#config.ES_INDEX = "pypro_tests"
#data = es.search(index=config.ES_INDEX)
#items = data["hits"]["hits"]
#print(str(items[0]["_source"]["bytes_sent"]))
#        data = self.es.get(config.ES_INDEX, doc_type="system_cpu")
#print(str(data))

class TestESNetLogs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TestESNetLogs.oid1 = OID("1.1.1.1.1", "test_oid1", "public", "127.0.0.1", 55, "test target 1", True)
        TestESNetLogs.oid2 = OID("1.1.1.1.1.0", "test_oid2", "private", "127.0.0.1", 255, "test target 2", True)
        TestESNetLogs.oid3 = OID("1.1.1.2.1", "test_oid3", "public", "127.0.0.1", 155, "test target 3", False)
        TestESNetLogs.oid4 = OID("1.1.1.2.1.0", "test_oid4", "private", "127.0.0.1", 233, "test target 4", False)
        config.SNMP_OIDS.append(TestESNetLogs.oid1)
        config.SNMP_OIDS.append(TestESNetLogs.oid2)
        config.SNMP_OIDS.append(TestESNetLogs.oid3)
        config.SNMP_OIDS.append(TestESNetLogs.oid4)
        config.ES_INDEX = "pypro_tests"
        config.PRINT_CONSOLE = False

    def setUp(self):
        if os.path.exists(utils.log_dir):
            shutil.rmtree(utils.log_dir, ignore_errors=True)
        self.es = Elasticsearch()
        self.es.delete_by_query(config.ES_INDEX, body='{"query":{"match_all":{}}}', ignore=[404])

    def test_numeric_oid_es(self):
        log = ESNetLogger()
        log.start(0)
        log.value(1, TestESNetLogs.oid1, 1)
        log.value(2, TestESNetLogs.oid1, 5)
        log.value(3, TestESNetLogs.oid2, 7)
        log.value(4, TestESNetLogs.oid2, 9)
        log.value(5, TestESNetLogs.oid1, 11)
        log.value(6, TestESNetLogs.oid1, 12)
        log.close()

        self.assert_es('expected_numeric.es')

    def test_string_oid_es(self):
        log = ESNetLogger()
        log.start(0)
        log.value(1, TestESNetLogs.oid3, "omg its bob\n\ron the line")
        log.value(2, TestESNetLogs.oid4, "now for bunnies..")
        log.value(3, TestESNetLogs.oid3, "this is a test\nwith linefeed")
        log.value(4, TestESNetLogs.oid4, "once upon a time")
        log.value(5, TestESNetLogs.oid3, "hello")
        log.value(6, TestESNetLogs.oid3, 11)
        log.value(7, TestESNetLogs.oid3, "ok passed?")
        log.close()

        self.assert_es('expected_string.es')

    def test_mixed_oid_es(self):
        log = ESNetLogger()
        log.start(0)
        log.value(1, TestESNetLogs.oid3, "omg its bob\n\ron the line")
        log.value(2, TestESNetLogs.oid4, "now for bunnies..")
        log.value(3, TestESNetLogs.oid1, 1)
        log.value(7, TestESNetLogs.oid1, 5)
        log.value(8, TestESNetLogs.oid2, 7)
        log.value(33, TestESNetLogs.oid3, "this is a test\nwith linefeed")
        log.value(555, TestESNetLogs.oid4, "once upon a time")
        log.value(3331, TestESNetLogs.oid3, "hello")
        log.value(11111, TestESNetLogs.oid1, 12)
        log.value(42322, TestESNetLogs.oid3, 11)
        log.value(111111, TestESNetLogs.oid3, "ok passed?")
        log.value(112223, TestESNetLogs.oid2, 9)
        log.value(22, TestESNetLogs.oid1, 11)
        log.close()

        self.assert_es('expected_mixed.es')

    def test_error_es(self):
#        time.sleep(1)
        log = ESNetLogger()

        log.error(11111, "epic fail")
        log.error(11111, "fail")
        log.error(11112, "little fail")

        self.assert_es('expected_errors.es')

    def assert_es(self, expected_file_name):
        time.sleep(1)
#        query='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}'
        data = self.es.search(index=config.ES_INDEX, scroll="10m",
                              body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
        scroll_id = data['_scroll_id']
        actual = self.read_es(data, "")
        items = data["hits"]["hits"]
        while len(items) > 0:
            data = self.es.scroll(scroll_id=scroll_id, scroll= "10m")
            items = data["hits"]["hits"]
            actual = self.read_es(data, actual)
#        print(actual)
        expected = pkg_resources.resource_string(__name__, expected_file_name).decode('utf8')
        t_assert.equal(actual, expected)

#this will produce only the first 10 items (or the size given... however that is done)
#        data = self.es.search(index=config.ES_INDEX, body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
#this is a scan, which loses the sort but is effective for very large data sets
#        response = self.es.search(index=config.ES_INDEX, search_type="scan", scroll="10m",
#                              body='{"query":{"match_all":{}}, "sort": { "time": { "order": "asc" }}}')
#        data = helpers.scan(client = self.es, query=query, scroll= "10m", index=config.ES_INDEX, timeout="1m")


    def read_es(self, data, actual):
        items = data["hits"]["hits"]
        for item in items:
            #sort the keys for deterministic comparison
            src = sorted(item["_source"].items(), key=itemgetter(0))
            #the linefeed at the end is not really needed but it makes for more readable error reports
            actual += str(src)+"\n"
        return actual