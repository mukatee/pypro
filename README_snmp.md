Python Resource Probes, SNMP version
====================================

Python probes for collecting information about system resources by using SNMP queries over the network.
Based on the *pysnmp* library.
Built using Python 3.4. No idea about workings with other versions.

Requirements
------------
- Python3. Tested with 3.4.
- PySNMP. The Python package used to perform SNMP queries. Should install as dependency, otherwise "pip3 install pysnmp".
- Elascticsearch package (for ES logger). Should install as dependency, otherwise "pip3 install elasticsearch".
- Python Kafka package (for Kafka logger). Should install as dependency. Otherwise "pip3 install kafka-python".

On a unix-based system you likely need to sudo yourself to install the dependencies, or this package itself (for pip3).
If you know how to add an external dependency for the mysql.connector to the setup file so it is installed as dependency, let me know.

Installation
------------
"pip3 install pypro-snmp" for the SNMP version. Or just get the source and go with it.

Data stores
-----------
Supported logging targets are:
- CSV file
- Elasticsearch bulk import file
- Elasticsearch indexing directly over network
- Kafka producer (you need to write the consumer)

Session Information
-------------------
For each recording session, the following information is also recorded:
- Description: User provided description of the recording session.
- Start time: Time when session was started.

Timestamps
----------
Besides the above resource data fields ("metrics"), each recorded entry also contains a timestamp.
The timestamps are recorded as Epoch timestamps.
Seconds for Kafka/CSV, milliseconds for Elasticsearch.

NOTE: If you use Elasticsearch to store the data, you should use the
[schema.json](https://github.com/mukatee/pypro/blob/master/src/schema_snmp.json) file to set up the mapping.
For example, "curl -XPOST 'http://localhost:9200/session1' --data-binary @schema.json"
The mapping is the ES equivalent of a database schema.
If you don't do this, the automatically generated schema will consider the timestamp as a "long" data type and
any date related functions will be unavailable.
For example, Kibana will not recognize is as a potential time column for visualization unless the type is correct.

Metrics
-------

You can use any SNMP OID supported by your target device.

Usage
-----
Configuration is defined in the pypro.snmp.config.py file.
Start from the pypro.snmp.main(.py) module.

Example use:

```python
import pypro.snmp.config as config
from pypro.snmp.oid import OID
from pypro.snmp.oids import *
import pypro.snmp.main as main

config.ES_FILE_ENABLED = True
config.CSV_ENABLED = False

#example for querying whatever OID you like, in this case the system uptime
config.SNMP_OIDS.append(OID('1.3.6.1.2.1.1.3.0', 'system uptime', 'public', '192.168.2.1', 161, 'router', True))
#These who are examples of build-in OID values
config.SNMP_OIDS.append(UserCPUTimeRaw('public', '192.168.2.1', 161, 'router'))
config.SNMP_OIDS.append(UserCPUTimePrct('public', '192.168.2.1', 161, 'router'))
#example of a derived value built from two OID's (total ram and free ram) to show used ram
config.SNMP_OIDS.append(RamUsed('public', '192.168.2.1', 161, 'router'))

main.run_poller()
```

For the example code, see [example.py](https://github.com/mukatee/pypro/blob/master/src/pypro/snmp/example.py).

For configuration options, see [config.py](https://github.com/mukatee/pypro/blob/master/src/pypro/snmp/config.py).

For a list of prebuilt OID's to poll, see [oids.py](https://github.com/mukatee/pypro/blob/master/src/pypro/snmp/oids.py).

For an example of how to build "derived measures",
see RamUsed class in [oids.py](https://github.com/mukatee/pypro/blob/master/src/pypro/snmp/oids.py).
This is a measure built from two or more oid values when the measure we want is not directly available.
You can extend the OID class in a similar way to build your own and append them to the config list.

License
-------

MIT License


