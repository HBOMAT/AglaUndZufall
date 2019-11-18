#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


                                                     
#                                                 
# Basis - Klasse  von agla           
#                                                 

#
# This file is part of agla
#
#
# Copyright (c) 2019 Holger Böttcher  hbomat@posteo.de
#
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License
# You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#  
		
		
													  
from sympy.core.basic import Basic
from sympy.core.sympify import sympify
from sympy.printing import sstr



class AglaObjekt(Basic):                     
    """Basisklasse für alle geometrischen Objekte"""

    def __new__(cls, *args, **kwargs):
        return Basic.__new__(cls, *sympify(args))


    def __str__(self):
        """String-Repräsentation für ein agla-Objekt"""
        return type(self).__name__ + sstr(self.args)

    def __repr__(self):
        """repr-Repräsentation für ein agla-Objekt"""
        return type(self).__name__ + repr(self.args)     


    
