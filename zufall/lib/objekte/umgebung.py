#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
#  Umgebung von zufall           
#                                                 
                                  
#
#  This file is part of zufall
#
#
#  Copyright (c) 2019 Holger Böttcher  hbomat@posteo.de
#
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  



from zufall.lib.objekte.basis import ZufallsObjekt


class Umgebung(ZufallsObjekt):
    """Umgebung von zufall"""
             
    def __new__(cls, *args, **kwargs): 
	
        # Variable für die Grundmenge bei der Arbeit mit einer Ereignis-Algebra    
        cls.OMEGA = None
		
        # Variable zur Steuerung der Eingabe von Vektoren
        #    bei UMG.SIMPL == False erfolgt keine Umwandlung von 
        #    float-Komponenten in rationale    
        cls.SIMPL = True

        return ZufallsObjekt.__new__(cls)
			

UMG = Umgebung()
OMEGA = Umgebung().OMEGA


