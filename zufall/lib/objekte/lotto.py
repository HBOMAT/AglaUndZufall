#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  Lotto - Klasse  von zufall           
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
from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse
from zufall.lib.objekte.hyper_geometrische_verteilung import HyperGeometrischeVerteilung
from zufall.lib.objekte.datenreihe import DatenReihe
from zufall.lib.objekte.wuerfel import Wuerfel
from zufall.lib.funktionen.funktionen import zuf_zahl
from zufall.lib.funktionen.graf_funktionen import verlauf as verlauf_grafik

from zufall.lib.objekte.ausnahmen import ZufallError



# Lotto - Klasse  
# --------------
	
class Lotto(ZufallsObjekt):                                      
    """
	
Lotto 6 aus 49
	
**Erzeugung**    

   Lotto( )

    """
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            lotto_hilfe(kwargs["h"])		
            return
  
        return ZufallsObjekt.__new__(cls)
					
			
    def __str__(self):  
        return "Lotto 6 aus 49"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def regeln(self):
        """Regeln für Lotto"""	
		
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\\text{Zahlenlotto 6 aus 49}')
        print(' ')		
		
        dm('\\text{Aus einer Trommel (Urne) werden nacheinander sechs der von 1 bis 49 numme-}') 
        dm('\\text{rierten Kugeln gezogen (die Zusatzzahl wird hier nicht beachtet). Auf einem }')
        dm('\\text{Lottoschein müssen diese 6 Zahlen durch Ankreuzen im Voraus erraten werden}')
			
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        d = 0.5

        def linie(x, y):
            plt.plot(x, y, color='k', linewidth=0.8)
    
        def rlinie(x, y):
            plt.plot(x, y, color='r', linewidth=0.8)
    
        def text(x, y, t):
            ax.text(x, y, t, fontsize=11, alpha=0.9, horizontalalignment='center',
            verticalalignment='center', fontname='Times New Roman')
    
        def rtext(x, y, t):
            ax.text(x, y, t, fontsize=11, alpha=0.9, horizontalalignment='right',
            verticalalignment='center', fontname='Times New Roman') 
    
        def kreuz(x, y):
            rlinie([x-d/3, x+d/3], [y+d/3, y-d/3])
            rlinie([x-d/3, x+d/3], [y-d/3, y+d/3])
    
        plt.close('all')    
        fig = plt.figure(figsize=(2.8, 2.8))
        ax = fig.add_subplot(1, 1, 1, aspect='equal')
        ax.axis('off')
        plt.xlim(-0.2, 8*d)
        plt.ylim(-0.2, 8*d)

        linie([0, 0], [0, 7*d])        
        linie([d, d], [0, 7*d])
        linie([2*d, 2*d], [0, 7*d])
        linie([4*d, 4*d], [0, 7*d])
        linie([5*d, 5*d], [0, 7*d])
        linie([6*d, 6*d], [0, 7*d])
        for i in range(8):
            linie([i*d, i*d], [0, 7*d])
        for i in range(8):
            linie([0, 7*d],[i*d, i*d])
			
        for i in range(1, 8):    
            text((i-0.5)*d, (6+0.5)*d, str(i))    
        for i in range(8, 8+7):    
            text((i-7-0.5)*d, (5+0.5)*d, str(i))    
        for i in range(15, 15+7):    
            text((i-14-0.5)*d, (4+0.5)*d, str(i))    
        for i in range(22, 22+7):    
            text((i-21-0.5)*d, (3+0.5)*d, str(i))    
        for i in range(29, 29+7):    
            text((i-28-0.5)*d, (2+0.5)*d, str(i)) 
        for i in range(36, 36+7):    
            text((i-35-0.5)*d, (1+0.5)*d, str(i)) 
        for i in range(43, 43+7):    
            text((i-42-0.5)*d, (0+0.5)*d, str(i)) 
        kreuz(3.5*d, (1-0.5)*d)    
        kreuz(0.5*d, (1-0.5)*d)    
        kreuz(2.5*d, (2-0.5)*d)    
        kreuz(4.5*d, (4-0.5)*d)    
 			
        kreuz(2.5*d, (1-0.5)*d)    
        kreuz(1.5*d, (3-0.5)*d)    
        
        re = patches.Rectangle((0, 0), 7*d, 7*d, facecolor=(0,1,0), alpha=0.2)   
        ax.add_patch(re)                       
        
        plt.show()		

        dm('\\text{Für den Gewinnplan der Spielsimulation werden die durchschnittlichen Gewinn-}')
        dm('\\text{quoten aus 5 aufeinander folgenden Ziehungen des \'echten\' Lotto benutzt:}')
        dm('\qquad\\text{6 Richtige	564.165 Euro}')		   
        dm('\qquad\\text{5 Richtige	3.239 Euro}')
        dm('\qquad\\text{4 Richtige	47 Euro}')
        dm('\qquad\\text{3 Richtige	11 Euro}')	 
        dm('\\text{Der Einsatz je Spiel beträgt 10 Euro}')
        print(' ')		
		
        return		
		
    @property
    def formeln(self):
	
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\\text{Berechnung der Wahrscheinlichkeiten beim  Lotto \'6 aus 49\'}')
        print(' ')	
        dm('\\text{Es gibt }{49\choose 6} \\text{ = 13983816 Möglichkeiten der Ziehung, die alle gleich wahrschein-}' )
        dm('\\text{lich sind. Also ist}')
        dm('\\qquad P(\\text{\'6 Richtige\'}) = \dfrac{1}{13983816} = 0.000000071511238420185162619416617')	
        print(' ')		
		
        dm('\\text{Die Wahrscheinlichkeit für das Ereignis \'4 Richtige\' kann z.B. so ermittelt werden:}')
        dm('\\text{6 der 49 Kugel werden als schwarz (\'günstig\') angenommen, die restlichen 43 als }')		
        dm('\\text{weiß. 4 schwarze kann man aus den 6 auf } {6 \choose 4} \\text{Arten ziehen, 2 weiße aus den 43}')
        dm('\\text {weißen auf } {43 \choose 2} \\text{ Arten, also ist die Anzahl der Ziehungen mit 4 Richtigen}')
        dm('{6 \choose 4} \cdot {43 \choose 2} = 13545 \\text{, woraus die gesuchte Wahrscheinlichkeit folgt}')
        dm('\\qquad P(\\text{\'4 Richtige\'}) = \dfrac{13545}{13983816} = \dfrac{645}{665896} = 0.000968619724401408') 
        print(' ') 		
        dm('\\text{Die Wahrscheinlichkeitsverteilung, die diesem Modell entspricht, ist eine}') 
        dm('\\text{Hypergeometrische Verteilung mit den Parametern   49, 6, 6}') 
        print(' ')	
		
    def spiel(self, *args, **kwargs):
        """Spiel zur Simulation"""
		
        if kwargs.get('h'):
            print("\nSpiel     ( Lotto 6 aus 49 )\n")
            print("Aufruf   l . spiel( /[ tipp ] /[, m ] )\n")
            print("               l        Lotto-Objekt")
            print("               tipp     abgegebener Tipp (Liste mit 6 Zahlen aus ")			
            print("                        {1, 2,..., 49}); fehlt die Angabe, wird")
            print("                        ein zufälliger Tipp angenommen")			
            print("               m        Anzahl Spiele (mit dem gleichen Tipp);")
            print("                        Standard=1\n")			
            print("Zusatz   z=ja  Es wird ein zufälliger Tipp angenommen")
            print("               (ein eventuell angegebener Tipp wird nicht beachtet)")
            print("         d=ja  Bei Angabe von m > 1 Rückgabe einer DatenReihe")
            print("               mit der Anzahl Richtige je Spiel")			
            return			
	  
        def zuf_tipp()	  :
            return sorted(zuf_zahl((1, 49), 6, w=False))
			
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
        if len(tipp) != 6 or not all([x in range(1, 50) for x in tipp]):			
            print('zufall: Tipp als Liste von 6 Zahlen zwischen 1 und 49 angeben')
            return			
        if len(set(tipp)) != 6:			
            print('zufall: die Zahlen müssen verschieden sein')
            return			
			
        ergebnis = zuf_tipp()		

        def dm(x):
            return display(Math(x))				

        print(' ')
			
        if m == 1:
            tipp.sort()		
            ti = latex(tipp).replace(',', '')
            ti = ti.replace('\\left [', '').replace('\\right ]', '')
            if not zufall:		
                dm('\\text{Tipp} \\quad \;\; : \\qquad' + ti)
            else:
                dm('\\text{Tipp} \\quad \;\; : \\qquad' + ti + '\\quad \\text{(zufällig)}')
            erg = latex(ergebnis).replace(',', '')
            erg = erg.replace('\\left [', '').replace('\\right ]', '')				
            dm('\\text{Ergebnis :} \\qquad \;' + erg)	
            erg = 0			
            for t in tipp:
                if t in ergebnis:
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
                for t in tipp:
                    if t in erg:
                        sum += 1
                if kwargs.get('d'):
                    dr += [sum]						
                try:						
                    summen[sum] += 1
                except KeyError:
                    summen[sum] = 1
            dm(latex(m) + '\; \\text{Spiele}')
            dm('\\text{Spielergebnisse (Richtige : Anzahl Spiele, relative Häufigkeit, \
    			  theoretische Wahr-}')
            dm('\\text{scheinlichkeit)}')			
            hgv = HyperGeometrischeVerteilung(49, 6, 6)
            for s in summen:
                sum = summen[s]	
                if s <= 4:
                    komma = '.4f'
                else:
                    komma = '.10f'
                ff = format(float(sum/m), '.4f')					
                if ff == '0.0000':
                    ff = format(float(sum/m), '.10f')					
                dm(latex(s) + '\\text{ : } \\quad' + latex(sum) + '\\quad' + \
				     latex(ff) + '\\quad ' + latex(format(float(hgv.P(s)), komma)) + \
				     '=' + latex(hgv.P(s)))
        print(' ')       
        if kwargs.get('d'):
            return DatenReihe(dr)			
				
    @property
    def richtige(self):
        """ZufallsGröße "Richtige" """							
        return HyperGeometrischeVerteilung(49, 6, 6)
	
    @property
    def gewinn(self):
        """ZufallsGröße "Gewinn" (entsprechend dem Gewinnplan)"""							

        e = 10 # Einsatz
        hgv = HyperGeometrischeVerteilung(49, 6, 6)		
        vert = { 564165 - e : hgv.P(6),
		           3239 - e : hgv.P(5),
		             47 - e : hgv.P(4),
		             11 - e : hgv.P(3),
                       - e : hgv.P(0) + hgv.P(1) + hgv.P(2) }
        return ZufallsGroesse(vert)					 
				 
    @property		
    def hilfe(self):  
        """Bezeichner der Attribute und Methoden"""
        lotto_hilfe(3)	
		
    h = hilfe					
		
				 	
			
# Benutzerhilfe für Lotto
# -----------------------

def lotto_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Attribute und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
Lotto - Objekt
	
Erzeugung    Lotto( )
				 
Zuweisung    l = Lotto()   (l - freier Bezeichner)
	   """)
        return 
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Lotto
 	
l.hilfe          Bezeichner der Eigenschaften und Methoden 
l.formeln        Berechnungsformeln
l.gewinn         ZufallsGröße-Objekt 'Gewinn'
l.regeln         Spielregeln
l.richtige       ZufallsGröße-Objekt 'Richtige'
l.spiel(...)  M  Spiel

Ausgewählte Eigenschaften und Methoden für die ZufallsGrößen 
l.richtige und l.gewinn

l.richtige.erw	       l.gewinn.erw             Erwartungswert
l.richtige.F                                 M  kumulative Verteilungsfunktion
l.richtige.hist                                 Histogramm der Wahrscheinlichkeiten
l.richtige.hist_kum                             Histogramm d. kum. Wahrscheinlichkeiten
l.richtige.n_omega     l.gewinn.n_omega         Größe der Ergebnismenge
l.richtige.omega       l.gewinn.omega           Ergebnismenge
l.richtige.P                                 M  Wahrscheinlichkeit eines Ereignisses
l.richtige.sigma                                Standardabweichung
l.richtige.stich_probe l.gewinn.stich_probe  M  Stichprobe
l.richtige.var                                  Varianz
l.richtige.versuch     l.gewinn.versuch         Versuch
l.richtige.vert        l.gewinn.vert            Wahrscheinlichkeitsverteilung 
l.richtige.vert_kum                             kumulierte Wahrscheinlichkeitsverteilung

Synonyme Bezeichner

hilfe         h
hist_kum      histKum
n_omega       nOmega
stich_probe   stichProbe
vert_kum      vertKum
""")
        return 
		
		
