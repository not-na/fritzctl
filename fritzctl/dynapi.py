#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dynapi.py
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


class DynamicAPI(object):
    """
    Dynamic API class that automagically generates methods for calling actions.
    
    This class will generate API methods based on the device definitions found in the session.
    You may pass arguments to the auto-generated methods via keyword arguments only.
    
    If you need to pass an argument that is not a valid Python identifier, use this trick: ``api.MyAPIMethod(**{"Some-Strange-Name":"Value"})``\ .
    
    :param Session session: :py:class:`Session()` object used for requests
    :param str urn: Service Type URN to be wrapped by this instance
    
    :ivar session: Stored session object
    :ivar urn: Stored URN for requests
    :ivar url: Action URL for requests, specific to the URN
    """
    def __init__(self,session,urn):
        self.session = session
        self.urn = urn
        self.url = self.session.device.getControlURL(self.urn)
        methods = self.session.device.deviceSCPD[self.urn]
        def _apiMethod(self,method):
                def callAPI(*args,**kwargs):
                    return self.session.execute(self.url,self.urn,method,*args,**kwargs)
                return callAPI
        for method in methods:
            setattr(self,method,_apiMethod(self,method))
    def callAPI(self,action,*args,**kwargs):
        """
        Fallback to use if the API action is not a valid Python identifier or was added after the session was initialized.
        """
        return self.session.execute(self.url,self.urn,action,*args,**kwargs)
