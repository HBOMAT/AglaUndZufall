#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  AlternativTest - Klasse  von zufall           
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

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.funktionen.graf_funktionen import balken1, balken_plus_balken
from zufall.lib.objekte.ausnahmen import ZufallError
import zufall

bv = importlib.import_module('zufall.lib.objekte.binomial_verteilung')
BinomialVerteilung = bv.BinomialVerteilung



# AlternativTest - Klasse  
# -----------------------
	
class AlternativTest(ZufallsObjekt):                                      
    """
	
Alternativtest

**Kurzname** **AT**
	
**Erzeugung** AT( *p0, p1, zahl1, zahl2* )

   *p0*, *p1* : Wahrscheinlichkeiten bei :math:`H_0`, :math:`H_1`
				 
**Berechnung**

   ===================== ===================== ===========   
   gegeben:  zahl1       zahl2                 berechnet              
   ===================== ===================== ===========
   *n*                   *k*                   *alpha*, *beta*
   *n*                   ob. Grenze f. *alpha* *k*, *beta*
   ob. Grenze f. *alpha* ob. Grenze f. *beta*  *n*, *k*
   ===================== ===================== ===========
			  
   *n* :       Stichprobenumfang
   
   *k* :      kritische Zahl
   
   *alpha* :   Wahrscheinlichkeit für Fehler 1. Art 
   
   *beta* : ebenso, 2. Art
				 
    """
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            alternativ_test_hilfe(kwargs["h"])		
            return	
				
        try:
            n, k, alpha, beta = (None,) * 4		
            if len(args) != 4:
                raise ZufallError('vier Argumente angeben')
            p0, p1, zahl1, zahl2 = args[:4]
            if not (isinstance(p0, (Rational, float, Float)) and 0 < p0 < 1):
                raise ZufallError('für p0 Zahl aus (0,1) angeben')
            if not (isinstance(p1, (Rational, float, Float)) and 0 < p1 < 1):
                raise ZufallError('für p1 Zahl aus (0,1) angeben')
            if p1 ==p0:
                raise ZufallError('p0 und p1 müssen verschieden sein')			
            if not (isinstance(zahl1, (int, Integer)) and zahl1 > 0 or \
                     isinstance(zahl1, (Rational, float, Float)) and 0 < zahl1 < 1):
                raise ZufallError('für zah1l ganze Zahl > 0 oder Zahl aus (0,1) angeben')
            if not (isinstance(zahl2, (int, Integer)) and zahl2 > 0 or \
                     isinstance(zahl2, (Rational, float, Float)) and 0 < zahl2 < 1):
                raise ZufallError('für zah12 ganze Zahl > 0 oder Zahl aus (0,1) angeben')
            if isinstance(zahl1, (int, Integer)): 
                if isinstance(zahl2, (int, Integer)):			          
                    fall = 'nk'
                    n, k = zahl1, zahl2	
                    if k > n:
                        raise ZufallError('die kritische Zahl kann nicht größer als der Stichprobenumfang sein')                        					
                elif isinstance(zahl2, (Rational, float, Float)): 
                    fall = 'na'
                    n, alpha = zahl1, zahl2
                else:
                    raise ZufallError('für zah12 Zahl aus (0,1) angeben')				
            else:
                if isinstance(zahl2, (Rational, float, Float)):             			
                    fall = 'ab'
                    alpha, beta = zahl1, zahl2				
                else:
                    raise ZufallError('für zah12 Zahl aus (0,1) angeben')				
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        if fall == 'na':
            bv0 = BinomialVerteilung(n, p0)			
            if p0 < p1:
                k = bv0.quantil(1-alpha) + 1   
            else:
                k = bv0.quantil(alpha) - 1				
        elif fall == 'ab':
		
            def sign(x):
                if x > 0:			
                    return 1
                elif x < 0:
                    return -1
                else:
                    return 0
					
            n = 2
            bv0 = BinomialVerteilung(n, p0)			
            bv1 = BinomialVerteilung(n, p1)			
            if p0 < p1:                                                
                k0 = bv0.quantil(1-alpha) + 1
                k1 = bv1.quantil(beta)
                si = sign(k1-k0)
                while sign(k1-k0) == si:
                    n += 1
                    bv0 = BinomialVerteilung(n, p0)			
                    bv1 = BinomialVerteilung(n, p1)			
                    k0 = bv0.quantil(1-alpha) + 1
                    k1 = bv1.quantil(beta)		  
            else: 			
                k0 = bv0.quantil(alpha) - 1
                k1 = bv1.quantil(1-beta)
                si = sign(k1-k0)
                while sign(k1-k0) == si:
                    n += 1
                    bv0 = BinomialVerteilung(n, p0)			
                    bv1 = BinomialVerteilung(n, p1)			
                    k0 = bv0.quantil(alpha) - 1
                    k1 = bv1.quantil(1-beta)
            k = k1;
				
        return ZufallsObjekt.__new__(cls, p0, p1, n, k, alpha, beta, fall)

		
    def __str__(self):  
        return "AlternativTest"

		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def n(self):
        """Stichprobenumfang"""
        return self.args[2]		

    @property
    def k(self):
        """Kritische Zahl"""
        return self.args[3]		

    K = k		
		
    @property
    def h0(self):
        """Nullhypothese"""
        display(Math('p =' + str(self.args[0])))		
        return 

    H0 = h0		

    @property
    def h1(self):
        """Alternativhypothese"""
        display(Math('p =' + str(self.args[1])))		
        return 		
			
    H1 = h1
	
    @property
    def bv0(self):
        """BinomialVerteilung bei :math:`H_0`"""
        n, p = self.n, self.args[0]		
        return BinomialVerteilung(n, p)		

    @property
    def bv1(self):
        """BinomialVerteilung bei :math:`H_1`"""
        n, p = self.n, self.args[1]		
        return BinomialVerteilung(n, p)		
			
    @property
    def an_ber(self):
        """Annahmebereich von :math:`H_0`"""
        p0, p1, n, k = self.args[:4]	
        if p0 < p1:		
            return set(range(k))
        else:
            return set(range(k+1, n+1))
    def an_ber_(self, **kwargs):
        """ebenso; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   g=ja   grafische Darstellung\n")
            return  
        ab_ber, om = self.ab_ber, self.bv0.omega
        mark = []		
        for k in om:	
            if k in ab_ber:	
                mark += [k]			
        if kwargs.get('g'):	
            balken1(self.bv0._vert, typ='W', titel='Annahmebereich (hell) und ' + \
                      'Ablehnungsbereich (dunkel)\nvon $H_0$\n', mark=mark)	
            return			
        return self.an_ber		

    anBer = an_ber
    AnBer = an_ber_	
		
    @property
    def ab_ber(self):
        """Ablehnungsbereich von :math:`H_0`"""
        ber, bv0 = self.an_ber, self.bv0        		
        return bv0.omega.difference(ber)
    def ab_ber_(self, **kwargs):
        """ebenso; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   g=ja   grafische Darstellung\n")
            return  
        ab_ber, om = self.ab_ber, self.bv0.omega
        mark = []		
        for k in om:	
            if k in ab_ber:	
                mark += [k]			
        if kwargs.get('g'):		
            balken1(self.bv0._vert, typ='W', titel='Annahmebereich (hell) und ' + \
                      'Ablehnungsbereich (dunkel)\nvon $H_0$\n', mark=mark)	
            return			
        return self.ab_ber		

    abBer = ab_ber
    AbBer = ab_ber_	
		
    @property
    def alpha(self):
        """Wahrscheinlichkeit für Fehler 1. Art"""
        ber, bv0 = self.ab_ber, self.bv0        		
        return float('{0:.6f}'.format(float(bv0.P(ber))))

    @property
    def beta(self):
        """Wahrscheinlichkeit für Fehler 2. Art"""
        ber, bv1 = self.an_ber, self.bv1        		
        return float('{0:.6f}'.format(float(bv1.P(ber))))

    @property
    def begriffe(self):
        """Begriffe beim Testen von Hypothesen"""
		
        def dm(x):
            return display(Math(x))	

        print(' ')			
        dm('\mathrm{Begriffe\; beim\; Testen\; von\; Hypothesen}')		
        print(' ')		
        dm('H_0 - \mathrm{Nullhypothese\;\;\;z.B.}\;\; p_0 = 0.3')			
        dm('H_1 - \mathrm{Alternativhypothese\; oder\; Gegenhypothese\;\;\;z.B.}\;\; p_1 = 0.5')			
        dm('\mathrm{Alternativtest - die\; beiden\; Hypothesen\; sind\; jeweils\; durch\; einen\; ' + \
            'einzelnen\; Wert\; festgelegt}')			
        dm('\mathrm{Signifikanztest - allgemeiner\; Test\; für\; einen\; Parameter\; einer\; Verteilung\; bei' + \
            '\;einer\; beliebi-}')
        dm('\\qquad \mathrm{gen\; Form\; der\; Hypothesen}')
        dm('\mathrm{Ablehnungsbereich\; von\;} ' + 'H_0' + '\mathrm{= kritischer\;  Bereich - Bereich \; der \;' + \
            'Ergebnismenge,\; für\; dessen\;}')
        dm('\\qquad \mathrm{ Werte\;}' + 'H_0' + '\mathrm{\; abgelehnt\; wird}')
        dm('\mathrm{Annahmebereich\; von\;} ' + 'H_0' + '\mathrm{- Bereich \; der \;' + \
            'Ergebnismenge,\; für\; dessen\;Werte\;}' + 'H_0' + '\mathrm{\; nicht\; abge- }')
        dm('\\qquad \mathrm{lehnt\; wird}')
        dm('\mathrm{Kritische\; Zahl - Grenze\; des\; Ablehnungsbereiches}')
        dm('\mathrm{Fehler\; 1.\; Art -\; } H_0\; \mathrm{wird\; abgelehnt,\; trotzdem\; sie\; wahr\; ist}')		
        dm('\mathrm{Fehler\; 2.\; Art -\; } H_0\; \mathrm{wird\; nicht \;abgelehnt,\; trotzdem\; sie\; falsch\; ist}')		
        dm('\\qquad \mathrm{beide\; Fehler\; sind\; zufällige\; Ereignisse}')	
        dm('P(\; \mathrm{Fehler\; 1. Art\; ) = Risiko\; 1. Art = Irrtumswahrscheinlichkeit\; 1. Art = }\; \\alpha ' + \
		    '\mathrm{-Fehler = }\; \\alpha')
        dm('P(\; \mathrm{Fehler\; 2. Art\; ) = Risiko\; 2. Art = Irrtumswahrscheinlichkeit\; 2. Art = }\; \\beta ' + \
		    '\mathrm{-Fehler = }\; \\beta')
        print(' ')			
        

    def _regel(self, **kwargs):
        """Entscheidungsregel; interne Methode"""
				
        def dm(x):
            return display(Math(x))	

        p0, p1, n, k, alpha, beta, fall = self.args			
        print(' ')			
        dm('\mathrm{Alternativtest\;zweier\;Hypothesen\;für\;die\;unbekannte\;Wahrscheinlichkeit\;einer}')
        dm('\mathrm{Binomialverteilung}')		
        print(' ')			
        dm('\mathrm{Gegeben:}')	
        dm('H_0: p=' + str(p0) + '\\quad\\quad H_1: p=' + str(p1))	
        if fall == 'nk':
            dm('\mathrm{Stichprobenumfang =\,}' + str(n) + ',\\quad \mathrm{Kritische\; Zahl =\,}' + str(k))		
        elif fall == 'na':
            dm('\mathrm{Stichprobenumfang =\, }' + str(n))		
            dm('\mathrm{Obere\; Grenze\;\;}' + '\\alpha \\le' + str(alpha))		
        else:
            dm('\mathrm{Obere\; Grenze\;\;}' + '\\alpha \\le' + str(alpha) + '\\quad \\beta \\le' + str(beta))		
        print(' ')
        if fall == 'na':		
            dm('\mathrm{Berechnet:}')
            dm('\mathrm{Kritische\; Zahl =\,}' +str(k))		
        if fall == 'ab':		
            dm('\mathrm{Berechnet:}')
            dm('\mathrm{Stichprobenumfang =\,}' +str(n))					
            dm('\mathrm{Kritische\; Zahl =\,}' +str(k))		
        dm('\mathrm{Entscheidungsregel:}')	
        if p0 < p1:
            dm('X \\lt ' + str(k) + '\\Rightarrow \mathrm{Entscheidung\; für}\; H_0\; \mathrm{(das\; Ergebnis\; liegt\;' + \
               'im\; Annahmebereich)}')	
            dm('X \\ge ' + str(k) + '\\Rightarrow \mathrm{Entscheidung\; für}\; H_1\; \mathrm{(das\; Ergebnis\; liegt\;' + \
               'im\; Ablehnungsbereich)}')	
        else:
            dm('X \\gt ' + str(k) + '\\Rightarrow \mathrm{Entscheidung\; für}\; H_0\; \mathrm{(das\; Ergebnis\; liegt\;' + \
               'im\; Annahmebereich)}')	
            dm('X \\le ' + str(k) + '\\Rightarrow \mathrm{Entscheidung\; für}\; H_1\; \mathrm{(das\; Ergebnis\; liegt\;' + \
               'im\; Ablehnungsbereich)}')	
        if fall == 'nk':		
            dm('\mathrm{Berechnet:}')
        aa = self.bv0.P(self.ab_ber)		
        bb = self.bv1.P(self.an_ber)		
        dm('\\alpha =' + '{0:.4f}'.format(float(aa)) + '\\quad [\; =\,P_{H_0}(\mathrm{Ablehnung\;von\;}H_0)\;]') 		
        dm('\\beta =' + '{0:.4f}'.format(float(bb)) + '\\quad [\; =\,P_{H_1}(\mathrm{Annahme\;von\;}H_0)\;]')
        if kwargs.get('leer'): 		
            print(' ')
		
    @property		
    def regel(self, **kwargs):
        """Entscheidungsregel"""
        self._regel(leer=True)		
		
    def regel_(self, **kwargs):
        """ebenso; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   g=ja   Grafische Darstellung\n")
            return 
        self._regel()	
        if kwargs.get('g'):
            if self.args[0] < self.args[1]:		
                titel = 'links - Verteilung bei $H_0$, rechts - bei $H_1$'	
            else:
                titel = 'links - Verteilung bei $H_1$, rechts - bei $H_0$'	
            balken_plus_balken(self.bv0._vert, self.bv1._vert, typ1='W', typ2='W', titel=titel, ) 	
		
    Regel = regel_
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        alternativ_test_hilfe(3)	
		
    h = hilfe					

	
		
def alternativ_test_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
AlternativTest - Objekt     Alternativtest für die unbekannte Wahrschein-
                            lichkeit der Binomialverteilung

Kurzname     AT
		
Erzeugung    AT( p0, p1, zahl1, zahl2 )

                 p0, p1       Wahrscheinlichkeiten bei H0, H1
				 
Berechnung   gegeben                                     berechnet
             zahl1                 zahl2
             n                     k                     alpha, beta
             n                     ob. Grenze f. alpha   k, beta
             ob. Grenze f. alpha   ob. Grenze f. beta    n, k
			  
             n       Stichprobenumfang
             k       kritische Zahl
             alpha   Wahrscheinlichkeit für Fehler 1. Art bzw.
             beta    2. Art
								 
Zuweisung     at = AT(...)   (at - freier Bezeichner)

Beispiele

AT( 0.4, 0.6, 40, 21 )	    Vorgabe   : Stichprobenumfang, kritische Zahl
                            Berechnung: Wahrsch. für Fehler 1. und 2. Art

AT( 0.4, 0.6, 40, 0.01 )    Vorgabe   : Stichprobenumfang, Grenze der Wahrsch.
                                        für Fehler 1. Art
                            Berechnung: kritische Zahl, Wahrsch. für Fehler 
                                        2. Art

AT( 0.4, 0.6, 0.005, 0.1 )  Vorgabe   : Grenzen der Wahrsch. für Fehler 1. 
                                        und 2. Art
                            Berechnung: Stichprobenumfang, kritische Zahl							
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für AlternativTest

at.hilfe            Bezeichner der Eigenschaften und Methoden
at.ab_ber           Ablehnungsbereich für H0
at.ab_ber_(...)  M  ebenso, zugehörige Methode
at.an_ber           Annahmebereich für H0
at.an_ber(...)   M  ebenso, zugehörige Methode
at.alpha            Wahrscheinlichkeit für Fehler 1. Art
at.begriffe         Begriffe
at.beta             Wahrscheinlichkeit für Fehler 2. Art
at.bv0              BinomialVerteilung bei H0
at.bv1              BinomialVerteilung bei H1
at.h0               Nullhypothese
at.h1               Alternativhypothese
at.k                kritische Zahl
at.n                Stichprobenumfang
at.regel            Ermittlung der Entscheidungsregel
at.regel_(...)  M   ebenso, zugehörige Methode

Synonyme Bezeichner

hilfe     h
ab_ber    abBer
an_ber    anBer
h0        H0
h1        H1
k         K
regel_    Regel
    """)		
        return
	
	
AT = AlternativTest