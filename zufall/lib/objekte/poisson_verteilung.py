#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  PoissonVerteilung - Klasse  von zufall           
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

from sympy.core.numbers import Integer, Rational, Float   
from sympy.core.symbol import Symbol
from sympy import sympify
from sympy import factorial, exp, N
from sympy.printing.latex import latex

from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse

from zufall.lib.objekte.ausnahmen import ZufallError
	
	

# PoissonVerteilung - Klasse  
# --------------------------
#
# erbt von ZufallsGroesse
#

	
class PoissonVerteilung(ZufallsGroesse):                                      
    """

Poissonverteilung

**Kurzname** **PV**
	
**Erzeugung** 
	
   PV( *a* )

**Parameter**
 
   *a* : Parameter der Verteilung (Zahl > 0)
			
    """	
		
    # interne args: Verteilung, parameter = ( a )
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            poisson_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 1:
                raise ZufallError("ein Argument angeben")
            a = args[0]
            a = sympify(a)
            if not (isinstance(a, (int, Integer, Rational, float, Float))):
                raise ZufallError("das Argument muß dine Zahl sein")
            if a <= 0:
                raise ZufallError("der Parameter muß > 0 sein")

            vert, k, sum = [], 0, 0
            while True:
                pk = N(a**k * exp(-a) / factorial(k))
                sum += pk
                if sum > 1 - 1e-12:
                    break
                vert += [[k, pk]]
                k += 1
            print('\nDie Verteilung wurde auf die Werte aus dem Intervall [0, ' + str(k-1) + '] eingeschränkt')				
            print('Die Summe der Wahrscheinlichkeiten aller restlichen Werte ist < 10^-12\n')				
            vert = dict(vert)
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsGroesse.__new__(cls, vert, parameter=(a), kontrolle=False)

			
    def __str__(self):  
        a = self.args[1]
        return "PoissonVerteilung(" + str(a) + ")"	

		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def lamda(self):
        """Parameter"""	
        return self.args[1]

    par = lamda		

    @property
    def erw(self):
        """Erwartungswert"""	
        a = self.args[1]	
        return a

    @property
    def var(self):
        """Varianz"""	
        a = self.args[1]	
        return a
			
    @property	
    def formeln(self):
        """Formeln"""
        print(' ')		
        g = self.n_omega
        k = Symbol('k')		
        display(Math('\mathrm{Ergebnismenge}  \\qquad\\qquad\;\;\;\,\, \\Omega = \{0,\; 1,\; 2,\;...\}, \;\;\; ' + \
               '\mathrm{eingeschränkt\;auf}\;\; \\{0,\;1,\;...,\;' + latex(g-1) + '\}'))
        display(Math('\mathrm{Wahrscheinlichkeiten} \\qquad\:\:\:\, P(X=k) = \\frac{\\lambda ^k\,' + \
               latex(exp(-k)) + '}{k\,!}, \;\;\;\, k \\in \\Omega'))
        display(Math('\mathrm{Erwartungswert} \\qquad\\qquad\,\:\; \\lambda'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad\\qquad\\quad\;\; \\lambda'))	
        display(Math('\\lambda \mathrm{- Parameter\;der\;Verteilung} \\qquad \mathrm{aktuell} \;\;\;\\lambda = ' + \
           latex(self.lamda)))	
        print(' ')		
  
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        poisson_verteilung_hilfe(3)	
		
    h = hilfe					
  
		
				
# Benutzerhilfe für PoissonVerteilung
# -----------------------------------

def poisson_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
PoissonVerteilung - Objekt

Kurzname     PV
		
Erzeugung    PoissonVerteilung( a )

                 a    Parameter der Verteilung
				 
Zuweisung     pv = PV(...)   (pv - freier Bezeichner)

Beispiel
PV( 2 )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für PoissonVerteilung
 
pv.hilfe                Bezeichner der Eigenschaften und Methoden
pv.erw                  Erwartungswert	
pv.erw(...)          M  ebenso, zugehörige Methode	
pv.F(...)            M  Verteilungsfunktion
pv.formeln              Formeln
pv.graf_F               Graf der Verteilungsfunktion
pv.hist                 Histogramm
pv.hist_(...)        M  ebenso, zugehörige Methode
pv.hist_kum             ebenso, kumulierte Wahrscheinlichkeiten
pv.lamda                = pv.par; Schreibweise! 
pv.n_omega              Größe der Ergebnismenge 
pv.omega                Ergebnismenge 
pv.par                  Parameter der Verteilung 
pv.P(...)            M  Wahrscheinlichkeit eines Ereignisses
pv.poly_zug             Polygonzug-Diagramm der Wahrscheinlichkeiten
pv.poly_zug_(...)    M  ebenso, zugehörige Methode
pv.quantil(...)      M  Quantile
pv.relh2p            M  Stabilisierung der relativen Häufigkeiten        
pv.sigma                Standardabweichung
pv.sigma_(...)       M  ebenso, zugehörige Methode
pv.stich_probe(...)  M  Stichprobe		
pv.var                  Varianz		
pv.var_(...)         M  ebenso, zugehörige Methode		
pv.versuch              Versuch		
pv.vert                 Wahrscheinlichkeitsverteilung		
pv.vert_(...)        M  ebenso, zugehörige Methode		
pv.vert_kum             kumulierte Wahrscheinlichkeitsverteilung
pv.vert_kum_(...)    M  ebenso, zugehörige Methode	

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
	
	
PV = PoissonVerteilung
		
		


