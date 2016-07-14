#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  avm_homeplug.py
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

class API_avm_homeplug(base.API_base):
    """
    AVM Homeplug TR64 Object-Oriented API.
    
    Can be instantiated via ``session.getOOAPI("avm_homeplug")`` or ``session.getAPI("urn:dslforum-org:service:X_AVM-DE_Homeplug:1")``
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    def getDeviceByIndex(self,index):
        """
        Returns a device object associated with the given index.
        
        :param int index: Index of the device to return
        :return: Device Object
        :rtype: HomeplugDevice
        :raises AssertionError: if the index is invalid, e.g. not an integer or less than 0
        :raises ValueError: if the index is out of bounds
        """
        assert isinstance(index,int) and index>=0
        return HomeplugDevice(self,index,self.dynapi.GetGenericDeviceEntry(NewIndex=index))
    def getDeviceListLength(self):
        """
        Returns the length of the list of devices.
        
        :return: Length of the device list
        :rtype: int
        """
        return int(self.dynapi.GetNumberOfDeviceEntries()["NewNumberOfEntries"])
    def getDeviceList(self):
        """
        Returns a list of all known Homeplug devices.
        
        :return: List of known Homeplug devices
        :rtype: List of instances of :py:class:`HomeplugDevice()`
        """
        out = []
        for i in range(self.getDeviceListLength()):
            out.append(self.getDeviceByIndex(i))
        return out
    def getDeviceByMAC(self,mac):
        """
        Returns an device based on its MAC Address.
        
        :param str mac: MAC Address of the device
        :return: Device corresponding to the MAC Address
        :rtype: HomeplugDevice
        :raises AssertionError: if the MAC Address is not a string
        :raises ValueError: if the MAC Address is not known
        """
        assert isinstance(mac,str)
        d = self.dynapi.GetSpecificDeviceEntry(NewMACAddress=mac)
        d["NewMACAddress"]=mac
        return HomeplugDevice(self,-1,d)
    def getMACByIndex(self,index):
        """
        Returns the MAC Address of the corresponding device.
        
        :param int index: Index of the device
        :return: MAC Address
        :rtype: str
        :raises AssertionError: if the index is invalid, e.g. not an integer or less than 0
        :raises ValueError: if the index is out of bounds
        """
        assert isinstance(index,int) and index>=0
        return self.dynapi.GetGenericDeviceEntry(NewIndex=index)["NewMACAddress"]

class HomeplugDevice(object):
    """
    Device class representing any device queryable via the Homeplug TR64 API.
    
    :param API_avm_homeplug api: API object used for queries
    :param int index: Index used to request this object, may be -1 if unknown
    :param dict info: Dictionary containing all the data about the device as a TR64 response
    
    :ivar API_avm_homeplug api: Stored API Object
    :ivar int index: Stored Index
    :ivar dict info: Stored Raw Data
    
    Device Variables:
    
    :ivar str mac: MAC Address of the Device
    :ivar bool active: Flag if the device is currently active
    :ivar str name: User-Defined Name of the device
    :ivar str model: Full Model Name of the device
    :ivar bool update_available: Flag if there is an update available
    :ivar bool update_successful: Flag if the last update was successful, also False if unknown.
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
        """
        self.mac = data["NewMACAddress"]
        self.active = data["NewActive"]=="1"
        self.name = data["NewModel"]
        self.model = data["NewName"]
        self.update_available = data["NewUpdateAvailable"]=="1"
        self.update_successful = data["NewUpdateSuccessful"]=="suceeded"
    def reloadData(self):
        """
        Reloads the data from the server.
        
        Note that even if the object was originally constructed using
        :py:meth:`getDeviceByIndex() <API_avm_homeplug.getDeviceByIndex>`
        this method will request the data via its MAC Address.
        """
        d = self.api.dynapi.GetSpecificDeviceEntry(NewMACAddress=self.mac)
        d["NewMACAddress"]=self.mac
        self.info = d
        self.loadData(d)
    def doUpdate(self):
        """
        Requests that the device should update itself.
        
        You can check if the update is done by comparing :py:attr:`update_available` and other attributes after refreshing.
        """
        self.api.dynapi.DeviceDoUpdate(NewMACAddress=self.mac)
