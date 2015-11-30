Python Resource Probes
======================

Python probes for collecting information about system resources.
Two versions, one that collects detailed information about the host it is running on.
And another one that performs SNMP queries over the network to collect data from (remote) hosts.

[Local](https://github.com/mukatee/pypro/blob/master/README_local.md) version is based on the *psutil* library.
[SNMP](https://github.com/mukatee/pypro/blob/master/README_snmp.md) version is based on the *pysnmp* library.
Built using Python 3.4. No idea about workings with other versions.

What for?
---------

I built these to learn some Python and to have simple and easy means to collect performance related statistics both
for the systems where I run my code, and for network devices in a larger network test environment.
Then I added options to stream the data to various "big data" tools such as Elasticsearch and Kafka
to provide support for analytics for a larger system. And to learn the tools myself..


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
- InFlux DB (pypro-snmp only)

Metrics
-------
Both the local version and the SNMP version support collecting various resource usage statistics from a system, such as
- Memory (including process level data for pypro-local)
- CPU (including process level data for pypro-local)
- Network I/O (including process level data for pypro-local)
- Anything else your device supports (for pypro-snmp)

Fore more information on the exact metrics for each version, check the pages for the
[Local](https://github.com/mukatee/pypro/blob/master/README_local.md) and
[SNMP](https://github.com/mukatee/pypro/blob/master/README_snmp.md) versions.


License
-------

MIT License


