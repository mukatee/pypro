Python Resource Probes
======================

Records statistics related to system resource use. Based on the *psutil* library.
Built using Python 3.4. No idea about workings with other versions.

Requirements
------------
- Python3. Tested with 3.4.
- PSUtil. The Python package used to read the resource metrics. Should install as dependency, otherwise "pip3 install psutil".
- Elascticsearch package. "pip3 install elasticsearch".
- Mysql.connector. "pip3 install mysql-connector-python –allow-external mysql-connector-python"

On a unix-based system you likely need to sudo yourself to install the dependencies, or this package itself (for pip3).

Installation
------------
"pip3 install resource_probes". Or just get the source and go with it.

Data stores
-----------
Supported logging targets are:
- CSV file
- Elasticsearch bulk import file
- Elasticsearch database
- MySQL database

Metrics
-------
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

Usage
-----
Configuration is defined in the resource_probes/config.py file.
Start from the resource_probes.main(.py) module.

Example use:

```python
import resource_probes.config as config
import resource_probes.main

config.ES_FILE_ENABLED = True
config.CSV_ENABLED = False

resource_probes.main.run_poller()
```

For configuration options, see [config.py](https://github.com/mukatee/pypro/blob/master/src/resource_probes/config.py).

License
-------

MIT License


