__author__ = 'teemu kanstren'

from setuptools import setup

setup(name='pypro-local',
      version='0.3.0',
      description='System resource probes',
      url='https://github.com/mukatee/pypro',
      author='Teemu Kanstren',
      author_email='tkanstren@gmail.com',
      license='MIT',
      packages=['pypro', 'pypro.local'],
      zip_safe=True,
      install_requires=[
          'psutil', 'elasticsearch'
      ],
     )
