""" Install the cecdaemon package
"""
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='cecdaemon',
      version='1.0.0',
      description='Daemon and tools for managing CEC capabilities',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/simons-public/cecdaemon',
      author='Chris Simons',
      author_email='chris@simonsmail.net',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: No Input/Output (Daemon)',
          'Topic :: Games/Entertainment',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: BSD License'
          ],
      keywords='libcec cec daemon htpc',
      packages=['cecdaemon'],
      install_requires=['cec', 'python-uinput'],
      data_files=[('/usr/share/cecdaemon', [
          'examples/cecdaemon.conf-example',
          'examples/cecdaemon.service-example',
          'examples/example_server.py',
          ])],
      entry_points={
          'console_scripts': [
              'cecdaemon=cecdaemon.__main__:main',
              'cecusercodes=cecdaemon.cecusercodes:main',
              ]
      })
