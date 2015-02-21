__author__ = 'teemu kanstren'

import resource_probes.config as config
import resource_probes.main

config.ES_FILE_ENABLED = True
config.CSV_ENABLED = False

resource_probes.main.run_poller()
