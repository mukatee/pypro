__author__ = 'teemu kanstren'

import pypro.local.main
import pypro.local.config as config

config.MYSQL_HOST = "192.168.2.79"
config.MYSQL_ENABLED = False

config.SESSION_NAME = "session2"
config.ES_INDEX = "pypro-local"
config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = True
config.CSV_ENABLED = True
config.KAFKA_ENABLED = True
config.KAFKA_TOPIC = "session2"
config.KAFKA_SERVER = "192.168.2.153"
config.PRINT_CONSOLE = True

config.INTERVAL = 1

config.PROCESS_LIST = ["iperf.exe"]

pypro.local.main.run_poller()




