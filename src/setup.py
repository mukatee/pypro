__author__ = 'teemu kanstren'

from setuptools import setup

setup(name='resource_probes',
      version='0.1.3',
      description='System resource probes',
      url='https://github.com/mukatee/pypro',
      author='Teemu Kanstren',
      author_email='tkanstren@gmail.com',
      license='MIT',
      packages=['resource_probes'],
      zip_safe=True,
      install_requires=[
          'psutil', 'elasticsearch'
      ],
     )
