#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  FussballToto - Klasse  von zufall           
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

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from sympy import Symbol, Rational, Integer, nsimplify
from sympy.core.compatibility import iterable
from sympy.printing.latex import latex

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.gleich_verteilung import GleichVerteilung
from zufall.lib.objekte.datenreihe import DatenReihe
from zufall.lib.objekte.urne import Urne
from zufall.lib.objekte.wuerfel import Wuerfel
from zufall.lib.funktionen.graf_funktionen import verlauf as verlauf_grafik
from zufall.lib.funktionen.funktionen import anzahl,zuf_zahl

from zufall.lib.objekte.ausnahmen import ZufallError



# FussballToto - Klasse  
# ---------------------
	
class FussballToto(ZufallsObjekt):                                      
    """
	
Fußball - Toto

**Kurznaame** **Toto**
	
**Erzeugung**    

   Toto( )

    """
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            toto_hilfe(kwargs["h"])		
            return
  
        return ZufallsObjekt.__new__(cls)
					
			
    def __str__(self):  
        return "FussballToto (7 Mannschaften)"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def regeln(self):
        """Regeln für Toto"""	
		
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\\text{Fussballtoto}')
        print(' ')		
		
        dm('\\text{Beim echten Fussballtoto sagt man den Ausgang von 11 Spielen voraus. Es inte- }') 
        dm('\\text{ressiert die Anzahl der richtig vorausgesagten Spielentscheidungen}') 
        dm('\\text{Das Ankreuzen von 1, 0 bzw. 2 bedeutet: der erstgenannte Verein gewinnt, unent- }')
        dm('\\text{schieden bzw. der zweitgenannte Verein gewinnt. Verlegt man sich aufs Raten, so}')
        dm('\\text{entspricht das Ausfüllen dem elfmaligen Ziehen mit Zurücklegen aus einer Urne, }') 
        dm('\\text{die 3 Kugeln mit den Ziffern 0, 1 bzw. 2 enthält}')
		
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        d = 0.5

        def linie(x, y):
            plt.plot(x, y, color='k', linewidth=0.8)
    
        def rlinie(x, y):
            plt.plot(x, y, color='r', linewidth=0.8)
    
        def text(x, y, t):
            ax.text(x, y, t, fontsize=10, alpha=0.9, horizontalalignment='center',
            verticalalignment='center', fontname='Times New Roman')
    
        def rtext(x, y, t):
            ax.text(x, y, t, fontsize=10, alpha=0.9, horizontalalignment='right',
            verticalalignment='center', fontname='Times New Roman') 
    
        def kreuz(x, y):
            rlinie([x-d/3, x+d/3], [y+d/3, y-d/3])
            rlinie([x-d/3, x+d/3], [y-d/3, y+d/3])
    
        plt.close('all')    
        fig = plt.figure(figsize=(2, 5))
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        ax.axis('off')
        plt.ylim(-0.2, 12*d)

        linie([-0.2, -0.2], [0, 11*d])        
        linie([d, d], [0, 11*d])
        linie([0.9*d, 0.9*d], [0, 11*d])
        linie([2*d, 2*d], [0, 11*d])
        linie([3*d, 3*d], [0, 11*d])
        linie([4*d, 4*d], [0, 11*d])
        linie([5*d, 5*d], [0, 11*d])

        for i in range(12):
            linie([-0.2, 4*d],[i*d, i*d])
        for i in range(11):    
            text(1.5*d, (i+0.5)*d, '1')    
            text(2.5*d, (i+0.5)*d, '0')  
            text(3.5*d, (i+0.5)*d, '2')
            rtext(0.7*d, (10.5-i)*d, str(i+1))
    
        for i in (3,  4, 5, 8, 10):    
            kreuz(2.5*d, (i-0.5)*d)    
        for i in (1, 6, 11):    
            kreuz(1.5*d, (i-0.5)*d)            
        for i in (2, 7, 9):    
            kreuz(3.5*d, (i-0.5)*d)     
        
        re = patches.Rectangle((-0.2, 0), 4.4*d, 11*d, facecolor=(0,1,0), alpha=0.2)   
        ax.add_patch(re)                       
        
        plt.show()		

        return		
		
    @property
    def formeln(self):
        """Berechnungsformeln"""	
	
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\\text{Berechnung der Wahrscheinlichkeiten beim  FussballToto}')
        dm('\\text{(Es wird angenommen, dass das Tippen rein zufällig erfolgt)}')
        print(' ')	
        dm('\\text{Hier werden 7 Spiele (statt 11) betrachtet. Damit ist das zugrunde liegende Urne-}')
        dm('\\text{Modell explizit benutzbar, was bei 11 Spielen wegen des extremen Anstiegs der }')
        dm('\\text{Rechenzeiten nicht mehr sinnvoll möglich ist. Die theoretischen Überlegungen sind }') 
        dm('\\text{jedoch auch dort gültig, so dass die Wahrscheinlichkeiten für 11 Spiele auf analoge }')
        dm('\\text{Weise gewonnen werden können. Sie bilden die Verteilung für die ZufallsGröße}')
        dm('\\text{\'Richtige\'}')
        print(' ')
        dm('\\text{Der abgegebene Tipp sei für jedes der 7 Spiele \'1\' - Gewinn, Ausgangspunkt ist das }')
        dm('\\text{Urne-Objekt}')
        dm('\qquad\\text{Urne( [0, 1, 2],  7 )}')
        dm('\\text{Die Wahrscheinlichkeiten für }7,\,6,...,\,1,\,0 \\text{ Richtige lassen sich dann anhand der }') 
        dm('\\text{ZufallsGröße \'Anzahl der 1-en\' berechnen. Diese wird mit der Funktion }')
        dm('\\text{ $f= anzahl(1)$   (es werden die Einsen gezählt) erzeugt. Das zugrundeliegende Urne-}')
        dm('\\text{Objekt ist damit}')
        dm('\qquad\\text{Urne( [0, 1, 2], 7, f=anzahl(1) )}')      
        dm('\\text{Die Wahrscheinlichkeiten lassen sich auch mit folgender Überlegung gewinnen:}')
        dm('\\text{Für das Ereignis \'5 Richtige\' sind alle Scheine mit 5 Richtigen und 2 Falschen }') 
        dm('\\text{günstig, egal, welche 2 Spiele getippt wurden}')
        dm('\\text{Auf }{7\choose 2} \\text{ Arten kann man 2 von 7 Spielen herausgreifen, für jedes}')
        dm('\\text{der zwei falschen Spiele gibt es 2 Möglichkeiten, falsch zu tippen, es gilt}')		
        dm('P( \\text{\'5 Richtige\')} =\\dfrac{4\cdot {7\choose 2}}{3^7}=\\dfrac{28}{729}')
        dm('\\text{Die anderen Werte ergeben sich auf die selbe Art und Weise}')		
        print(' ')	
  							
    @property
    def richtige(self):
        """ZufallsGröße "Richtige" """							
        return Urne( [0, 1, 2], 7, f=anzahl(1) )

		 
    def spiel(self, *args, **kwargs):
        """Spiel zur Simulation; 7 Mannschaften"""
		
        if kwargs.get('h'):
            print("\nSpiel     ( FussballToto, 7 Mannschaften )\n")
            print("Aufruf   t . spiel( /[ tipp ] /[, m ] )\n")
            print("             t        Toto-Objekt")
            print("             tipp     abgegebener Tipp (Liste mit 7 Zahlen aus {0, 1, 2})")			
            print("                      fehlt die Angabe, wird ein zufälliger Tipp angenom-")
            print("                      men")			
            print("             m        Anzahl Spiele (mit dem gleichen Tipp); Standard=1\n")
            print("Zusatz   z=ja  Es wird ein zufälliger Tipp angenommen")
            print("               (ein eventuell angegebener Tipp wird nicht beachtet)")
            print("         d=ja  Bei Angabe von m > 1 Rückgabe einer DatenReihe")
            print("               mit der Anzahl Richtige je Spiel\n")			
            return			
	  
        def zuf_tipp()	  :
            return zuf_zahl((0, 2), 7)		
	  
        zufall = False	  
        if len(args) not in (0, 1, 2):
            print('zufall: 0 bis 2 Argumente angeben')
            return
        if len(args) == 0:
            m = 1
            zufall = True			
        elif len(args) == 1:
            m = args[0]
            if isinstance(m, (int, Integer)):	
                zufall = True			
            elif isinstance(m, (list, tuple)):
                tipp = m
                m = 1
            else:				
                print('zufall: positive ganze Zahl oder Tipp-Liste angeben')
        elif len(args) == 2:
            tipp, m = args	

        if m <= 0:
            print('zufall: Anzahl der Spiele >= 1 angeben')
            return	

        if kwargs.get('z'):
            zufall = True

        if zufall:
            tipp = zuf_tipp()
			
        if len(tipp) != 7 or not all([x in (0,1,2) for x in tipp]):			
            print('zufall: Tipp als Liste von 7 Zahlen aus (0,1,2) angeben')
            return			
			
        ergebnisse = zuf_tipp()			

        def dm(x):
            return display(Math(x))				

        print(' ')
			
        if m == 1:
            if not zufall:		
                 dm('\\text{Tipp}' + '\\quad\\quad \,:' + latex(tipp))
            else:
                dm('\\text{Tipp}' + '\\quad\\quad :\;' + latex(tipp) + '\;\;\\text{(zufällig)}')
            dm('\\text{Ergebnisse :} \;' + latex(ergebnisse))	
            erg = 0			
            for i, t in enumerate(tipp):
                if t == ergebnisse[i]:
                    erg += 1
            if erg == 1:					
                dm(latex(erg) + '\;\\text{Richtiger}')	
            else:					
                dm(latex(erg) + '\;\\text{Richtige}')	
        else:			
            summen = {}
            dr = []			
            for i in range(m):
                erg = zuf_tipp()
                sum = 0				
                for j, t in enumerate(tipp):
                    if t == erg[j]:
                        sum += 1
                if kwargs.get('d'):
                    dr += [sum]						
                try:						
                    summen[sum] += 1
                except KeyError:
                    summen[sum] = 1
            dm(latex(m) + '\; \\text{Spiele}')
            dm('\\text{Spielergebnisse (Richtige : Anzahl Spiele, relative Häufigkeit, \
    			theoretische}') 
            dm('\\text{Wahrscheinlichkeit)}')			
            u = Urne([0, 1, 2], 7, f=anzahl(1), info=False)			
            for s in summen:
                sum = summen[s]		
                dm(latex(s) + '\\text{ : } \\quad' + latex(sum) + '\\quad' + \
				   latex(format(float(sum/m), '.4f')) + '\\quad ' + \
				   latex(format(float(u.P(s)), '.4f')) + '=' + latex(u.P(s)))
        print(' ')       
        if kwargs.get('d'):
            print('Rückgabe einer DatenReihe (Anzahl Richtige je Spiel)')		
            return DatenReihe(dr)			
			
			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        toto_hilfe(3)	
		
    h = hilfe								
				
			
			
# Benutzerhilfe für Toto
# ----------------------

def toto_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
FussballToto - Objekt

Kurzname     Toto
	
Erzeugung    Toto( )
				 
Zuweisung    t = Toto()   (t - freier Bezeichner)
	   """)
        return 
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Toto
 	
t.hilfe          Bezeichner der Eigenschaften und Methoden
t.formeln        Berechnungsformeln
t.regeln         Spielregeln
t.richtige       ZufallsGröße 'Richtige'
t.spiel(...)  M  Spiel

Synoymer Bezeichner

hilfe    h

Eigenschaften und Methoden für die ZufallsGröße t.richtige siehe Hilfeseite 
für ZufallsGröße
""")
        return 
		
		
Toto = FussballToto		
