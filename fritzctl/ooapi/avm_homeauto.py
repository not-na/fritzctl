#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  avm_homeauto.py
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

import sys

import base

STATE2SwStateEnum = {
    True:"ON",
    False:"OFF",
    "toggle":"TOGGLE",
    }
"""
Mapping for mapping Python Boolean values to ``SwStateEnum`` members.

Either ``True`` or ``False`` can be used to force-switch or you can use ``toggle`` for toggling the current state.

See :py:meth:`switchByAIN() <API_avm_homeauto.switchByAIN>` for more information about switches.
"""

PresentEnum2INT = {
    "DISCONNECTED":0,
    "CONNECTED":1,
    "REGISTERED":2,
    "UNKNOWN":-1,
    }
"""
Mapping for mapping ``PresentEnum`` members to Integers.

======================== ===================
``PresentEnum`` member   Python Equivalent  
======================== ===================
``DISCONNECTED``         ``0``
``CONNECTED``            ``1``
``REGISTERED``           ``2``
``UNKNOWN``              ``-1``
======================== ===================

See :py:data:`HomeautoDevice.present` for more information.
"""

class API_avm_homeauto(base.API_base):
    """
    AVM Homeauto TR64 Object-Oriented API.
    
    Can be instantiated via ``session.getOOAPI("avm_homeauto")`` or ``session.getOOAPI("urn:dslforum-org:service:X_AVM-DE_Homeauto:1")``\ .
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    def getDeviceByIndex(self,index):
        """
        Returns the device identified by the integer ``index``\ .
        
        :param int index: Index of the device to return
        :return: the device object
        :rtype: Instance of :py:class:`HomeautoDevice()`
        :raises ValueError: if the supplied index is invalid
        :raises AssertionError: if the supplied index is invalid, e.g. not an integer or less than 0
        """
        assert isinstance(index,int) and index>=0
        return HomeautoDevice(self,index,self.dynapi.GetGenericDeviceInfos(NewIndex=index))
    def getDeviceList(self,limit=-1):
        """
        Returns a list of devices, optionally up to the specified limit.
        
        :param int limit: Optional Limit for the returned list
        :return: List of all known devices
        :rtype: List of instances of :py:class:`HomeautoDevice()`\ .
        :raises AssertionError: if the supplied limit is invalid, e.g. not an integer or less than -1
        """
        assert isinstance(limit,int)
        out = []
        i = 0
        while i!=limit:
            try:
                out.append(self.getDeviceByIndex(i))
            except ValueError:
                break
            i+=1
        return out
    def getAINByIndex(self,index):
        """
        Returns the AIN associated with the given index.
        
        :param int index: Index of the Device
        :return: AIN corresponding to the given index
        :rtype: str
        :raises AssertionError: if the supplied index is invalid, e.g. not an integer or less than 0
        :raises ValueError: if the supplied index is out of range
        """
        assert isinstance(index,int) and index>=0
        return self.dynapi.GetGenericDeviceInfos(NewIndex=index)["NewAIN"]
    def getDeviceByAIN(self,ain):
        """
        Returns the device associated to the given AIN.
        
        :param str ain: AIN of the device to return
        :return: Device Object allowing manipulation of its properties
        :rtype: HomeautoDevice
        :raises AssertionError: if the supplied AIN is not a string
        :raises ValueError: if the supplied AIN is unknown
        """
        assert isinstance(ain,str)
        d = self.dynapi.GetSpecificDeviceInfos(NewAIN=ain)
        d["NewAIN"]=ain
        return HomeautoDevice(self,-1,d)
    def switchByAIN(self,ain,state):
        """
        Switches the given Actors socket on, off or toggles it.
        
        :param str ain: AIN of the device to switch
        :param state: State to switch to, see :py:data:`STATE2SwStateEnum` for a list of values
        :type state: ``True``\ , ``False`` or ``toggle``
        :raises ValueError: if the supplied AIN is unknown
        :raises KeyError: if the supplied state is invalid
        """
        self.dynapi.SetSwitch(NewAIN=ain,NewSwitchState=STATE2SwStateEnum[state])

class HomeautoDevice(object):
    """
    Generic Device class representing any device queryable via the TR64 Homeauto API.
    
    Note that some instance variables may be set to arbitrary values if the device does not support the feature.
    
    :param API_avm_homeauto api: API object to use when querying for data
    :param int index: Index this device had when requested via ``GetGenericDeviceInfos()``\ , may be -1 if unknown
    :param dict info: Dictionary containing the TR64 Response with all the data about the device; automatically passed to :py:meth:`loadData()`
    
    :ivar API_avm_homeauto api: stores the supplied API object
    :ivar int index: stores the supplied index
    :ivar dict info: stores the data in a dictionary
    
    General Device Variables:
    
    :ivar str ain: AIN of the device
    :ivar int deviceID: Device ID
    :ivar int functionbitmask: Bitmask containing the flags if specific features are enabled, also see the :py:data:`*_flag` variables
    :ivar str fwversion: Firmware Version currently installed
    :ivar str manufacturer: Manufacturer Name, e.g. ``AVM``
    :ivar str productname: Full Product Name of the device, e.g. ``FRITZ!Powerline 546E``
    :ivar str name: User-Defined Name of the device
    :ivar int present: Integer determining the connection state, see :py:data:`PresentEnum2INT` for more information
    
    Energy/Multimeter specific Variables:
    
    :ivar bool energy_flag: Flag if the device supports Multimeter features
    :ivar bool energy_valid: Flag if the following variables are valid
    :ivar float energy_power: Current power flowing through the device, in Watts
    :ivar float energy_energy: Total amount of energy that flowed through this device since the last reset in Watthours
    
    Temperature/Thermometer specific Variables:
    
    :ivar bool temp_flag: Flag if the device supports Thermometer features
    :ivar bool temp_valid: Flag if the following variables are valid
    :ivar float temp_celsius: Current temperature measured in degrees Celsius
    :ivar float temp_offset: Offset Temperature defined by the User in degrees Celsius
    
    Switch specific Variables:
    
    :ivar bool switch_flag: Flag if the device supports switch features
    :ivar bool switch_valid: Flag if the following variables are valid
    :ivar bool switch_state: Property used to switch the switch, see :py:attr:`switch_state`
    :ivar str switch_mode: Either ``automatic`` or ``manual``\ , as set by the user
    :ivar bool switch_lock: Flag if the switch is locked via hardware
    
    HKR/Heating regulator specific Variables, all temperatures are in degrees celsius:
    
    
    :ivar bool hkr_flag: Flag if the device supports HKR features
    :ivar bool hkr_valid: Flag if the following variables are valid
    :ivar float hkr_temp_is: Current temperature
    :ivar str hkr_valve_set: Set Valve state
    :ivar float hkr_temp_set: Set Temperature
    :ivar str hkr_valve_reduce: Reduce Valve state
    :ivar float hkr_temp_reduce: Reduce Temperature
    :ivar str hkr_valve_comfort: Comfort Valve state
    :ivar float hkr_temp_comfort: Comfort Temperature
    
    Valve states may be either ``open``\ , ``close`` or ``temp``\ , where temp means regulated.
    Refer to the documentation of the TR-064 AVM API for more information.
    """
    def __init__(self,api,index,info):
        self.api = api
        self.index = index
        self.info = info
        self.loadData(info)
    def loadData(self,data):
        """
        Populates instance variables with the supplied TR64 response.
        This method is automatically called upon construction with the supplied info dict.
        """
        self.ain = data["NewAIN"]
        self.deviceID = int(data["NewDeviceId"])
        self.functionbitmask = int(data["NewFunctionBitMask"])
        self.fwversion = data["NewFirmwareVersion"]
        self.manufacturer = data["NewManufacturer"]
        self.productname = data["NewProductName"]
        self.name = data["NewDeviceName"]
        self.present = PresentEnum2INT[data["NewPresent"]]
        # Energy/Multimeter
        self.energy_flag = data["NewMultimeterIsEnabled"]=="ENABLED"
        self.energy_valid = data["NewMultimeterIsValid"]=="VALID"
        self.energy_power = float(data["NewMultimeterPower"])/100
        self.energy_energy = float(data["NewMultimeterEnergy"])
        # Temp/Temperature
        self.temp_flag = data["NewTemperatureIsEnabled"]=="ENABLED"
        self.temp_valid = data["NewTemperatureIsValid"]=="VALID"
        self.temp_celsius = float(data["NewTemperatureCelsius"])/10
        self.temp_offset = float(data["NewTemperatureOffset"])/10
        # Switch
        self.switch_flag = data["NewSwitchIsEnabled"]=="ENABLED"
        self.switch_valid = data["NewSwitchIsValid"]=="VALID"
        self._switch_state = data["NewSwitchState"]=="ON"
        self.switch_mode = "automatic" if data["NewSwitchMode"]=="AUTO" else "manual"
        self.switch_lock = data["NewSwitchLock"]=="1"
        # HKR/Heating regulators
        self.hkr_flag = data["NewHkrIsEnabled"]=="ENABLED"
        self.hkr_valid = data["NewHkrIsValid"]=="VALID"
        self.hkr_temp_is = float(data["NewHkrIsTemperature"])/10
        self.hkr_valve_set = data["NewHkrSetVentilStatus"].lower()
        self.hkr_temp_set = float(data["NewHkrSetTemperature"])/10
        self.hkr_valve_reduce = data["NewHkrReduceVentilStatus"].lower()
        self.hkr_temp_reduce = float(data["NewHkrReduceTemperature"])/10
        self.hkr_valve_comfort = data["NewHkrComfortVentilStatus"].lower()
        self.hkr_temp_comfort = float(data["NewHkrComfortTemperature"])/10
    def reloadData(self):
        """
        Reloads the data from the server.
        
        Note that even if the object was originally constructed using
        :py:meth:`getDeviceByIndex() <API_avm_homeauto.getDeviceByIndex>`
        this method will request the data via its AIN.
        """
        d = self.api.dynapi.GetSpecificDeviceInfos(NewAIN=self.ain)
        d["NewAIN"]=self.ain
        self.info = d
        self.loadData(d)
    
    @property
    def switch_state(self):
        """
        Property used for getting and setting the switch state.
        
        The value returned by the getter is only updated when :py:meth:`reloadData()` is called.
        
        The setter immediately sets the switch state and refreshes the data.
        
        See :py:data:`STATE2SwStateEnum` for a list of valid values.
        
        :raises AssertionError: if this device does not support switching
        :raises KeyError: if the assigned value is invalid
        """
        assert self.switch_flag
        return self._switch_state
    @switch_state.setter
    def switch_state(self,value):
        self.api.switchByAIN(self.ain,value)
        self.reloadData()
