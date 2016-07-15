#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  session.py
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

__all__ = ["NAME_TO_URN","Session"]

import simpletr64

from . import dynapi
from . import ooapi

OO_APIS = ooapi.OO_APIS

NAME_TO_URN = {
    # AVM APIs
    "avm_homeauto":"urn:dslforum-org:service:X_AVM-DE_Homeauto:1",              # OO Done -> fritzctl.ooapi.avm_homeauto.API_avm_homeauto
    "avm_myfritz":"urn:dslforum-org:service:X_AVM-DE_MyFritz:1",                # Priority: medium
    "avm_remoteaccess":"urn:dslforum-org:service:X_AVM-DE_RemoteAccess:1",      # Priority: medium
    "avm_storage":"urn:dslforum-org:service:X_AVM-DE_Storage:1",                # Priority: medium-high
    "avm_speedtest":"urn:dslforum-org:service:X_AVM-DE_Speedtest:1",
    "avm_appsetup":"urn:dslforum-org:service:X_AVM-DE_AppSetup:1",              # Priority: lowest
    "avm_dect":"urn:dslforum-org:service:X_AVM-DE_Dect:1",
    "avm_upnp":"urn:dslforum-org:service:X_AVM-DE_UPnP:1",                      # Priority: medium-high
    "avm_ontel":"urn:dslforum-org:service:X_AVM-DE_OnTel:1",
    "avm_filelinks":"urn:dslforum-org:service:X_AVM-DE_Filelinks:1",            # Priority: medium-low
    "avm_webdavclient":"urn:dslforum-org:service:X_AVM-DE_WebDAVClient:1",      # Priority: medium-low
    "avm_homeplug":"urn:dslforum-org:service:X_AVM-DE_Homeplug:1",              # OO Done -> fritzctl.ooapi.avm_homeplug.API_avm_homeplug
    "avm_tam":"urn:dslforum-org:service:X_AVM-DE_TAM:1",                        # Priority: low
    
    # General Purpose APIs
    
    "general_time":"urn:dslforum-org:service:Time:1",                           # OO Done -> fritzctl.ooapi.general_time.API_general_time
    "general_deviceinfo":"urn:dslforum-org:service:DeviceInfo:1",               # OO Done -> fritzctl.ooapi.general_deviceinfo.API_general_deviceinfo
    "general_deviceconfig":"urn:dslforum-org:service:DeviceConfig:1",           # OO Done -> fritzctl.ooapi.general_deviceconfig.API_general_deviceconfig
    "general_hosts":"urn:dslforum-org:service:Hosts:1",                         # OO Done -> fritzctl.ooapi.general_hosts.API_general_hosts
    "general_userinterface":"urn:dslforum-org:service:UserInterface:1",         # Priority: medium
    "general_managementserver":"urn:dslforum-org:service:ManagementServer:1",
    "general_layer3fwd":"urn:dslforum-org:service:Layer3Forwarding:1",          # Priority: medium-high
    "general_x_voip":"urn:dslforum-org:service:X_VoIP:1",
    
    "net_wan_dsllinkconfig":"urn:dslforum-org:service:WANDSLLinkConfig:1",
    "net_wan_ipconnection":"urn:dslforum-org:service:WANIPConnection:1",
    "net_wan_commoninterfacecfg":"urn:dslforum-org:service:WANCommonInterfaceConfig:1",
    "net_wan_dslinterfacecfg":"urn:dslforum-org:service:WANDSLInterfaceConfig:1",
    "net_wan_pppconnection":"urn:dslforum-org:service:WANPPPConnection:1",
    "net_wan_ethernetlinkcfg":"urn:dslforum-org:service:WANEthernetLinkConfig:1",
    
    "net_lan_configsecurity":"urn:dslforum-org:service:LANConfigSecurity:1",
    "net_lan_hostcfgmanagement":"urn:dslforum-org:service:LANHostConfigManagement:1",
    "net_lan_ethernetinterfacecfg":"urn:dslforum-org:service:LANEthernetInterfaceConfig:1",
    
    "net_wlan_2.4ghz":"urn:dslforum-org:service:WLANConfiguration:1",           # OO Done -> fritzctl.ooapi.net_wlan_multi.API_net_wlan_multi
    "net_wlan_2nd":"urn:dslforum-org:service:WLANConfiguration:2",              # OO Done -> fritzctl.ooapi.net_wlan_multi.API_net_wlan_multi
    "net_wlan_3rd":"urn:dslforum-org:service:WLANConfiguration:3",              # OO Done -> fritzctl.ooapi.net_wlan_multi.API_net_wlan_multi
    # TODO: add the rest of the URNs to this list
    
    }
"""
Allows for conversion between user-friendly names and internal Service Type URNs.

All service types that could be found in the file ``/tr64desc.xml`` on the 7th of July 2016 with a FRITZ!Box 7580 are supported.

The naming scheme is quite simple, all AVM specific names begin with ``avm_``\ , all general-purpose names begin with ``general_`` and
all network-related names begin with ``net_``\ . For ``net_*`` names, there are three sub-categories: ``net_wan_``\ , ``net_lan_`` and ``net_wlan_``\ .

.. seealso::
   
   See the docs for :py:meth:`getAPI() <fritzctl.session.Session.getAPI>` and :py:meth:`getOOAPI() <fritzctl.session.Session.getOOAPI()>` for more information about how to use these names.

Table of Name -> URN mapping:

======================== ======================================================= ==========
Name                     URN                                                     OO-Support
======================== ======================================================= ==========
avm_homeauto             ``urn:dslforum-org:service:X_AVM-DE_Homeauto:1``        Yes
avm_myfritz              ``urn:dslforum-org:service:X_AVM-DE_MyFritz:1``         No
avm_remoteaccess         ``urn:dslforum-org:service:X_AVM-DE_RemoteAccess:1``    No
avm_storage              ``urn:dslforum-org:service:X_AVM-DE_Storage:1``         No
avm_speedtest            ``urn:dslforum-org:service:X_AVM-DE_Speedtest:1``       No
avm_appsetup             ``urn:dslforum-org:service:X_AVM-DE_AppSetup:1``        No
avm_dect                 ``urn:dslforum-org:service:X_AVM-DE_Dect:1``            No
avm_upnp                 ``urn:dslforum-org:service:X_AVM-DE_UPnP:1``            No
avm_ontel                ``urn:dslforum-org:service:X_AVM-DE_OnTel:1``           No
avm_filelinks            ``urn:dslforum-org:service:X_AVM-DE_Filelinks:1``       No
avm_webdavclient         ``urn:dslforum-org:service:X_AVM-DE_WebDAVClient:1``    No
avm_homeplug             ``urn:dslforum-org:service:X_AVM-DE_Homeplug:1``        Yes
avm_tam                  ``urn:dslforum-org:service:X_AVM-DE_TAM:1``             No
general_time             ``urn:dslforum-org:service:Time:1``                     Yes
general_deviceinfo       ``urn:dslforum-org:service:DeviceInfo:1``               Yes
general_deviceconfig     ``urn:dslforum-org:service:DeviceConfig:1``             Yes
general_hosts            ``urn:dslforum-org:service:Hosts:1``                    Yes
general_userinterface    ``urn:dslforum-org:service:UserInterface:1``            No
general_managementserver ``urn:dslforum-org:service:ManagementServer:1``         No
general_layer3fwd        ``urn:dslforum-org:service:Layer3Forwarding:1``         No
general_x_voip           ``urn:dslforum-org:service:X_VoIP:1``                   No
net_wan_dsllinkconfig    ``urn:dslforum-org:service:WANDSLLinkConfig:1``         No
net_wan_ipconnection     ``urn:dslforum-org:service:WANIPConnection:1``          No
|urn_net_wan_cmifacecfg| ``urn:dslforum-org:service:WANCommonInterfaceConfig:1`` No
net_wan_dslinterfacecfg  ``urn:dslforum-org:service:WANDSLInterfaceConfig:1``    No
net_wan_pppconnection    ``urn:dslforum-org:service:WANPPPConnection:1``         No
net_wan_ethernetlinkcfg  ``urn:dslforum-org:service:WANEthernetLinkConfig:1``    No
net_lan_configsecurity   ``urn:dslforum-org:service:LANConfigSecurity:1``        No
|urn_net_lan_hostcfgmgr| ``urn:dslforum-org:service:LANHostConfigManagement:1``  No
|urn_net_lan_ethifcfg|   |urn_net_lan_ethifcfg_urn|                              No
net_wlan_2.4ghz          ``urn:dslforum-org:service:WLANConfiguration:1``        Yes
net_wlan_2nd             ``urn:dslforum-org:service:WLANConfiguration:2``        Yes
net_wlan_3rd             ``urn:dslforum-org:service:WLANConfiguration:3``        Yes
======================== ======================================================= ==========

.. |urn_net_wan_cmifacecfg| replace:: net_wan_commoninterfacecfg
.. |urn_net_lan_hostcfgmgr| replace:: net_lan_hostcfgmanagement
.. |urn_net_lan_ethifcfg| replace:: net_lan_ethernetinterfacecfg
.. |urn_net_lan_ethifcfg_urn| replace:: ``urn:dslforum-org:service:LANEthernetInterfaceConfig:1``

As you may have noticed, there are three WLANConfiguration URNs, this is because they correspond to the normal wifi, 5ghz wifi and the guest network.

The first URN always corresponds to the 2.4ghz network, but the second depends on what networks are active.
If there is an 5ghz network, it will always be the second network and the guest network will be the third network.
If there is no 5ghz network, the second network will be the guest network.

You may be able to make an educated guess about which network is which by querying certain parameters of each network.

See the :py:mod:`fritzctl.ooapi` package for specific OO APIs, as indicated in the table.
"""

class Session(object):
    """
    Session object storing the credentials and context.
    
    :param str server: Server to connect to, e.g. ``fritz.box``
    :param str user: Optional Username for authentification
    :param str pwd: Optional Password for authentification
    :param int port: Port to use when connecting, defaults to ``49000``
    :param bool authcheck: If the credentials should be checked, simply requests the ``general_deviceinfo`` API.
    
    Instance Variables:
    
    :ivar server: Server connected to
    :ivar user: Username for authentification
    :ivar pwd: Password for authentification
    :ivar device: :py:class:`simpletr64.DeviceTR64()` Instance used for managing authentification
    :ivar urns: List of URNs found on the server, can be used for debugging
    """
    def __init__(self,server=None,user=None,pwd=None,port=49000,authcheck=True):
        if server is None:
            raise NotImplementedError("Server search is currently not implemented")
        else:
            self.server = server
        
        self.user = user if user is not None else ""
        self.pwd = pwd if pwd is not None else ""
        self.device = simpletr64.DeviceTR64(server,port=port)
        self.device.username = self.user
        self.device.password = self.pwd
        self.device.loadDeviceDefinitions("http://"+self.server+":"+str(self.device.port)+"/tr64desc.xml")
        self.device.loadSCPD()
        self.urns = self.device.deviceSCPD.keys()
        if authcheck:
            try:
                self.getOOAPI("general_deviceinfo").getDeviceInfo()
            except Exception:
                raise ValueError("Invalid Credentials for user %s!"%user)
    def getAPI(self,name):
        """
        Requests an API object by either URN or user-friendly name.
        
        See :py:data:`NAME_TO_URN` for a list of user-friendly names.
        
        :param str name: API Name, either Service Type URN or user-friendly name
        :return: A :py:class:`DynamicAPI() <fritzctl.dynapi.DynamicAPI>` instance ready-for-use
        :raises ValueError: if the URN is not known or is not in :py:data:`NAME_TO_URN`
        """
        if name.startswith("urn:"):
            if name not in self.urns:
                raise ValueError("Invalid URN!")
            urn = name
        else:
            if name not in NAME_TO_URN:
                raise ValueError("Invalid Name!")
            urn = NAME_TO_URN[name]
        return dynapi.DynamicAPI(self,urn)
    def getOOAPI(self,name):
        """
        Requests an Object-Oriented API by either URN or user-friendly name.
        
        See :py:data:`NAME_TO_URN` for a list of user-friendly names.
        
        Note that the methods available vary depending on what API you requested, see the appropriate module in :py:module`fritzctl.ooapi` for specific informations.
        
        :param str name: API Name, either Service Type URN or user-friendly name
        :return: An Object-oriented API interface
        :rtype: Instance of a subclass of :py:class:`fritzctl.ooapi.base.API_base()``
        """
        if name.startswith("urn:"):
            if name not in self.urns:
                raise ValueError("Invalid URN!")
            urn = name
        else:
            if name not in NAME_TO_URN:
                raise ValueError("Invalid Name!")
            urn = NAME_TO_URN[name]
        return OO_APIS[urn](self,urn)
    
    def execute(self,*args,**kwargs):
        """
        Executes the given action on the server.
        
        This method simply passes through all parameters to the internal :py:class:`simpletr64.DeviceTR64()` instance.
        """
        return self.device.execute(*args,**kwargs)
