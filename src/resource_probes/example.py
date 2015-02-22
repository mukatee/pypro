__author__ = 'teemu kanstren'

import resource_probes.main
import resource_probes.config as config

config.CSV_ENABLED = False
config.MYSQL_HOST = "192.168.2.79"
config.MYSQL_ENABLED = True

config.ES_NW_ENABLED = False
config.ES_FILE_ENABLED = False
config.INTERVAL = 1

resource_probes.main.run_poller()




