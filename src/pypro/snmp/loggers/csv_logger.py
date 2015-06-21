__author__ = 'teemu kanstren'

import pypro.utils as utils
import pypro.snmp.config as config

class CSVFileLogger:
    files = {}

    def __init__(self):
        oids = config.SNMP_OIDS
        utils.check_dir()

        self.event_log = open(utils.event_log+".csv", "w", encoding="utf-8")
        event_header = "time;type;description"
        self.event_log.write(event_header + "\n")
        self.event_log.flush()

        for oid in oids:
            file_name = utils.log_dir + "/" + oid.oid_name.replace(' ', '_') + "_log.csv"
            log = open(file_name, "w", encoding="utf-8")
            header = "time;target;target_name;oid;oid_name;value"
            log.write(header + "\n")
            log.flush()
            self.files[oid.oid_id] = log

    def close(self):
        for file in self.files:
            file.close()
        self.event_log.close()

    def start(self, epoch):
        line = str(epoch) + ";info;session started ("+config.SESSION_NAME+")"
        self.event_log.write(line + "\n")
        self.event_log.flush()
        if config.PRINT_CONSOLE: print(line)

    def stop(self, epoch):
        line = str(epoch) + ";info;session stopped ("+config.SESSION_NAME+")"
        self.event_log.write(line + "\n")
        self.event_log.flush()
        if config.PRINT_CONSOLE: print(line)
        self.close()

    def value(self, epoch, oid, value):
        line = str(epoch) + ";" + oid.target() + ";" + oid.target_name + ";" + str(oid.oid_id) + ";" + str(oid.oid_name) + ";" + str(value)
        log = self.files[oid.oid_id]
        log.write(line + "\n")
        log.flush()
        if config.PRINT_CONSOLE: print(line)

    def error(self, epoch, description):
        line = str(epoch) + ";error;" + description
        self.event_log.write(line + "\n")
        self.event_log.flush()
        if config.PRINT_CONSOLE: print(line)
