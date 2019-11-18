#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  BinomialVerteilung - Klasse  von zufall           
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

from sympy.core.numbers import Integer, Rational, Float
from sympy import Pow, N
from sympy import sympify, nsimplify
from sympy.functions.combinatorial.factorials import binomial
from sympy.printing.latex import latex

from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse

from zufall.lib.objekte.ausnahmen import ZufallError
	
import zufall	
	

# BinomialVerteilung - Klasse  
# ---------------------------
#

	
class BinomialVerteilung(ZufallsGroesse):                                      
    """
	
Binomialverteilung

**Kurzname** **BV**
	
**Erzeugung** 
	
   BV( *n*, *p* )

**Parameter**

   *n* : Anzahl Versuche
   
   *p* : TrefferWahrscheinlichkeit
							 				  	  
    """
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            binomial_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 2:
                raise ZufallError("zwei Argumente angeben")
            n, p = args
            n, p = sympify(n), sympify(p)
            if not isinstance(n, (int, Integer)):
                raise ZufallError("die Anzahl Versuche muß eine ganze Zahl sein")
            if n < 1:
                raise ZufallError("die Anzahl Versuche muß > 0 sein")
            if not isinstance(p, (float, Float, Rational)):
                raise ZufallError("die Trefferwahrscheinlichkeit muß eine Zahl sein")
            if not (0 <= p <= 1):
                raise ZufallError("die Trefferwahrscheinlichkeit muß in [0,1] liegen") 
            p = nsimplify(p)
            vert = []
            for k in range(n+1):
                vert += [[k, binomial(n, k) * Pow(p, k) * Pow(1-p, n-k)]]
            vert = dict(vert)				
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsGroesse.__new__(cls, vert, parameter=(n, p), kontrolle=False)

			
    def __str__(self):  
        n, p = self.args[1][:2]
        return "BinomialVerteilung(" + str(n) + "," + str(p) + ")"	
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def n(self):
        """Anzahl Versuche"""	
        return self.args[1][0]	

    @property
    def p(self):
        """Trefferwahrscheinlichkeit"""	
        return Rational(self.args[1][1])	

    @property
    def erw(self):
        """Erwartungswert"""	
        n, p = self.args[1][:2]	
        return nsimplify(n * p)

    @property
    def var(self):
        """Varianz"""	
        n, p = self.args[1][:2]	
        return nsimplify(n * p * (1-p))
		
    @property	
    def e_sigma_umg(self):
        """Sigma-Umgebungen des Erwartungswertes"""
        e = N(self.erw)
        s = N(self.sigma)	
        print(' ')		
        display(Math('p = 0.68: [' + latex(N(e-s,4)) + ',' + latex(N(e+s, 4)) + '] \
                  \\qquad 1\,\\sigma - Umgebung'))	
        display(Math('p = 0.955: [' + latex(N(e-2*s, 4)) + ',' + latex(N(e+2*s, 4)) + '] \
                  \\qquad 2\,\\sigma - Umgebung'))	
        display(Math('p = 0.997: [' + latex(N(e-3*s, 4)) + ',' + latex(N(e+3*s, 4)) + '] \
                  \\qquad 3\,\\sigma - Umgebung'))	
        display(Math('p = 0.9: [' + latex(N(e-1.64*s, 4)) + ',' + latex(N(e+1.64*s, 4)) + '] \
                  \\qquad 1.64\,\\sigma - Umgebung'))			
        display(Math('p = 0.95: [' + latex(N(e-1.96*s, 4)) + ',' + latex(N(e+1.96*s, 4)) + '] \
                  \\qquad 1.96\,\\sigma - Umgebung'))	
        display(Math('p = 0.99: [' + latex(N(e-2.58*s, 4)) + ',' + latex(N(e+2.58*s, 4)) + '] \
                  \\qquad 2.58\,\\sigma - Umgebung'))	
        display(Math('Laplace-Bedingung: \,\,\\sigma^2 \\gt 9 = ' + 
                   latex(bool(s**2 > 9)) + '\\qquad ( \\sigma = ' + latex(s) + ')'))
        print(' ')		

    eSigmaUmg = e_sigma_umg
		
    @property	
    def p_sigma_umg(self):
        """Sigma-Umgebungen des Erwartungswertes"""
        p = N(self.p)
        s = N(self.sigma/self.n)	
        print(' ')		
        display(Math('p = 0.68: [' + latex(N(p-s, 4)) + ',' + latex(N(p+s, 4)) + '] \
                       \\qquad 1\,\\sigma - Umgebung'))	
        display(Math('p = 0.955: [' + latex(N(p-2*s, 4)) + ',' + latex(N(p+2*s, 4)) + '] \
                       \\qquad 2\,\\sigma - Umgebung'))	
        display(Math('p = 0.997: [' + latex(N(p-3*s, 4)) + ',' + latex(N(p+3*s, 4)) + '] \
                       \\qquad 3\,\\sigma - Umgebung'))	
        display(Math('p = 0.9: [' + latex(N(p-1.64*s, 4)) + ',' + latex(N(p+1.64*s, 4)) + '] \
                   \\qquad 1.64\,\\sigma - Umgebung'))			
        display(Math('p = 0.95: [' + latex(N(p-1.96*s, 4)) + ',' + latex(N(p+1.96*s, 4)) + '] \
                   \\qquad 1.96\,\\sigma - Umgebung'))	
        display(Math('p = 0.99: [' + latex(N(p-2.58*s, 4)) + ',' + latex(N(p+2.58*s, 4)) + '] \
                   \\qquad 2.58\,\\sigma - Umgebung'))	
        display(Math('Laplace-Bedingung: \,\,\\sigma^2 \\gt 9 = ' + 
                   latex(bool(s**2 > 9)) + '\\qquad ( \\sigma = ' + latex(s) + ')'))
        print(' ')		
	
    pSigmaUmg = p_sigma_umg	
	
    @property	
    def formeln(self):
        """Formeln"""
        print(' ')		
        display(Math('\mathrm{Ergebnismenge} \\qquad\\qquad\; \\Omega = \{0, 1, 2,..., n\}'))	
        display(Math('\mathrm{Wahrscheinlichkeiten} \\qquad P(X=k) = {n \choose k}\, p^k \,(1-p)^{n-k}, \\quad k=0,...,n'))	
        display(Math('\\qquad\\qquad\\qquad\\qquad\\quad\;\;\, P(\, X \\le K\, )  = F(n,\,p,\,K) ='))
        display(Math('\\qquad\\qquad\\qquad\\qquad\\qquad\qquad\quad\;\;\, = \\sum_{i=0}^K {n \choose i}\, p^i' + \
           '\,(1-p)^{n-i},\\quad K=0,...,n'))
        display(Math('\\qquad\\qquad\\qquad\\qquad\\quad\;\;\,F - \mathrm{Verteilungsfunktion}'))	
        display(Math('\mathrm{Erwartungswert} \\qquad\\qquad\,  n\, p'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad\\qquad\\quad n \, p \,(1-p)'))	
        display(Math('n \mathrm{\,-\, Anzahl\; Versuche,} \; p \mathrm{\,-\, Trefferwahrscheinkichkeit,} \\quad ' + \
                   '\mathrm{aktuell} \;\;\; n = ' + latex(self.n) + ',\;\;\; p =' + latex(self.p)))	
        print(' ')		

    @property				
    def faust_regel(self):
        """Faustregel"""
        print(' ')		
        if self.sigma**2 > 9:
            txt = "\mathrm{ist\;erfüllt}"	
        else:			
            txt = "\mathrm{ist\;nicht\;erfüllt}"	
        display(Math("\mathrm{Moivre-Laplace-Bedingung\;für\; Approximation\; durch\; die\;Normalverteilung\; }")) 
        display(Math(txt))
        display(Math('\\sigma^2 = n\,p\, (1-p) \\gt 9 \\quad\\text{(gefordert)}'))		
        display(Math('\\sigma^2 = ' + latex(float(self.sigma**2))))	
        if self.n >= 100 and self.p <= 0.1:
            txt = "\mathrm{ist\;erfüllt}"	
        else:			
            txt = "\mathrm{ist\;nicht\;erfüllt}"	
        display(Math("\mathrm{Bedingung\; für\; Approximation\; durch\; die\;Poissonverteilung\;} " + txt)) 
        display(Math('n \\ge 100 , \\quad p \\le 0.1\\quad\\text{(gefordert)}'))
        display(Math('n = ' + latex(self.n) + ', \\quad p = ' + latex(float(self.p))))
				
    faustRegel = faust_regel

    @property	
    def nv_approx(self):
        """Approximation durch die Normalverteilung"""	
        modul = importlib.import_module('zufall.lib.objekte.normal_verteilung')
        NormalVerteilung = getattr(modul, 'NormalVerteilung')
        return NormalVerteilung(self.erw, self.sigma)
		
    nvApprox = nv_approx
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        binomial_verteilung_hilfe(3)	
		
    h = hilfe					

				
# Benutzerhilfe für BinomialVerteilung
# ------------------------------------

def binomial_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
BinomialVerteilung - Objekt

Kurzname     BV
		
Erzeugung    BinomialVerteilung( n, p )

                 n    Anzahl Versuche
                 p    Trefferwahrscheinlichkeit
				 
Zuweisung     bv = BV(...)   (bv - freier Bezeichner)

Beispiele
BV(20, 0.4)
BV(320, 1/5)
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für BinomialVerteilung
 
bv.hilfe               Bezeichner der Eigenschaften und Methoden
bv.e_sigma_umg         Sigma-Umgebungen des Erwartungswertes		
bv.erw                 Erwartungswert	
bv.erw_(...)        M  ebenso, zugehörige Methode	
bv.F(...)           M  Verteilungsfunktion
bv.faust_regel         Faustregeln
bv.formeln             Formeln
bv.graf_F              Graf der Verteilungsfunktion
bv.hist                Histogramm
bv.hist_(...)       M  ebenso, zugehörige Methode
bv.hist_kum            ebenso, kumulierte Wahrscheinlichkeiten
bv.n                   Anzahl Versuche
bv.n_omega             Größe der Ergebnismenge 
bv.nv_approx           Approximation durch Normalverteilung 
bv.omega               Ergebnismenge 
bv.p                   Trefferwahrscheinlichkeit
bv.P(...)           M  Wahrscheinlichkeit eines Ereignisses
bv.p_sigma_umg         Sigma-Umgebungen der Wahrscheinlichkeit
bv.poly_zug            Polygonzug-Diagramm der Wahrscheinlichkeiten
bv.poly_zug_(...)   M  ebenso, zugehörige Methode
bv.quantil(...)     M  Quantile
bv.relh2p           M  Stabilisierung der relativen Häufigkeiten        
bv.sigma               Standardabweichung
bk.sigma_(...)      M  ebenso, zugehörige Methode	
bk.stich_probe(...) M  Stichprobe		
bv.var                 Varianz		
bv.var_(...)        M  ebenso, zugehörige Methode		
bv.versuch             Versuch		
bv.vert                Wahrscheinlichkeitsverteilung		
bv.vert_(...)       M  ebenso, zugehörige Methode		
bv.vert_kum            kumulierte Wahrscheinlichkeitsverteilung
bv.vert_kum_(...)   M  ebenso, zugehörige Methode

Synonyme Bezeichner

hilfe          h
erw_           Erw	
e_sigma_umg    eSigmaUmg		
faust_regel    faustRegel
graf_F         grafF
hist_          Hist
hist_kum       histKum
nv_approx      nvApprox
n_omega        nOmega
poly_zug       polyZug
poly_zug_      PolyZug
p_sigma_umg    pSigmaUmg
sigma_         Sigma
stich_probe    stichProbe
var_           Var
vert_          Vert
vert_kum       vertKum
vert_kum_      VertKum
	   """)		
        return
	
	
BV = BinomialVerteilung
		
		