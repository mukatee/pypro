__author__ = 'teemu kanstren'

from setuptools import setup

setup(name='pypro-snmp',
      version='0.3.4',
      description='System resource probes',
      url='https://github.com/mukatee/pypro',
      author='Teemu Kanstren',
      author_email='tkanstren@gmail.com',
      license='MIT',
      packages=['pypro', 'pypro.snmp', 'pypro.snmp.loggers', 'pypro.snmp.oids'],
      package_data={'pypro.snmp': ['*.avsc']},
      zip_safe=True,
      install_requires=[
          'psutil', 'elasticsearch', 'kafka-python', 'pysnmp', 'avro-python3', 'influxdb'
      ],
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.4',
                   'Development Status :: 4 - Beta',
                   'Topic :: System :: Networking :: Monitoring'],
      keywords='monitoring',
     )