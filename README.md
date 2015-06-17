Python Resource Probes
======================

Python probes for collecting information about system resources.
Two versions, one that collects detailed information about the host it is running on.
And another one that performs SNMP queries over the network to collect data from other hosts.

Local version is based on the *psutil* library.
SNMP version is based on the *pysnmp* library.
Built using Python 3.4. No idea about workings with other versions.

Requirements
------------
- Python3. Tested with 3.4.
- PSUtil (for pypro-local). The Python package used to read the resource metrics. Should install as dependency, otherwise "pip3 install psutil".
- PySNMP (for pypro-snmp). The Python package used to perform SNMP queries. Should install as dependency, otherwise "pip3 install pysnmp".
- Elascticsearch package. Should install as dependency, otherwise "pip3 install elasticsearch".
- Python Kafka package. Should install as dependency. Otherwise "pip3 install kafka-python".
- Mysql.connector. "pip3 install mysql-connector-python --allow-external mysql-connector-python" or possibly
"sudo pip3 install --allow-external mysql-connector-python mysql-connector-python".

On a unix-based system you likely need to sudo yourself to install the dependencies, or this package itself (for pip3).
If you know how to add an external dependency for the mysql.connector to the setup file so it is installed as dependency, let me know.

Installation
------------
- "pip3 install pypro-local" for the local version. Or just get the source and go with it.
- "pip3 install pypro-snmp" for the SNMP version. Or just get the source and go with it.

Data stores
-----------
Supported logging targets are:
- CSV file
- Elasticsearch bulk import file
- Elasticsearch database
- MySQL database (for pypro-local only currently)
- Kafka producer

Metrics (pypro-local)
---------------------
The data collected consists of that supported by *psutil*.
Suggest to check [psutil](http://pythonhosted.org/psutil/) docs for more info.
As a summary the collected data contains:

- System Memory
  - Available: Memory available to processes on the system (bytes).
  - Free: Memory not used (bytes). Somehow different from available, check the psutil docs.
  - Used: Memory used on the system at given time (bytes).
  - Percent: Percentage of total memory used (0-100).
  - Swap total: Total size of swap memory on system (bytes).
  - Swap used: Used swap memory (bytes).
  - Swap free: Free swap memory (bytes).
  - Swap percent: Percentage of used swamp memory (0-100).
  - Swap in: Number of bytes swapped in from disk.
  - Swap out: Number of bytes swapped out to disk.

- System CPU
  - User time: Time spent in user mode (seconds).
  - System time: Time spent in kernel mode (seconds).
  - Idle time: Time spend idle (seconds).
  - Percent: CPU load percentage between polling intervals (0-100, can be higher e.g. 0-200 on dual-core).

- System IO (Network)
  - Bytes received: Number of bytes received.
  - Bytes sent: Number of bytes sent.
  - Dropped in: Number of dropped incoming packets.
  - Dropped out: Number of dropped outgoing packets.
  - Errors in: Total number of errors while receiving data.
  - Errors out: Total number of errors while sending data.
  - Packets sent: Number of packets sent.
  - Packets received: Number of packets received.

- Process Memory
  - Used: Amount of used memory for this process.
  - Virtual memory: Amount of virtual memory for this process.
  - Percentage: Percentage of system memory used by this process.
  - Process ID: ID for this process.

- Process CPU
  - Context switches: Number of context switches by this process.
  - System time: Time spent in kernel mode (seconds).
  - User time: Time spent in user mode (seconds).
  - Priority: Process priority.
  - Thread count: Number of threads currently used by this process.
  - Percentage: Percentage of system CPU used by this process in polling interval.
  - Process ID: ID for this process.

Disk stats should be added later.

Session Information
-------------------
For each recording session, the following information is also recorded:
- Description: User provided description of the recording session.
- Start time: Time when session was started.

Timestamps
----------
Besides the above resource data fields ("metrics"), each recorded entry also contains a timestamp.
The timestamps are recorded as Epoch timestamps.
Seconds for MySQL/CSV, milliseconds for Elasticsearch.

NOTE: If you use Elasticsearch to store the data, you should use the
[schema.json](https://github.com/mukatee/pypro/blob/master/src/schema.json) file to set up the mapping.
For example, "curl -XPOST 'http://localhost:9200/session1' --data-binary @schema.json"
The mapping is the ES equivalent of a database schema.
If you don't do this, the automatically generated schema will consider the timestamp as a "long" data type and
any date related functions will be unavailable.
For example, Kibana will not recognize is as a potential time column for visualization unless the type is correct.

Usage (pypro-local)
-------------------
Configuration is defined in the pypro.local.config.py file.
Start from the pypro.local.main(.py) module.

Example use:

```python
import pypro.local.main
import pypro.local.config as config

config.ES_FILE_ENABLED = True
config.CSV_ENABLED = False

pypro.local.main.run_poller()
```

For the example code, see [example.py](https://github.com/mukatee/pypro/blob/master/src/pypro/local/example.py).

For configuration options, see [config.py](https://github.com/mukatee/pypro/blob/master/src/pypro/local/config.py).

Metrics (pypro-snmp)
--------------------

You can use any SNMP OID supported by your target device.

Usage (pypro-snmp)
------------------
Configuration is defined in the pypro.snmp.config.py file.
Start from the pypro.snmp.main(.py) module.

Example use:

```python
import pypro.snmp.config as config
from pypro.snmp.oid import OID
import pypro.snmp.main as main

config.ES_FILE_ENABLED = True
config.CSV_ENABLED = False

#raw user space cpu time
config.SNMP_OIDS.append(OID('1.3.6.1.4.1.2021.11.50.0', 'user cpu time', 'public', '192.168.2.1', 161, 'router', True))
#percentage of user space cpu time
config.SNMP_OIDS.append(OID('.1.3.6.1.4.1.2021.11.9.0', 'percentage user cpu time', 'public', '192.168.2.1', 161, 'router', True))

main.run_poller()
```

For the example code, see [example.py](https://github.com/mukatee/pypro/blob/master/src/pypro/snmp/example.py).

For configuration options, see [config.py](https://github.com/mukatee/pypro/blob/master/src/pypro/snmp/config.py).


License
-------

MIT License


