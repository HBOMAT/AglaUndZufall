#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  VierFelderTafel - Klasse  von zufall           
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



import copy
from itertools import product
from inspect import isfunction

from IPython.display import display, Math

import numpy as np
from scipy.stats import chi2

from mpmath import nint

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from sympy.core.numbers import Integer, Rational, Float  
from sympy import Max, binomial
from sympy.core.symbol import Symbol, symbols
from sympy import nsimplify
from sympy.functions.combinatorial.factorials import binomial as B
from sympy import solve

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.zufalls_experiment import ZufallsExperiment 
from zufall.lib.funktionen.funktionen import summe
	
from zufall.lib.objekte.haeufigkeits_baum import HaeufigkeitsBaum	
from zufall.lib.objekte.ausnahmen import ZufallError

import zufall



# VierFelderTafel - Klasse  
# ------------------------
	
class VierFelderTafel(ZufallsObjekt):                                      
    """
	
Vier-Felder-Tafel

**Kurzname** **VT**
	
**Erzeugung** 
	
   VT( *werte /[, bezeichner]* )

**Parameter**

   *werte*: 
      | Liste mit 4 Werten: innere Werte der Tafel
      | Liste mit 9 Werten: alle Werte der Tafel (einschließlich 
	  Randwerte)
      | *x* bzw. '*x*' steht für einen nicht gegebenen Wert
      | die Eingabe der Werte erfolgt zeilenweise
		
   *bezeichner*: 
      | Liste mit den Bezeichnern der Zeilen / Spalten (4 oder 2 Bezeichner; 
      | bei 2 Bezeichnern wird das jeweilige Gegenereignis automatisch 
        bezeichnet)					   
      | sind keine Bezeichner angegeben, werden automatisch die Bezeichner 
        *A* und *B* angenommen					   
      | Merkmal *A* - 1. Zeile				
      | Merkmal *B* - 1. Spalte	
					
    """
				
    # Verwendete Adressierung der Felder einer Tafel
    #
    #        '00'     '01'      '02'      '03'
    #        '10'     '11' a    '12' b    '13' c
    #        '20'     '21' d    '22' e    '23' f
    #        '30'     '31' g    '32' h    '33'	s
    #	
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            vier_felder_tafel_hilfe(kwargs["h"])		
            return
  
        kontr = kwargs.get('kontrolle')  
						
        def listen_kontrolle(): 
            w = liste	
            x, x0, x1, x2, x3, x4, x5, x6 = symbols('x, x0 x1 x2 x3 x4 x5 x6')			
            x7, x8 = symbols('x7 x8')	
            hasx = False			
            if x in w or 'x' in w:
                hasx = True			
                for i in range(len(w)):
                    if w[i] in (x, 'x'):
                        w[i] = Symbol('x' + str(i))	
            gl = [ w[0]+w[1]-w[2], 
                  w[3]+w[4]-w[5],
                  w[0]+w[3]-w[6],
                  w[1]+w[4]-w[7],
                  w[2]+w[5]-w[8],
                  w[6]+w[7]-w[8],
                  w[0]+w[1]+w[3]+w[4]-w[8] ]
            if hasx and kontr != False:				  
                L = solve(gl)
                if L:
                    if not all([isinstance(L[0][x], (int, Integer, Rational, \
                          float, Float)) for x in L[0]]):
                         return ZufallError('zufall: die Werte bestimmen die \
                                     Tafel nicht eindeutig')					  
                    for i, el in enumerate(w):		
                        if isinstance(el, Symbol):
                            w[i] = L[0][Symbol('x'+str(i))]
                    return w
                else:
                     return ZufallError('zufall: mit den Werten kann keine Tafel erzeugt werden')					  
            else:
                if kontr==False:
                    return w				
                elif all([abs(x) < 1e-8 for x in gl]):
                    return w
                return ZufallError('zufall: die Werte sind widersprüchlich')		
				
        try:	
            if len(args) not in (1, 2):		
	             raise ZufallError('eine oder zwei Listen angeben')
            if not isinstance(args[0], list):
	             raise ZufallError('als 1. Argument Liste angeben')
            if len(args) == 2 and not isinstance(args[1], list):
	             raise ZufallError('als 2. Argument Liste angeben')
            tafel = dict()	
            x = Symbol('x')			
            liste = args[0]
            if len(liste) not in (4, 9):
	             raise ZufallError('die Liste muß 4 oder 9 Elemente haben')
            hasx = False			
            if x in liste or 'x' in liste:
                hasx = True	
            if len(liste) == 4:
                if hasx:					
                    raise ZufallError('es müssen alle 9 Elemente eingetragen sein')
                if not all([isinstance(x, (int, Integer, Rational, \
                    float, Float)) for x in liste]):							
                    raise ZufallError('die Elemente müssen Zahlen sein')
                tafel['11'] = liste[0]							
                tafel['12'] = liste[1]							
                tafel['21'] = liste[2]							
                tafel['22'] = liste[3]	
                tafel['13'] = tafel['11'] + tafel['12']						
                tafel['23'] = tafel['21'] + tafel['22']		
                tafel['31'] = tafel['11'] + tafel['21']						
                tafel['32'] = tafel['12'] + tafel['22']						
                tafel['33'] = tafel['11'] + tafel['12'] + tafel['21'] + \
                            tafel['22']					
                tafel['01'] = 'BEZEICHNER_A'                 				
                tafel['02'] = 'BEZEICHNER_NICHT_A'                 				
                tafel['10'] = 'BEZEICHNER_B'                 				
                tafel['20'] = 'BEZEICHNER_NICHT_B'                 				
            elif len(liste) == 9:
                if not all([isinstance(y, (int, Integer, Rational, \
                            float, Float, str)) or y in (x, 'x') for y in liste]):							
                    raise ZufallError("nur Zahlen oder x bzw. 'x' angeben")
                if not isinstance(liste[0], str):					
                    liste = listen_kontrolle()
                    if isinstance(liste, ZufallError):
                        print(liste.args[0])
                        return
                if liste[8] == 1:
                    liste = [nsimplify(x, rational=True) for x in liste]	
                if any([isinstance(y, (float, Float)) for y in liste]):
                    li = []
                    for y in liste:
                        if y not in (x, 'x'):
                            li += [float(y)]
                    liste = li		
                tafel['11'] = liste[0]							
                tafel['12'] = liste[1]							
                tafel['13'] = liste[2]							
                tafel['21'] = liste[3]	
                tafel['22'] = liste[4]		
                tafel['23'] = liste[5]						
                tafel['31'] = liste[6]						
                tafel['32'] = liste[7]					
                tafel['33'] = liste[8]					
                tafel['01'] = 'BEZEICHNER_A'                 				
                tafel['02'] = 'BEZEICHNER_NICHT_A'                 				
                tafel['10'] = 'BEZEICHNER_B'                 				
                tafel['20'] = 'BEZEICHNER_NICHT_B'                 				
            if len(args) == 2:
                bez = args[1]
                if len(bez) not in (2, 4):
                    raise ZufallError('zwei oder vier Merkmalsbezeichner angeben')				
                if not all([isinstance(x, (str, Symbol)) for x in bez]):
                    raise ZufallError('als Bezeichner der Merkmale sind nur Symbole oder Zeichenketten zulässig')
                bez = [str(x) for x in bez]
                if len(bez) == 4:				
                    tafel['01'] = bez[0]                 				
                    tafel['02'] = bez[1]                 				
                    tafel['10'] = bez[2] 
                    tafel['20'] = bez[3] 
                else:
                    tafel['01'] = bez[0]                 				
                    tafel['02'] = bez[0]                 				
                    tafel['10'] = bez[1] 
                    tafel['20'] = bez[1] 				
        except ZufallError as e:
            print('zufall:', str(e))
            return

        if hasx:			
            print('Die Tafel wird automatisch vervollständigt')		
		
        return ZufallsObjekt.__new__(cls, tafel)
					
			
    def __str__(self):  
        return "VierFelderTafel"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def ausg(self):
        """Ausgabe der Tafel"""	
        return _ausg(self.args[0])		

    @property
    def umkehr(self):
        """Umkehrung der Tafel"""	
        t = self.args[0]
        liste = [t['11'], t['21'], t['31'], t['12'], t['22'], t['32'], \
                t['13'], t['23'], t['33']] 		
        bez = [t['10'], t['20'], t['01'], t['02']]	
        return VierFelderTafel(liste, bez)		
		        
    @property
    def _ze(self):
        """Zugehöriges ZufallsExperiment; internes Attribut"""
        t = self.args[0]	
        if t['01'] == 'BEZEICHNER_A':
            t['01'] = 'A'		
        if t['02'] == 'BEZEICHNER_NICHT_A':
            t['02'] = 'nichtA'	
        if t['10'] == 'BEZEICHNER_B':
            t['10'] = 'B'		
        if t['20'] == 'BEZEICHNER_NICHT_B':
            t['20'] = 'nichtB'		
        return ZufallsExperiment( [ (t['10'], t['13']), [ (t['01'], t['11']),
              (t['02'], t['12']) ], (t['20'], t['23']),  [ (t['01'], t['21']),
              (t['02'], t['22']) ] ] )
	
    @property
    def baum(self):
        """Baumdiagramm (für das zugehörige ZufallsExperiment)"""
        ze = self._ze		
        return ze.baum
    def baum_(self, **kwargs):
        """zugehörige Methode"""
        return self._ze.baum_(**kwargs)

    Baum = baum_        
		
    @property		
    def hb(self):
        """Zugehöriger Häufigkeitsbaum"""
        return self.hb_()	
		
    def hb_(self, *args, **kwargs):
        """zugehörige Methode"""
		
        if kwargs.get('h'):		
            print("\nZugehöriger HäufigkeitsBaum für die Vier-Felder-Tafel\n")
            print("Aufruf   v . hb_( /[ grund ] )\n")	
            print("             v       VierFelderTafel")			
            print("             grund   Grundwert; alle Tafelwerte werden auf")
            print("                     diesen Wert umgerechnet; falls nicht an-")
            print("                     gegeben, ist der Grundwert die (eventuell")
            print("                     gerundete) Summe der Tafelwerte\n")
            return			
        if len(args) > 1:
            print('zufall: höchstens ein Argument angeben')	
            return
        elif len(args) == 1:
            grund = args[0]
        else:
            grund = None		
        t = self.args[0]
        if grund:		
            if not (isinstance(grund, (int, Integer)) and grund > 0):
                print('zufall: für den Grundwert ganze Zahl > 0 angeben')
                return
        else:		
            grund = int(nint(t['33']))	
        werte = [t['11'], t['12'], t['21'], t['22']]
        umr = False
        f = grund / summe(werte)
        if all([isinstance(x, (int, Integer)) for x in werte]):
            if grund != summe(werte):
                print('Umrechnen auf ' + str(grund) + '\n' + \
                     'bei Notwendigkeit Runden, deshalb kleine Differenzen möglich')
                umr = True 
        else:
            txt = ''			
            if f != 1:
                txt = ', Umrechnen auf ' + str(grund)			
            print('Erzeugen ganzzahliger Werte' + txt + '\n' + \
				    'bei Notwendigkeit Runden, deshalb kleine Differenzen möglich')
            umr = True 
        w = werte				
        if umr:		
            w = [int(nint(f*x)) for x in werte]		
        hb = HaeufigkeitsBaum(              
		      'Insgesamt', summe(w),
              t['10'], w[0]+w[1], t['20'], w[2]+w[3],
              t['01'],w[0], t['02'],w[1], t['01'],w[2], t['02'],w[3] )
        return hb							
				
    Hb = hb_
	
    @property		
    def abs_h(self):
        """Tafel mit absoluten / natürlichen Häufigkeiten"""
        return self.abs_h_()	
			
    absH = abs_h        
    nat_h = abs_h
    natH = abs_h
			
    def abs_h_(self, *args, **kwargs):
        """ebenso; zugehörige Methode"""
		
        if kwargs.get('h'):		
            print("\nVier-Felder-Tafel mit absoluten Häufigkeiten\n")
            print("Aufruf   v . abs_h_( /[ grund ] )\n")	
            print("             v       VierFelderTafel")			
            print("             grund   Grundwert; alle Tafelwerte werden auf")
            print("                     diesen Wert umgerechnet; falls nicht an-")
            print("                     gegeben, ist der Grundwert die (eventuell")
            print("                     gerundete) Zeilen-/Spaltensumme der Tafel-")
            print("                     werte\n")			
            return			
        if len(args) > 1:
            print('zufall: höchstens ein Argument angeben')	
            return
        elif len(args) == 1:
            grund = args[0]
        else:
            grund = None		
        t = self.args[0]
        if grund:		
            if not (isinstance(grund, (int, Integer)) and grund > 0):
                print('zufall: für den Grundwert ganze Zahl > 0 angeben')
                return
        else:		
            grund = int(nint(t['33']))	
        werte = [t['11'], t['12'], t['21'], t['22']]
        umr = False
        f = grund / summe(werte)
        if all([isinstance(x, (int, Integer)) for x in werte]):
            if grund != summe(werte):
                print('Umrechnen auf ' + str(grund) + '\n' + \
                'bei Notwendigkeit Runden, deshalb kleine Differenzen möglich')
                umr = True 
        else:
            txt = ''			
            if f != 1:
                txt = ', Umrechnen auf ' + str(grund)			
            print('Erzeugen ganzzahliger Werte' + txt + '\n' \
		          'bei Notwendigkeit Runden, deshalb kleine Differenzen möglich')
            umr = True 
        w = werte				
        if umr:		
            w = [int(nint(f*x)) for x in werte]	
        x = Symbol('x')			
        vt = VierFelderTafel( [w[0], w[1], w[0]+w[1], w[2], w[3], w[2]+w[3], \
                           w[0]+w[2], w[1]+w[3], grund], \
                           [t['01'], t['02'], t['10'], t['20']], kontrolle=False )							 
        return vt							
			
    AbsH = abs_h_		
    nat_h_ = abs_h_
    NatH = abs_h_
	
    @property
    def unabh(self):
        """Test auf Unabhängigkeit """
        t = self.args[0]
        for el in ('01', '02', '10', '20'):	
            if str(t[el]) == 'BEZEICHNER_A':
                t[el] = 'A'
            elif str(t[el]) == 'BEZEICHNER_NICHT_A':
                t[el] = 'nichtA'
            elif str(t[el]) == 'BEZEICHNER_B':
                t[el] = 'B'
            elif str(t[el]) == 'BEZEICHNER_NICHT_B':
                t[el] = 'nichtB'													
        print(' ')				
        display(Math('\mathrm{Vorliegende\; VierFelderTafel}'))
        self.ausg
        display(Math('\mathrm{Bei\;Unabhängigkeit\;der\;Ereignisse}\;' + str(t['01']) + \
             '\;\mathrm{und}\;' + str(t['10']) + '\;\mathrm{gilt\;nach\;dem\;Multiplikationssatz}'))	
        A, B = str(t['01']), str(t['10'])
        a, b, c, s = t['31'], t['13'], t['11'], t['33']			 		
        sa, sb, sc, ss = fausg(a), fausg(b), fausg(c), fausg(s)			 
        display(Math('\\qquad P(' + A + ' \\cap ' + B + ') = P(' + A +') \\cdot P(' + B + ')' ))
        display(Math('\mathrm{Hier\;ist}' ))
        display(Math('\\qquad P(' + A + ') = ' + ('\\frac{'+sa+'}{'+ss+'}=' if s !=1 else '') + pqausg(a, s) + \
		            '\\qquad P(' + B + ') = ' + ('\\frac{'+sb+'}{'+ss+'}=' if s !=1 else '') + pqausg(b, s)))
        display(Math('\\qquad P(' + A + ' \\cap ' + B + ') = ' + ('\\frac{'+sc+'}{'+ss+'}=' if s !=1 else '') \
           + pqausg(c, s) + \
           '\\qquad P(' + A + ')\\cdot P( ' + B + ') = ' + pqausg(a, s) + \
           '\\cdot' + pqausg(b, s) + '=' + fausg(a/s*b/s, frac=True) ))
        display(Math('\\qquad P(' + A + ' \\cap ' + B + ') - P(' + A + ')\\cdot P( ' + B + ') = ' + \
           fausg(c/s - a/s*b/s, frac=True) + ('=' + fausg(c/s - a/s*b/s) if \
		    isinstance(c/s - a/s*b/s, Rational) else '') ))			
        print(' ')

		
    @property
    def wahrsch(self):
        """Anhand der Tafel berechnete Wahrscheinlichkeiten"""
        t = self.args[0]
        for el in ('01', '02', '10', '20'):	
            if str(t[el]) == 'BEZEICHNER_A':
                t[el] = 'A'
            elif str(t[el]) == 'BEZEICHNER_NICHT_A':
                t[el] = 'nichtA'
            elif str(t[el]) == 'BEZEICHNER_B':
                t[el] = 'B'
            elif str(t[el]) == 'BEZEICHNER_NICHT_B':
                t[el] = 'nichtB'
        A, B, nA, nB = str(t['01']), str(t['10']), str(t['02']), str(t['20'])
        a, b, c, d, e, f, g, h, s = t['11'], t['12'], t['13'], \
                            t['21'], t['22'], t['23'], \
                            t['31'], t['32'], t['33']	
        sa, sb, sc, sd, se, sf, sg, sh, ss = fausg(a, bruch=True), fausg(b, bruch=True), fausg(c, bruch=True), \
             fausg(d, bruch=True), fausg(e, bruch=True), fausg(f, bruch=True), fausg(g, bruch=True), \
			   fausg(h, bruch=True), fausg(s, bruch=True)
        print(' ')			 
        display(Math('\\text{Vorliegende Vierfeldertafel}'))
        self.ausg
        display(Math('\\text{In der Tafel enthaltene Wahrscheinlichkeiten}'))		
        display(Math('\\qquad P(' + A + ' \\cap ' + B + ') = ' + ('\\frac{'+sa+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(a/s, k=4, frac=True) + ('=' + fausg(a/s, k=4) if isinstance(a/s, Rational) else '') + \
             '\\qquad P(' + nA + ' \\cap ' + B + ') = ' + ('\\frac{'+sb+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(b/s, k=4, frac=True) + ('=' + fausg(b/s, k=4) if isinstance(b/s, Rational) else '') + \
			   ' \\qquad '))			   
        display(Math('\\qquad\\qquad\\qquad P(' + B + ')= ' + ('\\frac{'+sc+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(c/s, k=4, frac=True) + ('=' + fausg(c/s, k=4) if isinstance(c/s, Rational) else '') + \
             '\\qquad P(' + nB + ')= ' + ('\\frac{'+sf+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(f/s, k=4, frac=True) + ('=' + fausg(f/s, k=4) if isinstance(f/s, Rational) else '') ))
        display(Math('\\qquad P(' + A + ' \\cap ' + nB + ') = ' + ('\\frac{'+sd+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(d/s, k=4, frac=True) + ('=' + fausg(d/s, k=4) if isinstance(d/s, Rational) else '') + \
             '\\qquad P(' + nA + ' \\cap ' + nB + ') = ' + ('\\frac{'+se+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(e/s, k=4, frac=True) + ('=' + fausg(e/s, k=4) if isinstance(e/s, Rational) else '') + \
			   ' \\qquad '))
        display(Math('\\qquad\\qquad\\qquad P(' + A + ') = ' + ('\\frac{'+sg+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(g/s, k=4, frac=True) + ('=' + fausg(g/s, k=4) if isinstance(g/s, Rational) else '') + \
             '\\qquad P(' + nA + ') = ' + ('\\frac{'+sh+'}{'+ss+'}=' if s !=1 else '') + \
             fausg(h/s, k=4, frac=True) + ('=' + fausg(h/s, k=4) if isinstance(h/s, Rational) else '') ))
			 
        display(Math('\\text{Bedingte Wahrscheinlichkeiten  (Verwendung der Bayes-Formel)}'))			 
			 
        def bedp(A, B, a, b):
            display(Math('\\qquad P(' + A + '\,|\,' + B + ') = ' + '\\frac{P(' + A + ' \\cap ' + B + ')}{' + \
			  'P(' + B + ')} = \\frac{' + fausg(a, bruch=True) + '}{' + fausg(b, bruch=True) + '} = ' \
			  + fausg(a/b, k=4) ))		
			 
        bedp(A, B, a, c) 
        bedp(A, nB, d, f)
        bedp(B, A, a, g) 	
        bedp(B, nA, b, h) 
        bedp(nA, B, b, c) 			 
        bedp(nA, nB, e, f) 			 
        bedp(nB, A, d, g) 			 
        bedp(nB, nA, e, h)
        display(Math('\mathrm{siehe\; auch} \\quad vt.hb.wahrsch' ))	
		
        print(' ')

    rel_h = wahrsch		
    relH = wahrsch		
	
    @property
    def fisher_test(self):
        """Fishertest auf Unabhängigkeit"""
        t = self.args[0]
        if not all([isinstance(x, (int, Integer)) and x > 0 for x in (t['11'], \
              t['11'], t['11'], t['11'])]):		
            print('zufall: die Elemente der Tafel müssen ganzzahlig und größer als 0 sein')
            return
			
        def dm(x):
            return display(Math(x))
			
        print(' ')
        dm('\mathrm{Test\; auf\; Unabhängigkeit\; von\; zwei\; Merkmalen}')
        dm('\mathrm{(Exakter\; Test\; von\; Fisher)}')
        print(' ')
        dm('\mathrm{Erläuterung\; des\; Verfahrens}')
        dm('\mathrm{Ein\; Versuch\; soll\; die\; folgende\; Tafel\; ergeben\; haben,\; wobei\; die\; Zahlen\; der\; ' + \
            'rechten\; }')
        dm('\mathrm{Spalte \;zuvor\; festgelegt\; worden\; sind; es\; sei\;} b \\ge a,\; \mathrm{was\; durch\; Umstellen\; der\; \
              Tafel}') 
        dm('\mathrm{immer\; möglich\; ist}')		
        vv = VierFelderTafel(['$x$', '$a - x$', '$a$', '$b - x$', '$n+x - (a+b)$', '$n - a$', '$b$', '$n - b$', '$n$'])		
        dm('\mathrm{Es\; wurden\;} n\; \mathrm{Objekte\; anhand\; von\; zwei\; Merkmalen\;} A\; \mathrm{und\;} B\;' + \
           '\mathrm{in\; Klassen\; eingeteilt}')
        dm('\mathrm{In\; den\; vier\; gelben\; Zellen\; stehen\; die\; Zahlen}')
        dm('x = \\left|\,A \\cap B\,\\right|,\\qquad\;\; a-x= \\left|\,A \\cap \\overline{B}\,\\right|')
        dm('b-x = \\left|\,\\overline{A} \\cap B\,\\right|,\\quad n+x-(a+b) = \\left|\,\\overline{A} \\cap \\overline{B}\,\\right|') 
        print(' ')		
        dm('\mathrm{Die\;} \mathrm{Hypothesen\; sind}')			
        dm('H_0:\; A\; \mathrm{und\;} B\; \mathrm{sind\; unabhängig,\; die\; Ergebnisse\; sind\; rein\; zufällig\; ' + \
           'zustande\; gekom-}')
        dm('\quad\quad\mathrm{men}')			
        dm('H_1:\; A\; \mathrm{und\;} B\; \mathrm{sind\; nicht\; unabhängig}')			
        dm('\mathrm{Es\; wird\; die\; Wahrscheinlichkeit\; für\; das\; Ergebnis\; in\; der\; Tafel\; oder\; ein\;noch' + \
           '\;günsti-}')
        dm('\mathrm{geres\; Resultat\; unter\; den\; Bedingungen\; von\;} H_0\; \mathrm{ermittelt,\; hier}\;\\alpha = ' + \
           'P\\left(\\left|\,A \\cap B\, \\right| \\ge x\\right),')
        dm('\mathrm{also\;die\; Wahrscheinlichkeit\; dafür,\; daß\; von\;} a\; \mathrm{Objekten\; mit\;} A\; \mathrm{mindestens\;}' + \
           'x \;\mathrm{auch}\; B')
        dm('\mathrm{haben. \;Die\; Anzahl\; der\; für\; das\; betrachtete\; Ereignis\; günstigen\; Möglichkeiten\; ergibt}')
        dm('\mathrm{sich\; zu\quad}' + \
           '{b \choose x} \\cdot {n-b \choose a-x}	\, +\, {b \choose x+1} \\cdot {n-b \choose a-x-1}\, + \\dots +\,' \
           '{b \choose a} \\cdot {n-b \choose 0}')		
        dm('\mathrm{Diese\; Zahl\; muss\; noch\; durch\; die\; Anzahl\; aller\; Möglichkeiten\; zur\; Auswahl\; von\;} a\;')
        dm('\mathrm{Objekten\;aus\;} n,\; \mathrm{also}\; {a \choose n}, \;\mathrm{dividiert\; werden}' )		
        print(' ')
        dm('\mathrm{Berechnung}')
        dm('\mathrm{Für\; die\; vorliegende\; Tafel}')	
        self.ausg
        n, a, b, x = t['33'], t['13'], t['31'], t['11']
        gg = 0
        for i in range(x, a+1):
            gg += binomial(b, i)*binomial(n-b, a-i)
        hh = binomial(n, a)    
        aa = float(gg / binomial(n, a))    
        sn, sa, sb, sx = str(n), str(a), str(b), str(x)		
        dm('\mathrm{ist}\; n =' + sn + ',\; a =' + sa + ',\; b =' + sb + ',\; x =' + sx) 
        dm('\mathrm{Zahl\; der\; günstigen\; Möglichkeiten}\;\;= {'+sb+' \choose '+sx+'} \\cdot {'+str(n-b) + \
           '\choose '+str(a-x)+'}\,' + \
           '\, + {'+sb+' \choose '+str(x+1)+'} \\cdot {'+str(n-b)+' \choose '+str(a-x-1)+'}\, +\\dots +\,' \
           '{'+sb+' \choose '+sa+'} \\cdot {'+str(n-b)+' \choose 0} =')		
        dm('\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\quad = ' + str(gg))
        dm('{a \choose n} = {'+sa+' \choose '+sn+'} = '+str(hh))		
        dm('\\alpha= ' + '{0:.4f}'.format(aa))
        dm('\mathrm{Bei\; sehr\; kleinen\; Werten\; von\;} \\alpha\; \mathrm{ist\; die\; Hypothese\; der\; Unabhängigkeit\;' + \
           'abzulehnen}')
        print(' ')		
		
    fisherTest = fisher_test  
		
    @property
    def chi2_test(self):
        """Chi-Quadrat-Test auf Unabhängigkeit"""
        t = self.args[0]
        if not all([isinstance(x, (int, Integer)) and x > 0 for x in (t['11'], \
              t['11'], t['11'], t['11'])]):		
            print('zufall: die Elemente der Tafel müssen ganzzahlig und größer als 0 sein')
            return
			
        def dm(x):
            return display(Math(x))
			
        print(' ')
        dm('\\chi^2 \, \mathrm{-\,Test\; auf\; Unabhängigkeit\; von\; zwei\; Merkmalen}')
        print(' ')
        dm('\mathrm{Erläuterung\; des\; Verfahrens}')
        dm('\mathrm{Es\; liege\; folgende\; Tafel\; vor}')
        VierFelderTafel(['$r$', '$s$', '$b=r+s$', '$t$', '$u$', '$n - b$', '$a=r+t$', '$n - a$', '$n$'])		
        dm('\mathrm{Anhand\; von\; zwei\; Merkmalen}\; A\; \mathrm{und}\; B\; \mathrm{wurden}\; n\; \mathrm{Objekte}' + \
           '\; \mathrm{in\; Klassen\; eingeteilt, \; in}')
        dm('\mathrm{den\; gelben\; Zellen\; stehen\; die\; Zahlen}\;\ r=\\left| \, A \\cap B\,\\right|,\;' + \
           's=\\left|\,\\overline{A} \\cap B\,\\right|,\;' + \
		    ' t=\\left|\,A\\cap \\overline{B}\,\\right|,\;') 
        dm('u=\\left|\,\\overline{A} \\cap \\overline{B}\,\\right|')		
        dm('\mathrm{Die\; Hypothese}\; H_0\; \mathrm{der\; Unabhängigkeit\; von}\; A\; \mathrm{und}\; B\;' + \
           '\mathrm{beinhaltet,\; dass\;die\;Wahrschein-}')
        dm('\mathrm{lichkeiten\; in\; den\; Zellen\; durch\; Multiplikation\; erhalten\; werden\; können,}') 
        dm('P(A \cap B) = P(A) \\cdot P(B)\; \mathrm{usw.}')	
        dm('\mathrm{Es\; sei\;} p = P(A),\; q = P(B),\; \mathrm{dann\; muss\; näherungsweise\; gelten\;}')
        dm('r=n\,p\,q,\; s=n\,p\,(1-q)\; \mathrm{usw.}')
        dm('\mathrm{Mit\; den\; Schätzwerten\;\;}  \\hat{p}=\\frac{a}{n}\;\mathrm{und}\;\; \\hat{q}=\\frac{b}{n}\;' + 
           '\mathrm{kann\; die\; Tafel}')
        VierFelderTafel(['$n\,\hat{p}\,\hat{q}$', '$n\,(1-\\hat{p})\,\hat{q}$', '$b$', '$n\,\hat{p}\,(1-\hat{q})$', \
		    '$n\,(1-\\hat{p})\,(1-\\hat{q})$', '$n - b$', '$a$', '$n - a$', '$n$'])		
        dm('\mathrm{ermittelt\; werden.\; Sie\; enthält\; die\; Erwartungswerte\; der\; Häufigkeiten\; unter\; der\; ' + \
           'Hy-}')
        dm('\mathrm{pothese}\; H_0. \mathrm{Als\; Maß\; der\; Abweichung\; der\; ersten\; von\; der\; zweiten\; }' + \
		    '\mathrm{Tafel\;wird\;die\; }')
        dm('\mathrm{Zufallsgröße}\;\\chi_1^2\;\mathrm{definiert}')
        dm('\mathrm{Dazu\; wird\; die\; Summe\; der\; Quadrate\; der\; Abweichungen\; jedes\; Feldes\; vom\; jeweili-}')
        dm('\mathrm{gen\; Erwartungswert,\; dividiert\; durch\; den\; jeweiligen\; Erwartungswert,\; gebildet,}')
        dm('\mathrm{es\; ist\; also}')
        dm('\\chi_1^2 = \\frac{(r-n\,\\hat{p}\,\\hat{q})^2}{n\,\\hat{p}\,\\hat{q}} +' + \
            '\\frac{(s-n\,\\hat{p}\,(1-\\hat{q}))^2}{n\,\\hat{p}\,(1-\\hat{q})} +' + \
            '\\frac{(t-n\,(1-\\hat{p})\,\\hat{q})^2}{n\,(1-\\hat{p})\,\\hat{q}} +' + \
			  '\\frac{(u-n\,(1-\\hat{p})\,(1-\\hat{q}))^2}{n\,(1-\\hat{p})\,(1-\\hat{q})} ')
        dm('\mathrm{Der\; Wert\; dieser\; Zufallsgröße\; dient\; als\; Maß\; für\; die\; Unabhängigkeit\; von\;}' + \
           'A\; \mathrm{und\;} B,')
        dm('\mathrm{kleine\; Werte\; legen\; Unabhängigkeit\; nahe,\; große\; sprechen\; dagegegen}')
        print(' ')
        dm('\mathrm{Berechnung}')
        dm('\mathrm{Zu\; der\; vorliegenden\; Tafel}')	
        self.ausg	
        dm('\mathrm{wird\; die\; Tafel\; der\; bei\; Unabhängigkeit\; erwarteten\; Häufigkeiten\; ermittelt}')
        n, a, b = t['33'], t['31'], t['13']
        sn,  sa, sb = str(n), str(a), str(b)		
        r, s, t, u = t['11'], t['12'], t['21'], t['22']
        sr, ss1, st, su = str(r), str(s), str(t), str(u)
        PA, PB = Rational(a, n), Rational(b, n)
        rr, ss = n * PA * PB, n * (1-PA) * PB
        tt, uu = n * PA * (1-PB), n * (1-PA) * (1-PB)
        srr, sss, stt, suu = str(rr), str(ss), str(tt), str(uu)		
        VierFelderTafel([rr, ss, tt, uu])
        if any([isinstance(x, Rational) for x in (rr, ss,tt,uu)]):
            dm('\mathrm{bzw.\; (Dezimaldarstellung)}')	
            srr = '{0:.2f}'.format(float(rr))
            sss = '{0:.2f}'.format(float(ss))
            stt = '{0:.2f}'.format(float(tt))
            suu = '{0:.2f}'.format(float(uu))			
            VierFelderTafel([float(srr), float(sss), float(stt),float(suu)])
        dm('\mathrm{(\,z.B.\; ist\;\;} '+srr+ '=' + sn + '\\cdot \\frac{'+sa+'}{'+sn+'} \\cdot \\frac{'+sb+'}{'+sn+'}' + \
		     ',\;\;' + sss+ '=' + sn + '\\cdot \\frac{'+str(n-a)+'}{'+sn+'} \\cdot \\frac{'+sb+'}{'+sn+'}\;\mathrm{ )}')
        dm('\mathrm{Der\; Wert\; von\;} \\chi_1^2\; \mathrm{ist\; dann}')
        dm('\\chi_1^2 = \\frac{('+sr+'-'+srr+')^2}{'+srr+'} + \\frac{('+ss1+'-'+sss+')^2}{'+sss+'} +' + \
		     '\\frac{('+st+'-'+stt+')^2}{'+stt+'} + \\frac{('+su+'-'+suu+')^2}{'+suu+'} =')
        wert = '{0:.4}'.format(float((r-rr)**2/rr + (s-ss)**2/ss + (t-tt)**2/tt + (u-uu)**2/uu))		 
        dm('\\quad\, = ' +  wert)
        print(' ')		
        dm('\mathrm{Anhand\; dieser\; Größe\; kann\; eine\; Entscheidung\; getroffen\; werden:\; Bei\; einem\; gro-}')
        dm('\mathrm{ßen\; Wert\; wird\; die\; Hypothese\; der\; Unabhängigkeit\; abgelehnt,\;die\; Sicherheitswahr-}')
        dm('\mathrm{scheinlichkeit\; kann \;der\;Grafik\; entnommen\; werden; diese\; enthält\; einen\; Ausschnitt\;}')
        dm('\mathrm{des\; Graphen\; der\; Verteilungsfunktion\;der\;} \\chi_1^2 \, \mathrm{-\, Zufallsgröße\; }' + \
           '\mathrm{mit\; ausgewählten\; Si-}')
        dm('\mathrm{cherheitswahrscheinlichkeiten\; [in\; Prozent]}')		
        print(' ')		
		
        def pline(x, y, f):
            return plt.plot(x, y, color=f, lw=0.5)

        fig = plt.figure(figsize=(4, 2.5))
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['top'].set_visible(False)		
        ax.spines['bottom'].set_linewidth(0.8)		
        ax.spines['right'].set_visible(False)		
        ax.spines['left'].set_linewidth(0.8)		
        df = 1
        ax.set_yticks([])
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(9)		
            tick.label1.set_fontname('Times New Roman')
        plt.axes().xaxis.set_ticks_position('none')
        for x in (2, 4, 6, 8):		
            pline([x, x], [85, 85.3], 'black')
        plt.axes().yaxis.set_ticks_position('none')		
				
        plt.xlim(0, 10)
        plt.ylim(85, 100)
        x = np.linspace(chi2.ppf(0.84, df), chi2.ppf(0.9999999, df), 100)
        ax.plot(x, 100*chi2.cdf(x, df), 'black', lw=1, alpha=0.5)
        pline([0, chi2.ppf(0.9, df)], [90, 90], 'b')
        pline([chi2.ppf(0.9, df), chi2.ppf(0.9, df)], [0, 90], 'r')
        pline([0, chi2.ppf(0.95, df)], [95, 95], 'b')
        pline([chi2.ppf(0.95, df), chi2.ppf(0.95, df)], [0, 95], 'r')
        pline([0, chi2.ppf(0.975, df)], [97.5, 97.5], 'b')
        pline([chi2.ppf(0.975, df), chi2.ppf(0.975, df)], [0, 97.5], 'r')
        pline([0, chi2.ppf(0.99, df)], [99, 99], 'b')
        pline([chi2.ppf(0.99, df), chi2.ppf(0.99, df)], [0, 99], 'r')
        pline([0, 10], [100, 100], 'b')	

        def ptext(y, t):
            return ax.text(-0.2, y, t, fontsize=9, horizontalalignment='right', \
                  fontname='Times New Roman', verticalalignment='center', color=(0,0,0))

        ptext(100, '100')	
        ptext(99, '99')
        ptext(97.5, '97.5')
        ptext(95, '95')
        ptext(90, '90')
		
        plt.show()
        print(' ')		
		
    chi2Test =  chi2_test		  
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        vier_felder_tafel_hilfe(3)	
		
    h = hilfe					
		
		

# Funktionen zur Ausgabe der Tafel
# --------------------------------	

def komma(x):
    if isinstance(x, (int, Integer, Rational)):
        return 0
    else:
        s = str(x)	
        return len(s[s.find('.')+1:])	
		
def fausg(x, **kwargs):
    if isinstance(x, str):
        return x	
    fx = float(x)  
    if isinstance(x, (int, Integer)):
        return str(x)
    elif isinstance(x, Rational) and kwargs.get('frac'):
        return '\\frac{' + str(x.p) + '}{' + str(x.q) + '}'
    elif isinstance(x, Rational) and kwargs.get('bruch'):
        return str(x)
    else:
        k = kwargs.get('k')   # Kommastellen
        if k==1:
            s = '{0:.2f}'.format(fx)
        elif k==2:
            s = '{0:.2f}'.format(fx)            
        elif k==3:
            s = '{0:.3f}'.format(fx)     
        elif k==4:
            s = '{0:.4f}'.format(fx)            
        elif k==5:
            s = '{0:.5f}'.format(fx)    
        else:
            s = '{0:.6f}'.format(fx)  
        for j in range(len(s)):
            if s[-1] == '0':
                s = s[:-1]
        if s[-1] == '.':
            s += '0'		
        return s
		
def pqausg(x, y):
    if isinstance(x, Rational) and isinstance(y, Rational):
        z = nsimplify(x/y, rational=True)			
        return '\\frac{' + str(z.p) + '}{' + str(z.q) + '}' 
    s = '{0:.4f}'.format(x/y)
    for j in range(len(s)):
        if s[-1] == '0':
            s = s[:-1]
    return s					
        	
			
def _ausg(tafel):
    t = tafel	
    if t['01'] == 'BEZEICHNER_A': 	
        b0, bb = 10, 20								
    else:
        b0 = Max(len(t['10']), len(t['20']), len('Summe')) + 2
        bb = Max(*[len(str(t[s])) for s in ('01', '02', '11', '12', '13', '21', \
	                            '22', '23', '31', '32', '33')], 3)
        bb = 2*bb
    if bb > 20:	
        fig = plt.figure(figsize=(6, 1.5))
    else:
        fig = plt.figure(figsize=(5, 1.5))	
		
    ax = fig.add_subplot(1, 1, 1)
    for side in ['bottom', 'right', 'top', 'left']:
        ax.spines[side].set_visible(False)
    plt.axes().xaxis.set_ticks_position('none')
    plt.axes().yaxis.set_ticks_position('none')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlim(0, float(b0+3.1*bb)) 
    dy = 0.2		
    plt.ylim(-0.01, 0.8)    
    f = (0.5, 0.5, 0.5)
    f1 = (0.2, 0.2, 0.2)
    fs = 11	
    w = 0.8								
    
    def ptext(x, y, t):
        return ax.text(x, y, t, fontsize=fs, horizontalalignment='center', \
              verticalalignment='center', color=f, fontname='Times New Roman')
    def ptext1(x, y, t):
        return ax.text(x, y, t, fontsize=fs, horizontalalignment='center', \
              verticalalignment='center', color=f1, fontname='Times New Roman', \
              fontstyle='italic'
			  )
    def pline(x, y):
        return plt.plot(x, y, color=f, lw=w)
    k = Max(*[komma(x) for x in (t['11'], t['12'], t['21'], t['22'])])				
    d = 10
	
    ptext(b0+0.5*bb, 2.5*dy, fausg(t['11'], k=k, bruch=True))
    ptext(b0+1.5*bb, 2.5*dy, fausg(t['12'], k=k, bruch=True))	 
    ptext(b0+2.5*bb, 2.5*dy, fausg(t['13'], k=k+1, bruch=True))
    ptext(b0+0.5*bb, 1.5*dy, fausg(t['21'], k=k, bruch=True))
    ptext(b0+1.5*bb, 1.5*dy, fausg(t['22'], k=k, bruch=True))
    ptext(b0+2.5*bb, 1.5*dy, fausg(t['23'], k=k+1, bruch=True))
    ptext(b0+0.5*bb, 0.5*dy, fausg(t['31'], k=k+1, bruch=True))
    ptext(b0+1.5*bb, 0.5*dy, fausg(t['32'], k=k+1, bruch=True))
    ptext(b0+2.5*bb, 0.5*dy, fausg(t['33'], k=k+1, bruch=True))
    pline([b0, b0], [0, 3*dy])
    pline([b0+bb, b0+bb], [0, 3.8*dy])
    pline([b0+2*bb, b0+2*bb], [0, 3.8*dy])	
    pline([b0+3*bb, b0+3*bb], [0, 3*dy])	
    pline([b0, b0+3*bb], [0, 0])		
    pline([0.7*b0, b0+3*bb], [dy, dy])		
    pline([0.7*b0, b0+3*bb], [2*dy, 2*dy])		
    pline([b0, b0+3*bb], [3*dy, 3*dy])		
	
    if t['01'] == 'BEZEICHNER_A': 	
        ptext1(b0+0.5*bb, 3.5*dy, '$A$')
        ptext1(b0+1.5*bb, 3.5*dy, '$\overline{A}$')
        ax.text(0.85*b0, 2.5*dy, '$B$', fontsize=fs, horizontalalignment='right', \
              verticalalignment='center', color=f1, fontname='Times New Roman', \
              fontstyle='italic')		
        ax.text(0.85*b0, 1.45*dy, '$\overline{B}$', fontsize=fs, \
              horizontalalignment='right', \
              verticalalignment='center', color=f1, fontname='Times New Roman', \
              fontstyle='italic')	
    elif t['01'] == 'BEZEICHNER_B': 	
        ptext1(b0+0.5*bb, 3.5*dy, '$B$')
        ptext1(b0+1.5*bb, 3.5*dy, '$\overline{B}$')
        pline([b0+1.45*bb, b0+1.55*bb], [3.8*dy, 3.8*dy])
        ax.text(0.85*b0, 2.5*dy, '$A$', fontsize=fs, horizontalalignment='right', \
              verticalalignment='center', color=f1, fontname='Times New Roman', \
              fontstyle='italic')		
        ax.text(0.85*b0, 1.35*dy, '$\overline{A}', fontsize=fs, \
              horizontalalignment='right', \
              verticalalignment='center', color=f1, fontname='Times New Roman', \
              fontstyle='italic')	
        pline([0.69*b0, 0.83*b0],[1.7*dy, 1.7*dy])
    else:
        if t['01'] == t['02']:		
            ptext1(b0+0.5*bb, 3.5*dy, '$' + t['01'] + '$')
            ptext1(b0+1.5*bb, 3.5*dy, '$\overline{' + t['02'] + '}$')
            ax.text1(0.92*b0, 2.5*dy, '$' + t['10'] + '$', fontsize=fs, \
                  horizontalalignment='right', \
                  verticalalignment='center', color=f1, fontname='Times New Roman')	
            ax.text(0.92*b0, 1.45*dy, '$\overline{' + t['20'] + '}$', fontsize=fs, \
                  horizontalalignment='right', \
                  verticalalignment='center', color=f1, fontname='Times New Roman')
        else:		
            ptext1(b0+0.5*bb, 3.5*dy, '$' + t['01'] + '$')
            ptext1(b0+1.5*bb, 3.5*dy, '$' + t['02'] + '$')
            ax.text(0.92*b0, 2.5*dy, '$' + t['10'] + '$', fontsize=fs, \
                  horizontalalignment='right', \
                  verticalalignment='center', color=f1, fontname='Times New Roman')	
            ax.text(0.92*b0, 1.5*dy, '$' + t['20'] + '$', fontsize=fs, \
                  horizontalalignment='right', \
                  verticalalignment='center', color=f1, fontname='Times New Roman')
			  
    ax.text(b0+2.5*bb, 3.5*dy, '$Summe$', fontsize=fs, \
          horizontalalignment='center', \
          verticalalignment='center', color=f1, fontname='Times New Roman')		
    ax.text(0.92*b0, 0.5*dy, '$Summe$', fontsize=fs, \
          horizontalalignment='right', \
          verticalalignment='center', color=f1, fontname='Times New Roman')
    ax.add_patch(patches.Rectangle((b0, 0), 3*bb, dy, alpha=0.1, \
        facecolor='#00ff22'))			  
    ax.add_patch(patches.Rectangle((b0+2*bb, 0), bb, 3*dy, alpha=0.1, \
        facecolor='#00ff22'))			  
    ax.add_patch(patches.Rectangle((b0, dy), 2*bb, 2*dy, facecolor='#ffff11', \
               alpha=0.2))
	
    plt.show()
    print(' ')		
	
		
VT = VierFelderTafel		


		
# Benutzerhilfe für VierFelderTafel
# ---------------------------------

def vier_felder_tafel_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Attribute und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
VierFelderTafel - Objekt

Kurzname     Tafel	
	
Erzeugung    VierFelderTafel( werte  /[, bezeichner ] )
  
                werte   Liste mit 4 Werten: innere Werte der Tafel
                                  9 Werten: alle Werte der Tafel 
                                            (einschließlich Randwerte)
                        x bzw. 'x' steht für einen nicht gegebenen Wert
                        die Eingabe der Werte erfolgt zeilenweise
                bezeichner
                       Liste mit den Bezeichnern der Zeilen / Spalten
                       (4 oder 2 Bezeichner; bei 2 Bezeichnern wird das
                       jeweilige Gegenereignis automatisch bezeichnet)					   
                       sind keine Bezeichner angegeben, werden automa-
                       tisch die Bezeichner A und B angenommen					   
                       Merkmal A - 1. Zeile				
                       Merkmal B - 1. Spalte	
				
Zuweisung     vt = VierFelderTafel(...)   (vt - freier Bezeichner)

Beispiele
Tafel([22, 33, 18, 27])
Tafel([22, 33, 18, 27], ['weiblich', 'männlich', 'ParteiA', 'andPartei'])
Tafel( [19, 21, 6, 14], ['MethodeA', 'geheilt'])
Tafel([x, 32.7, 55, x, x, x, 40.7, x, 100], ['Raucher', 'NichtRaucher', 'jung', 'alt'])
	   """)		
        return 
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für VierFelderTafel
 	
vt.hilfe            Bezeichner der Eigenschaften und Methoden
vt.abs_h            Absolute Häufigkeiten
vt.abs_h_(...)   M  ebenso, zugehörige Methode
vt.ausg             Ausgabe der Tafel
vt.baum             Zugehöriges Baumdiagramm
vt.baum_(...)    M  ebenso, zugehörige Methode
vt.chi2_test        Chi-Quadrat-Test auf Unabhängigkeit
vt.fisher_test      Vier-Felder-Test auf Unabhängigkeit
vt.hb               Zugehöriger HäufigkeitsBaum
vt.hb(...)       M  ebenso, zugehörige Methode
vt.nat_h            = vt.abs_h  ( natürliche Häufigkeiten )
vt.nat_h_(....)  M  ebenso, zugehörige Methode
vt.rel_h            = vt.wahrsch  ( relative Häufigkeiten )
vt.umkehr           Umkehrung der Tafel
vt.wahrsch          Wahrscheinlichkeiten / relative Häufigkeiten

Synonyme Bezeichner

hilfe        h
abs_h        absH
abs_h_       AbsH
baum_        Baum
chi2_test    chi2Test
fisher_test  fisherTest
hb_          Hb
nat_h        natH
nat_h_       NatH
rel_h        relH
""")
        return 
	
