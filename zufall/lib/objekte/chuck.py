#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  ChuckALuck - Klasse  von zufall           
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

from sympy import Rational, Integer
from sympy.printing import latex

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse
from zufall.lib.objekte.datenreihe import DatenReihe
from zufall.lib.funktionen.funktionen import zuf_zahl, anzahl

from zufall.lib.objekte.ausnahmen import ZufallError


# ChuckALuck - Klasse  
# -------------------
	
class ChuckALuck(ZufallsObjekt):                                      
    """Chuck a Luck - ein Würfelspiel aus den USA

**Kurzname**     **Chuck**
	
**Erzeugung**    

   Chuck( )

		"""
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            chuck_hilfe(kwargs["h"])		
            return
  
        return ZufallsObjekt.__new__(cls)
					
			
    def __str__(self):  
        return "ChuckALuck"

		
# Eigenschaften + Methoden
# ------------------------

    @property
    def regeln(self):
        """Regeln für Chuck"""	
		
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\\text{Chuck a Luck  ( Würfelspiel aus den USA )}')
        print(' ')		
        dm('\\text{Ein Spieler zahlt an den Glücksspielleiter 1 Dollar Einsatz und nennt eine der}') 
        dm('\\text{Zahlen von 1 bis 6. Danach darf er dreimal würfeln. Zeigt der Würfel bei genau }') 
        dm('\\text{einem Wurf die genannte Zahl, so bekommt der Spieler 2 Dollar ausgezahlt. Zeigt}') 
        dm('\\text{der Würfel genau zweimal die genannte Zahl, erhält der Spieler 3 Dollar, und sind}') 
        dm('\\text{alle drei Wurfergebnisse gleich der genannten Zahl, so werden 4 Dollar an den Spie- }') 
        dm('\\text{ler zurückgegeben. In allen anderen Fällen ist der Einsatz verloren.}')
        print(' ')
        dm('\\text{Für den Spieler gilt} \\quad \\text{Gewinn = Auszahlung - Einsatz}')
        print(' ')
        return		
		
    @property
    def formeln(self):
        """Formeln für Chuck"""	
	
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\\text{Berechnung der Wahrscheinlichkeiten beim  Chuck a Luck - Spiel}')
        dm('\\text{Die genannte Zahl sei 6 (die Überlegungen sind für alle Zahlen die gleichen)}')
        dm('\\text{Die Ergebnismenge ist} \: \{ \;[i, j, k] \; | \; i,j,k \
            \in \{ 1,2,3,4,5,6 \} \;\} \\text{, es gibt} \: 6^3 = 216 ')
        dm('\\text{Möglichkeiten}')

        dm('\\text{3 Übereinstimmungen:} \\quad [6,6,6] \\quad \\text{Wahrscheinlichkeit = } \\dfrac{1}{216}')
        dm('\\text{2 Übereinstimmungen:}  \\quad 	[6,6,1], [6,6,2], [6,6,3], [6,6,4], [6,6,5],')
        dm('\\qquad\\qquad\qquad\\qquad\\quad [6,1,6], [6,2,6], [6,3,6], [6,4,6], [6,5,6],')
        dm('\\qquad\\qquad\qquad\\qquad\\quad[1,6,6], [2,6,6], [3,6,6], [3,6,6], [5,6,6]')
        dm('\\qquad\\qquad\qquad\\qquad\\qquad\\qquad\\quad\: \\text{Wahrscheinlichkeit = } \
             \\dfrac{15}{216} = \\dfrac{5}{72}')
        dm('\\text{1 Übereinstimmung:} \\quad 5^2\cdot 3 = 75 \\quad \\text{Wahrscheinlichkeit = } \\dfrac{75}{216} \
            = \\dfrac{25}{72}')		
        dm('\\text{0 Übereinstimmungen:} \\quad 5^3=125 \\quad \\text{Wahrscheinlichkeit = } \\dfrac{125}{216}')					
        dm('\\text{Als Zufallsgröße wird der Gewinn betrachtet. Der Erwartungswert ist} \
            \:-\\dfrac{17}{216} = -7.87\%')	
        print(' ') 			
				
    @property
    def gewinn(self):
        """ZufallsGröße "Gewinn" """		
        vert = {3:Rational(1, 216), 2:Rational(5, 72), 1:Rational(25, 72), \
               -1:Rational(125, 216), 0:0}		
        return ZufallsGroesse(vert, kontrolle=False)

		 
    def spiel(self, *args, **kwargs):
        """Spiel zur Simulation"""
		
        if kwargs.get('h'):
            print("\nSpiel     ( Chuck )\n")
            print("Aufruf    ch . spiel( /[ zahl ] /[, m ] )\n")
            print("               ch       Chuck-Objekt")
            print("               zahl     genannte Zahl aus {0, 1, 2, 3, 4, 5, 6})")			
            print("                        fehlt die Angabe, wird eine zufällige Zahl ange-")
            print("                        nommen")			
            print("               m        Anzahl Spiele (mit der selben Zahl); Standard=1\n")
            print("Zusatz   z=ja  Es wird eine zufällige Zahl angenommen;")
            print("               eine eventuell angegebene Zahl wird nicht beachtet")
            print("         d=ja  Bei Angabe von m > 1 Rückgabe einer DatenReihe")
            print("               mit dem Gewinn pro Spiel\n")			
            return			
	  
        zufall = False	  
        if len(args) not in (0, 1, 2):
            print('zufall: 0 bis 2 Argumente angeben')
            return
        if len(args) == 0:
            m = 1
            zufall = True				
        elif len(args) == 1:
            m = 1		
            tipp = args[0]
            if not tipp in range(1, 7):	
                print('zufall: Zahl aus {1,2,3,4,5,6}(genannte Zahl) angeben')
                return				
        elif len(args) == 2:
            tipp, m = args	
            if not tipp in range(1, 7):	
                print('zufall: genannte Zahl aus {1,2,3,4,5,6} angeben')
                return				
            if not (isinstance(m, (int, Integer)) and m > 0):	
                print('zufall: Anzahl der Spiele > 0 angeben')
                return				

        if kwargs.get('z'):
            zufall = True

        if zufall:
            tipp = zuf_zahl((1, 6))
						
        ergebnisse = zuf_zahl((1, 6), 3)			

        def dm(x):
            return display(Math(x))				

        print(' ')
			
        if m == 1:
            if not zufall:		
                 dm('\\text{Genannt}' + '\\quad :' + '\:\:\;' + latex(tipp))
            else:
                dm('\\text{Genannt}' + '\\quad :\;' + latex(tipp) + '\;\;\\text{(zufällig)}')
            dm('\\text{Ergebnisse} \, : \;' + latex(ergebnisse))	
            erg = 0			
            for e in ergebnisse:
                if e == tipp:
                    erg += 1
            if erg == 0:
                tt = '\\text{(Verloren, Gewinn = -1)}'			
            if erg == 1:
                tt = '\\text{(Gewonnen, Gewinn = 1)}'			
            if erg == 2:
                tt = '\\text{(Gewonnen, Gewinn = 2)}'			
            if erg == 3:
                tt = '\\text{(Gewonnen, Gewinn = 3)}'			
            dm(latex(erg) + '\;\\text{Richtige}' + '\quad\:\,' + tt)	
        else:			
            summen = {}
            dr = []			
            for i in range(m):
                erg = zuf_zahl((1, 6), 3)
                gew = anzahl(tipp)(erg)
                if gew == 0:
                    gew = -1				
                if kwargs.get('d'):
                    dr += [gew]						
                try:						
                    summen[gew] += 1
                except KeyError:
                    summen[gew] = 1
            dm(latex(m) + '\; \\text{Spiele}')
            dm('\\text{Spielergebnisse (Gewinn : Anzahl Spiele, relative Häufigkeit, }' +
    			 '\\text{theoretische Wahr-}') 
            dm('\\text{scheinlichkeit)}')			
            g = self.gewinn
            for s in summen:
                sum = summen[s]		
                dm(latex(s) + '\\text{ : } \\quad' + latex(sum) + '\\quad' + \
				   latex(format(float(sum/m), '.4f')) + '\\quad ' + \
				   latex(format(float(g.P(s)), '.4f')) + '=' + latex(g.P(s))  )
        print(' ')       
        if kwargs.get('d'):
            return DatenReihe(dr)			
			
			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        chuck_hilfe(3)	
		
    h = hilfe					
			

			
# Benutzerhilfe für ChuckALuck
# ----------------------------

def chuck_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
ChuckALuck - Objekt

Kurzname     Chuck
	
Erzeugung    Chuck( )
				 
Zuweisung    ch = Chuck()   (ch - freier Bezeichner)
	   """)
        return 
		
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Chuck
 	
ch.hilfe          Bezeichner der Eigenschaften und Methoden
ch.formeln        Berechnungsformeln
ch.regeln         Spielregeln
ch.gewinn         ZufallsGröße 'Gewinn'
ch.spiel(...)  M  Spiel

Synonymer Bezeichner

hilfe    h

Eigenschaften und Methoden für die ZufallsGröße ch.gewinn siehe Hilfeseite 
für ZufallsGröße
""")
        return 
		
		
Chuck = ChuckALuck
