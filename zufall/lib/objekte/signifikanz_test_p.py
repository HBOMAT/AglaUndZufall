#!/usr/bin/python
# -*- coding: utf-8 -*-

#                                      
#  SignifikanzTestP - Klasse  von zufall           
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

import numpy as np
from scipy.stats import norm

import matplotlib.pyplot as plt

from sympy import sqrt, floor, ceiling, Piecewise
from sympy.core.numbers import Integer, Rational, Float 
from sympy.printing.latex import latex

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.normal_verteilung import NormalVerteilung
from zufall.lib.funktionen.graf_funktionen import balken1
	
from zufall.lib.objekte.ausnahmen import ZufallError

import zufall

bv = importlib.import_module('zufall.lib.objekte.binomial_verteilung')
BinomialVerteilung = bv.BinomialVerteilung


	

# SignifikanzTestP - Klasse  
# -------------------------
	
class SignifikanzTestP(ZufallsObjekt):                                      
    """
	
Signifikanztest für die unbekannte Wahrscheinlichkeit der 
Binomialverteilung

**Kurzname** **STP**
	
**Erzeugung** 
	
   STP( *p0, alpha, seite, umfang, verfahren* )

**Parameter**

   *p0* : Wahrscheinlchkeit bei :math:`H_0`
   
   *alpha* : Signifikanzniveau; Zahl aus (0,1)
   
   *seite* :

      | '2' | 'l' | 'r'  *oder* 
	  
      | 'zwei' | 'links' | 'rechts'

      | zwei-, links- oder rechtsseitiger Test

   *umfang* : Stichprobenumfang	
   
   *verfahren* :

      'S' | 'Sigma' -
         | bei alpha = 0.05 (einseitiger Test)
         | bei alpha = 0.05, 0.1 (zweiseitiger Test)
         | Benutzung der Sigma-Umgebung des Erwartungswertes
		 
      'B' | 'BV' -
         Benutzung der Binomialverteilung selbst
		 
      'N' | 'NV' - 
         Benutzung der Approximation durch die Normalverteilung

    """
		
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            signifikanz_test_p_hilfe(kwargs["h"])		
            return	
				
        try:
            if len(args) != 5:
                raise ZufallError('fünf Argumente angeben')
            p0, alpha, seite, umfang, verfahren = args[:5]
            if not (isinstance(p0, (Rational, float, Float)) and 0 < p0 < 1):
                raise ZufallError('für p0 Zahl aus (0,1) angeben')
            if not (isinstance(alpha, (Rational, float, Float)) and 0 < alpha < 1):
                raise ZufallError('für alpha Zahl aus (0,1) angeben')
            if not seite in ('l', 'links', 'r', 'rechts', 2, '2', 'zwei'):
                raise ZufallError("für seite  'l'|'links',| 'r'|'rechts', '2'|'zwei'|2  angeben")
            if not (isinstance(umfang, (int, Integer)) and umfang > 0):
                raise ZufallError('für umfang ganze Zahl > 0 angeben')
            if not verfahren in ('S', 'Sigma', 'B', 'BV', 'N', 'NV'): 
                raise ZufallError("für verfahren  'S'|'Sigma',| 'B'|'BV', 'N'|'NV'  angeben")
            if verfahren in ('S', 'Sigma'):
                if seite in ('l', 'links', 'r', 'rechts') and alpha != 0.05:
                    raise ZufallError('das Verfahren ist nur für alpha=0.05 implementiert')
                if seite in ('2', 'zwei', 2) and alpha not in (0.05, 0.1):
                    raise ZufallError('das Verfahren ist nur für alpha=0.05 oder 0.1 implementiert')
				
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        return ZufallsObjekt.__new__(cls, p0, alpha, seite, umfang, verfahren)

		
    def __str__(self):  
        return "SignifikanzTestP"		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def n(self):
        """Stichprobenumfang"""
        return self.args[3]		
		
    @property
    def h0(self):
        """Nullhypothese"""
        display(Math('p =' + str(self.args[0])))		
        return 

    H0 = h0		

    @property
    def h1(self):
        """Alternativhypothese"""
        if self.args[2] in ('l', 'links'):
            rel = '\\lt'
        elif self.args[2] in ('r', 'rechts'):
            rel = '\\gt'
        else:
            rel = '\\ne'		
        display(Math('p' + rel + str(self.args[0])))				
        return 		
			
    H1 = h1
	
    @property
    def bv(self):
        """BinomialVerteilung bei :math:`H_0`"""
        n, p = self.n, self.args[0]		
        return BinomialVerteilung(n, p)		

    @property
    def sig_niv(self):
        """Signifikanzniveau"""
        return self.args[1]		
		
    sigNiv = sig_niv		
		
    @property
    def alpha(self):
        """Wahrscheinlichkeit für Fehler 1. Art"""
        ber, bv = self.ab_ber, self.bv        		
        return float('{0:.4f}'.format(float(bv.P(ber))))
				
    @property
    def begriffe(self):
        """Begriffe beim Testen von Hypothesen"""
		
        def dm(x):
            return display(Math(x))	

        print(' ')			
        dm('\mathrm{Begriffe\; beim\; Testen\; von\; Hypothesen}')		
        print(' ')		
        dm('H_0 - \mathrm{Nullhypothese\;\;\;z.B.}\;\; p = 0.4')			
        dm('H_1- \mathrm{Alternativhypothese\; oder\; Gegenhypothese}')			
        dm('\\quad\\quad p \\lt' + str(self.args[0]) + ' \\quad linksseitiger\; Test')			
        dm('\\quad\\quad p \\gt' + str(self.args[0]) + ' \\quad rechtsseitiger\; Test')	
        dm('\\quad\\quad p \\ne' + str(self.args[0]) + ' \\quad zweiseitiger\; Test')			
        dm('\mathrm{Prüfgröße - Stichprobenfunktion\; zur\; Konstruktion\; einer\; Entscheidungsregel\; zur\;}' + \
           '\mathrm{Ableh-}')
        dm('\\qquad \mathrm{nung \;bzw.\; Annahme\; von\; } H_0')		
        dm('\mathrm{Ablehnungsbereich\; von\;} ' + 'H_0' + '\mathrm{\;oder\; kritischer\;  Bereich - Bereich \; der \;' + \
            'Ergebnismenge,\;für}') 
        dm('\\qquad \mathrm{dessen\; Werte\;}' + 'H_0' + '\mathrm{\; abgelehnt\; wird}')
        dm('\mathrm{Annahmebereich\; von\;} ' + 'H_0' + '\mathrm{- Bereich \; der \;' + \
            'Ergebnismenge,\; für\; dessen\; Werte\;}' + 'H_0' + '\mathrm{\; nicht\; ab-}')
        dm('\\qquad \mathrm{gelehnt\; wird}')
        dm('\mathrm{Signifikanzgrenze(n)\; oder\; Kritische\; Zahl(en) - Randwert(e)\; des\; Ablehnungsbereiches}')
        dm('\mathrm{Fehler\; 1.\; Art \;-\;} H_0\; \mathrm{wird\; abgelehnt,\; trotzdem\; sie\; wahr\; ist}')		
        dm('\mathrm{Fehler\; 2.\; Art\; -\;} H_0\; \mathrm{wird\; nicht \;abgelehnt,\; trotzdem\; sie\; falsch\; ist}')		
        dm('\\qquad \mathrm{beide\; Fehler\; sind\; zufällige\; Ereignisse}')	
        dm('P(\; \mathrm{Fehler\; 1. Art\; ) = Risiko\; 1. Art = Irrtumswahrscheinlichkeit\; 1. Art = }\; \\alpha ' + \
		    '\mathrm{-Fehler = }\; \\alpha')
        dm('P(\; \mathrm{Fehler\; 2. Art\; ) = Risiko\; 2. Art = Irrtumswahrscheinlichkeit\; 2. Art = }\; \\beta ' + \
		    '\mathrm{-Fehler }')
        dm('\mathrm{Signifikanzniveau - obere \; Schranke\; für\; das\; Risiko\; 1. Art}')			
        dm('\mathrm{Gütefunktion}')
        dm('\\quad\\quad p \\longmapsto P(\,Ablehnung\; von\; H_0\,)')			
        dm('\mathrm{\\quad\\quad für\; die\;} p \mathrm{-Werte\; aus\; dem\; Bereich\; von\;} H_0 \mathrm{\;ist\; der\;' \
           'Funktionswert\; das\; zugehörige\; Risiko\; 1. Art}')			
        dm('\mathrm{Operationscharakteristik\; (OC,\; auch\; } \\beta \mathrm{-Funktion)}')			
        dm('\\quad\\quad p \\longmapsto 1-P(\,Ablehnung\; von\; H_0\,)')			
        dm('\mathrm{\\quad\\quad für\; die\;} p \mathrm{-Werte\; aus\; dem\; Bereich\; von\;} H_1 \mathrm{\;ist\; der\;' \
           'Funktionswert\; das\; zugehörige\; Risiko\; 2. Art}')			
		
        print(' ')			
		

    def quantil_bv(self, *args, **kwargs):
        """Quantile der zugehörigen Binomialverteilung"""
        if kwargs.get('h'):
            p0, n = str(self.args[0]), str(self.n)
            print('\nQuantile der Binomialverteilung(' + n + ', ' + p0 + ')\n')			
            print("Aufruf   t . quantil_bv( p )\n")		                     
            print("             t    SignifikanzTestP")
            print("             p    Zahl aus [0,1]\n")
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        pp = args[0]
        txt = 'zufall: Zahl aus [0,1] angeben'		
        if not isinstance(pp, (int, Integer, float, Float, Rational)):			
            print(txt)
            return			
        if not (0 <= pp <= 1):			
            print(txt)
            return
        q = self.bv.quantil(*args)	
        return q
		
    quantilBV	= quantil_bv	
		
    def quantil_nv(self, *args, **kwargs):
        """Quantile der Normalverteilung"""
        if kwargs.get('h'):
            print('\nQuantile der (0,1)-Normalverteilung\n')
            print("Aufruf   t . quantil_nv( p )\n")		                     
            print("             t    SignifikanzTestP")
            print("             p    Zahl aus [0,1]\n")
            return
        nv = NormalVerteilung(0, 1)
        q = nv.quantil(*args)	
        return q
			
    quantilNV = quantil_nv					
	
    @property		
    def schema(self):		
        """Schema eines Signifikanztestes"""
		
        def dm(x):
            return display(Math(x))
			
        seite, verf = self.args[2], self.args[4]
        print(' ')			
        dm('\mathrm{Schema\; eines\; Signifikanztestes\;}')
        dm('\mathrm{für\;die\;unbekannte\;Wahrscheinlichkeit\;einer\;Binomialverteilung}')		
		
        if seite in ('l', 'links'):
            if verf in ('S', 'Sigma'):
                dm('\mathrm{Benutzung\; der\;} \\sigma \mathrm{-Umgebungen\; des\; Erwartungswertes}')
                print(' ')				
                dm('\mathrm{H_0}: \;p \ge p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\lt p_0 \\quad \mathrm{(Gegenhypothese) \\quad linksseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Festlegung\; der\; Prüfgröße\; } X \mathrm{\;(Anzahl\; Treffer)\; auf\; der\; ' + \
                   'Grundlage\; einer\; Stichprobe \;}')				
                dm('\mathrm{\\quad  des\; Umfangs\;} n.\mathrm{Unter\; H_0\;ist\;}' + \
                   '\; X  \mathrm{\;binomialverteilt\;mit\;den\;Parametern\;}' + \
                   'n \mathrm{\;und\;} p_0 \mathrm{\;und\;}')
                dm('\\quad \mathrm{hat\; den\;Erwartungswert\;\;} \\mu = n\,p_0, \mathrm' + \
                   '{die\; Standardabweichung\; ist\;\;}\\sigma = \\sqrt{n \, p_0 \,(1-p_0)}' )				
                dm('\mathrm{3.\; Ermittlung\; der\; } \\sigma \mathrm{-Umgebung \;anhand\; von\; } \\alpha ' + \
                   '\mathrm{; \; bei\; } \\alpha =' + str(self.args[1]) + '\mathrm{\;liegt\; mit\; einer\; Wahr-}')
                a2 = '{0:.2f}'.format(float(1-2*self.args[1]))				   
                dm('\mathrm{\\quad scheinlichkeit\; von\;} 1-2 \\alpha =' + a2 + '\mathrm{\;ein\; Versuchsergebnis\; in\; der}' + \
                   '\mathrm{\; 1.64-Umgebung\;}') 
                dm('\\quad \mathrm{des\; Erwartungswertes}\;\;[ \\mu - 1.64 \, \\sigma, \;\mu + 1.64 \, \\sigma]')
                dm('\\quad \mathrm{Die\; Wahrscheinlichkeit\; für\; ein\; Ergebnis\; außerhalb\; des\; Intervalls\; ' + \
                   'ist\; } 2 \\alpha, \mathrm{\; jeweils\; }')
                dm('\\quad \\alpha =' + str(self.args[1]) + '\mathrm{\;für\; die\;Bereiche\ links\ und\ rechts\ des\ Intervalls}')
                dm('\\quad \mathrm{Als\; Ablehnungsbereich\;} \\overline{A} \mathrm{\;der\; Hypothese\; H_0\;wird\; \
                       der\; Bereich\; definiert,\;der\;links\;}')
                dm('\\quad \mathrm{von\;diesem\;Intervall\;liegt.\;Die\;Grenze\;(kritische\;Zahl)\;ist\;} K= \
                      \mathrm{abgerundeter\;Wert\;}')
                dm('\\quad\mathrm{der\;linken\;Intervallgrenze.\;Damit\;ist\;} \\overline{A} = \{0,\,1,...,K\}')				
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;} X \\in \\overline{A} \mathrm{,\;so\;wird\; H_0 \;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höchstens\;} \\alpha \mathrm{\;abge-}')
                dm('\\quad\mathrm{lehnt,\;sonst\;wird\; H_0 \;beibehalten}')

            elif verf in ('B', 'BV'):
                dm('\mathrm{Benutzung\; der\;Binomialverteilung}')
                print(' ')				
                dm('\mathrm{H_0}: \;p \ge p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\lt p_0 \\quad \mathrm{(Gegenhypothese) \\quad linksseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Festlegung\; der\; Prüfgröße\; } X \mathrm{\;(Anzahl\; Treffer)\; auf\; der\; ' + \
                   'Grundlage\; einer\; Stichprobe \;}')				
                dm('\mathrm{\\quad  des\; Umfangs\;} n.\mathrm{Unter\;H_0\;ist\;}' + \
                   ' X  \mathrm{\;binomialverteilt\;mit\;den\;Parametern\;}' + \
                   'n \mathrm{\;und\;} p_0')
                dm('\mathrm{3.\; Ermittlung\;der\;kritischen\;Zahl\;} K \mathrm{\;als\;der\;größten\;Zahl\;aus}\;' + \
                   '\{0....,n\}, \mathrm{\;für\; die\;}')
                dm('\\quad P(\,X \\le K\,) \\le \\alpha \\; \mathrm{gilt,\; mittels\; Berechnung\; nach\; der\;' + \
                   'Formel\;\;}')
                dm('\\quad P(X \\le K) = F(n,\,p_0,\,K) = \\sum_{i=0}^K ' + \
                   '{n \choose i}\, p_0^i \,(1-p_0)^{n-i} \mathrm{\;unter\;Beachtung\;von\;} ')
                dm('\\quad F(n,\,p_0,\,K) \\le \\alpha \mathrm{, \;wobei\;} F ' + \
                   '\mathrm{\;die\;Verteilungsfunktion\;der\;Binomialverteilung\;ist}')
                dm('\\quad\mathrm{Ablehnungsbereich\;ist\;\;} \\overline{A} = \{0,\,1,...,K\}')
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;} X \\in \\overline{A} \mathrm{,\;so\;wird\; H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höchstens\;} \\alpha')
                dm('\\quad\mathrm{abgelehnt,\;sonst\;wird\;H_0\;beibehalten}')
				
            else:
                dm('\mathrm{Benutzung\; der\; Approximation\; durch\; die\; Normalverteilung}')
                print(' ')				
                dm('\mathrm{H_0}: \;p \ge p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\lt p_0 \\quad \mathrm{(Gegenhypothese) \\quad linksseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Bestimmung\;von\;} c_\\alpha \mathrm{\;aus\;der\;Gleichung\;\;} \\Phi(c_\\alpha) = 1-\\alpha')				
                dm('\\quad (\\Phi \mathrm{-Verteilungsfunktion\;der\;(0,1)-Normalverteilung)}')				
                dm('\mathrm{3.\; Ermittlung\; der\; Prüfgröße\; } h_n \mathrm{\;(relative\; Trefferhäufigkeit)\; auf\; der\; ' + \
                   'Grundlage\; einer}')
                dm('\\quad \mathrm{ Stichprobe \;des\;Umfangs\;} n')				
                dm('\\quad \mathrm{Der\;Ablehnungsbereich\;wird\;durch\;das\;Kriterium\;}' + \
                   'h_n \\lt p_0-c_\\alpha \\sqrt{ \\frac{p_0(1-p_0)}{n}}') 
                dm('\\quad \mathrm{\;bestimmt}')
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;das\;Kriterium\;erfüllt,\;wird\; H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höch-}')
                dm('\\quad\mathrm{stens\;} \\alpha \mathrm{\;abgelehnt,\;sonst\;wird\;H_0\;beibehalten}')
				
        elif seite in ('r', 'rechts'):
            if verf in ('S', 'Sigma'):
                dm('\mathrm{Benutzung\; der\;} \\sigma \mathrm{-Umgebungen\; des\; Erwartungswertes}')
                print(' ')				
                dm('\mathrm{H_0}: \;p \le p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\gt p_0 \\quad \mathrm{(Gegenhypothese) \\quad rechtsseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus,\;hier\;} \\alpha=0.05')
                dm('\mathrm{2.\; Festlegung\; der\; Prüfgröße\; } X \mathrm{\;(Anzahl\; Treffer)\; auf\; der\; ' + \
                   'Grundlage\; einer\; Stichprobe \;}')				
                dm('\mathrm{\\quad  des\; Umfangs\;} n.\mathrm{Unter\; H_0\;ist\;}' + \
                   '\; X  \mathrm{\;binomialverteilt\;mit\;den\;Parametern\;}' + \
                   'n \mathrm{\;und\;} p_0 \mathrm{\;und\;}')
                dm('\\quad \mathrm{hat\; den\;Erwartungswert\;\;} \\mu = n\,p_0, \mathrm' + \
                   '{die\; Standardabweichung\; ist\;\;}\\sigma = \\sqrt{n \, p_0 \,(1-p_0)}' )				
                dm('\mathrm{3.\; Ermittlung\; der\; } \\sigma \mathrm{-Umgebung \;anhand\; von\; } \\alpha ' + \
                   '\mathrm{; \; bei\; } \\alpha =' + str(self.args[1]) + '\mathrm{\;liegt\; mit\; einer\; Wahr-}')
                a2 = '{0:.2f}'.format(float(1-2*self.args[1]))				   
                dm('\mathrm{\\quad scheinlichkeit\; von\;} 1-2 \\alpha =' + a2 + '\mathrm{\;ein\; Versuchsergebnis\; in\; der}' + \
                   '\mathrm{\; 1.64-Umgebung\;}') 
                dm('\\quad \mathrm{des\; Erwartungswertes}\;\;[ \\mu - 1.64 \, \\sigma, \;\mu + 1.64 \, \\sigma]')
                dm('\\quad \mathrm{Die\; Wahrscheinlichkeit\; für\; ein\; Ergebnis\; außerhalb\; des\; Intervalls\; ' + \
                   'ist\; } 2 \\alpha, \mathrm{\; jeweils\; }')
                dm('\\quad \\alpha =' + str(self.args[1]) + '\mathrm{\;für\; die\;Bereiche\ links\ und\ rechts\ des\ Intervalls}')
                dm('\\quad \mathrm{Als\; Ablehnungsbereich\;} \\overline{A} \mathrm{\;der\; Hypothese\; H_0\;wird\; \
                       der\; Bereich\; definiert,\;der\;rechts\;}')
                dm('\\quad \mathrm{von\;diesem\;Intervall\;liegt.\;Die\;Grenze\;(kritische\;Zahl)\;ist\;} K= \
                      \mathrm{aufgerundeter\;Wert\;}')
                dm('\\quad\mathrm{der\;rechten\;Intervallgrenze.\;Damit\;ist\;} \\overline{A} = \{K,\,K+1,...,n\}')				
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;} X \\in \\overline{A} \mathrm{,\;so\;wird\;H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höchstens\;} \\alpha \mathrm{\;abge-}')
                dm('\\quad\mathrm{lehnt,\;sonst\;wird\;H_0\;beibehalten}')

            elif verf in ('B', 'BV'):
                dm('\mathrm{Benutzung\; der\;Binomialverteilung}')
                print(' ')				
                dm('\mathrm{H_0}: \;p \le p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\gt p_0 \\quad \mathrm{(Gegenhypothese) \\quad rechtsseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Festlegung\; der\; Prüfgröße\; } X \mathrm{\;(Anzahl\; Treffer)\; auf\; der\; ' + \
                   'Grundlage\; einer\; Stichprobe \;}')				
                dm('\mathrm{\\quad  des\; Umfangs\;} n.\mathrm{Unter\;H_0\;ist\;}' + \
                   ' X  \mathrm{\;binomialverteilt\;mit\;den\;Parametern\;}' + \
                   'n \mathrm{\;und\;} p_0')
                dm('\mathrm{3.\; Ermittlung\;der\;kritischen\;Zahl\;} K \mathrm{\;als\;der\;kleinsten\;Zahl\;aus}\;' + \
                   '\{0....,n\}, \mathrm{\;für\; die\;} ')
                dm('\\quad P(\,X \\ge K\,) \\le \\alpha ' + \
                   '\;\; \mathrm{gilt,\; mittels\; Berechnung\; nach\; der\; Formel}') 
                dm('\quad P(X \\ge K) = 1-F(n,\,p_0,\,K-1) = \\sum_{i=K}^n' + \
                   '{n \choose i}\, p_0^i \,(1-p_0)^{n-i}')
                dm('\\quad \mathrm{unter\;Beachtung\;von\;} 1-\\alpha \\le F(n,\,p_0,\,K-1)'  + \
                   '\mathrm{,\;wobei\;} F \mathrm{\;die\;' + \
                   'Verteilungsfunktion}')
                dm('\\quad\mathrm{der\;Binomialverteilung\;ist}')
                dm('\\quad\mathrm{Ablehnungsbereich\;ist\;\;} \\overline{A} = \{K+1,\,K+2,...,n\}')
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;} X \\in \\overline{A} \mathrm{,\;so\;wird\;H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höchstens\;} \\alpha')
                dm('\\quad\mathrm{abgelehnt,\;sonst\;wird\;H_0\;beibehalten}')
				
            else:
                dm('\mathrm{Benutzung\; der\; Approximation\; durch\; die\; Normalverteilung}')
                print(' ')				
                dm('\mathrm{H_0}: \;p \le p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\gt p_0 \\quad \mathrm{(Gegenhypothese) \\quad rechtsseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Bestimmung\;von\;} c_\\alpha \mathrm{\;aus\;der\;Gleichung\;\;} \\Phi(c_\\alpha) = 1-\\alpha')				
                dm('\\quad (\\Phi \mathrm{-Verteilungsfunktion\;der\;(0,1)-Normalverteilung)}')				
                dm('\mathrm{3.\; Ermittlung\; der\; Prüfgröße\; } h_n \mathrm{\;(relative\; Trefferhäufigkeit)\; auf\; der\; ' + \
                   'Grundlage\; einer}')
                dm('\\quad \mathrm{ Stichprobe \;des\;Umfangs\;} n')				
                dm('\\quad \mathrm{Der\;Ablehnungsbereich\;wird\;durch\;das\;Kriterium\;}' + \
                   'h_n \\gt p_0+c_\\alpha \\sqrt{ \\frac{p_0(1-p_0)}{n}}') 
                dm('\\quad \mathrm{\;bestimmt}')
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;das\;Kriterium\;erfüllt,\;wird\;H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höch-}')
                dm('\\quad\mathrm{stens\;} \\alpha \mathrm{\;abgelehnt,\;sonst\;wird\;H_0\;beibehalten}')

        else:
            if verf in ('S', 'Sigma'):
                dm('\mathrm{Benutzung\; der\;} \\sigma \mathrm{-Umgebungen\; des\; Erwartungswertes}')
                print(' ')				
                dm('\mathrm{H_0}: \;p = p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\ne p_0 \\quad \mathrm{(Gegenhypothese) \\quad zweiseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Festlegung\; der\; Prüfgröße\; } X \mathrm{\;(Anzahl\; Treffer)\; auf\; der\; ' + \
                   'Grundlage\; einer\; Stichprobe \;}')				
                dm('\mathrm{\\quad  des\; Umfangs\;} n.\mathrm{Unter\;H_0\;ist\;}' + \
                   '\; X  \mathrm{\;binomialverteilt\;mit\;den\;Parametern\;}' + \
                   'n \mathrm{\;und\;} p_0 \mathrm{\;und\;}')
                dm('\\quad \mathrm{hat\; den\;Erwartungswert\;\;} \\mu = n\,p_0, \mathrm' + \
                   '{\;die\; Standardabweichung\; ist\;\;}\\sigma = \\sqrt{n \, p_0 \,(1-p_0)}' )				
                dm('\mathrm{3.\; Ermittlung\; der\; } \\sigma \mathrm{-Umgebung \;anhand\; von\; } \\alpha ')
                dm('\\quad \mathrm{Bei\; } \\alpha = 0.05 \mathrm{\;liegt\; mit\; einer\; Wahrscheinlichkeit\; von\;}' + \
                   '1-\\alpha =0.95 \mathrm{\;ein\; Versuchsergeb-}')
                dm('\\quad \mathrm{nis\; in\; der\; 1.96\\sigma-Umgebung\; des\; Erwartungswertes}\;\;[ \\mu - ' + \
                   '1.96 \, \\sigma, \;\mu + 1.96 \, \\sigma]')
                dm('\\quad \mathrm{Bei\; } \\alpha = 0.1 \mathrm{\;liegt\; mit\; einer\; Wahrscheinlichkeit\; von\;}' + \
                   '1-\\alpha =0.9 \mathrm{\;ein\; Versuchsergeb-}')
                dm('\\quad \mathrm{nis\; in\; der\; 1.64\\sigma-Umgebung\; des\; Erwartungswertes}\;\;[ \\mu - ' + \
                   '1.64 \, \\sigma, \;\mu + 1.64 \, \\sigma]')
                dm('\\quad \mathrm{Die\; Wahrscheinlichkeit\; für\; ein\; Ergebnis\; außerhalb\; des\; Intervalls\; ' + \
                   'ist\;jeweils\; } \\alpha')
                dm('\\quad \mathrm{Als\; Ablehnungsbereich\;} \\overline{A} \mathrm{\;der\; Hypothese\;H_0\;wird\; \
                       der\; Bereich\; außerhalb\;des\;In-}')
                dm('\\quad \mathrm{tervalles\;festgelegt.Die\;Grenzen\; (kritische\; Zahlen)\; sind}')
                dm('\\quad  L= \mathrm{abgerundeter\;Wert\;der\;linken\;Intervallgrenze}')
                dm('\\quad  K= \mathrm{aufgerundeter\;Wert\;der\;rechten\;Intervallgrenze}')
                dm('\\quad \mathrm{Damit\;ist\;} \\overline{A} = \{0,\,1,...,L\} \\cup \{K,\, K+1,...,n\}')				
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;} X \\in \\overline{A} \mathrm{,\;so\;wird\;H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höchstens\;} \\alpha \mathrm{\;abge-}')
                dm('\\quad\mathrm{lehnt,\;sonst\;wird\;H_0\;beibehalten}')
				
            elif verf in ('B', 'BV'):
                dm('\mathrm{Benutzung\; der\;Binomialverteilung}')
                print(' ')				
                dm('\mathrm{H_0}: \;p = p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\ne p_0 \\quad \mathrm{(Gegenhypothese) \\quad zweiseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Festlegung\; der\; Prüfgröße\; } X \mathrm{\;(Anzahl\; Treffer)\; auf\; der\; ' + \
                   'Grundlage\; einer\; Stichprobe \;}')				
                dm('\mathrm{\\quad  des\; Umfangs\;} n.\mathrm{Unter\;H_0\;ist\;}' + \
                   'X  \mathrm{\;binomialverteilt\;mit\;den\;Parametern\;}' + \
                   'n \mathrm{\;und\;} p_0')
                dm('\mathrm{3.\; Ermittlung\;der\;kritischen\;Zahlen\;} K \mathrm{\;und\;} L \mathrm{\;aus\;den\;Bedingungen}')				
                dm('\\quad P(\,X \\le K\,) \\le \\frac{\\alpha}{2}' + \
                   '\\quad\mathrm{(größte\;solche\;Zahl)}')
                dm('\\quad P(\,X \\ge L\,) \\le \\frac{\\alpha}{2} \mathrm{\\quad(kleinste\;solche\;Zahl)};' + \
                   '\\quad K, L \in \{0,1,...,n\}')
                dm('\\quad \mathrm{\;Berechnung\; von\;} K \\qquad P(\, X \\le K\, ) = \\sum_{i=0}^K' + \
                   '{n \choose i}\, p_0^i \,(1-p_0)^{n-i} = F(n,\,p_0,\,K)')
                dm('\\qquad\\qquad\\qquad\\qquad\\qquad F(n,\,p_0,\,K) \\le \\frac{\\alpha}{2}')				   
                dm('\\quad \mathrm{\;Berechnung\; von\;} L \\qquad P(\,X \\ge L\,) = \\sum_{i=L}^n' + \
                   '{n \choose i}\, p_0^i \,(1-p_0)^{n-i} =1-F(n,\,p_0,\,L-1)')
                dm('\\qquad\\qquad\\qquad\\qquad\\qquad 1-\\frac{\\alpha}{2} \\le F(n,\,p_0,L-1)')				   
                dm('\\quad \mathrm{\;mit\;} F \mathrm{-Verteilungsfunktion\; der\; Binomialverteilunng}')
                dm('\\quad\mathrm{Ablehnungsbereich\;ist\;\;} \\overline{A} = \{0,\,1,...,K\} \\cup \{L,\,L+1,...,n\}')
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;} X \\in \\overline{A} \mathrm{,\;so\;wird\;H_0\;mit\;einer\; \
                      Irrtumswahrscheinlichkeit\;von\;höchstens\;} \\alpha ')
                dm('\\quad\mathrm{abgelehnt,\;sonst\;wird\;H_0\;beibehalten}')
				
            else:
                dm('\mathrm{Benutzung\; der\; Approximation\; durch\; die\; Normalverteilung}')
                print(' ')				
                dm('\mathrm{H_0}: \;p = p_0 \\quad \mathrm{(Nullhypothese) \\quad   gegen}')				
                dm('\mathrm{H_1}: \;p \\ne p_0 \\quad \mathrm{(Gegenhypothese) \\quad zweiseitiger\;Test}')	
                print(' ')
                dm('\mathrm{1.\; Vorgabe\; des\; Signifikanzniveaus\;} \\alpha')
                dm('\mathrm{2.\; Bestimmung\;von\;} c_\\alpha \mathrm{\;aus\;der\;Gleichung\;\;} \\Phi(c_\\alpha) = ' + \
		            '1-\\frac{\\alpha}{2}')				
                dm('\\quad (\\Phi \mathrm{-Verteilungsfunktion\;der\;(0,1)-Normalverteilung)}')				
                dm('\mathrm{3.\; Ermittlung\; der\; Prüfgröße\; } h_n \mathrm{\;(relative\; Trefferhäufigkeit)\; auf\; der\; ' + \
                   'Grundlage\; einer}')
                dm('\\quad \mathrm{ Stichprobe \;des\;Umfangs\;} n')				
                dm('\\quad \mathrm{Der\;Ablehnungsbereich\;wird\;durch\;das\;Kriterium\;}' + \
                   '\\left|\,h_n-p_0 \\right| \\gt c_\\alpha \\sqrt{ \\frac{p_0(1-p_0)}{n}}') 
                dm('\\quad \mathrm{\;bestimmt}')
                dm('\mathrm{4.\; Entscheidung\; nach\;der\;Regel }')
                dm('\\quad\mathrm{Ist\;das\;Kriterium\;erfüllt,\;wird\;H_0\;mit\;einer\; \
                   Irrtumswahrscheinlichkeit\;von\;höch-}')
                dm('\\quad\mathrm{stens\;} \\alpha \mathrm{\;abgelehnt,\;sonst\;wird\;H_0\;beibehalten}')

        print(' ')			
				
    @property
    def ab_ber(self):
        """Ablehnungsbereich von :math:`H_0`"""
		
        nv = NormalVerteilung(0, 1)		
        n, bv, alpha = self.n, self.bv, self.sig_niv 
        p0, seite, verf = self.args[0], self.args[2], self.args[4]
        if seite in ('l', 'links'):
            if verf in ('S', 'Sigma'):
                K = ceiling(bv.erw - 1.64*bv.sigma)
                ab = {i for i in range(K)}

            elif verf in ('B', 'BV'):
                grenz = bv.quantil(alpha) - 1
                ab = {i for i in range(grenz+1)}				
            else:
                c = nv.quantil(1-alpha)
                krit = p0 - c*sqrt(p0*(1-p0)/n)
                krit = ceiling(n*krit) - 1
                ab = {i for i in range(krit+1)}				
        elif seite in ('r', 'rechts'):
            if verf in ('S', 'Sigma'):
                L = floor(bv.erw + 1.64*bv.sigma)+1
                ab = {i for i in range(L+1, n+1)}
            elif verf in ('B', 'BV'):
                grenz = bv.quantil(1-alpha)+1
                ab = {i for i in range(grenz, n+1)}				
            else:
                c = nv.quantil(1-alpha)
                krit = p0 + c*sqrt(p0*(1-p0)/n)
                krit = floor(n*krit) + 1
                ab = {i for i in range(krit, n+1)}         
        else:
            if verf in ('S', 'Sigma'):
                fakt = 1.64 if alpha == 0.1 else 1.96
                K = ceiling(bv.erw - fakt*bv.sigma) 
                L = floor(bv.erw + fakt*bv.sigma)
                ab = {i for i in range(K)}.union({i for i in range(L+1, n+1)})
            elif verf in ('B', 'BV'):
                K = ceiling(bv.quantil(Rational(alpha, 2)) - 1)
                L = floor(bv.quantil(1-Rational(alpha, 2)) + 1)
                ab = {i for i in range(K)}.union({ i for i in range(L, n+1)})
            else:
                c = nv.quantil(1-Rational(alpha, 2))			
                krit1 = p0 - c*sqrt(p0*(1-p0)/n)
                krit2 = p0 + c*sqrt(p0*(1-p0)/n)
                krit1 = ceiling(n*krit1) - 1
                krit2 = floor(n*krit2) + 1 
                ab= {i for i in range(krit1+1)}.union({i for i in range(krit2, n+1)})
        return ab				
    def ab_ber_(self, **kwargs):
        """ebenso; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   g=ja   grafische Darstellung\n")
            return  
        ab_ber, om = self.ab_ber, self.bv.omega
        mark = []		
        for k in om:	
            if k in ab_ber:	
                mark += [k]			
        if kwargs.get('g'):		
            balken1(self.bv._vert, typ='W', titel='Annahmebereich (hell) und ' + \
                      'Ablehnungsbereich (dunkel)\nvon $H_0$\n', mark=mark)	
            return			
        return self.ab_ber		
						
    abBer = ab_ber
    AbBer = ab_ber_
	
    @property
    def an_ber(self):
        """Annahmebereich von :math:`H_0`"""
        ab, om = self.ab_ber, self.bv.omega
        return om.difference(ab)		
    def an_ber_(self, **kwargs):
        """ebenso; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   g=ja   grafische Darstellung\n")
            return  
        ab_ber, om = self.ab_ber, self.bv.omega
        mark = []		
        for k in om:	
            if k in ab_ber:	
                mark += [k]			
        if kwargs.get('g'):		
            balken1(self.bv._vert, typ='W', titel='Annahmebereich (hell) und ' + \
                      'Ablehnungsbereich (dunkel)\nvon $H_0$\n', mark=mark)	
            return			
        return self.an_ber		

    anBer = an_ber
    AnBer = an_ber_
		
    @property
    def k(self):
        """Kritische Zahl(en)"""
        ab, bv, alpha, seite, verf = self.ab_ber, self.bv, self.args[1], \
		                             self.args[2], self.args[4]
        if	seite in ('l', 'links'):
            return max(ab)
        elif seite in ('r', 'rechts'):
            return min(ab) - 1
        else:			
            if verf in ('S', 'Sigma'):
                fakt = 1.64 if alpha == 0.1 else 1.96
                K = ceiling(bv.erw - fakt*bv.sigma) 
                L = floor(bv.erw + fakt*bv.sigma)
                return K, L
            elif verf in ('B', 'BV'):
                K = max(self.an_ber)
                L = ceiling(bv.quantil(1-Rational(alpha, 2)) + 1)
                return K, L
            else:
                p0, n = self.args[0], self.args[3] 			
                nv = NormalVerteilung(0, 1)					
                c = nv.quantil(1-Rational(alpha, 2))			
                krit1 = p0 - c*sqrt(p0*(1-p0)/n)
                krit2 = p0 + c*sqrt(p0*(1-p0)/n)
                krit1 = ceiling(n*krit1) - 1
                krit2 = floor(n*krit2) + 1 
                return krit1, krit2
		
    K = k		
		
    def guete(self, *args, **kwargs):
        """Güte-Funktion"""
        if kwargs.get('h'):
            print("\nGüte-Funktion   (SignifikanzTestP)\n")
            print("Aufruf   t . güte( p )\n")		                     
            print("             t    SignifikanzTestP")
            print("             p    Zahl aus [0,1]\n")
            print("Zusatz   g=ja   Graf der Funktion\n")			
            return
        if kwargs.get('g'):
            return _grafik_guete(self)				
        if len(args) != 1:
            print('zufall: ein Argument angeben')	 
            return
        p = float(args[0])			
        if not (isinstance(p, (Rational, float, Float)) and 0<=p<=1):
            print('zufall: Zahl aus dem Intervall [0,1] angeben')	
            return
        K, seite, n = self.k, self.args[2], self.args[3]
        p0 = float(self.args[0])		
        def guete(p):
            F = BinomialVerteilung(n, p).F		
            if seite in ('l', 'links'):
                if p <= p0:
                   return float(F(K))
            elif seite in ('r', 'rechts'):
                if p >= p0:
                    return float(1 - F(K-1))					
            else:
                return float(F(K[0]) + 1 - F(K[1]-1))
        return guete(p)					  
 																
		
    def oc(self, *args, **kwargs):
        """Operationscharakteristik"""
        if kwargs.get('h'):
            print("\nOperationscharakteristik-Funktion   (SignifikanzTestP)\n")
            print("Aufruf   st . oc( p )\n")		                     
            print("              st     SignifikanzTestP")
            print("              p      Zahl aus [0,1]\n")
            print("Zusatz   g=ja   Graf der Funktion\n")			
            return
        if kwargs.get('g'):
            return _grafik_oc(self)							
        if len(args) != 1:
            print('zufall: ein Argument angeben')	 
            return
        p = float(args[0])			
        if not (isinstance(p, (Rational, float, Float)) and 0<=p<=1):
            print('zufall: Zahl aus dem Intervall [0,1] angeben')	
            return
        if self.guete(p):			
            return 1.0 - self.guete(p)					  
		
    beta = oc		
		

    @property
    def regel(self):
        """Entscheidungsregel"""
		
        def dm(x):
            return display(Math(x))	
			
        print('')	
        dm('\mathrm{Ermittlung\; der\; Entscheidungsregel\; für\; den\; Signifikanztest}')
        seite, verf = self.args[2], self.args[4]
        p0, alpha, n = self.args[0], self.args[1], self.args[3]
        if verf in ('B', 'BV', 'N', 'NV'):		
            bv = self.bv
            K = self.K			
        if verf in ('N', 'NV'):
            nv0 = NormalVerteilung(0, 1)		
        sp, sa = str(p0), str(alpha)
        if seite in ('l', 'links'):
            ss = 'links'		
        elif seite in ('r', 'rechts'):
            ss = 'rechts'	
        else:
            ss = 'zwei'
        smy = '{0:.2f}'.format(float(self.bv.erw))
        ssi = '{0:.4f}'.format(float(self.bv.sigma))
        if verf in ('S', 'Sigma') and alpha == 0.1:		
            g1 = '{0:.2f}'.format(float(self.bv.erw - 1.64*self.bv.sigma))		
            g2 = '{0:.2f}'.format(float(self.bv.erw + 1.64*self.bv.sigma))	
        elif verf in ('S', 'Sigma') and alpha == 0.05:			
            g1 = '{0:.2f}'.format(float(self.bv.erw - 1.96*self.bv.sigma))		
            g2 = '{0:.2f}'.format(float(self.bv.erw + 1.96*self.bv.sigma))	
        if seite in ('l', 'links'):		
            if verf in ('S', 'Sigma'):
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p \ge' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße}\;\; X=\,\mathrm{"Anzahl\;Treffer", \;\;} \\mu=' + smy + \
                  ',\;\\sigma=' + ssi)
                dm('\mathrm{1.64\,\\sigma-Umgebung\;des\;Erwartungswertes}')
                dm('\\qquad [\, \\mu-1.64\,\\sigma,\; \\mu+1.64\,\\sigma\, ] = [' + g1 + ',\;' + g2 + ']')
                dm('\mathrm{Kritische\;Zahl\;\;}' + str(floor(g1)))
                dm('\mathrm{Ablehnungsbereich\;für\;H_0\;\;} X  \\le' + str(floor(g1)))
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Liegt\;der\;Wert\;der\;Prüfgröße\;im\;Ablehnungsbereich,\;wird\;H_0\;abgelehnt,\;sonst}')
                dm('\mathrm{wird\;H_0\;beibehalten}')                				 
            elif verf in ('B', 'BV'):
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p \ge' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\\text{Prüfgröße}  \;\; X=\\text{"Anzahl Treffer"}') 
                dm('\\qquad\\text{Verteilung von }X\;\;' + \
                   latex(bv))
                dm('\mathrm{Kritische\;Zahl\;\;}' + str(K))
                dm('\mathrm{Ablehnungsbereich\;für\;}H_0\;\; X  \\le' + str(K))
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Liegt\;der\;Wert\;der\;Prüfgröße\;im\;Ablehnungsbereich,\;wird\;} H_0\\text{ mit einer' + \
                   ' Irrtums-}')
                dm('\mathrm{wahrscheinlichkeit\;von\;höchstens\;}'+ sa + '\mathrm{\;abgelehnt,\;sonst\;' + \
                   'wird\;}H_0\\text{ beibehalten}')                				 				
            else:
                q = nv0.quantil(1-alpha)	
                g = p0 - q*sqrt(p0*(1-p0)/n)
                sq = '{0:.5}'.format(float(q))				
                sg = '{0:.5}'.format(float(g))				
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p \ge' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße\;\;} X=\,\mathrm{"Relative\;Trefferhäufigkeit"}')
                dm('\\qquad\mathrm{Verteilung\;von}\;X' + \
                   '\\quad ' + latex('NormalVerteilung(' + str(p0) + ',\,' + \
                   '{0:.4f}'.format(float(p0*(1-p0)/n)) + ')'))					
                print(' ')				  
                dm('\mathrm{Die\;Bestimmung\;von\;}c_\\alpha\mathrm{\;aus\;der\;Gleichung\;}' + \
                  '\\Phi(c_\\alpha) =' + latex(1-alpha) + '\mathrm{\;ergibt\;\;}' + \
                   'c_\\alpha =' +'{0:.4f}'.format(q))
                dm('\mathrm{(siehe\;Quantile\;der\;Normalverteilung\;oder\;untere\;Grafik;\;sie\;zeigt\;die\;' + \
			        'Vertei-}')
                dm('\mathrm{lungsfunktion\;der\;(0,1)-Normalverteilung\;(Ausschnitt)})')
                print(' ')				   
                _grafik_nv()					
                dm('\mathrm{Die\;Berechnung\;der\;Grenze\;des\;Ablehnungsbereiches\;ergibt\;\;}')
                dm('\\qquad ' + str(p0) + '-' + \
                  sq + '\,\\sqrt{\\frac{' + str(p0) + '\\cdot' + str(1-p0) +'}{' + str(n) + \
                  '}} =' + sg)
                print(' ')				  
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Ist\;die\;relative\;Trefferhäufigkeit\;} \\gt' + sg + \
                   '\mathrm{,\;so\;wird\;H_0} \mathrm{\;mit\;einer\;Irrtums-}')
                dm('\mathrm{wahrscheinlichkeit\;von\;}' + str(alpha)+ '\mathrm{\;abgelehnt,\;sonst\;wird\; H_0} ' + \
                   '\mathrm{\;beibehalten}')	
                print(' ')				   
                dm('\mathrm{oder\;\;\;(Verwendung\;der\;absoluten\;Trefferhäufigkeit)}')
                dm('\mathrm{Multiplikation\;des\;Grenzwertes\;mit\;} n =' + str(n) + '\mathrm{\;ergibt\;}' + \
                   str(floor(g*n)) + '\mathrm{\;(Rundung\;in\;sicherer\;Richtung)}')				
                dm('\mathrm{Ablehnungsbereich\;\;} X \\le' + str(floor(g*n)))
                dm('\mathrm{Fällt\;die\;absolute\;Trefferhäufigkeit\;} X \mathrm{\;in\;den\;' + \
                  'Ablehnungsbereich,\;so\;wird\;H_0} \mathrm{\;mit\;der}')
                dm('\mathrm{Irrtumswahrscheinlichkeit\;}' + str(alpha) + \
                   '\mathrm{\;abgelehnt,\;sonst\;wird\; H_0} \mathrm{\;beibehalten}')				
        elif seite in ('r', 'rechts'):
            if verf in ('S', 'Sigma'):
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p \le' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße}\;\; X=\,\mathrm{"Anzahl\;Treffer", \;\;} \\mu=' + smy + \
                   ',\;\\sigma=' + ssi)
                dm('\mathrm{1.64\,\\sigma-Umgebung\;des\;Erwartungswertes}')
                dm('\\qquad [\, \\mu-1.64\,\\sigma,\; \\mu+1.64\,\\sigma\, ] = [' + g1 + ',\;' + g2 + ']')
                dm('\mathrm{Kritische\;Zahl\;\;}' + str(ceiling(g2)))
                dm('\mathrm{Ablehnungsbereich\;für\;H_0\;\;} X  \\ge' + str(ceiling(g2)))
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Liegt\;der\;Wert\;der\;Prüfgröße\;im\;Ablehnungsbereich,\;wird\;}H_0 \
	                  \mathrm{\;abgelehnt,\;sonst}')
                dm('\mathrm{wird\;}H_0\mathrm{\;beibehalten}')                				 
            elif verf in ('B', 'BV'):
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p \le' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße\;\;} X=\,\mathrm{"Anzahl\;Treffer"}')
                dm('\mathrm{Verteilung\;von}\;X\;\;' + latex(bv))
                dm('\mathrm{Kritische\;Zahl\;\;}' + str(self.K))
                dm('\mathrm{Ablehnungsbereich\;für\;H_0\;\;} X  \\ge' + str(self.K + 1))
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Liegt\;der\;Wert\;der\;Prüfgröße\;im\;Ablehnungsbereich,\;wird\;H_0\;mit\;einer}') 
                dm('\mathrm{Irrtumswahrscheinlichkeit\;von\;höchstens\;}'+ sa + '\mathrm{\;abgelehnt,\;sonst\;}')
                dm('\mathrm{wird\;H_0\;beibehalten}')                				 								
            else:
                q = nv0.quantil(1-alpha)	
                g = p0 + q*sqrt(p0*(1-p0)/n)
                sq = '{0:.5}'.format(float(q))				
                sg = '{0:.5}'.format(float(g))				
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0:} \;p \le' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße\;\;} X=\,\mathrm{"Relative\;Trefferhäufigkeit"}')
                dm('\\qquad\mathrm{Verteilung\;von}\;X' + \
                '\\quad ' + latex('NormalVerteilung(' + str(p0) + ',' + '\, {0:.4f}'.format(float(p0*(1-p0)/n)) + \
                    ')'))					
                print(' ')				  
                dm('\mathrm{Die\;Bestimmung\;von\;}c_\\alpha\mathrm{\;aus\;der\;Gleichung\;}' + \
                  '\\Phi(c_\\alpha) =' + latex(1-alpha) + '\mathrm{\;ergibt\;\;}' + \
                   'c_\\alpha =' +'{0:.4f}'.format(q))
                dm('\mathrm{(siehe\;Quantile\;der\;Normalverteilung\;oder\;untere\;Grafik;\;sie\;zeigt\;die\;' + \
			        'Vertei-}')
                dm('\mathrm{lungsfunktion\;der\;(0,1)-Normalverteilung\;(Ausschnitt)})')
                print(' ')				   
                _grafik_nv()					
                dm('\mathrm{Die\;Berechnung\;der\;Grenze\;des\;Ablehnungsbereiches\;ergibt\;\;}')
                dm('\\qquad ' + str(p0) + '+' + \
                  sq + '\,\\sqrt{\\frac{' + str(p0) + '\\cdot' + str(1-p0) +'}{' + str(n) + \
                  '}} =' + sg)
                print(' ')				  
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Ist\;die\;relative\;Trefferhäufigkeit\;} \\gt' + sg + \
                   '\mathrm{,\;so\;wird \;H_0} \mathrm{\;mit\;einer\;Irrtums-}')
                dm('\mathrm{wahrscheinlichkeit\;von\;}' + str(alpha)+ '\mathrm{\;abgelehnt,\;sonst\;wird\; H_0} ' + \
                   '\mathrm{\;beibehalten}')	
                print(' ')				   
                dm('\mathrm{oder\;\;\;(Verwendung\;der\;absoluten\;Trefferhäufigkeit)}')
                dm('\mathrm{Multiplikation\;des\;Grenzwertes\;mit\;} n =' + str(n) + '\mathrm{\;ergibt\;}' + \
                   str(ceiling(g*n)) + '\mathrm{\;(Rundung\;in\;sicherer\;Richtung)}')				
                dm('\mathrm{Ablehnungsbereich\;\;} X \\ge' + str(ceiling(g*n)))
                dm('\mathrm{Fällt\;die\;absolute\;Trefferhäufigkeit\;} X \mathrm{\;in\;den\;' + \
                  'Ablehnungsbereich,\;so\;wird\; H_0} \mathrm{\;mit\;der}')
                dm('\mathrm{Irrtumswahrscheinlichkeit\;}' + str(alpha) + \
                   '\mathrm{\;abgelehnt,\;sonst\;wird \;H_0} \mathrm{\;beibehalten}')				
        else:
            if verf in ('S', 'Sigma'):
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p=' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße}\;\; X=\,\mathrm{"Anzahl\;Treffer", \;\;} \\mu=' + smy + ',\;\\sigma=' + ssi)
                if alpha ==0.1:				
                    dm('\mathrm{1.64\,\\sigma-Umgebung\;des\;Erwartungswertes}')
                    dm('\\qquad [\, \\mu-1.64\,\\sigma,\; \\mu+1.64\,\\sigma\, ] = [' + g1 + ',\;' + g2 + ']')
                elif alpha == 0.05:					
                    dm('\mathrm{1.96\,\\sigma-Umgebung\;des\;Erwartungswertes}')
                    dm('\\qquad [\, \\mu-1.96\,\\sigma,\; \\mu+1.96\,\\sigma\, ] = [' + g1 + ',\;' + g2 + ']')
                dm('\mathrm{Kritische\;Zahlen\;\;}' + str(floor(g1)) + ',\;' + str(ceiling(g2)))
                dm('\mathrm{Ablehnungsbereich\;für\;H_0\;\;} X  \\le' + str(floor(g1)) + \
                  '\mathrm{\;\;oder\;\; X \\ge}' + str(ceiling(g2)))
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Liegt\;der\;Wert\;der\;Prüfgröße\;im\;Ablehnungsbereich,\;wird\;H_0\;abgelehnt,\;sonst}')
                dm('\mathrm{wird\;H_0\;beibehalten}')                				 
				
            elif verf in ('B', 'BV'):
                dm('\mathrm{Gegeben}')
                dm('\\qquad \mathrm{H_0}:\;p=' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße\;\;} X=\,\mathrm{"Anzahl\;Treffer"}')
                dm('\\qquad\mathrm{Verteilung\;von}\;X\;\;' + latex(bv))
                dm('\mathrm{Kritische\;Zahlen\;\;}' + str(K[0]) + ',\;' + str(K[1]))
                dm('\mathrm{Ablehnungsbereich\;für\;H_0\;\;\;} X  \\le' + str(K[0]) + \
                  '\mathrm{\;\;oder\;\;} X \\ge' + str(K[1]) )
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Liegt\;der\;Wert\;der\;Prüfgröße\;im\;Ablehnungsbereich,\;wird\;H_0\;mit\;einer' + \
                   '\;Irrtums-}')
                dm('\mathrm{wahrscheinlichkeit\;von\;höchstens\;}'+ sa + '\mathrm{\;abgelehnt,\;sonst\;' + \
                   'wird\;H_0\;beibehalten}')                				 								
            else:
                q = nv0.quantil(1-alpha/2)	
                g1 = p0 - q*sqrt(p0*(1-p0)/n)
                g2 = p0 + q*sqrt(p0*(1-p0)/n)
                sq = '{0:.5}'.format(float(q))				
                sg1 = '{0:.5}'.format(float(g1))				
                sg2 = '{0:.5}'.format(float(g2))				
                dm('\mathrm{Gegeben}')
                dm('\\qquad\mathrm{H_0:}\;p=' + sp)
                dm('\\qquad\\alpha=' + sa + ',\;n=' + str(n) + ',\;' + \
                   '\mathrm{' + ss + 'seitiger\;Test}')			
                dm('\\qquad\mathrm{Prüfgröße\;\;} X=\,\mathrm{"Relative\;Trefferhäufigkeit"}')
                dm('\\quad\mathrm{Verteilung\;von}\;X' + \
                   '\\quad ' + latex('NormalVerteilung(' + str(p0) + ',\;' + \
				      '{0:.4f}'.format(float(p0*(1-p0)/n)) + ')'))					
                print(' ')				  
                dm('\mathrm{Die\;Bestimmung\;von\;}c_\\alpha\mathrm{\;aus\;der\;Gleichung\;}' + \
                  '\\Phi(c_\\alpha) =' + latex(1-alpha/2) + '\mathrm{\;ergibt\;\;}' + \
                   'c_\\alpha =' +'{0:.4f}'.format(q))
                dm('\mathrm{(siehe\;Quantile\;der\;Normalverteilung\;oder\;untere\;Grafik;\;sie\;zeigt\;die\;' + \
			        'Vertei-}')
                dm('\mathrm{lungsfunktion\;der\;(0,1)-Normalverteilung\;(Ausschnitt)})')
                print(' ')				   
                _grafik_nv()					
                dm('\mathrm{Die\;Berechnung\;der\;Grenzen\;des\;Ablehnungsbereiches\;ergibt\;\;}')
                dm('\\qquad' + str(p0) + '-' + sq + '\,\\sqrt{\\frac{' + str(p0) + '\\cdot' + str(1-p0) + \
                  '}{' + str(n) + \
                  '}} =' + sg1)
                dm('\\qquad' + str(p0) + '+' + sq + '\,\\sqrt{\\frac{' + str(p0) + '\\cdot' + str(1-p0) + \
                  '}{' + str(n) + \
                  '}} =' + sg2)
                print(' '	)			  
                dm('\mathrm{Entscheidungsregel}')
                dm('\mathrm{Ist\;die\;relative\;Trefferhäufigkeit\;} \\lt' + sg1 + \
                    '\mathrm{\;\;oder\;\;} \\gt ' + sg2 + ',')				
                dm('\mathrm{so\;wird\;H_0} \mathrm{\;mit\;einer\;Irrtums-' + \
                   'wahrscheinlichkeit\;von\;}' + str(alpha)+ '\mathrm{\;abgelehnt,\;sonst\;wird\; H_0} ')
                dm('\mathrm{\;beibehalten}')	
                print(' ')				   
                dm('\mathrm{oder\;\;\;(Verwendung\;der\;absoluten\;Trefferhäufigkeit)}')
                dm('\mathrm{Multiplikation\;der\;Grenzwerte\;mit\;} n =' + str(n) + '\mathrm{\;ergibt\;}' + \
                   str(floor(g1*n)) + ',\;' + str(ceiling(g2*n)) + '\mathrm{\;\;(Rundung\;in\;sicherer}')
                dm('\mathrm{Richtung)}')				
                dm('\mathrm{Ablehnungsbereich\;\;\;} X \\le' + str(floor(g1*n)) + '\mathrm{\;\;oder\;\;}'+ \
                   'X \\ge' + str(ceiling(g2*n)))
                dm('\mathrm{Fällt\;die\;absolute\;Trefferhäufigkeit\;} X \mathrm{\;in\;den\;' + \
                  'Ablehnungsbereich,\;so\;wird\;H_0} \mathrm{\;mit\;der}')
                dm('\mathrm{Irrtumswahrscheinlichkeit\;}' + str(alpha) + \
                   '\mathrm{\;abgelehnt,\;sonst\;wird\; H_0} \mathrm{\;beibehalten}')				
        print(' ')		
    def regel_(self, **kwargs):
        """ebenso; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   g=ja   grafische Darstellung\n")
            return  
        self.regel
        if kwargs.get('g'):
            self.an_ber_(g=1)		
		
    Regel = regel_		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        signifikanz_test_p_hilfe(3)	
		
    h = hilfe					

	

def signifikanz_test_p_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
SignifikanzTestP - Objekt     Signifikanztest für die unbekannte Wahr-
                              scheinlichkeit der Binomialverteilung

Kurzname     STP
		
Erzeugung    STP( p0, alpha, seite, umfang, verfahren )

                  p0          Wahrscheinlchkeit bei H0
                  alpha       Signifikanzniveau, Zahl aus (0,1)
                  seite       '2' | 'l' | 'r'  oder 
                              'zwei' | 'links' | 'rechts' 
                              zwei-, links- oder rechtsseitiger Test   				 
                  umfang      Stichprobenumfang	
                  verfahren   'S' | 'Sigma': bei alpha = 0.05 
                                             (einseitiger Test)
                                             bei alpha = 0.05, 0.1 
                                             (zweiseitiger Test)
                                             Benutzung der Sigma-Umgebung 
                                             des Erwartungswertes
                               'B' | 'BV'  : Benutzung der Binomialvertei-
                                             lung selbst	
                               'N' | 'NV'  : Benutzung der Approximation 
                                             durch die Normalverteilung
								 
Zuweisung     st = STP(...)   (st - freier Bezeichner)

Beispiele
STP( 0.4, 0.05, 'links', 56, 'Sigma' )
STP( 0.4, 0.05, '2', 1000, 'B' )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für SignifikanzTestP

st.hilfe               Bezeichner der Eigenschaften und Methoden
st.ab_ber              Ablehnungsbereich für H0
st.ab_ber_(...)     M  ebenso, zugehörige Methode
st.an_ber              Annahmebereich für H0
st.an_ber_(...)     M  ebenso, zugehörige Methode
st.alpha               Wahrscheinlichkeit für Fehler 1. Art
st.begriffe            Begriffe
st.beta(...)        M  = st.oc
st.bv                  Binomialverteilung bei H0
st.güte(...)        M  Gütefunktion
st.h0                  Nullhypothese
st.h1                  Alternativhypothese
st.k                   kritische Zahl(en)
st.n                   Stichprobenumfang
st.oc(...)          M  Operationscharakteristik
st.quantil_bv(...)  M  Quantile der Binomialverteilung st.bv
st.quantil_nv(...)  M  Quantile der (0,1)-Normalverteilung
st.regel               Ermittlung der Entscheidungsregel
st.regel_(...)      M  ebenso, zugehörige Methode
st.schema              Berechnungsschema        
st.sig_niv             Signifikanzniveau

Synonyme Bezeichner

hilfe       h
ab_ber      abBer
an_ber      anBer
beta        oc
beta_       Beta
h0          H0
h1          H1
k           K
quantil_bv  quantilBV
quantil_nv  quantilNV
regel_      Regel
sig_niv     sigNiv
    """)		
        return
	
	
STP = SignifikanzTestP


# Grafiken
# --------

def _grafik_nv():

    def pline(x, y, f):
        return plt.plot(x, y, color=f, lw=0.7)
		
    nv = norm
    fig = plt.figure(figsize=(3.5, 2))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_visible(False)		
    ax.spines['bottom'].set_linewidth(0.5)		
    ax.spines['right'].set_visible(False)		
    ax.spines['left'].set_linewidth(0.5)		
    df = 1
    ax.set_yticks([])
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)		
        tick.label1.set_fontname('Times New Roman')		
    plt.axes().xaxis.set_ticks_position('none')
    for x in (2, 4, 6, 8):		
        pline([x, x], [0.85, 0.853], 'black')
    plt.axes().yaxis.set_ticks_position('none')
    plt.xlim(0, 4)
    plt.ylim(0.85, 1.0)
    x = np.linspace(nv.ppf(0.84), nv.ppf(0.9999999), 100)
    ax.plot(x, nv.cdf(x), 'black', lw=1, alpha=0.5)
    pline([0, nv.ppf(0.9)], [0.90, 0.90], 'b')
    pline([nv.ppf(0.9), nv.ppf(0.9)], [0, 0.90], 'r')
    pline([0, nv.ppf(0.95)], [0.95, 0.95], 'b')
    pline([nv.ppf(0.95), nv.ppf(0.95)], [0, 0.95], 'r')
    pline([0, nv.ppf(0.975)], [0.975, 0.975], 'b')
    pline([nv.ppf(0.975), nv.ppf(0.975)], [0, 0.975], 'r')
    pline([0, nv.ppf(0.99)], [0.99, 0.99], 'b')
    pline([nv.ppf(0.99), nv.ppf(0.99)], [0, 0.99], 'r')
    pline([0, 10], [1.0, 1.0], 'b')	

    def ptext(y, t):
        return ax.text(-0.1, y, t, fontsize=9, horizontalalignment='right', \
              fontname = 'Times New Roman', verticalalignment='center', \
              color=(0,0,0))

    ptext(1.0, '1.0')	
    ptext(0.99, '0.99')
    ptext(0.975, '0.975')
    ptext(0.95, '0.95')
    ptext(0.9, '0.9')
    plt.show()

	
def _grafik_guete(self):
    p0, seite = self.args[0], self.args[2]
    fig = plt.figure(figsize=(3, 2.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0, 1.0])
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Times New Roman')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Times New Roman')
    ax.tick_params(top='off', left='off', bottom='off', right='off')		
    plt.grid()
    plt.xlim(0, 1)	
    plt.ylim(0, 1)	
    plt.title("$\mathrm{Gütefunktion:\;} p \\mapsto P\,(Ablehnung\;von\;H_0)$" + "\n", \
        fontsize=11, loc='left', style='italic')		
    xlabel = "$p$"
    ylabel = "$Güte$"
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    if seite in ('l', 'links'):
        x = np.linspace(0, p0, 50)
    elif seite in ('r', 'rechts'):
        x = np.linspace(p0, 1, 50)
    else:
        x = np.linspace(0, 1, 50)
    def f(p):
        if seite in ('l', 'links'):
            return Piecewise((self.guete(p), p <= p0), (0, p > p0))		
        elif seite in ('r', 'rechts'):
            return Piecewise((0, p <= p0), (self.guete(p), p > p0))
        return self.guete(p)			
    y = [f(p) for p in x]
    ax.plot(x, y, lw=1.5, color='g',alpha=0.8)
    ax.plot((p0, p0), (0, 1), lw=1.5, color='g',alpha=0.8, linestyle='dashed')
    plt.show()	
	
	
def _grafik_oc(self):
    p0, seite = self.args[0], self.args[2]
    fig = plt.figure(figsize=(3, 2.5))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0, 1.0])
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Times New Roman')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
        tick.label1.set_fontname('Times New Roman')
    ax.tick_params(top='off', left='off', bottom='off', right='off')		
    plt.grid()
    plt.xlim(0, 1)	
    plt.ylim(0, 1)	
    plt.title("$\mathrm{OC:\;} p \\mapsto 1-P\,(Ablehnung\;von\;H_0)$" + "\n", \
        fontsize=11, loc='left', style='italic')
    xlabel = "$p$"
    ylabel = "$OC$"
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    if seite in ('l', 'links'):
        x = np.linspace(0, p0, 50)
    elif seite in ('r', 'rechts'):
        x = np.linspace(p0+1e-10, 1, 50)
    else:
        x = np.linspace(0, 1, 50)
    def f(p):
        if seite in ('l', 'links'):
            return Piecewise((self.oc(p), p <= p0), (0, p > p0))		
        elif seite in ('r', 'rechts'):
            return Piecewise((0, p <= p0), (self.oc(p), p > p0))
        return self.oc(p)			
    y = [f(p) for p in x]
    ax.plot(x, y, lw=1.5, color=(0,0,1), alpha=0.8)
    ax.plot((p0, p0), (0, 1), lw=1.5, color='g',alpha=0.8, linestyle='dashed')
    plt.show()	
	