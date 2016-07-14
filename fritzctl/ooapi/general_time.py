#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  general_time.py
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

class API_general_time(base.API_base):
    """
    Time configuration TR64 Object-Oriented API.
    
    Can be instantiated via ``session.getOOAPI("general_time")`` or ``session.getOOAPI("urn:dslforum-org:service:Time:1")``\ .
    
    Same parameters and attributes as :py:class:`fritzctl.ooapi.base.API_base()`\ .
    """
    def getInfo(self):
        """
        Returns information about the time configuration.
        
        :return: Information about the time configuration on the server
        :rtype: TimeInfo
        """
        return TimeInfo(self,self.dynapi.GetInfo())
    def setNTPServers(self,server1,server2):
        """
        Sets the NTP Servers to be used by the server.
        
        :param str server1: NTP Server #1
        :param str server2: NTP Server #2
        :raises ValueError: if the servers are invalid
        """
        self.dynapi.SetNTPServers(NewNTPServer1=server1,NewNTPServer2=server2)

class TimeInfo(object):
    """
    Time configuration information class.
    
    :param API_general_time api: API object to use when querying for data
    :param dict info: Dictionary containing the TR64 Response with all the data about the device; automatically passed to :py:meth:`loadData()`
    
    :ivar API_general_time api: stores the supplied API object
    :ivar dict info: stores the data in a dictionary
    
    Configuration Variables:
    
    :ivar server1: NTP Server address #1
    :type server1: str or None
    :ivar server2: NTP Server address #2
    :type server2: str or None
    :ivar str time: String containing the formatted current time on the server.
    
    Variables not supported by the FRITZ!Box, but included for compatibility:
    
    :ivar str timezone: String Representing the local Timezone
    :ivar bool dst_used: Flag if Daylight Saving Time is enabled
    :ivar str dst_start: Formatted Time when DST begins
    :ivar str dst_end: Formatted Time when DST ends
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
        self.server1 = data["NewNTPServer1"]
        self.server2 = data["NewNTPServer2"]
        self.time = data["NewCurrentLocalTime"]
        # These options are not supported by the FRITZ!Box, but they are included here for forward-compatibility
        self.timezone = data["NewLocalTimeZone"]
        self.timezonename = data["NewLocalTimeZoneName"]
        self.dst_used = data["NewDaylightSavingsUsed"]=="1"
        self.dst_start = data["NewDaylightSavingsStart"]
        self.dst_end = data["NewDaylightSavingsEnd"]
    def reloadData(self):
        """
        Reloads the data from the server in-place.
        """
        d = self.api.dynapi.GetInfo()
        self.info = d
        self.loadData(d)
