#!/usr/bin/env python

"""
distutils/setuptools install script.
"""

import os
import re
import sys

from setuptools import setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

def get_version():
    """
    get_version reads the version info from bin/puppet-enc-ec2:__version__
    """

    init = open(os.path.join(ROOT, 'bin', 'puppet-enc-ec2')).read()
    return VERSION_RE.search(init).group(1)

setup(name='puppet-enc-ec2',
      version=get_version(),
      description='A Puppet ENC which assigns Nodes based on their AWS EC2 metadata.',
      long_description=open('README.rst').read(),
      url='http://github.com/cavaliercoder/puppet-enc-ec2',
      author='Ryan Armstrong',
      author_email='ryan@cavaliercoder.com',
      license='MIT',
      install_requires=['boto3'],
      scripts=['bin/puppet-enc-ec2'])
