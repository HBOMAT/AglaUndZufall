#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  GeometrischeVerteilung - Klasse  von zufall           
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

from sympy.core.numbers import Rational, Float   
from sympy.core.symbol import Symbol
from sympy import sympify, nsimplify, Pow
from sympy.printing.latex import latex

from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse

from zufall.lib.objekte.ausnahmen import ZufallError
	
	

# GeometrischeVerteilung - Klasse  
# -------------------------------
#
# erbt von ZufallsGroesse
#

	
class GeometrischeVerteilung(ZufallsGroesse):                                      
    """
	
Geometrische Verteilung

**Kurzname**     **GV**
		
**Erzeugung**

   GV( *p* )

**Parameter**

   *p* : Trefferwahrscheinlichkeit (Zahl aus [0, 1])
		
    """
		
    # interne args: Verteilung, parameter = ( a )
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            geometrische_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 1:
                raise ZufallError("ein Argument angeben")
            p = args[0]
            p = sympify(p)
            if not isinstance(p, (float, Float, Rational)):
                raise ZufallError("die Trefferwahrscheinlichkeit muß eine Zahl sein")
            if not (0 <= p <= 1):
                raise ZufallError("die Trefferwahrscheinlichkeit muß in [0,1] liegen") 
            p = nsimplify(p)
            vert, k, sum = [], 1, 0
            while True:
                pk = p * Pow(1-p, k-1)
                sum += pk
                if sum > 1 - 1e-12:
                    break
                vert += [[k, pk]]
                k += 1
            print('\nDie Verteilung wurde auf die Werte aus dem Intervall [1, ' + str(k-1) + '] eingeschränkt')				
            print('Die Summe der Wahrscheinlichkeiten aller restlichen Werte ist < 10^-12\n')				
            vert = dict(vert)
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsGroesse.__new__(cls, vert, parameter=(p), kontrolle=False)

			
    def __str__(self):  
        a = self.args[1]
        return "GeometrischeVerteilung(" + str(a) + ")"	
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def p(self):
        """Trefferwahrscheinlichkeit"""	
        return self.args[1]

    @property
    def erw(self):
        """Erwartungswert"""	
        p = self.p	
        return nsimplify(1 / p)

    @property
    def var(self):
        """Varianz"""	
        p = self.p	
        return nsimplify((1-p) / p**2)
			
    @property	
    def formeln(self):
        """Formeln"""
        print(' ')		
        g = self.n_omega
        p, k = Symbol('p'), Symbol('k')		
        display(Math('\mathrm{Ergebnismenge} \\qquad\\qquad\;\;\;\,\, \\Omega = \{1,\; 2,\; 3,\;...\}, \;\; ' + \
               '\mathrm{eingeschränkt\;auf}\;\; \{1,...,' + latex(g) + '\}'))
        display(Math('\mathrm{Wahrscheinlichkeiten} \\qquad\:\:\:\: P(X=k) = \\frac{1}{p}, \;\;\; k \\in \\Omega' ))
        display(Math('\mathrm{Erwartungswert} \\qquad\\qquad\,\,\:\: \\frac{1}{p}'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad\\qquad\\quad\;\; \\frac{1-p}{p^2}'))	
        display(Math('p \,\mathrm{- Trefferwahrscheinlichkeit, \\quad aktuell} \;\;\; p = ' + latex(self.p)))	
        print(' ')		
        
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        geometrische_verteilung_hilfe(3)	
		
    h = hilfe					
		
				
# Benutzerhilfe für GeometrischeVerteilung
# ----------------------------------------

def geometrische_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
GeometrischeVerteilung - Objekt

Kurzname     GV
		
Erzeugung    GeometrischeVerteilung( p )

                 p    Trefferwahrscheinlichkeit (Zahl aus [0, 1])
				 
Zuweisung     gv = GV(...)   (gv - freier Bezeichner)

Beispiel
GV( 1/2 )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für GeometrischeVerteilung
 
gv.hilfe               Bezeichner der Eigenschaften und Methoden
gv.erw                 Erwartungswert	
gv.erw(...)         M  ebenso, zugehörige Methode	
gv.F(...)           M  Verteilungsfunktion
gv.formeln             Formeln
gv.graf_F              Graf der Verteilungsfunktion
gv.hist                Histogramm
gv.hist_(...)       M  ebenso, zugehörige Methode
gv.hist_kum            ebenso, kumulierte Wahrscheinlichkeiten
gv.n_omega             Größe der Ergebnismenge 
gv.omega               Ergebnismenge 
gv.p                   Trefferwahrscheinlichkeit 
gv.P(...)           M  Wahrscheinlichkeit eines Ereignisses
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
		
	
GV = GeometrischeVerteilung
		
		


