#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#
#  Copyright 2016-2022 fritzctl Contributors
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# Distribution command:
# sudo python setup.py install sdist bdist register upload
# With setuptools installed:
# sudo python setup.py install sdist bdist bdist_wheel register upload

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    longdesc = open("README.txt", "r").read()
except IOError:
    print("README.txt not found, using description as longdesc instead")
    longdesc = "Object oriented TR64 FRITZ!Box Client Library"

setup(name='fritzctl',
      version="1.1.0",
      description="Object oriented TR64 FRITZ!Box Client Library",
      long_description=longdesc,
      author="notna",
      author_email="notna@apparat.org",
      url="https://pypi.python.org/pypi/fritzctl",
      packages=['fritzctl', "fritzctl.ooapi"],
      install_requires=["requests", "simpletr64"],
      provides=["fritzctl"],
      classifiers=[
        "Development Status :: 5 - Production/Stable",

        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",

        "Intended Audience :: Developers",

        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",

        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: OS Independent",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Home Automation",
        ],
      )
