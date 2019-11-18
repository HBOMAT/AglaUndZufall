#!/usr/bin/python
# -*- coding: utf-8 -*-


#              
                        
#  HyperGeometrischeVerteilung - Klasse  von zufall           
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
from sympy import sympify
from sympy.functions.combinatorial.factorials import binomial
from sympy.printing.latex import latex

from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse
from zufall.lib.objekte.ausnahmen import ZufallError
	
	

# HyperGeometrischeVerteilung - Klasse  
# ---------------------------
#
# erbt von ZufallsGroesse
#
	
class HyperGeometrischeVerteilung(ZufallsGroesse):                                      
    """

Hypergeometrische Verteilung

**Kurzname** **HGV**
	
**Erzeugung** 
	
   HGV( *N*, *M*, *n* )

**Parameter**
 
   *N* : Größe der Population 
				 
   *M* : Größe der Treffermenge
   
   *n* : Anzahl Versuche   
	  
    """
		
    # interne args: Verteilung, parameter = ( N - Größe der Population
    #                                         M - Größe der Treffermenge	
    #                                         n - Anzahl Versuche )
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            hyper_geometrische_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 3:
                raise ZufallError("drei Argumente angeben")
            N, M, n = args
            N, M, n = sympify(N), sympify(M), sympify(n)
            if not (isinstance(N, (int, Integer)) and isinstance(M, (int, Integer)) \
               and isinstance(n, (int, Integer))):
                raise ZufallError("die Argumente müssen ganze Zahlen sein")
            if N < 1 or M < 1 or n < 1:
                raise ZufallError("die Angben müssen > 0 sein")
            if M > N:
                raise ZufallError("2. Argument muss <= 1. Argument seinn")
            if n > N:
                raise ZufallError("3. Argument muss <= 1. Argument seinn")
            vert = []
            for k in range(max(0, n-(N-M)), min(n,M)+1):
                vert += [[k, binomial(M, k) * Rational(binomial(N-M, n-k), binomial(N, n))]]				
            vert = dict(vert)
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsGroesse.__new__(cls, vert, parameter=(N, M, n), kontrolle=False)

			
    def __str__(self):  
        N, M, n = self.args[1]
        return "HyperGeometrischeVerteilung(" + str(N) + "," + str(M) + "," + str(n) + ")"	
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def N(self):
        """Größe der Popultion"""	
        return self.args[1][0]	

    @property
    def M(self):
        """Größe der Treffermenge"""	
        return Rational(self.args[1][1])	

    @property
    def n(self):
        """Anzahl Versuche"""	
        return Rational(self.args[1][2])			
		
    @property
    def erw(self):
        """Erwartungswert"""	
        N, M, n = self.args[1]	
        return Rational(M*n, N)			

    @property
    def var(self):
        """Varianz"""	
        N, M, n = self.args[1]	
        return Rational(M*n, N) * (1-Rational(M, N)) * Rational(N-n, N-1)
			
    @property	
    def formeln(self):
        """Formeln"""
        print(' ')	
        om = list(self.omega)		
        om.sort()
        a, b, n = om[0], om[1], om[-1]
        display(Math('\mathrm{Ergebnismenge} \\qquad\\qquad\;\;\;\,\, \\Omega = \{max(0,n-(N-M)),..., min(n, M)\},' + \
                  '\;\;\; hier \;\; \\Omega = \{' + latex(a) + ', ' + latex(b) + ', ...,' +latex(n) + '\}'))	
        display(Math('\mathrm{Wahrscheinlichkeiten} \\qquad\:\:\: P(X=k) = {M \choose k}\, \\frac{N-M ' + \
              '\choose n-k}{N \choose n}, \\quad k \in \\Omega'))	
        display(Math('\mathrm{Erwartungswert} \\qquad\\qquad\,\,\, \\frac{M\,n}{N}'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad\\qquad\\quad\; \\frac{M\,n}{N} \\left(1-\\frac{M}{N} \\right) \\frac{N-n}{N-1}'))	
        display(Math('N\mathrm{-Größe\;der\;Population,}\; M\mathrm{-Größe\;der\;Treffermenge},\;n \mathrm{- ' + \
              'Anzahl\; Versuche}'))
        display(Math('\mathrm{aktuell} \;\;\; N = ' + latex(self.N) + ',\;\;\; M =' + \
            latex(self.M) + ',\;\;\;n =' + latex(self.n)))	
        print(' ')		
        
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hyper_geometrische_verteilung_hilfe(3)	
		
    h = hilfe					
		
				
# Benutzerhilfe für HyperGeometrischeVerteilung
# ---------------------------------------------

def hyper_geometrische_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
HypergeometrischeVerteilung - Objekt

Kurzname     HGV
		
Erzeugung    HyperGeometrischeVerteilung( N, M, n )

                 N    Größe der Population
                 M    Größe der Treffermenge
                 n    Anzahl Versuche
				 
Zuweisung     hgv = HGV(...)   (hgv - freier Bezeichner)

Beispiel
HGV(20, 12, 5)
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für HyperGeometrischeVerteilung 

hgv.hilfe               Bezeichner der Eigenschaften und Methoden
hgv.erw                 Erwartungswert	
hgv.erw(...)         M  ebenso, zugehörige Methode	
hgv.F(...)           M  Verteilungsfunktion
hgv.formeln             Formeln
hgv.graf_F              Graf der Verteilungsfunktion
hgv.hist                Histogramm
hgv.hist_(...)       M  ebenso, zugehörige Methode
hgv.hist_kum            ebenso, kumulierte Wahrscheinlichkeiten
hgv.M                   Größe der Treffermenge
hgv.N                   Größe der Population
hgv.n                   Anzahl Versuche
hgv.n_omega             Größe der Ergebnismenge 
hgv.omega               Ergebnismenge 
hgv.P(...)           M  Wahrscheinlichkeit eines Ereignisses
hgv.poly_zug            Polygonzug-Diagramm der Wahrscheinlichkeiten
hgv.poly_zug_(...)   M  ebenso, zugehörige Methode
hgv.quantil(...)     M  Quantile
hgv.relh2p           M  Stabilisierung der relativen Häufigkeiten        
hgv.sigma               Standardabweichung
hgv.sigma_(...)      M  ebenso, zugehörige Methode
hgv.stich_probe(...) M  Stichprobe		
hgv.var                 Varianz		
hgv.var_(...)        M  ebenso, zugehörige Methode		
hgv.versuch             Versuch		
hgv.vert                Wahrscheinlichkeitsverteilung		
hgv.vert_(...)       M  ebenso, zugehörige Methode		
hgv.vert_kum            kumulierte Wahrscheinlichkeitsverteilung
hgv.vert_kum_(...)   M  ebenso, zugehörige Methode	

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
	
	
HGV = HyperGeometrischeVerteilung
		
		


