#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  Wuerfel - Klasse  von zufall           
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



from sympy.core.numbers import Integer, Rational
from sympy import Add
from zufall.lib.objekte.zufalls_experiment import ZufallsExperiment 
from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse 
from zufall.lib.funktionen.funktionen import summe
	
from zufall.lib.objekte.ausnahmen import ZufallError



# Würfel - Klasse  
# ---------------
	
class Wuerfel(ZufallsGroesse):                                      
    """
	
Würfel
	
**Erzeugung** 

   Würfel( */[ anzahl] )* ) 

**Parameter**
   	
   *anzahl* :  Anzahl der Würfe bzw. der Würfel; Standard=1		
   
Erzeugung eines Würfel-ZufallsGröße-Objektes; zugehörige Zufallsgröße 
ist "Augensumme"
   
**Zusatz**
   `ze=ja` - Erzeugung eines ZufallsExperiment-Objektes
   
   `flächen=n` - Anzahl der Flächen des Würfels (2, 3, ...); jeder 
   Fläche mit der Nummer 1, 2, ..., *n* ist ihre Nummer als Augenzahl 
   zugeordnet; Standard=6
		 
Bei der Erzeugung eines ZufallsExperiment-Objektes siehe entsprechende
Seite
		 
    """			
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            wuerfel_hilfe(kwargs["h"])		
            return
			
        try:			
            anzahl = 1	
            if len(args) == 1:
                if not (isinstance(args[0], (int, Integer)) and args[0] > 0):
                    raise ZufallError('Anzahl Würfe als ganze Zahl > 0 angeben')
                anzahl = args[0]
            else:		
                if len(args) > 0:			
                    raise ZufallError('kein oder ein Argument angeben')
            flaechen = 6			
            if kwargs.get('flaechen'):
                flaechen = kwargs.get('flaechen')
                if not isinstance(flaechen, (int, Integer)):			
                    raise ZufallError('Anzahl Flächen als ganze Zahl > 1 angeben')
                if flaechen < 2:				
                    raise ZufallError('Anzahl Flächen als ganze Zahl > 1 angeben')
        except ZufallError as e:
            print('zufall:', str(e))
            return

        if not kwargs.get('ze'):
            if kwargs.get('info') is None:		
                print("Erzeugung eines ZufallsGröße-Objektes 'AugenSumme'")
            n, f = anzahl, flaechen
			
            # es wird ein spezieller Algorithmus zur Berechnung der 
            # Verteilung implementiert		
            if n == 1:				
                vv = dict([[i, 1] for i in range(1, f+1)])
            else:				
                L = [[i, 1] for i in range(1, f+1)]			               		   
                w2 = ZufallsExperiment(L, 2, f=summe, info=False)	
                vv = w2.vert
                for k in vv:
                    vv[k] = vv[k] * f**2   
                leiste = f * [0] + [vv[k] for k in vv] + f * [0]
                for i in range(3, n+1):    
                    m = i*f-i + 1
                    L, v = [], 0
                    for k in range(i, m+i):
                        L += [[k, *leiste[-(f+1)-v : -(f+1)-v+f]]]
                        v += 1 
                    vv = dict()    
                    for ll in L:
                        vv[ll[0]] = Add(*ll[1:])    
                    leiste = f * [0] + [vv[k] for k in vv] + f * [0]
            for k in vv:
                vv[k] = Rational(vv[k], f**n)		
            return ZufallsGroesse.__new__(cls, vv, parameter=(anzahl, 
                       flaechen), kontrolle=False)		
        else:		
            print('Erzeugung eines ZufallsExperiment-Objektes ')
            di = dict([[i, 1] for i in range(1, flaechen+1)])
            return ZufallsExperiment(di, anzahl) 			
					
			
    def __str__(self):  
        return "Würfel" + "(Anzahl=" + str(self.anzahl) + ", Flächen=" + \
              str(self.flaechen)  + ")"
	
    @property		
    def anzahl(self):
        """Anzahl Würfel / Würfe"""	
        return self.args[1][0]

    @property		
    def flaechen(self):
        """Anzahl Flächen"""	
        return self.args[1][1]
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        wuerfel_hilfe(3)	
		
    h = hilfe					
		
		
		
# Benutzerhilfe für Wuerfel
# ------------------------

def wuerfel_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
Würfel - Objekt

Erzeugung    Würfel( /[ anzahl ] )

                 Erzeugung eines Würfel-ZufallsGröße-Objektes
                 zugehörige Zufallsgröße ist "Augensumme"
				 				 
                 anzahl    Anzahl der Würfe bzw. der Würfel; Standard=1
				 
Zusatz   ze=ja   Erzeugung eines ZufallsExperiment-Objektes   
         flächen=Anzahl der Flächen des Würfels (2, 3, ...); jeder 
         Fläche mit der Nummer 1, 2, ..., *n* ist ihre Nummer als Augenzahl 
         zugeordnet; Standard n=6
		 
Zuweisung     w = Würfel(...)   (w - freier Bezeichner)

Beispiele
Würfel( )     
Würfel( 12 )		
Würfel( 25, flächen=4 )		
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Würfel (ZufallsGröße-Objekt)
 
w.hilfe                Bezeichner der Eigenschaften und Methoden 
w.anzahl               Anzahl der Würfe / Würfel	
w.erw                  Erwartungswert	
w.erw_(...)            ebenso, zugehörige Methode	
w.flächen              Anzahl der Flächen	
w.F(...)            M  Verteilungsfunktion
w.graf_F               Graf der Verteilungsfunktion
w.hist                 Histogramm
w.hist_(...)        M  ebenso, zugehörige Methode
w.hist_kum             ebenso, kumulierte Wahrscheinlichkeiten
w.n_omega              Größe der Ergebnismenge 
w.omega                Ergebnismenge 
w.P(...)            M  Wahrscheinlichkeit eines Ereignisses
w.poly_zug             Polygonzug-Diagramm der Wahrscheinlichkeiten
w.poly_zug_(...)    M  ebenso, zugehörige Methode
w.quantil(...)      M  Quantile
w.relh2p(...)       M  Stabilisierung der relativen Häufigkeiten        
w.sigma                Standardabweichung
w.sigma_(...)       M  ebenso, zugehörige Methode	
w.stich_probe(...)  M  Stichprobe		
w.var                  Varianz		
w.var_(...)         M  ebenso, zugehörige Methode		
w.versuch              Versuch		
w.vert                 Wahrscheinlichkeitsverteilung		
w.vert_(...)        M  ebenso, zugehörige Methode		
w.vert_kum             kumulierte Wahrscheinlichkeitsverteilung
w.vert_kum_(...)    M  ebenso, zugehörige Methode
		
Synonyme Bezeichner

hilfe        h        
erw_         Erw	
graf_F       grafF
hist_        Hist
hist_kum     histKum
n_omega      nOmega
poly_zug     polyZug
poly_zug_    PolyZug
sigma_       Sigma
stich_probe  stichProbe
var_         Var
vert_        Vert
vert_kum     vertKum
vert_kum_    VertKum

Bei der Erzeugung eines ZufallsExperiment-Objektes siehe entsprechende
Hilfeseite		
	   """)		
        return	
	
