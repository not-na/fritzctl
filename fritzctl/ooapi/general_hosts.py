#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  general_hosts.py
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

import base

class API_general_hosts(base.API_base):
    """
    General Host Information TR64 Object-Oriented API.
    
    Can be instantiated via ``session.getOOAPI("general_hosts")`` or ``session.getOOAPI("urn:dslforum-org:service:Hosts:1")``\ .
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    def getHostByIndex(self,index,ext=True):
        """
        Returns the Host associated with the given Index.
        
        :param int index: The Index of the Host
        :param bool ext: Optional Flag if information from the AVM Extension should be integrated, defaults to True
        :return: Host Information Object
        :rtype: Host
        :raises AssertionError: if the index is invalid, e.g. not an integer or lower than 0
        :raises ValueError: if the index is out-of-bounds
        """
        assert isinstance(index,int) and index>=0
        d = self.dynapi.GetGenericHostEntry(NewIndex=index)
        if ext:
            d.update(self.dynapi.callAPI("X_AVM-DE_GetGenericHostEntryExt",NewIndex=index))
            d["_ext"]=True
        else:
            d["_ext"]=False
        return Host(self,index,d)
    def getHostByMAC(self,mac,ext=True):
        """
        Returns the Host associated with the given MAC Address.
        
        :param str mac: MAC Address of the Host
        :param bool ext: Optional Flag if information from the AVM Extension should be integrated, defaults to True
        :return: Host Information Object
        :rtype: Host
        :raises AssertionError: if the MAC Address is invalid, e.g. not a string
        :raises ValueError: if the MAC Address is unknown
        """
        assert isinstance(mac,str)
        d = self.dynapi.GetSpecificHostEntry(NewMACAdress=mac)
        d["NewMACAddress"]=mac
        if ext:
            d.update(self.dynapi.callAPI("X_AVM-DE_GetSpecificHostEntryExt",NewMACAddress=mac))
            d["_ext"]=True
        else:
            d["_ext"]=False
        return Host(self,-1,d)
    def getHostListLength(self):
        """
        Returns the length of the List of all known Hosts.
        
        :return: Number of Entries in the host list.
        :rtype: int
        """
        return int(self.dynapi.GetHostNumberOfEntries()["NewHostNumberOfEntries"])
    def getHostList(self,ext=True):
        """
        Returns a list of all hosts.
        
        :param bool ext: Optional Flag if information from the AVM Extension should be integrated, defaults to True
        :return: List of Hosts
        :rtype: List of :py:class:`Host()`
        """
        out = []
        for i in range(self.getHostListLength()):
            out.append(self.getHostByIndex(i,ext=ext))
        return out
    def getMacByIndex(self,index):
        """
        Returns the MAC Address of the device associated with the given index.
        
        :param int index: Index of the Device to return
        :return: MAC Address
        :rtype: str
        """
        return self.dynapi.GetGenericHostEntry(NewIndex=index)["NewMACAddress"]
    def getChangeCounter(self):
        """
        Returns the current change counter.
        
        :return: The current change counter
        :rtype: int
        """
        return int(self.dynapi.callAPI("X_AVM-DE_GetChangeCounter")["NewX_AVM-DE_GetChangeCounter"])
    def wakeUp(self,mac):
        """
        Sends a WakeOnLAN request to the specified Host.
        
        :param str mac: MAC Address to wake up
        :raises AssertionError: if the MAC Address is invalid, e.g. not a string
        :raises ValueError: if the MAC Address is unknown
        """
        assert isinstance(mac,str)
        self.dynapi.callAPI("X_AVM-DE_WakeOnLANByMACAddress",NewMACAddress=mac)

class Host(object):
    """
    Host Information and Configuration Class.
    
    :param API_avm_homeauto api: API object to use when querying for data
    :param int index: Index this device had when requested via ``GetGenericHostEntry()``\ , may be -1 if unknown
    :param dict info: Dictionary containing the TR64 Response with all the data about the device; automatically passed to :py:meth:`loadData()`
    
    :ivar API_avm_homeauto api: stores the supplied API object
    :ivar int index: stores the supplied index
    :ivar dict info: stores the data in a dictionary
    
    :py:attr:`info` stores a flag if extension data is available in the ``_ext`` key.
    
    :ivar str mac: MAC Address of this Host
    :ivar str ip: IP Address of this Host
    :ivar str address_source: Source of the Address
    :ivar int lease_remaining: Time in second until the DHCP Lease expires
    :ivar str interface_type: Type of the interface this Host is connected with
    :ivar bool active: Flag if this host is active
    :ivar str hostname: Property for reading and writing hostname, see :py:attr:`hostname`
    
    Extension Variables:
    
    :ivar int ethport: Which ethernet port the host is connected with, from 1-4 or 0 if not via LAN
    :ivar float speed: Current Connection Speed
    :ivar bool updateAvailable: Flag if an update is available, where applicable
    :ivar bool updateSuccessful: Flag if the last update was successful, where applicable
    :ivar str infourl: URL for getting Information
    :ivar str model: Model of the Host
    :ivar str url: URL of the Host
    """
    def __init__(self,api,index,info):
        self.api = api
        self.index = index
        self.info = info
        self.loadData(self.info)
    def loadData(self,data):
        """
        Populates instance variables with the supplied TR64 response.
        This method is automatically called upon construction with the supplied info dict.
        
        Note that the ``_ext`` key must be set to a boolean flag indicating if extension information is contained in the response.
        """
        self.mac = data["NewMACAddress"]
        self.ip = data["NewIPAddress"]
        self.address_source = data["NewAddressSource"]
        self.lease_remaining = int(data["NewLeaseTimeRemaining"])
        self.interface_type = data["NewInterfaceType"]
        self.active = data["NewActive"]=="1"
        self._hostname = data["NewHostName"]
        if data["_ext"]:
            self.ethport = int(data["NewX_AVM-DE_Port"])
            self.speed = float(data["NewX_AVM-DE_Speed"])
            self.updateAvailable = data["NewX_AVM-DE_UpdateAvailable"]=="1"
            self.updateSuccessful = data["NewX_AVM-DE_UpdateSuccessful"]=="succeeded"
            self.infourl = data["NewX_AVM-DE_InfoURL"]
            self.model = data["NewX_AVM-DE_Model"]
            self.url = data["NewX_AVM-DE_URL"]
        
    def reloadData(self):
        """
        Reloads the data from the server.
        
        Note that this method will only request extension data if the key ``_ext`` is set to ``True``\ .
        """
        d = self.api.dynapi.GetSpecificHostEntry(NewMACAddress=self.mac)
        if self.info["_ext"]:
            d.update(self.api.dynapi.callAPI("X_AVM-DE_GetSpecificHostEntryExt",NewMACAddress=self.mac))
        d["_ext"]=self.info["_ext"]
        d["NewMACAddress"]=self.mac
        self.info = d
    def doUpdate(self):
        """
        Requests that the host does an update.
        
        Note that this may not work on every host
        """
        self.checkForUpdates()
        self.api.dynapi.callAPI("X_AVM-DE_HostDoUpdate",NewMACAddress=self.mac)
    def checkForUpdates(self):
        """
        Checks for Updates.
        
        Note that this method does not return anything as the underlying API call gives no variables in return.
        This method automatically reloads the data to update any update flags that may have changed.
        """
        self.api.dynapi.callAPI("X_AVM-DE_HostsCheckUpdate")
        self.reloadData()
    @property
    def autoWOL(self):
        """
        Property controlling the Auto-WakeOnLAN Feature.
        
        This Property is not cached and can be written to and read from.
        """
        return self.api.dynapi.callAPI("X_AVM-DE_GetAutoWakeOnLANByMACAddress",NewMACAddress=self.mac)["NewAutoWOLEnabled"]=="1"
    @autoWOL.setter
    def autoWOL(self,value):
        self.api.dynapi.callAPI("X_AVM-DE_SetAutoWakeOnLANByMACAddress",NewMACAddress=self.mac,NewAutoWOLEnabled=str(int(value)))
    
    @property
    def hostname(self):
        """
        Property controlling the hostname of the device.
        
        This property will only update the displayed hostname if it is modified or the data is refreshed.
        
        This property can be read from and written to
        """
        return self._hostname
    @hostname.setter
    def hostname(self,value):
        self.api.dynapi.callAPI("X_AVM-DE_SetHostNameByMACAddress",NewMACAddress=self.mac,NewHostName=value)
        self.reloadData()
    
    def wakeUp(self):
        """
        Sends a WakeOnLAN request to this host and tries to wake it up.
        """
        self.api.wakeUp(self.mac)
