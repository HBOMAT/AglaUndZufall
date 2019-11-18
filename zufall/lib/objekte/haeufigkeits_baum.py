#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  HaeufigkeitsBaum - Klasse  von zufall           
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

import matplotlib.pyplot as plt

from sympy.core.numbers import Integer, Rational 
from sympy import Max	
from sympy.core.symbol import Symbol

from zufall.lib.objekte.basis import ZufallsObjekt	
from zufall.lib.objekte.ausnahmen import ZufallError
import zufall



# HaeufigkeitsBaum - Klasse  
# -------------------------
	
class HaeufigkeitsBaum(ZufallsObjekt):                                      
    """
	
Häufigkeitsbaum

**Kurzname** **HB**
	
**Erzeugung** 
	
   HB( *name1, wert1,..., name7, wert7* )

**Parameter**

   *name*: gültiger Bezeichner / Zeichenkette
   
   *wert* : ganze Zahl > 0
   
   Es werden Name und Wert aller Knoten des Baumes der Tiefe 2 angegeben
   (Beispiel siehe im Notebook über die HB-Hilfeseite)
				 
    """
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            haeufigkeits_baum_hilfe(kwargs["h"])		
            return
			
        try:			
            if len(args) != 14:
	             raise ZufallError('14 Argumente angeben')
            if not all([isinstance(args[i], (str, Symbol)) for i in range(0, 14, 2)]):
	             raise ZufallError('gültige Namen (eventuell als Zeichenkette) angeben')
            if not all([isinstance(args[i], (int, Integer)) and args[i] > 0 for i in range(1, 14, 2)]):
	             raise ZufallError('Anzahlen als ganze Zahlen > 0 angeben')
            if args[3]+args[5] != args[1] or args[7]+args[9] != args[3]	or args[11]+args[13] != args[5]:
	             raise ZufallError('die Zahlenangaben sind fehlerhaft')             			
        except ZufallError as e:
            print('zufall:', str(e))
            return

        return ZufallsObjekt.__new__(cls, *args)
					
			
    def __str__(self):  
        return "HäufigkeitsBaum"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def ausg(self):
        """Ausgabe des Baumes"""	
        return _ausg(self.args)		

    @property
    def umkehr(self):
        """Umkehrung des Baumes"""	
        a = self.args		
        return HaeufigkeitsBaum(a[0], a[1],  a[6], a[7]+a[11], a[8], a[9]+a[13], a[2], a[7], 
                            a[4], a[11], a[2], a[9], a[4], a[13])		
		
    @property
    def vt(self):
        """Zugehörige Vier-Felder-Tafel"""
        a = self.args
        l1 = [a[7], a[11], a[9], a[13]]
        l2 = [a[2], a[4], a[6], a[8]]
        vt = importlib.import_module('zufall.lib.objekte.vier_felder_tafel')
        VierFelderTafel = vt.VierFelderTafel 		
        return VierFelderTafel(l1, l2)		
		
    @property
    def wahrsch(self):
        """Wahrscheinlichkeiten / relative Häufigkeiten) auf der Basis 
des Baumes"""
		
        def br(x, y):
            return '= \\frac{' + str(x) + '}{' + str(y) + '}'		
        def fl(x):
            return "= %6.4f" % x		
        def pr(x):
            return ("= %5.2f" % (100*x)) + '\\%' 
        def von(x, y):
            return '=' + str(x) + '\mathrm{\, von\, }' +  str(y) 
			
        a = self.args	
        print(' ')		
        display(Math("\mathrm{Vorliegendes\; Baumdiagramm:}"))		
        _ausg(self.args)
        display(Math("\mathrm{Gegeben:}"))		
        display(Math('\\qquad P(' + str(a[2]) + ')' + br(a[3], a[1]) + fl(a[3]/a[1]) + pr(a[3]/a[1])))
        display(Math('\\qquad P(' + str(a[6]) + '\,|\,' + str(a[2]) + ')' + br(a[7], a[3]) + fl(a[7]/a[3]) + \
               pr(a[7]/a[3])))
        display(Math('\\qquad P(' + str(a[6]) + '\,|\,' + str(a[4]) + ')' + br(a[11], a[5]) + fl(a[11]/a[5]) + \
                   pr(a[11]/a[5]) ))
        display(Math("\mathrm{Berechnung\; nach\; der\; Bayes-Formel\; für\; natürliche\; Häufigkeiten:}"))	
        display(Math('\\qquad P(' + str(a[2]) + '\,|\,' + str(a[6]) + ')= \\frac{a}{a+b}')) 
        display(Math('\\qquad\\qquad a - \mathrm{Anzahl\;}' + '\mathrm{\;mit\;}' + str(a[2]) + \
          '\mathrm{\;und\;}' + str(a[6])))
        display(Math('\\qquad\\qquad b - \mathrm{Anzahl\;}' + '\mathrm{\;mit\;}' + str(a[4]) + 
          '\mathrm{\;und\;}' + str(a[6])))
        r = Rational(a[7], a[7]+a[11])		
        display(Math('\\qquad P(' + str(a[2]) + '\,|\,' + str(a[6]) + ') = \\frac{' + str(a[7]) + '}{' + str(a[7]) \
		            + '+' + str(a[11]) + '}' + br(a[7], a[7]+a[11]) + fl(a[7]/(a[7]+a[11])) + \
					  pr(a[7]/(a[7]+a[11])) + von(r.p, r.q))) 
        display(Math("\mathrm{analog:}"))		
        r = Rational(a[9], a[9]+a[13])		
        display(Math('\\qquad P(' + str(a[2]) + '\,|\,' + str(a[8]) + ') = \\frac{' + str(a[9]) + '}{' + str(a[9]) \
		            + '+' + str(a[13]) + '}' + br(a[9], a[9]+a[13]) + fl(a[9]/(a[9]+a[13])) + \
					  pr(a[9]/(a[9]+a[13])) + von(r.p, r.q))) 
        r = Rational(a[11], a[7]+a[11])		
        display(Math('\\qquad P(' + str(a[4]) + '\,|\,' + str(a[6]) + ') = \\frac{' + str(a[11]) + '}{' + str(a[7]) \
		            + '+' + str(a[11]) + '}' + br(a[11], a[7]+a[11]) + fl(a[11]/(a[7]+a[11])) + \
					  pr(a[	11]/(a[7]+a[11])) + von(r.p, r.q))) 
        r = Rational(a[13], a[9]+a[13])		
        display(Math('\\qquad P(' + str(a[4]) + '\,|\,' + str(a[8]) + ') = \\frac{' + str(a[13]) + '}{' + str(a[9]) \
		            + '+' + str(a[13]) + '}' + br(a[13], a[9]+a[13]) + fl(a[13]/(a[9]+a[13])) + \
					  pr(a[	13]/(a[9]+a[13])) + von(r.p, r.q))) 
				
        display(Math('\mathrm{Die\; Wahrscheinlichkeiten}\;\; P(' + str(a[4]) + '),\;P(' + str(a[8]) + \
          '\,|\,' + str(a[2]) + '),P(' + str(a[8]) + \
          '\,|\,' + str(a[4]) + ')' ))
        display(Math('\mathrm{werden\; analog\; berechnet,}'))	
        display(Math('P(' + str(a[6]) + ') =' + '\\frac{'+str(a[7])+'+'+str(a[11])+'}{'+str(a[1])+'}' \
          + fl((a[7]+a[11])/a[1]) + pr((a[7]+a[11])/a[1])))
        display(Math('P(' + str(a[8]) + ') =' + '\\frac{'+str(a[9])+'+'+str(a[13])+'}{'+str(a[1])+'}' \
          + fl((a[9]+a[13])/a[1]) + pr((a[9]+a[13])/a[1])))
				
        print(' ')					  
        
    rel_h = wahrsch		
    relH = wahrsch		

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        haeufigkeits_baum_hilfe(3)	
		
    h = hilfe					

	
		
# Ausgabe des Baumes
# ------------------		
		
def _ausg(args):
    fig = plt.figure(figsize=(4, 2))
    ax = fig.add_subplot(1, 1, 1)
    for side in ['bottom', 'right', 'top', 'left']:
        ax.spines[side].set_visible(False)
    plt.axes().xaxis.set_ticks_position('none')
    plt.axes().yaxis.set_ticks_position('none')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlim(0, 8) 
    dy = 0.5		
    plt.ylim(1, 8.5*dy)    
    f = (0.4, 0.4, 0.4)
    fs, fs1 = 11, 11		
    w = 0.5
	
    tt = Max(*[len(args[i],) for i in (2, 4, 6, 8)])
    d, d1 = 0.5, 0	
    if tt > 5:	
        d, d1 = 1.8, 1
		
    def ptext(x, y, t, fs):	
        return ax.text(x, y, t, fontsize=fs, horizontalalignment='center', \
              fontname='Times New Roman', color=f)
	
    args = list(args)	
    for i in (2, 4, 6, 8, 10, 12):
        if args[i] == 'BEZEICHNER_A':
            args[i] = 'A'		
        if args[i] == 'BEZEICHNER_NICHT_A':
            args[i] = 'nichtA'		
        if args[i] == 'BEZEICHNER_B':
            args[i] = 'B'		
        if args[i] == 'BEZEICHNER_NICHT_B':
            args[i] = 'nichtB'		
    ptext(2+d+d1/2, 7.4*dy, args[0], fs1)
    ptext(2+d+d1/2, 8*dy, args[1], fs)		 
    ptext(1+d/2, 4.4*dy, args[2], fs1)
    ptext(3+3/2*d+d1, 4.4*dy, args[4], fs1)
    ptext(1+d/2, 5*dy, args[3], fs)
    ptext(3+3/2*d+d1, 5*dy, args[5], fs)		
    ptext(0.5, 2*dy, args[7], fs)
    ptext(0.5, 1.4*dy, args[6], fs1)
    ptext(1.3+d, 2*dy, args[9], fs)
    ptext(1.3+d, 1.4*dy, args[8], fs1)		
    ptext(2.6+d+d1, 2*dy, args[11], fs)
    ptext(2.6+d+d1, 1.4*dy, args[10], fs1)
    ptext(3.4+2*d+d1, 2*dy, args[13], fs)
    ptext(3.4+2*d+d1, 1.4*dy, args[12], fs1)  
	
    def pline(x, y):
        return plt.plot(x, y, color=f, lw=w)
	
    pline([1.8+d+d1/2, 1.1+d/2], [3.6, 2.8])
    pline([2.15+d+d1/2, 2.93+d*3/2+d1], [3.6, 2.8])
    pline([0.875+d/2, 0.6], [2.1, 1.3])	
    pline([1.1+d/2, 1.29+d], [2.1, 1.3])	
    pline([2.88+3/2*d+d1, 2.68+d+d1], [2.1, 1.3])		
    pline([3.13+3/2*d+d1, 3.4+2*d+d1], [2.1, 1.3])		
    plt.show()
    print(' ')	
	
		
HB = HaeufigkeitsBaum		

		
# Benutzerhilfe für HaeufigkeitsBaum
# ----------------------------------

def haeufigkeits_baum_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
HäufigkeitsBaum - Objekt

Kurzname     HB
		
Erzeugung    HäufigkeitsBaum( name1, wert1,..., name7, wert7 )

                 Name und Wert der Knoten des Baumes der Tiefe 2 
                 (siehe Beispiel)
				 
                 name    gültiger Bezeichner/Zeichenkette
                 wert    ganze Zahl > 0
				 
Zuweisung     h = HäufigkeitsBaum(...)   (h - freier Bezeichner)

Beispiel   (die Eingabe ist günstig in dieser Form zu machen)

HB(                 'Patienten', 1000, 
            'krank', 8,            'nichtkrank', 992,
    'positiv',7,  'negativ',1,  'positiv',70,  'negativ',922 )     
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften für HäufigkeitsBaum
	
h.hilfe      Bezeichner der Eigenschaften und Methoden
h.ausg       Ausgabe des Baumes
h.rel_h      = h.wahrsch  ( relative Häufigkeiten )
h.umkehr     Umkehrung des Baumes
h.vt         Zugehörige VierFelderTafel
h.wahrsch    Wahrscheinlichkeiten / relative Häufigkeiten

Synonyme Bezeichner

hilfe   h
rel_h   relH
	   """)		
        return	
	
