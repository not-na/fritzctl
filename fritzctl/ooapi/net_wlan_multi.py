#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  net_wlan_multi.py
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

KEYLONG = {
    "wep0":"NewWEPKey0",
    "wep1":"NewWEPKey1",
    "wep2":"NewWEPKey2",
    "wep3":"NewWEPKey3",
    "psk":"NewPreSharedKey",
    "passphrase":"NewKeyPassphrase",
    }
"""
Mapping converting between user-friendly key names and TR64 State Variables.

Mapping:

==================== ===========================
User-Friendly Name   Internal Name              
==================== ===========================
``wep0``             ``NewWEPKey0``
``wep1``             ``NewWEPKey1``
``wep2``             ``NewWEPKey2``
``wep3``             ``NewWEPKey3``
``psk``              ``NewPreSharedKey``
``passphrase``       ``NewKeyPassphrase``
==================== ===========================

"""

WLANHYBRIDNAMES = {
    "enable":"NewEnable",
    "beacontype":"NewBeaconType",
    "keypassphrase":"NewKeyPassphrase",
    "ssid":"NewSSID",
    "bssid":"NewBSSID",
    "trafficmode":"NewTrafficMode",
    "manualspeed":"NewManualSpeed",
    "maxspeed_down":"NewMaxSpeedDS",
    "maxspeed_up":"NewMaxSpeedUS",
    }
"""
Dictionary used to convert a :py:class:`WlanHybridModeConfig()` to a dictionary.

Mapping:

==================== ===========================
User-Friendly Name   Internal Name
==================== ===========================
``enable``           ``NewEnable``
``beacontype``       ``NewBeaconType``
``keypassphrase``    ``NewKeyPassphrase``
``ssid``             ``NewSSID``
``bssid``            ``NewBSSID``
``trafficmode``      ``NewTrafficMode``
``manualspeed``      ``NewManualSoeed``
``maxspeed_down``    ``NewMaxSpeedDS``
``maxspeed_up``      ``NewMaxSpeedUS``
==================== ===========================
"""

class API_net_wlan_multi(base.API_base):
    """
    Wlan Configuration TR64 Object-Oriented API.
    
    Can be instantiated via ``session.getOOAPI("avm_homeauto")`` or ``session.getOOAPI("urn:dslforum-org:service:X_AVM-DE_Homeauto:1")``\ .
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    def getConfig(self,ext=True):
        """
        Returns a WLAN Information Object about the current network.
        
        :param bool ext: Optional Flag if AVM Extension Wlan data should be integrated, defaults to True
        :return: WLAN Information Object
        :rtype: WlanConfig
        """
        d = self.dynapi.GetInfo()
        d["_ext"]=ext
        if ext:
            d.update(self.dynapi.callAPI("X_AVM-DE_GetWLANExtInfo"))
        return WlanConfig(self,d)
    def getDeviceByIndex(self,index):
        """
        Returns a specific Wlan device by Index.
        
        :param int index: Index of the Wlan Device
        :return: Wlan Device Object
        :rtype: AssociatedDeviceInfo
        :raises AssertionError: if the index is invalid, e.g. not an integer or less than zero.
        :raises ValueError: if the index is out of bounds
        """
        assert isinstance(index,int) and index>=0
        return AssociatedDeviceInfo(self,index,self.dynapi.GetGenericAssociatedDeviceInfo(NewAssociatedDeviceIndex=index))
    def getDevices(self):
        """
        Returns a list of Wlan Devices.
        
        :return: List of Wlan Devices
        :rtype: List of :py:class:`AssociatedDeviceInfo()`
        """
        out = []
        for i in range(self.getConfig().totalAssociations):
            out.append(self.getDeviceByIndex(i))
        return out
    def getDeviceByMAC(self,mac):
        """
        Returns the Wlan Device associated with the MAC Address.
        
        :param str mac: MAC Address of the device to return
        :return: Wlan Device Object
        :rtype: AssociatedDeviceInfo
        :raises AssertionError: if the MAC Address is invalid, e.g. not a string
        :raises ValueError: if the MAC Address was rejected by the server or unknown
        """
        assert isinstance(mac,str)
        return AssociatedDeviceInfo(self,-1,self.dynapi.GetSpecificAssociatedDeviceInfo(NewAssociatedDeviceMACAddress=mac))

class AssociatedDeviceInfo(object):
    """
    General Wlan Device Class.
    
    :param API_net_wlan_multi api: API object to use when querying for data
    :param int index: Index this device had when requested via ``GetGenericAssociatedDeviceInfos()``\ , may be -1 if unknown
    :param dict info: Dictionary containing the TR64 Response with all the data about the device; automatically passed to :py:meth:`loadData()`
    
    :ivar API_net_wlan_multi api: stores the supplied API object
    :ivar int index: stores the supplied index
    :ivar dict info: stores the data in a dictionary
    
    Device Variables:
    
    :ivar str mac: MAC Address of the Device
    :ivar str ip: IP Address of the Device
    :ivar bool authstate: Flag if the device is authentificated or not
    :ivar int speed: Speed of the connection in Mbits/s
    :ivar int signalstrength: Strength of the signal from 0 to 70, unit unknown
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
        self.mac = data["NewAssociatedDeviceMACAddress"]
        self.ip = data["NewAssociatedDeviceIPAddress"]
        self.authstate = data["NewAssociatedDeviceAuthState"]=="1"
        self.speed = int(data["NewX_AVM-DE_Speed"])
        self.signalstrength = int(data["NewX_AVM-DE_SignalStrength"])
    def reloadData(self):
        """
        Reloads the data from the server and integrates it in-place.
        """
        d = self.api.dynapi.GetSpecificAssociatedDeviceInfo(NewAssociatedDeviceMACAddress=self.mac)
        d["NewAssociatedDeviceMACAddress"]=self.mac
        self.info = d
        self.loadData(d)

class WLANGuestInfo(object):
    """
    Simple storage object used by :py:class:`WlanConfig()` to represent a guest network.
    
    :param API_net_wlan_multi api: API object stored for future use
    
    :ivar API_net_wlan_multi api: Stored API object
    
    Instance Variables set by :py:meth:`WlanConfig.loadData()`\ :
    
    :ivar bool apenabled: Flag indicating if the Guest Network is enabled
    :ivar str aptype: Access Point Type, e.g. ``normal``
    :ivar bool timeout_active: Flag if a timeout was set
    :ivar timeout_remain: Time in seconds that remain
    :type timeout_remain: str or ``None``
    :ivar timeout_timeout: Duration of the Timeout
    :type timeout_timeout: str or ``None``
    :ivar bool noforcedoff: Flag if force should be used when going off
    :ivar userisolation: Type of Userisolation
    :type userisolation: str or ``None``
    :ivar encmode: Type of Encryption used
    :type encmode: str or ``None``
    :ivar int timestamp: Timestamp of the Access Point
    """
    def __init__(self,api):
        self.api = api

class WlanConfig(object):
    """
    WLAN Configuration Object.
    
    Allows getting and setting various properties of the network this object is associated with.
    
    .. seealso::
       
       See :py:data:`fritzctl.session.NAME_TO_URN` for more information about how to get specific networks.
    
    :param API_net_wlan_multi api: API object to use when querying for data
    :param dict info: Dictionary containing the TR64 Response with all the data about the device; automatically passed to :py:meth:`loadData()`
    
    :ivar API_net_wlan_multi api: stores the supplied API object
    :ivar dict info: stores the supplied data in a dictionary
    
    :ivar WlanSecurityKeys keylist: Keylist allowing for easy key access, see :py:class:`WlanSecurityKeys()`
    :ivar WlanHybridModeConfig hybrid: Special config for accessing the hybrid network
    
    WLAN Network Configuration Values:
    
    :ivar bool enable: Flag if the network is enabled, see :py:attr:`enable` for more information about this propertys
    :ivar str status: Status string, either ``Up`` or ``Down``
    :ivar str maxbitrate: String containing either ``Auto`` or the maximum bitrate
    :ivar int channel: Property containing the current channel used, see :py:attr:`channel`
    :ivar list possibleChannels: List of all possible channels, updated when getting :py:attr:`channel`
    :ivar str ssid: Property containing the SSID of the network, see :py:attr:`ssid`
    :ivar str beaconType: Property containing the Beacon Type used by this network, see :py:attr:`beaconType`
    :ivar bool maccontrol: Flag if the MAC Address Filter is enabled, allowing only known devices to connect
    :ivar str standard: WLAN Standard supported by the network, e.g. ``g``
    :ivar str bssid: Property containing the BSSID of the network, see :py:attr:`bssid`
    :ivar str basic_enc_modes: Basic Encryption Modes as set by the server, seems to be ``"None"`` right now
    :ivar str basic_auth_mode: Basic Authentification Mode as set by the server, seems to be ``"None"`` right now
    :ivar int ssid_maxlen: Maximum allowed length of the SSID
    :ivar int ssid_minlen: Minimum allowed length of the SSID
    :ivar str ssid_allowedchars: String of all characters allowed in an SSID
    :ivar int psk_minlen: Minimum allowed length of the PreSharedKey
    :ivar int psk_maxlen: Maximum allowed length of the PreSharedKey
    :ivar str psk_allowedchars: Similiar to :py:attr:`ssid_allowedchars`\ , but for PSK
    
    Extension Variables only present if the ``_ext`` key is set to True:
    
    :ivar WLANGuestInfo guest: Guest Network Information Object, see :py:class:`WLANGuestInfo()` for more information
    
    """
    def __init__(self,api,info):
        self.api = api
        self.info = info
        self.keylist = WlanSecurityKeys(self,api)
        self.hybrid = WlanHybridModeConfig(self,api)
        self.loadData(self.info)
    def loadData(self,data):
        """
        Populates instance variables with the supplied TR64 response.
        This method is automatically called upon construction with the supplied info dict.
        """
        self._enable = data["NewEnable"]=="1"
        self.status = data["NewStatus"]
        self.maxbitrate = data["NewMaxBitRate"]
        #self.channel = int(data["NewChannel"])
        self.possibleChannels = [int(i) for i in self.api.dynapi.GetChannelInfo()["NewPossibleChannels"].split(",")]
        #self.ssid = data["NewSSID"]
        #self.beaconType = data["NewBeaconType"]
        self.maccontrol = data["NewMACAddressControlEnabled"]=="1"
        self.standard = data["NewStandard"]
        #self.bssid = data["NewBSSID"]
        self.basic_enc_modes = data["NewBasicEncryptionModes"]
        self.basic_auth_mode = data["NewBasicAuthenticationMode"]
        self.ssid_maxlen = int(data["NewMaxCharsSSID"])
        self.ssid_minlen = int(data["NewMinCharsSSID"])
        self.ssid_allowedchars = data["NewAllowedCharsSSID"]
        self.psk_minlen = int(data["NewMinCharsPSK"])
        self.psk_maxlen = int(data["NewMaxCharsPSK"])
        self.psk_allowedchars = data["NewAllowedCharsPSK"]
        if data["_ext"]:
            self.guest = WLANGuestInfo(self.api)
            self.guest.apenabled = data["NewX_AVM-DE_APEnabled"]=="1"
            self.guest.aptype = data["NewX_AVM-DE_APType"]
            self.guest.timeout_active = data["NewX_AVM-DE_TimeoutActive"]=="1"
            self.guest.timeout_timeout = data["NewX_AVM-DE_Timeout"]
            self.guest.timeout_remain = data["NewX_AVM-DE_TimeRemain"]
            self.guest.noforcedoff = data["NewX_AVM-DE_NoForcedOff"]=="1"
            self.guest.userisolation = data["NewX_AVM-DE_UserIsolation"]
            self.guest.encmode = data["NewX_AVM-DE_EncryptionMode"]
            self.guest.timestamp = int(data["NewX_AVM-DE_LastChangedStamp"])
    def reloadData(self):
        """
        Reloads the stored information in-place.
        
        Note that extension data is only refreshed if the ``_ext`` key is set to True.
        """
        d = self.api.dynapi.GetInfo()
        d["_ext"]=self.info["_ext"]
        if d["_ext"]:
            d.update(self.api.dynapi.callAPI("X_AVM-DE_GetWLANExtInfo"))
        self.info = d
        self.loadData(d)
    
    def pushConfig(self):
        """
        Pushes modified data to the server.
        
        Note that only some variables are pushed, as not all are supported.
        
        Mapping of variable names to internal names:
        
        ============================ ===============================
        Instance Variable            TR64 State Variable            
        ============================ ===============================
        :py:attr:`maxbitrate`        ``NewMaxBitRate``
        :py:attr:`channel`           ``NewChannel``
        :py:attr:`ssid`              ``NewSSID``
        :py:attr:`beaconType`        ``NewBeaconType``
        :py:attr:`maccontrol`        ``NewMacAddressControlEnabled``
        :py:attr:`basic_enc_modes`   ``NewBasicEncryptionModes``
        :py:attr:`basic_auth_mode`   ``NewBasicAuthenticationMode``
        ============================ ===============================
        """
        d = {"NewMaxBitRate":self.maxbitrate,
             "NewChannel":self.channel,
             "NewSSID":self.ssid,
             "NewBeaconType":self.beaconType,
             "NewMacAddressControlEnabled":self.maccontrol,
             "NewBasicEncryptionModes":self.basic_enc_modes,
             "NewBasicAuthenticationMode":self.basic_auth_mode,
            }
        self.api.dynapi.SetConfig(**d)
        self.reloadData()
    
    def getStatistics(self):
        """
        Returns packet statistics for the current network.
        
        .. todo::
           
           Check the difference between ``GetStatistics()`` and ``GetPacketStatistics()``
        
        :return: 2-tuple of ``(TotalPacketsSent,TotalPacketsReceived)``
        :rtype: tuple
        """
        d = self.api.dynapi.GetStatistics()
        return d["NewTotalPacketsSent"],d["NewTotalPacketsReceived"]
    def getNightControl(self):
        """
        Gets the night control settings.
        
        :return: 2-tuple of ``(NightControl,NoForcedOff)`` where NightControl may be None
        :rtype: tuple
        """
        d = self.api.dynapi.callAPI("X_AVM-DE_GetNightControl")
        return d["NewNightControl"],d["NewNightTimeControlNoForcedOff"]=="1"
    
    @property
    def enabled(self):
        """
        Property used to control if the network is enabled.
        
        This property can also be written to with standard Python bool values.
        """
        return self._enable
    @enabled.setter
    def enabled(self,value):
        self.api.dynapi.SetEnable(NewEnable=str(int(value)))
        self.reloadData()
    
    @property
    def enableHighFrequencyBand(self):
        """
        Read-only Property for setting the high frequency band either on or off.
        
        :raises AssertionError: if the value is not a boolean value
        :raises NotImplementedError: if you try to read from this property
        """
        raise NotImplementedError("enableHighFrequencyBand has no setter since there is no API call available")
    @enableHighFrequencyBand.setter
    def enableHighFrequencyBand(self,value):
        assert isinstance(value,bool)
        value = "1" if value else "0"
        self.api.dynapi.X_SetHighFrequencyBand(NewEnableHighFrequency=value)
    
    @property
    def ssid(self):
        """
        Property allowing access to the SSID of the network.
        
        The SSID is often displayed by User Agents for ease-of-use.
        
        This property is uncached and may also be written to,
        see the :py:attr:`ssid_minlen`\ , :py:attr:`ssid_maxlen` and :py:attr:`ssid_allowedchars` attributes.
        
        :raises AssertionError: if the supplied SSID is invalid, e.g. not a string or contains characters that are not allowed
        :raises ValueError: if the server rejects the SSID, examine the traceback for more information
        """
        return self.api.dynapi.GetSSID()["NewSSID"]
    @ssid.setter
    def ssid(self,value):
        assert isinstance(value,str) and self.ssid_minlen<len(value)<self.ssid_maxlen
        s = value
        for char in self.ssid_allowedchars:
            s = s.replace(char,"")
        assert len(s)==0
        self.api.dynapi.SetSSID(NewSSID=value)
    
    @property
    def channel(self):
        """
        Property used to manage the wireless channel used by the network.
        
        This property can also be written to.
        
        Note that even just reading this property will also update the :py:attr:`possibleChannels` attribute.
        
        :raises AssertionError: if the supplied channel is invalid, e.g. not an integer or not in :py:attr:`possibleChannels`
        :raises ValueError: if the channel is rejected by the server
        """
        info = self.api.dynapi.GetChannelInfo()
        self.possibleChannels = [int(i) for i in info["NewPossibleChannels"].split(",")]
        return int(info["NewChannel"])
    @channel.setter
    def channel(self,value):
        assert isinstance(value,int) and value in self.possibleChannels
        self.api.dynapi.SetChannel(NewChannel=value)
    
    @property
    def bssid(self):
        """
        Property for getting the BSSID of the current network.
        
        Note that this property is not cached and will be slow to get.
        """
        return self.api.dynapi.GetBSSID()["NewBSSID"]
    
    @property
    def beaconType(self):
        """
        Property for managing the beacon type used by the network.
        
        This property may also be written to.
        
        :raises AssertionError: if the supplied beacon type is invalid, e.g. not a string
        :raises ValueError: if the beacon type is rejected by the server
        """
        return self.api.dynapi.GetBeaconType()["NewBeaconType"]
    @beaconType.setter
    def beaconType(self,value):
        assert isinstance(value,str)
        self.api.dynapi.SetBeaconType(NewBeaconType=beaconType)
    
    @property
    def beaconAdvertisement(self):
        """
        Property Flag if the network uses a beacon advertisement.
        
        This property can also be written to.
        
        :raises AssertionError: if the given flag is not a boolean value
        """
        return bool(self.api.dynapi.GetBeaconAdvertisement()["NewBeaconAdvertisementEnabled"])
    @beaconAdvertisement.setter
    def beaconAdvertisement(self,value):
        assert isinstance(value,bool)
        value = "1" if value else "0"
        self.api.dynapi.SetBeaconAdvertisement(NewBeaconAdvertisementEnabled=value)
    
    @property
    def beaconSecurityProperties(self):
        """
        Property for accessing the security properties of the beacon.
        
        This property can also be written to.
        
        The format of both getter and setter is ``(EncryptionMode,AuthMode)``\ .
        
        :raises AssertionError: if the given value is invalid, e.g. not a tuple or list, length not equal to two or one of the values is not a string
        :raises ValueError: if the given values were rejected by the server
        """
        d = self.api.dynapi.GetBasBeaconSecurityProperties()
        return d["NewBasicEncryptionModes"],d["NewBasicAuthenticationMode"]
    @beaconSecurityProperties.setter
    def beaconSecurityProperties(self,value):
        assert (isinstance(value,tuple) or isinstance(value,list)) and len(value)==2
        assert isinstance(value[0],str) and isinstance(value[1],str)
        self.api.dynapi.SetBasBeaconSecurityProperties(NewBasicEncryptionModes=value[0],NewBasicAuthenticationMode=value[1])
    
    @property
    def totalAssociations(self):
        """
        Property containing the amount of total associations by this network.
        
        This property is read-only.
        """
        return int(self.api.dynapi.GetTotalAssociations()["NewTotalAssociations"])
    
    @property
    def defaultWEPKeyIndex(self):
        """
        Property for managing the default WEP Key Index.
        
        This property is not cached and can also be written to.
        
        :raises AssertionError: if the supplied key index is invalid, e.g. not an integer or not between 0 and 3 inclusive
        """
        return int(self.api.dynapi.GetDefaultWEPKeyIndex()["NewDefaultWEPKeyIndex"])
    @defaultWEPKeyIndex.setter
    def defaultWEPKeyIndex(self,value):
        assert isinstance(value,int) and 0<=value<=3
        self.api.dynapi.SetDefaultWEPKeyIndex(NewDefaultWEPKeyIndex=value)
    
    @property
    def stickSurfEnable(self):
        """
        Write-Only property used to set if sticksurf should be enabled.
        
        :raises AssertionError: if the supplied value is not boolean
        :raises NotImplementedError: if you try to write to this property
        """
        raise NotImplementedError("Missing API for stickSurfEnable getter, currently only a setter is available")
    @stickSurfEnable.setter
    def stickSurfEnable(self,value):
        assert isinstance(value,bool)
        value = "1" if value else "0"
        self.api.dynapi.callAPI("X_AVM-DE_SetStickSurfEnable",NewStickSurfEnable=value)
    
    @property
    def iptvOptimized(self):
        """
        Property for managing if the network is IPTV Optimized.
        
        This property is not cached but can be written to.
        
        :raises AssertionError: if the supplied value is not boolean
        """
        return self.api.dynapi.callAPI("X_AVM-DE_GetIPTVOptimized")["NewX_AVM-DE_IPTVoptimize"]=="1"
    @iptvOptimized.setter
    def iptvOptimized(self,value):
        assert isinstance(value,bool)
        value = "1" if value else "0"
        self.api.dynapi.callAPI("X_AVM-DE_SetIPTVOptimized",**{"NewX_AVM-DE_IPTVOptimize":value})
   
class WlanSecurityKeys(object):
    """
    Security Key Helper class for ease-of-use.
    
    This object may be used like a list or a dict.
    
    If used like a list, only indices 0-3 are accepted, referring to the respective WEP Keys.
    
    The dictionary access allows for usage of user-friendly short names:
    
    ======== =========== ===================
    Index    Short Name  Long Name
    ======== =========== ===================
    0        wep0        NewWEPKey0
    1        wep1        NewWEPKey1
    2        wep2        NewWEPKey2
    3        wep3        NewWEPKey3
    ---      psk         NewPreSharedKey
    ---      passphrase  NewKeyPassphrase
    ======== =========== ===================
    
    You can also use both of these access methods for reading and writing.
    
    Note that it is slow if you set each key sequentially, instead see :py:meth:`setKeys()` for batched key setting.
    
    It *should* also be possible to set this object to a list, tuple or dict by setting the corresponding attribute of its parent.
    This mechanic will not work if this object is not an attribute.
    """
    def __init__(self,wlaninfo,api):
        self.wlaninfo = wlaninfo
        self.api = api
    def __getitem__(self,item):
        if isinstance(item,int):
            assert 0<=item<=3
            return self.api.dynapi.GetSecurityKeys()["NewWEPKey%s"%item]
        elif isinstance(item,str):
            assert item in KEYLONG
            return self.api.dynapi.GetSecurityKeys()[KEYLONG[item]]
        else:
            raise TypeError("Invalid Type for Security key, must be int or str")
    def __setitem__(self,item,value):
        if isinstance(item,int):
            assert 0<=item<=3
            d = self.getKeyList()
            d[item] = value
            self.setKeys(d)
        elif isinstance(item,str):
            assert item in KEYLONG
            d = self.getKeyDict()
            d[item]=value
            self.setKeys(d)
        else:
            raise TypeError("Invalid Type for Security key, must be int or str")
    def getKeyList(self):
        """
        Returns the keys in form of a list.
        
        The list has the order ``[wep0,wep1,wep2,wep3,psk,passphrase]``\ .
        
        You can modify this list without modifying the list on the server and when you are done you may apply these changes via :py:meth:`setKeys()`\ .
        
        :return: List of all 6 keys
        :rtype: list
        """
        d = self.api.dynapi.GetSecurityKeys()
        out = [d["NewWEPKey0"],d["NewWEPKey1"],d["NewWEPKey2"],d["NewWEPKey3"],d["NewPreSharedKey"],d["NewKeyPassphrase"]]
        return out
    def getKeyDict(self):
        """
        Returns the keys as a dictionary.
        
        For a list of keys see :py:class:`WlanSecurityKeys()` or :py:data:`KEYLONG`\ .
        
        You can change the keys without modifying the keys on the server, but you may apply the changes you made via :py:meth:`setKeys()`\ .
        
        :return: Dictionary with all 6 keys
        :rtype: dict
        """
        d = self.api.dynapi.GetSecurityKeys()
        out = {"wep0":d["NewWEPKey0"],
               "wep1":d["NewWEPKey1"],
               "wep2":d["NewWEPKey2"],
               "wep3":d["NewWEPKey3"],
               "psk":d["NewPreSharedKey"],
               "passphrase":d["NewKeyPassphrase"],
            }
        return out
    def setKeys(self,keys):
        """
        Sets the keys on the server from either a list, tuple or dict.
        
        See :py:meth:`getKeyList()` for the format of the list or tuple and see :py:meth:`getKeyDict()` for the keys of the dictionary.
        
        :param keys: Keys to be set
        :type keys: list, tuple or dict
        :raises TypeErrror: if the given keys are neither a list, tuple or dict
        """
        if isinstance(keys,list) or isinstance(key,tuple):
            d = {"NewWEPKey0":keys[0],
                 "NewWEPKey1":keys[1],
                 "NewWEPKey2":keys[2],
                 "NewWEPKey3":keys[3],
                 "NewPresharedKey":keys[4],
                 "NewKeyPassphrase":keys[5],
                }
        elif isinstance(keys,dict):
            d = {"NewWEPKey0":keys["wep0"],
                 "NewWEPKey1":keys["wep1"],
                 "NewWEPKey2":keys["wep2"],
                 "NewWEPKey3":keys["wep3"],
                 "NewPresharedKey":keys["psk"],
                 "NewKeyPassphrase":keys["passphrase"],
                }
        else:
            raise TypeError("Invalid type for key collection, must be list, tuple or dict")
    def __get__(self,obj,objtype=None):
        return self
    def __set__(self,obj,val):
        self.setKeys(val)

class WlanHybridModeConfig(object):
    """
    WLAN Hybrid Mode Configuration Helper Class.
    
    This object can be used like a dictionary, for valid keys see :py:data:`WLANHYBRIDNAMES`\ .
    
    Note that none of these Methods are cached.
    
    If you need to get multiple variables you can do a batched request with :py:meth:`toDict()`
    """
    def __init__(self,wlaninfo,api):
        self.wlaninfo = wlaninfo
        self.api = api
    def __getitem__(self,item):
        return self.api.dynapi.callAPI("X_AVM-DE_GetWLANHybridMode")[WLANHYBRIDNAMES[item]]
    def __setitem__(self,item,value):
        d = self.api.dynapi.callAPI("X_AVM-DE_GetWLANHybridMode")
        d[WLANHYBRIDNAMES[item]]=value
        self.api.dynapi.callAPI("X_AVM-DE_SetWLANHybridMode",**d)
    def toDict(self):
        """
        Gets the whole WLAN Hybrid Mode Config as a dictionary.
        
        :return: Dictionary containing the WLAN Hybrid Config
        :rtype: dict
        """
        d = self.api.dynapi.callAPI("X_AVM-DE_GetWLANHybridMode")
        out = {}
        for key,value in WLANHYBRIDNAMES.items():
            out[key]=d[value]
        return out

