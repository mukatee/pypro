Python Resource Probes
======================

Python probes for collecting information about system resources.
Two versions, one that collects detailed information about the host it is running on.
And another one that performs SNMP queries over the network to collect data from other hosts.

[Local](https://github.com/mukatee/pypro/blob/master/README_local.md) version is based on the *psutil* library.
[SNMP](https://github.com/mukatee/pypro/blob/master/README_snmp.md) version is based on the *pysnmp* library.
Built using Python 3.4. No idea about workings with other versions.

What for?
---------

I built these to learn some Python and to have simple and easy means to collect performance related statistics both
for the systems where I run my code, and for network devices in a test environment.
Then I added options to stream the data to various "big data" tools such as Elasticsearch and Kafka.

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

Metrics
-------
Both the local version and the SNMP version support collecting various resource usage statistics from a system, such as
- memory
- CPU
- network I/O

Fore more information, check the pages for the
[Local](https://github.com/mukatee/pypro/blob/master/README_local.md) and
[SNMP](https://github.com/mukatee/pypro/blob/master/README_snmp.md) versions.


License
-------

MIT License


