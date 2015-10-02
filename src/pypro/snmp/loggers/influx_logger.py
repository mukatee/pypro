__author__ = 'teemu kanstren'

from pypro.snmp import config
from pypro import utils
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

class InFluxLogger:
    indices = {}

    def __init__(self):
        self.client = InfluxDBClient(config.INFLUX_HOST, config.INFLUX_PORT, config.INFLUX_USER, config.INFLUX_PW, config.DB_NAME)
        try:
            self.client.create_database(config.DB_NAME)
        except InfluxDBClientError as e:
            print("Error while creating database, assuming it already exists:"+str(e))

    def close(self):
        pass

    def start(self, epoch):
        pass

    def stop(self, epoch):
        pass

    def value(self, epoch, oid, name, value):
        epoch *= 1000000
#        name = oid._name()
        name = name.replace(' ', '_')
        #get index with default value of 0, add 1
        index = self.indices.get(name, 0) + 1
        self.indices[name] = index
        #TODO: logging
        is_error = False
        str_value = str(value)
        if oid.is_numeric() and not utils.is_number(str_value):
            is_error = True
            print("Error: received non-numeric value for numeric value:"+str_value)
            return
        if oid.is_numeric(): value = float(value)
        else: value = str_value
        json_body = [{"measurement": name,
                      "tags": {"tom": oid.target_name, "oid": str(oid.oid_id)},
                      "time": epoch,
                      "time_precision": "ms",
                      "fields": {"value": value}
                     }
                    ]
        self.client.write_points(json_body)
        if config.PRINT_CONSOLE: print(json_body)

    def error(self, epoch, description):
        pass

