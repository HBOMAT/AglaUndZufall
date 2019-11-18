#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  GlueckRad - Klasse  von zufall           
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



from sympy.core.numbers import Integer, Tuple
from sympy.core.symbol import Symbol

from zufall.lib.objekte.zufalls_experiment import ZufallsExperiment 
from zufall.lib.funktionen.funktionen import (kombinationen, summe,
     anzahl_treffer)
	
from zufall.lib.objekte.ausnahmen import ZufallError



# GluecksRad - Klasse  
# -------------------
	
class GluecksRad(ZufallsExperiment): 
    """
	
Glücksrad 

**Kurzname**     **GR**,  **Rad**
		 
**Erzeugung**

   Rad( *liste1 /[, liste2, ... ] /[, stufen ]* )

**Parameter**
   
   *liste* :    *dict* | *dliste* 
				 
   *dict* :	  *{ obj1:zahl1, obj2:zahl2, ... }*  (dictionary)
  
   *dliste*: 
      | *[ [obj1, zahl1], [obj2, zahl2], ... ]* *oder*
      | *[ (obj1, zahl1), (obj2, zahl2), ... ]* *oder*   
      | *[ obj1, obj2, ...] ]*, ist gleich 
      | *[  [obj1, 1], [obj2, 1], ... ]*
			  
   *obj* :      Bezeichner | ganze Zahl >= 0
				 
   *stufen* :   Anzahl Stufen; Standard=1
				 
**Zusatz**
   `a=nein` -  keine Beachtung der Anordnung/Reihenfolge; Standard=ja
   
   `f=funktions_name` - Name einer ZG-Funktion ((diese ordnet den Elementen 
   der Ergebnismenge Zahlen zu)
		 
Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette 
eingegeben oder vordeklariert werden, etwa ``Raucher = Symbol('Raucher')``
			
    """			
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            gluecksrad_hilfe(kwargs["h"])		
            return
			
        def list_kontrolle(liste):
            if all([isinstance(x, (Symbol, str, int, Integer)) for x in liste]):
                return True
            if all([isinstance(x, (list, tuple, Tuple)) and len(x) == 2 for x in liste]):
                s = all([isinstance(x[0], (Symbol, str, int, Integer)) for x in liste])		
                w = all([isinstance(x[1], (int, Integer)) for x in liste])
                if s and w:
                    return True
                return False
            return False				
  
        def einfach(liste):
            if all([isinstance(x, list) and len(x)==2 and not isinstance(x[1], list) \
                    for x in liste]):
                return True                
            if any([isinstance(x, list)  for x in liste]):
                return False			
            return True                 
				
        def einfacheinfach(liste):
            if all([isinstance(x, (Symbol, str, int, Integer)) for x in liste]):
                return True
            return False
				
        try:			
            if len(args) == 1:
                args = args[0], 1			
            elif len(args) == 2 and not isinstance(args[0], (list, dict)) and \
                 isinstance(args[1], (int, Integer)):
                if isinstance(args[0], list):	
			
                    if not list_kontrolle(args[0]):     
                        raise ZufallError('Liste überprüfen')
                    if not einfach(args[0]):     
                        raise ZufallError('es sind nur einfache Listen erlaubt')
                    aa = args[0]					
                    if einfacheinfach(aa): 
                        aa = [[x, 1] for x in aa]                    				
                    try:					
                        args = dict(aa), args[1]
                    except ValueError:
                        print('zufall: Liste muß in dict transformierbar sein')
                        return					
				
            ze = ZufallsExperiment(*args, a=kwargs.get('a'))
			
            if ze is None:
                raise ZufallError('Argumente überprüfen')
				
        except ZufallError as e:
            print('zufall:', str(e))
            return

        return ZufallsExperiment.__new__(cls, *args, **kwargs)			
			
		
			
    def __str__(self):  
        txt1 = (', mit' if self.wiederh else ', ohne') + ' Wiederholung '
        txt2 = (', mit' if self.anordn else ', ohne') + ' Anordnung)'
        return "GluecksRad"	+ "(Stufen=" + str(self.stufen) + txt1 + txt2
		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        gluecksrad_hilfe(3)	
		
    h = hilfe					

	
Rad = GluecksRad
GR = GluecksRad


		
		
# Benutzerhilfe für GluecksRad
# ----------------------------

def gluecksrad_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
GlücksRad - Objekt

Kurzname     GR,  Rad
		 
Erzeugung    Rad( liste1 /[, liste2, ... ] /[, stufen ] )

                 liste    dict | dliste 
                 dict	  { obj:zahl, obj1:zahl1, ... }  (dictionary)
                 dliste	  [ [obj,zahl], [obj1,zahl1], ... ] oder
                    	  [ obj, obj1, ...] ], ist gleich 
                          [  [obj,1], [obj1,1], ... ]
                 obj      Bezeichner | ganze Zahl >= 0
                 stufen   Anzahl Stufen, > 1 bei mehrstufigem Experiment
				 
Zusatz   a=nein  keine Beachtung der Anordnung/Reihenfolge; Standard=ja
         f=funktions_name   Name einer ZG-Funktion (Element der Ergebnis-
                                                           menge -> Zahl)
		 
Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette ein-
gegeben oder vordeklariert werden, etwa Raucher = Symbol('Raucher')
		
Zuweisung     r = Rad(...)   (r - freier Bezeichner)

Beispiele 
Rad([a, b, c])	
GlücksRad( {r:3, g:4, b:2 }, 4)        	
Rad( {r:3, g:4, b:5 }, {r:2, g:3, b:4}, {r:1, g:2, b:3})		
Rad( [ [1, 3], [2, 4], [3, 2] ], 2) - ZufallsExperiment- und entsprech.
Rad( [ [1, 3], [2, 4], [3, 2] ], 2, f=summe) - ZufallsGröße-Objekt
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für GlücksRad
 
r.hilfe                Bezeichner der Eigenschaften und Methoden
r.anordn               Beachtung der Anordnung/Reihenfolge
r.ausfall              = r.versuch
r.baum                 Baumdiagramm
r.baum_(...)        M  ebenso; zugehörige Methode
r.n_omega              Größe der Ergebnismenge
r.omega                Ergebnismenge
r.omega_(...)       M  ebenso; zugehörige Methode
r.P(...)            M  Wahrscheinlichkeit eines Ereignisses
r.relh2p(...)       M  Stabilisierung der relativen Häufigkeiten
r.stich_probe(...)  M  Stichprobe
r.stufen               Stufenanzahl des Experimentes
r.versuch              Versuch
r.vert                 Wahrscheinlichkeitsverteilung
r.vert_(...)        M  ebenso; zugehörige Methode
r.wurf                 = r.versuch

Synonyme Bezeichner

hilfe         h
baum_         Baum
n_omega       nOmega
omega_        Omega
stich_probe   stichProbe
vert_         Vert
	   """)		
        return
	
	
