__author__ = 'teemu kanstren'

from setuptools import setup

setup(name='pypro-local',
      version='0.4.2',
      description='System/SNMP resource probes',
      url='https://github.com/mukatee/pypro',
      author='Teemu Kanstren',
      author_email='tkanstren@gmail.com',
      license='MIT',
      packages=['pypro', 'pypro.local', 'pypro.local.loggers'],
      zip_safe=True,
      install_requires=[
          'psutil', 'elasticsearch', 'kafka-python'
      ],
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.4',
                   'Development Status :: 4 - Beta',
                   'Topic :: System :: Monitoring'],
      keywords='monitoring'
     )
