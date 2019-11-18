#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  GleichVerteilung - Klasse  von zufall           
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



from IPython.display import display, Math

from sympy.core.numbers import Integer, Rational
from sympy.core.symbol import Symbol
from sympy import sympify, nsimplify
from sympy.printing.latex import latex

from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse

from zufall.lib.objekte.ausnahmen import ZufallError
	
	

# GleichVerteilung - Klasse  
# -------------------------------
#
# erbt von ZufallsGroesse
#

	
class GleichVerteilung(ZufallsGroesse): 
    """
	
Gleichverteilung

**Kurzname**     **GLV**
		
**Erzeugung**

   GLV( *n* )

**Parameter**

   *n* :    Anzahl Werte
				 
   Es wird eine Gleichverteilung auf {*1, 2, ..., n* } erzeugt
		
    """
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            gleich_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 1:
                raise ZufallError("ein Argument angeben")
            n = args[0]
            n = sympify(n)
            if not isinstance(n, (int, Integer)):
                raise ZufallError("die Anzahl Werte muß eine ganze Zahl sein")
            if not n > 0:
                raise ZufallError("die Anzahl Werte muß in > 0 sein") 
            vert = []
            for k in range(1, n+1):
                pk = Rational(1, n)
                vert += [[k, pk]]
                k += 1
            vert = dict(vert)
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsGroesse.__new__(cls, vert, parameter=(n), kontrolle=False)

			
    def __str__(self):  
        n = self.args[1]
        return "GleichVerteilung(" + str(n) + ")"	

		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def n(self):
        """Anzahl Werte"""	
        return self.args[1]

    par = n		
		
    @property
    def erw(self):
        """Erwartungswert"""	
        n = self.n	
        return nsimplify((n+1) / 2)

    @property
    def var(self):
        """Varianz"""	
        n = self.n	
        return nsimplify((n**2-1) / 12)
			
    @property	
    def formeln(self):
        """Formeln"""
        print(' ')		
        n = Symbol('n')		
        display(Math('\mathrm{Ergebnismenge} \\qquad\\qquad\;\;\;\,\,\\, \\Omega = \{1,\; 2,\; 3,\;...,\; n\}' ))
        display(Math('\mathrm{Wahrscheinlichkeiten} \\qquad\quad P(X=k) = \\frac{1}{n}, \;\;\; k \\in \\Omega' ))
        display(Math('\mathrm{Erwartungswert} \\qquad\\qquad\,\,\,\;  \\frac{n+1}{2}'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad\\qquad\\quad\;\;\; \\frac{n^2-1}{12}'))	
        display(Math('n\,\mathrm{ -\, Anzahl\;Werte, \\quad aktuell}\; n = ' + latex(self.n)))	
        print(' ')		
        
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        gleich_verteilung_hilfe(3)	
		
    h = hilfe					
		
				
# Benutzerhilfe für GleichVerteilung
# ----------------------------------

def gleich_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
GleichVerteilung - Objekt

Kurzname     GLV
		
Erzeugung    GleichVerteilung( n )

                 n    Anzahl Werte
				 
Es wird eine Gleichverteilung auf {1, 2, ..., n} erzeugt
		
Zuweisung     gv = GLV(...)   (gv - freier Bezeichner)

Beispiel
GLV( 12 )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für GleichVerteilung
 
gv.hilfe               Bezeichner der Eigenschaften und Methoden
gv.erw                 Erwartungswert	
gv.erw(...)         M  ebenso, zugehörige Methode	
gv.F(...)           M  Verteilungsfunktion
gv.formeln             Formeln
gv.graf_F              Graf der Verteilungsfunktion
gv.hist                Histogramm
gv.hist_(...)       M  ebenso, zugehörige Methode
gv.hist_kum            ebenso, kumulierte Wahrscheinlichkeiten
gv.n                   Anzahl Werte
gv.n_omega             Größe der Ergebnismenge 
gv.omega               Ergebnismenge 
gv.P(...)           M  Wahrscheinlichkeit eines Ereignisses
gv.par                 Parameter ( = gv.n)
gv.poly_zug            Polygonzug-Diagramm der Wahrscheinlichkeiten
gv.poly_zug_(...)   M  ebenso, zugehörige Methode
gv.quantil(...)     M  Quantile
gv.relh2p           M  Stabilisierung der relativen Häufigkeiten        
gv.sigma               Standardabweichung
gv.sigma_(...)      M  ebenso, zugehörige Methode
gv.stich_probe(...) M  Stichprobe		
gv.var                 Varianz		
gv.var_(...)        M  ebenso, zugehörige Methode		
gv.versuch             Versuch		
gv.vert                Wahrscheinlichkeitsverteilung		
gv.vert_(...)       M  ebenso, zugehörige Methode		
gv.vert_kum            kumulierte Wahrscheinlichkeitsverteilung
gv.vert_kum_(...)   M  ebenso, zugehörige Methode	

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
	   """)		
        return
		
	
GLV = GleichVerteilung
		
		


