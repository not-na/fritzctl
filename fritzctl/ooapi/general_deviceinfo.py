#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  general_deviceinfo.py
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

import re

_provisioningpattern = re.compile(r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3}")

import base

class API_general_deviceinfo(base.API_base):
    """
    Device Information TR64 Object-Oriented Wrapper API.
    
    Can be instantiated via ``session.getOOAPI("general_deviceinfo")`` or ``session.getOOAPI("urn:dslforum-org:service:DeviceInfo:1")``\ .
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    def getDeviceInfo(self):
        """
        Returns an information object with all relevant data.
        
        :return: Information Object about the server
        :rtype: DeviceInfo
        """
        return DeviceInfo(self,self.dynapi.GetInfo())
    def setProvisioningCode(self,code):
        """
        Sets the TR-069 Provisioning Code.
        The provisioning code must match the RegEx ``[0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3}``\ .
        
        :param str code: A Valid TR-069 Provisioning Code
        :raises AssertionError: if the supplied code does not match the RegEx
        :raises ValueError: if the supplied code was rejected by the server
        """
        assert _provisioningpattern.match(code)
        self.dynapi.SetProvisioningCode(NewProvisioningCode=code)
    def getDeviceLog(self):
        """
        Returns the device log since the last reboot.
        
        Note that the log is just one long string, and may need to be split on newlines.
        
        :return: The device log since the last reboot
        :rtype: str
        """
        return self.dynapi.GetDeviceLog()["NewDeviceLog"]
    def getSecurityPort(self):
        """
        Returns the secure port number used for secure TR64 Connections.
        
        :returns: The Secure Port Number
        :rtype: int
        """
        return int(self.dynapi.GetSecurityPort()["NewSecurityPort"])

class DeviceInfo(object):
    """
    Class representing the system the server runs on, e.g. the FRITZ!Box.
    
    :param API_general_deviceinfo api: API object to use when querying for data
    :param dict info: Dictionary containing the TR64 Response with all the data about the device; automatically passed to :py:meth:`loadData()`
    
    :ivar API_general_deviceinfo api: stores the supplied API object
    :ivar dict info: stores the data in a dictionary
    
    General Device Variables:
    
    :ivar str manufacturer: Manufacturer, e.g. ``AVM``
    :ivar str manufacturerOUI: Manufacturer OUI, e.g. ``00040E``
    :ivar str modelname: Name of the Model of the device, e.g. ``FRITZ!Box 7580``
    :ivar str description: Short description of the Model, usually a longer version of :py:attr:`modelname`
    :ivar str productclass: Class of the Product, e.g. ``FRITZ!Box``
    :ivar str serialnumber: Serialnumber of the Device, can be used to distinguish devices.
    :ivar str swversion: Softwareversion of the device, e.g. ``153.06.51``
    :ivar str hwversion: Hardwareversion of the device, e.g. ``FRITZ!Box 7580``
    :ivar str specversion: Version of the Specification, e.g. ``1.0``
    :ivar str provisioningcode: TR-069 Provisioning Code, can be set via :py:meth:`API_general_deviceinfo.setProvisioningCode()`
    :ivar int uptime: Uptime of the Device in seconds, as of the creation of this object. Can be refreshed with :py:meth:`reloadData()`
    :ivar str devicelog: String containing the log of the device, see :py:meth:`API_general_deviceinfo.getDeviceLog()` for more information.
    
    All the examples are based on a FRITZ!Box 7580 on the newest Beta Firmware as of the 12th of July 2016.
    """
    def __init__(self,api,info):
        self.api = api
        self.info = info
        self.loadData(info)
    def loadData(self,data):
        """
        Populates instance variables with the supplied TR64 response.
        This method is automatically called upon construction with the supplied info dict.
        """
        self.manufacturer = data["NewManufacturerName"]
        self.manufacturerOUI = data["NewManufacturerOUI"]
        self.modelname = data["NewModelName"]
        self.description = data["NewDescription"]
        self.productclass = data["NewProductClass"]
        self.serialnumber = data["NewSerialNumber"]
        self.swversion = data["NewSoftwareVersion"]
        self.hwversion = data["NewHardwareVersion"]
        self.specversion = data["NewSpecVersion"]
        self.provisioningcode = data["NewProvisioningCode"]
        self.uptime = int(data["NewUpTime"])
        self.devicelog = data["NewDeviceLog"]
    def reloadData(self):
        """
        Reloads the data from the server and updates it in-place.
        """
        d = self.api.dynapi.GetInfo()
        self.info = d
        self.loadData(d)
