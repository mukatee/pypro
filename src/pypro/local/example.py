__author__ = 'teemu kanstren'

import pypro.local.main
import pypro.config as config

config.CSV_ENABLED = False
config.MYSQL_HOST = "192.168.2.79"
config.MYSQL_ENABLED = False

config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = True
config.INTERVAL = 1

config.PROCESS_LIST = [1132]

pypro.local.main.run_poller()




