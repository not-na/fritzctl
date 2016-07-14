#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  base.py
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

class API_base(object):
    """
    Base class for all Object-Oriented API Classes.
    
    This class simply stores the session and URN and requests a dynamic API.
    
    :param Session session: Session object this API should be bound to
    :param str urn: Service Type URN for identifying the service to be wrapped.
    
    :ivar session: Same as the argument
    :ivar urn: Same as the argument
    :ivar dynapi: :py:class:`DynamicAPI() <fritzctl.dynapi.DynamicAPI>` instance to be used for requesting data.
    """
    def __init__(self,session,urn):
        self.session = session
        self.urn = urn
        self.dynapi = self.session.getAPI(self.urn)
