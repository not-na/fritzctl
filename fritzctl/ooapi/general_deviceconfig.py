#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  general_deviceconfig.py
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

import requests
from requests.auth import HTTPDigestAuth

import base

class API_general_deviceconfig(base.API_base):
    """
    Device Configuration TR64 Object-Oriented API.
    
    Can be instantiated via ``session.getOOAPI("general_deviceconfig")`` or ``session.getOOAPI("urn:dslforum-org:service:DeviceConfig:1")``\ .
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    @property
    def persistentData(self):
        """
        Property allowing the user to store Persistent Data on the Device.
        
        This Property is not cached and requests/stores the persistent Data immediately and blocking on the device.
        
        This Property can be written to and read from.
        """
        return self.dynapi.GetPersistentData()["NewPersistentData"]
    @persistentData.setter
    def persistentData(self,value):
        self.dynapi.SetPersistentData(NewPersistentData=value)
    
    def startConfiguration(self):
        """
        Starts a single Configuration Transaction during which no other client may modify settings.
        
        This session will timeout after 45 seconds.
        
        You can alos use every instance of this class as a context manager::
           
           with api:
               # do some configuration...
           # Session automatically closed
        
        """
        self.dynapi.ConfigurationStarted(NewSessionID=self.dynapi.X_GenerateUUID()["NewUUID"])
    def finishConfiguration(self):
        """
        Counterpart to :py:meth:`startConfiguration()`\ , closes the session.
        
        :return: the new status of the configuration
        :rtype: str
        """
        return self.dynapi.ConfigurationFinished()["NewStatus"]
    def __enter__(self):
        self.startConfiguration()
    def __exit__(self,*args):
        self.finishConfiguration()
        return False
    
    def factoryReset(self):
        """
        Factory Resets the Device.
        
        .. warning::
           
           Use extreme care when using this method in your programs,
           as accidentally triggering it due to bugs can and will cut your internet.
        """
        self.dynapi.FactoryReset()
    def reboot(self):
        """
        Reboots the Device.
        
        .. warning::
           
           Be careful when using this method in automated scripts, as it can cause boot-shutdown-boot... loops.
        """
        self.dynapi.Reboot()
    
    def getConfigFileURL(self,password):
        """
        Returns an HTTPS URL valid for less than 30 seconds to request an encrypted configfile.
        
        Additionally, the FRITZ!Box requires HTTP Digest Authentication using the TR64 credentials to request the URL.
        
        .. seealso::
           
           See :py:meth:`getConfigFile()` for an easier way to get the config file.
        
        :param str password: Password used to encrypt the configfile, needed to decrypt
        :return: An URL allowing you to access the configfile for 30 seconds
        :rtype: str
        :raises AssertionError: if the password is not a string
        :raises ValueError: if the password was rejected by the server
        """
        assert isinstance(password,str)
        return self.dynapi.callAPI("X_AVM-DE_GetConfigFile",**{"NewX_AVM-DE_Password":password})["NewX_AVM-DE_ConfigFileUrl"]
    def getConfigFile(self,password):
        """
        Helper method wrapping :py:meth:`getConfigFileURL()` for an easier way to get the configfile.
        
        :param str password: Password used to encrypt the configfile, needed to decrypt
        :return: The raw encrypted Configfile
        :rtype: str
        """
        return requests.get(self.getConfigFileURL(password),auth=HTTPDigestAuth(self.session.user,self.session.pwd)).content
    
    def setConfigFile(self,password,configurl):
        """
        Sets the configfile to the file found at the specified URL and encrypted with the password.
        
        :param str password: Password usable to decrypt the configfile
        :param str configurl: URL storing the encrypted configfile
        :raises AssertionError: if the password is not a string
        :raises ValueError: if the password was rejected by the server or invalid
        """
        assert isinstance(password,str)
        data = {"NewX_AVM-DE_Password":password,"NewX_AVM-DE_ConfigFileUrl":configurl}
        self.dynapi.callAPI("X_AVM-DE_SetConfigFile",**data)
    
    def createURLSessionID(self):
        """
        Creates an Session ID usable with e.g. the AHA HTTP API or the user interface.
        
        :return: A Valid Session ID
        :rtype: str
        """
        return self.dynapi.callAPI("X_AVM-DE_CreateUrlSID")["NewX_AVM-DE_UrlSID"]
    def getSecureURL(self,url):
        """
        Gets a secure URL using a Session ID.
        
        Make sure that your URLs end either with a slash or a questionmark, else you will get ConnectionErrors.
        Also, you must include a scheme.
        
        :param str url: URL to GET the data from
        :return: The raw page content
        :rtype: str
        :raises requests.exceptions.*: if there is an error while getting the URL
        """
        return requests.get(url+self.createURLSessionID()).content
