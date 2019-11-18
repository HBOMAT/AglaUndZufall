#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  Muenze - Klasse  von zufall           
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



import importlib

from IPython.display import display, Math

from sympy.core.numbers import Integer, Rational
from sympy.core.symbol import Symbol
from sympy.core.compatibility import iterable

from zufall.lib.objekte.zufalls_experiment import ZufallsExperiment 
	
from zufall.lib.objekte.ausnahmen import ZufallError

bk = importlib.import_module('zufall.lib.objekte.bernoulli_kette')
BernoulliKette = bk.BernoulliKette



# Muenze - Klasse  
# ---------------
	
class Muenze(BernoulliKette):                                      
    """

Münze
	
**Erzeugung** 
	
   Münze( /[ *anzahl* ] )
	 
**Parameter**

   *anzahl* : Anzahl der Würfe bzw. der Münzen; Standard=1
   
Erzeugung eines BernoulliKette-Objektes; zugehörige Zufallsgröße ist 
"Anzahl Treffer"

**Zusatz**
   `ze=ja` - Erzeugung eines ZufallsExperiment-Objektes
   
   `tn=[treffer, niete]` -Bezeichner für Treffer/Niete; Standard=[1, 0]

   Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette 
   eingegeben oder vordeklariert werden, etwa  
   ``Raucher = Symbol('Raucher')``
					
    """			
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            muenze_hilfe(kwargs["h"])		
            return
			
        try:			
            anzahl = 1		
            treffer, niete = Symbol(str(1)), Symbol(str(0))
            if len(args) == 1:
                if not (isinstance(args[0], (int, Integer)) and args[0] > 0):
                    raise ZufallError('Anzahl Würfe/Münzen als ganze Zahl > 0 angeben')
                anzahl = args[0]
            else:		
                if len(args) > 0:			
                    raise ZufallError('kein oder ein Argument angeben')
            tn = kwargs.get('tn')			
            if tn:
                if not iterable(tn) and len(tn) == 2:				
                    raise ZufallError('Liste mit Treffer/Niete angeben')
                treffer, niete = tn
                if isinstance(treffer, (str, int, Integer)):
                    treffer = Symbol(str(treffer))				
                if isinstance(niete, (str, int, Integer)):
                    niete = Symbol(str(niete))
                if not isinstance(treffer, Symbol) and isinstance(niete, Symbol):				
                    raise ZufallError('gültige Bezeichner für Treffer/Niete angeben')	
        except ZufallError as e:
            print('zufall:', str(e))
            return

        if not kwargs.get('ze'):
            print('Erzeugung eines Münze-BernoulliKette-Objektes')
            return BernoulliKette(anzahl, Rational(1, 2), tn=[treffer, niete], info=False)				
        else:		
            print('Erzeugung eines Münze-ZufallsExperiment-Objektes')
            return BernoulliKette(anzahl, Rational(1, 2), tn=[treffer, niete], ze=True, info=False) 			
					
			
    def __str__(self):  
        return "Münze" + "(Anzahl=" + str(self.stufen) + ", Treffer=" + str(self.treffer) + ")"
		
    @property		
    def anzahl(self):  
        """Anzahl Münzen / Würfe"""	
        return	 self.args[1][0]
		
    @property		
    def treffer(self):  
        """Treffer"""	
        return	 self.args[1][2]
		
    @property		
    def niete(self):  
        """Niete"""	
        return	 self.args[1][3]
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        muenze_hilfe(3)	
		
    h = hilfe					

	
		
# Benutzerhilfe für Muenze
# ------------------------

def muenze_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
Münze - Objekt

Erzeugung    Münze( /[ anzahl ] )

                 Erzeugung eines BernoulliKette-Objektes
                 zugehörige Zufallsgröße ist 'Anzahl Treffer'
				 
                 anzahl  Anzahl der Würfe bzw. der Münzen; Standard=1
				 
Zusatz   ze=ja   Erzeugung eines ZufallsExperiment-Objektes  
         tn=[treffer, niete]   Bezeichner für Treffer/Niete; Standard=[1,0]
         Bezeichner, die länger als ein Zeichen sind, müssen als Zei-
         chenkette eingegeben oder vordeklariert werden, etwa 
         Wappen = Symbol('Wappen')
		 
Zuweisung     m = Münze(...)   (m - freier Bezeichner)

Beispiele
Münze( )     
Münze( 50, tn=[W, Z] )		
Münze( 5, ze=ja, tn=['Wappen', 'Zahl'] )		
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Münze (BernoulliKette-Objekt)
 
m.hilfe               Bezeichner der Eigenschaften und Methoden 
m.anzahl              Anzahl der Würfe / Münzen
m.erw                 Erwartungswert	
m.erw_(...)           ebenso, zugehörige Methode	
m.e_sigma_umg         Sigma-Umgebungen des Erwartungswertes		
m.F(...)           M  Verteilungsfunktion
m.faust_regel         Faustregeln
m.graf_F              Graf der Verteilungsfunktion
m.hist                Histogramm
m.hist_(...)       M  ebenso, zugehörige Methode
m.hist_kum            ebenso, kumulierte Wahrscheinlichkeiten
m.niete               Niete
m.n_omega             Größe der Ergebnismenge 
m.omega               Ergebnismenge 
m.P(...)           M  Wahrscheinlichkeit eines Ereignisses
m.poly_zug            Polygonzug-Diagramm der Wahrscheinlichkeiten
m.poly_zug_(...)   M  ebenso, zugehörige Methode
m.p_sigma_umg         Sigma-Umgebungen der Wahrscheinlichkeit
m.quantil(...)     M  Quantile
m.relh2p           M  Stabilisierung der relativen Häufigkeiten        
m.sigma               Standardabweichung
m.sigma_(...)      M  ebenso, zugehörige Methode	
m.stich_probe(...) M  Stichprobe		
m.treffer             Treffer
m.var                 Varianz		
m.var_(...)        M  ebenso, zugehörige Methode		
m.versuch             Versuch		
m.vert                Wahrscheinlichkeitsverteilung		
m.vert_(...)       M  ebenso, zugehörige Methode		
m.vert_kum            kumulierte Wahrscheinlichkeitsverteilung
m.vert_kum_(...)   M  ebenso, zugehörige Methode
		
Synonyme Bezeichner

hilfe         h
erw_          Erw
e_sigma_umg   eSigmaUmg
faust_regel   faustRegel
graf_F        grafF
hist_         Hist
hist_kum      histKum
n_omega       nOmega
poly_zug      polyZug
poly_zug_     PolyZug
p_sigma_umg   pSigmaUmg
sigma_        Sigma
stich_probe   stichProbe
var_          Var
vert_         Vert
vert_kum      vertKum
vert_kum_     VertKum
		
Bei der Erzeugung eines ZufallsExperiment-Objektes siehe entsprechende
Hilfeseite		
	   """)		
        return	
	
