#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  Urne - Klasse  von zufall           
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



from sympy.core.numbers import Integer
from sympy.core.symbol import Symbol
from sympy import sympify, sqrt, nsimplify
from sympy.functions.combinatorial.factorials import binomial as B

from zufall.lib.objekte.zufalls_experiment import ZufallsExperiment 
from zufall.lib.funktionen.funktionen import anzahl_treffer
	
from zufall.lib.objekte.ausnahmen import ZufallError

import zufall



# Urne - Klasse  
# -------------
	
class Urne(ZufallsExperiment):                                      
    """
	
Urne
	
**Erzeugung** 

   Urne( *liste | dict /[, stufen]* )  
	
      *dict* : *{ obj1:zahl1, obj2:zahl2, ...}*
	  
      *liste* : 
	  
        | *[ (obj, zahl1), (obj2, zahl2), ...]* 
		
         *oder*
		  
        | *[ [obj1, zahl1], [obj2, zahl12, ...]* 
		
         *oder*
		 
        | *[ obj1, obj2, ...]* = *[ [obj1, 1], [obj2, 1], ...]*
		 
        | (*obj-zahl*-Paare als Tupel oder Liste)
		 
      *obj* : Bezeichner | ganze Zahl >= 0
	  
      *stufen* : Anzahl Stufen; Standard=1
				 
**Zusatz**
   `a=nein` - keine Beachtung der Anordnung/Reihenfolge; Standard=ja
   
   `w=nein` - keine Wiederholung von Elementen; Standard=ja
   
   `f=funktions_name` - Name einer ZG-Funktion (diese ordnet den Elementen 
   der Ergebnismenge Zahlen zu)
		 
Wird eine Liste mit nur zwei unterschiedlichen Objekten angegeben, wird 
bei Verwendung der Funktion ``anzahl_treffer``
 
   bei Wiederholung von Elementen ein BernoulliKette - Objekt
   
   bei Nicht-Wiederholung von Elementen ein HyperGeometrischeVerteilung -
   Objekt
   
erzeugt

Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette 
eingegeben oder vordeklariert werden, etwa ``Raucher = Symbol('Raucher'``)

    """
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            urne_hilfe(kwargs["h"])	 
            return
			
        try:			
            if len(args) == 1:
                args = args[0], 1			
            if len(args) != 2:
                raise ZufallError('ein oder zwei Argumente angeben')
            if not isinstance(args[0], (list, dict)) and isinstance(args[1], (int, Integer)):
                raise ZufallError('Liste/dict und Anzahl Stufen angeben')
            if isinstance(args[0], list):				
                def list_kontrolle(liste):
                    if all([isinstance(x, (Symbol, str, int, Integer)) for x in liste]):
                        return True
                    if all([isinstance(x, (list, tuple)) and len(x) == 2 for x in liste]):
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
            ze = ZufallsExperiment(*args, w=kwargs.get('w'), a=kwargs.get('a'))
			
            if ze is None:
                raise ZufallError('Argumente überprüfen')
				
        except ZufallError as e:
            print('zufall:', str(e))
            return

        return ZufallsExperiment.__new__(cls, *args, **kwargs)			
					
			
    def __str__(self):  
        txt1 = (', mit' if self.wiederh else ', ohne') + ' Wiederholung '
        txt2 = (', mit' if self.anordn else ', ohne') + ' Anordnung)'
        return "Urne"	+ "(Stufen=" + str(self.stufen) + txt1 + txt2
				
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        urne_hilfe(3)	
		
    h = hilfe					
		
		
# Benutzerhilfe für Urne
# ----------------------

def urne_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
Urne - Objekt

Erzeugung    Urne( liste | dict /[, stufen ] )

                 dict    { obj1:zahl1, obj2:zahl2, ...}
                 liste   [ [obj, zahl], [obj1, zahl1], ...] oder
                    	 [ obj1, obj2, ...] = [ [obj1, 1], [obj2, 1], ...]
                 obj     Bezeichner | ganze Zahl >= 0
                 stufen  Anzahl Stufen; Standard=1 
				 
Zusatz   a=nein  keine Beachtung der Anordnung/Reihenfolge; Standard=ja
         w=nein  keine Wiederholung von Elementen; Standard=ja
         f=funktions_name   Name einer ZG-Funktion (Element der Ergebnis-
                                                    menge -> Zahl)
		 
Wird eine Liste mit nur zwei unterschiedlichen Objekten angegeben, wird 
bei Verwendung der Funktion anzahl_treffer
 
   bei Wiederholung von Elementen ein BernoulliKette-Objekt
   
   bei Nicht-Wiederholung von Elementen ein HyperGeometrischeVerteilung-
                                            Objekt
   
erzeugt

Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette ein-
gegeben oder vordeklariert werden, etwa  Raucher = Symbol('Raucher')
		
Zuweisung     u = Urne(...)   (u - freier Bezeichner)

Beispiele
Urne([a, b, c])  ( = Urne( {a:1, b:1, c:1} ) )
Urne( {'rot':3, 'grün':4, 'blau':2 }, 2)		
Urne( {r:3, g:4, b:2 }, 4, a=nein)		
Urne( {r:3, g:4 }, 4, f=anzahl_treffer)    - BernoulliKette-Objekt		
Urne( [ [r,3], [g,4] ], 4, w=nein, f=anzahl_treffer)
                              - HyperGeometrischeVerteilung-Objekt		
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Urne (ZufallsExperiment-Objekt)
 
u.hilfe                Bezeichner der Eigenschaften und Methoden
u.anordn               Beachtung der Anordnung/Reihenfolge
u.ausfall              = u.versuch
u.baum                 Baumdiagramm
u.baum_(...)        M  ebenso; zugehörige Methode
u.n_omega              Größe der Ergebnismenge
u.omega                Ergebnismenge
u.omega_(...)       M  ebenso; zugehörige Methode
u.P(...)            M  Wahrscheinlichkeit eines Ereignisses
u.relh2p(...)       M  Stabilisierung der relativen Häufigkeiten
u.stich_probe(...)  M  Stichprobe
u.stufen               Stufenanzahl des Experimentes
u.versuch              Versuch
u.vert                 Wahrscheinlichkeitsverteilung
u.vert_(...)        M  ebenso; zugehörige Methode
u.wiederh              Wiederholung von Elementen
u.ziehen               = u.versuch

Synonyme Bezeichner

hilfe        h
baum_        Baum
n_omega      nOmega
omega_       Omega
stich_probe  stichProbe
vert_        Vert

Bei der Erzeugung eines BernoulliKette- oder HyperGeometrischeVerteilung-
Objektes siehe entsprechende Hilfeseite		
	   """)		
        return
	
	
