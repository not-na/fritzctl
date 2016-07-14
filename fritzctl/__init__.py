#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#  
#  Copyright 2016 notna <notna@apparat.org>
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
"""
Root module for fritzctl containing the :py:mod:`fritzctl.session`\ , :py:mod:`fritzctl.dynapi` and :py:mod:`fritzctl.ooapi` modules and packages.

This package automatically imports the :py:mod:`session <fritzctl.session>` module
with ``from ... import *``\ , this means that you can access e.g. :py:class:`fritzctl.session.Session()` as :py:class:`fritzctl.Session()`\ .
"""

from session import *
