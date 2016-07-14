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
Package containing Object-Oriented API Wrappers around :py:class:`DynamicAPI()` making it easier to work with these APIs.

You should not directly instantiate these APIs, instead see :py:meth:`getOOAPI() <fritzctl.session.Session.getOOAPI>` for how to request these APIs.
"""

from . import avm_homeauto,avm_homeplug
from . import general_time,general_deviceinfo,general_deviceconfig,general_hosts
from . import net_wlan_multi

OO_APIS = {
    # AVM APIs
    "urn:dslforum-org:service:X_AVM-DE_Homeauto:1":avm_homeauto.API_avm_homeauto,
    "urn:dslforum-org:service:X_AVM-DE_Homeplug:1":avm_homeplug.API_avm_homeplug,
    
    # General Purpose APIs
    "urn:dslforum-org:service:Time:1":general_time.API_general_time,
    "urn:dslforum-org:service:DeviceInfo:1":general_deviceinfo.API_general_deviceinfo,
    "urn:dslforum-org:service:DeviceConfig:1":general_deviceconfig.API_general_deviceconfig,
    "urn:dslforum-org:service:Hosts:1":general_hosts.API_general_hosts,
    
    # Networking APIs
    "urn:dslforum-org:service:WLANConfiguration:1":net_wlan_multi.API_net_wlan_multi,
    "urn:dslforum-org:service:WLANConfiguration:2":net_wlan_multi.API_net_wlan_multi,
    "urn:dslforum-org:service:WLANConfiguration:3":net_wlan_multi.API_net_wlan_multi,
    # TODO: add more OO apis
}
"""
Mapping of Service Type URNs to OO API classes.

See :py:data:`NAME_TO_URN <fritzctl.session.NAME_TO_URN>` for a list of URNs, names and which of these have Object-Oriented APIs defined.
"""
