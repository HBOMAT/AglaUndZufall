#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  Craps - Klasse  von zufall           
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

from sympy import Integer

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.datenreihe import DatenReihe
from zufall.lib.objekte.wuerfel import Wuerfel
from zufall.lib.funktionen.graf_funktionen import verlauf as verlauf_grafik

from zufall.lib.objekte.ausnahmen import ZufallError


# Craps - Klasse  
# --------------
	
class Craps(ZufallsObjekt):                                      
    """
	
Craps
	
**Erzeugung**    

   Craps( )

		"""
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            craps_hilfe(kwargs["h"])		
            return
  
        return ZufallsObjekt.__new__(cls)
					
			
    def __str__(self):  
        return "Craps"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def regeln(self):
        """Regeln für Crapsspiel"""	
		
        print("\nCraps - ein beliebtes Würfelspiel\n")
        print("Beim Craps wird mit zwei Würfeln gespielt, die man gleichzeitig wirft.\n")
        print("Bei einer Kombination von 1+6, 2+5, 3+4 oder 5+6, also der Augenzahl 7 ")
        print("oder 11 ist das Spiel augenblicklich gewonnen. Diese Kombinationen wer- ")
        print("den auch als Natural bezeichnet.\n")
        print("Bei der Kombination 1+1, 1+2 oder 6+6, also den Augenzahlen 2, 3 oder ")
        print("12, ist das Spiel sofort verloren. Diese Kombinationen werden auch als ")
        print("Craps bezeichnet.\n") 
        print("Bei den übrigen Kombinationen mit den Augenzahlen 4, 5, 6, 8, 9 oder 10 ")
        print("geht dasSpiel in eine zweite Runde. Wird in der zweiten Runde die selbe ")
        print("Summe gewürfelt wie beim ersten Wurf, ist das Spiel gewonnen. Ist die Sum-") 
        print("me 7, geht das Spiel verloren.")
        print("Bei einer anderen Kombination muss ein drittes Mal gewürfelt werden, wo-")
        print("bei für die dritte Runde die selben Regeln gelten wie für die zweite Run-")
        print("de.\n")		
        print("Es wird nach der ersten Runde, wenn nicht augenblicklich verloren oder ")
        print("gewonnen wurde, solange weitergewürfelt, bis die selbe Augenzahl erreicht ")
        print("wird wie in der ersten Runde oder das Spiel mit einer 7 verloren geht\n")	
        return		
		
    @property
    def formeln(self):
        """Formeln für Crapsspiel"""
	
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\mathrm{Berechnung\; der\; Gewinnwahrscheinlichkeit\; beim\;  Craps - Spiel}')
        print(' ')	
        dm('\mathrm{Die\;Wahrscheinlichkeiten\;beim\;gleichzeitigen\;Werfen\;von\;2\; Würfeln\;sind\;die}')
        dm('\mathrm{gleichen\; wie \;beim\;2-maligen\;Werfen\;eines\;Würfels.\;Als\;Grundlage\;für\;die\;}')
        dm('\mathrm{Berechnungen\;kann\;deshalb\;ein\;Wuerfel(2)-Objekt\;dienen}')
        print(' ')		
        dm('\mathrm{1.\;Wurf}')
        dm('\\qquad\mathrm{Die\;Wahrscheinlichkeit,\;sofort\;zu\;gewinnen,\;ist} \\quad P([7,11])=\\frac{2}{9}')		
        dm('\\qquad\mathrm{Analog\;ist\;die\;Wahrscheinlichkeit,\;sofort\;zu\; verlieren,} \\quad P([2,3,12])=\\frac{1}{9}')  		
        dm('\mathrm{2.\;und\;folgende\;Würfe}')
        dm('\\qquad\mathrm{Der\;2.\;Wurf\;wird\;mit\;einer\;Wahrscheinlichkeit\;von\;2/3\;ausgeführt}')
        dm('\\qquad\\qquad P([4,5,6,8,9,10])=\\frac{2}{3}')		
        dm('\\qquad\mathrm{Zur\;weiteren\;Berechnung\;ist\;die\;gemeinsame\;Betrachtung\;der\;Augensummen}')
        dm('\\qquad\mathrm{4\;und\;10,\;5\;und\;9\;sowie\;6\;und\; 8\;sinnvoll\;(beide\;beteiligte\;Zahlen\;haben\;je-}')
        dm('\\qquad\mathrm{weils\;die\;selbe\;Wahrscheinlichkeit,\;geworfen\;zu werden).\;Die\;Wahrschein-}')
        dm('\\qquad\mathrm{lichkeiten\;sind}')
        dm('\\qquad\\qquad P(4)=P(10)=\\frac{1}{12},\;\; P(5)=P(9)=\\frac{1}{9},\;\; P(6)=P(8)=\\frac{5}{36}') 		
        dm('\\qquad\mathrm{Die\;Situation\;wird\;für\;das\;Würfeln\;einer\;4\;oder\;10\;im\;1.\;Wurf\;anhand\;ei-}')
        dm('\\qquad\mathrm{nes\;Baumausschnittes \;dargestellt}')
        print('\n                                       --- 1/12 --- [4,10] gewonnen')
        print('                --- o                 |')
        print('               |                      |')
        print('          o ---.--- 1/6 --- [4,10] ---.--- 3/4 --- [sonst] --- ...')
        print('               |                      |')
        print('                --- o                 |')
        print('                                       --- 1/6 --- [7] verloren\n')		
        dm('\\qquad\mathrm{Mit\;einer\;Wahrscheinlichkeit\;von\;1/12\;wird\;im\;2.\;Wurf\;wieder\;die\;gleiche}')
        dm('\\qquad \mathrm{Zahl\;wie\;im\;ersten\;Wurf\;(eine\;4\;oder\;eine\;10)\;geworfen\;und\;gewonnen,\;mit}')
        dm('\\qquad \mathrm{einer\;Wahrscheinlichkeit\;von1/6\;eine\;7\;und\;damit\;verloren.\;Ein\;dritter\;Wurf}')
        dm('\\qquad\mathrm{wird\;mit\;einer\;Wahrscheinlichkeit\;von}' + \
           '\;\; 1-\\frac{1}{12}-\\frac{1}{6}=\\frac{3}{4} \mathrm{\;erforderlich}')
        dm('\\qquad\mathrm{Diese\;Überlegungen\;gelten\;auch\;für\;die\;nachfolgenden\; Würfe.\;Es\;ist}')		
        dm('\\qquad\\quad \mathrm{die\;Wahrscheinlichkeit,\;mit\;4\;oder\;10\;beim\;2.\;Wurf\;zu\;gewinnen}')
        dm('\\qquad\\qquad \\quad= \\frac{1}{6}\\cdot\\frac{1}{12}')		
        dm('\\qquad\\quad \mathrm{die\;Wahrscheinlichkeit,\;mit\;4\;oder\;10\;beim\;3.\;Wurf\;zu\;gewinnen}')
        dm('\\qquad\\qquad\\quad = \\frac{1}{6}\\cdot\\frac{3}{4}\\cdot\\frac{1}{12}')		
        dm('\\qquad\\quad \mathrm{die\;Wahrscheinlichkeit,\;mit\;4\;oder\;10\;beim\;n.\;Wurf\;zu\;gewinnen}')
        dm('\\qquad\\qquad\\quad = \\frac{1}{6}\\cdot \\left( \\frac{3}{4}\\right)^{n-2} \\cdot\\frac{1}{12}')		
        dm('\\qquad\mathrm{Damit\;ist\;die\;Wahrscheinlichkeit,\;irgendwann\;mit\;4\;oder\;10\;zu\;gewinnen}')		
        dm('\\qquad\\qquad P_{4oder10}=\\frac{1}{6}\\cdot\\frac{1}{12}+\\frac{1}{6}\\cdot\\frac{3}{4}' + \
           '\\cdot\\frac{1}{12} +\\frac{1}{6}\\cdot\\frac{3}{4} \\cdot\\frac{3}{4}\\cdot\\frac{1}{12}'+ \
           '+ \;...\;')
        dm('\\qquad\\qquad\\qquad\\quad =\\frac{1}{6}\\cdot \\left( \\sum_{n=0}^{\\infty} \\left( \\frac{3}{4}\\right)^n' + \
           '\\right) \\cdot\\frac{1}{12} ')		   
        dm('\\qquad\mathrm{Der\;mittlere\;Wert\;ist\;4\;(über\;die\;Formel\;für\;die\;geometrische\;Reihe\;zu\;er-}')
        dm('\\qquad\mathrm{halten),\;somit\;ist}')		
        dm('\\qquad\\quad\\quad P_{4oder10}=\\frac{1}{18}') 
        dm('\\qquad\mathrm{Analoge\;Überlegungen\;führen\;zu\;der\;Wahrscheinlichkeit,\;irgendwann\;mit\;5}')
        dm('\\qquad\mathrm{oder\;9\;zu\; gewinnen}')		
        dm('\\qquad\\quad\\quad P_{5oder9}=\\frac{2}{9}\\cdot \\left( \\sum_{n=0}^{\\infty} \\left( \\frac{13}{18}\\right)^n' + \
           '\\right) \\cdot\\frac{1}{9} = \\frac{2}{9}\\cdot\\frac{18}{5}\\cdot\\frac{1}{9} =' + \
           '\\frac{4}{45} ')		   
        dm('\\qquad\mathrm{und\;der\;Wahrscheinlichkeit,\;irgendwann\;mit\;6\;oder\;8\;zu\; gewinnen}')		
        dm('\\qquad\\quad\\quad P_{6oder8}=\\frac{5}{18}\\cdot \\left( \\sum_{n=0}^{\\infty} \\left( \\frac{25}{36}\\right)^n' + \
           '\\right) \\cdot\\frac{5}{36} = \\frac{5}{18}\\cdot\\frac{36}{11}\\cdot\\frac{5}{36} =' + \
           '\\frac{25}{198} ')		   
        dm('\mathrm{Zusammen\;mit\;der\;Wahrscheinlichkeit,\;im\;1.\;Wurf\;zu\;gewinnen,\;ergibt\;sich\;}')
        dm('\mathrm{die\;Gewinnwahrscheinlichkeit\;für\;das\;Spiel\;(die\; Wahrscheinlichkeit,\;irgend-}')
        dm('\mathrm{wann\; zu\; gewinnen)}')		
        dm('\\qquad P_{Gewinn} = P_{7\,imerstenWurf}+P_{4oder10}+P_{5oder9}+P_{6oder8}')
        dm('\qquad\\qquad\;\;\; =\\frac{2}{9}+\\frac{1}{18}+\\frac{4}{45}+\\frac{25}{198}=\\frac{244}{495}=0.4929')
        print(' ')	
        dm('\mathrm{Ein\;anderer\;Ansatz\;für\;die\;Berechnungen\;beruht\;auf\;der\;Theorie\;der\;}' + \
          '\mathrm{Markoff-}')  
        dm('\mathrm{Ketten.\;Dabei\;kann \;auch\;die\;mittlere\;Spieldauer\;berechnet\;werden.\; Sie\;beträgt}')
        dm('3.38\;\mathrm{Würfe}')
        print(' ')	
  				
    def spiel(self, *args, **kwargs):
		
        if kwargs.get('h'):
            print("\nSpiel    ( Craps )\n")
            print("Aufruf   c . spiel( /[ m ] )\n")		                     
            print("             c        Craps-Objekt")
            print("             m        Anzahl Spiele; Standard=1\n")			
            print("Zusatz   g=ja   Grafik des Gewinn-Verlaufes")
            print("         d=ja   Grafik des Verlaufes der mittleren Spieldauer")
            print("         dr=ja  Bei Angabe von m > 1 Rückgabe von zwei DatenReihen")
            print("                    - mit 1 (Gewinn) oder -1 (Verlust) je Spiel")			
            print("                    - mit der Spieldauer je Spiel")			
            print("         gdr=ja   Gewinnverlauf + DatenReihen")
            print("         ddr=ja   ebenso mittlere Dauer\n")
            return			
	  
        if len(args) not in (0, 1):
            print('zufall: kein oder ein Argument angeben')
            return
        if len(args) == 1:
            m = args[0]
            if not (isinstance(m, (int, Integer)) and m > 0):			
                print('zufall: für m positive ganze Zahl angeben')
                return

        wuerfel = Wuerfel(2, info=False)
				
        def _spiel(m, gewinn, zahl, verlauf, dauer):	
            for i in range(m):
                augen1 = wuerfel.wurf
                verlauf = [augen1]
                ende = False
                if augen1 in (7, 11):
                   gewinn += [1]
                   zahl += [7]
                   ende = True
                elif augen1 in (2, 3, 12):
                    gewinn += [-1]
                    ende = True
                while not ende:
                    augen = wuerfel.wurf
                    verlauf += [augen]
                    if augen == augen1:
                        gewinn += [1]
                        zahl += [augen]
                        ende = True
                    elif augen == 7:
                        gewinn += [-1]
                        ende = True
                dauer += [len(verlauf)]
            return gewinn, zahl, verlauf, dauer				
				
        def dm(x):
            return display(Math(x))				
			
        gewinn = []
        zahl = []
        verlauf = []		
        dauer = []
			
        if not args or m == 1:
            sp = _spiel(1, gewinn, zahl, verlauf, dauer)
            gewinn, zahl, verlauf, dauer = sp			
            print(' ')
            dm('\mathrm{1. Wurf:\\qquad\\quad}' + str(verlauf[0])) 
            for i, augen in enumerate(verlauf[1:]):
                if augen != verlauf[0]:
                    dm(str(i+2) + '\mathrm{. Wurf:\;\;}' + str(augen))	
                else:				
                    dm(str(i+2) + '\mathrm{. Wurf\\qquad\\quad}' + str(augen))
            if gewinn[0] == 1:			
                dm('\mathrm{Spiel\; gewonnen}')
            else:			
                dm('\mathrm{Spiel\; verloren}')
            print(' ')
            return			

        else:
            gewinn, zahl, verlauf, dauer = _spiel(m, gewinn, zahl, verlauf, dauer)
            if kwargs.get('g') or kwargs.get('gdr'):
                print(' ')			
                dm('\\qquad\mathrm{Verlauf\;Anzahl\;Gewinnspiele - Anzahl\;Verlustspiele}')			
                verlauf_grafik(gewinn, art='summe', xlabel='Anzahl Spiele')
            elif kwargs.get('d') or kwargs.get('ddr'):	
                pass
                print(' ')			
                dm('\;\;\;\mathrm{Verlauf\;Mittlere\; Spieldauer;\; grün-theoretischer\; Erwartungswert\; (3.38)}')			
                verlauf_grafik(dauer, art='mittel', vergl=3.38, xlabel='Anzahl Spiele')			
            print(' ')
            gewonnen = gewinn.count(1)
            verloren = len(gewinn) - gewonnen
            if not kwargs:			
                gew_7_11 = zahl.count(7) + zahl.count(11)
                gew_4_10 = zahl.count(4) + zahl.count(10)
                gew_5_9 = zahl.count(5) + zahl.count(9)
                gew_6_8 = zahl.count(6) + zahl.count(8)
                anz = len(gewinn)
                p_gewonnen = '{0:.2f}'.format(float(100*gewonnen/anz)) + '\,\%'	
                t_gewonnen = '{0:.2f}'.format(float(100*244/495))	+ '\,\%'
                p_verloren = '{0:.2f}'.format(float(100*verloren/anz))+ '\,\%'	
                t_verloren = '{0:.2f}'.format(float(100*251/495))+ '\,\%'
                p_7_11 = '{0:.2f}'.format(float(100*gew_7_11/anz)) + '\,\%'	
                t_7_11 = '{0:.2f}'.format(float(100*2/9)) + '\,\%'
                p_4_10 = '{0:.2f}'.format(float(100*gew_4_10/anz)) + '\,\%'	
                t_4_10 = '{0:.2f}'.format(float(100*1/18))	+ '\,\%'
                p_5_9 = '{0:.2f}'.format(float(100*gew_5_9/anz)) + '\,\%'	
                t_5_9 = '{0:.2f}'.format(float(100*4/45))	+ '\,\%'
                p_6_8 = '{0:.2f}'.format(float(100*gew_6_8/anz)) + '\,\%'	
                t_6_8 = '{0:.2f}'.format(float(100*25/198))	+ '\,\%'
                m_dauer = '{0:.2f}'.format(float(sum(dauer)/anz))			
                dm('\mathrm{Spielergebnisse}')
                dm('\mathrm{Gewonnen:\;\;}' + str(gewonnen) + '\mathrm{\;\, Spiele}' + \
                 '\\qquad\mathrm{relative\;Häufigkeit=\,}' + p_gewonnen)
                dm('\\qquad\\qquad\\qquad\mathrm{theoretische\;Wahrcheinlichkeit} = \\frac{244}{495}=' + t_gewonnen) 			   
                dm('\mathrm{Verloren:\;\;\;\;}' + str(verloren) + '\mathrm{\;\,Spiele}' + \
                   '\\qquad\mathrm{relative\;Häufigkeit=\,}' + p_verloren)
                dm('\\qquad\\qquad\\qquad\mathrm{theoretische\;Wahrcheinlichkeit} = \\frac{251}{495}=' + t_verloren) 			   			
                dm('\mathrm{Gewonnen\;mit\;7,11:\;\;}' + str(gew_7_11) + \
                   '\\qquad\mathrm{rel.H.=\,}' + p_7_11 + '\\qquad' + \
                   '\mathrm{theor.W.} = \\frac{2}{9}=' + t_7_11) 			   
                dm('\mathrm{Gewonnen\;mit\;4,10:\;\;}' + str(gew_4_10) + \
                   '\\qquad\mathrm{rel.H.=\,}' + p_4_10 + '\\qquad' + \
                   '\mathrm{theor.W.} = \\frac{1}{18}=' + t_4_10) 			   
                dm('\mathrm{Gewonnen\;mit\;5,9:\,\;\;\;}' + str(gew_5_9) + \
                   '\\qquad\mathrm{rel.H.=\,}' + p_5_9 + '\\qquad' + \
                   '\mathrm{theor.W.} = \\frac{4}{45}=' + t_5_9) 			   
                dm('\mathrm{Gewonnen\;mit\;6, 8:\,\;\;\;}' + str(gew_6_8) + \
                   '\\qquad\mathrm{rel.H.=\,}' + p_6_8 + '\\qquad' + \
                   '\mathrm{theor.W.} = \\frac{25}{198}=' + t_6_8) 			   
                dm('\mathrm{Mittlere\; Spieldauer:\;\;}' + m_dauer + '\\qquad' + \
                   '\mathrm{theoretischer\;Wert:\;\;3.38}')
                print(' ')
            if kwargs.get('dr') or kwargs.get('gdr') or kwargs.get('ddr'):
                print('Rückgabe einer DatenReihe mit 1 (Gewonnen) oder -1 (Verloren) je Spiel')
                print('und einer DatenReihe mit der Dauer je Spiel')
                print(' ')				
                gewinn, dauer = DatenReihe(gewinn), DatenReihe(dauer)	
                return gewinn, dauer
				
				
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        craps_hilfe(3)	
		
    h = hilfe					
				
			
			
# Benutzerhilfe für Craps
# -----------------------

def craps_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
Craps - Objekt
	
Erzeugung    Craps( )
				 
Zuweisung    c = Craps()   (c - freier Bezeichner)
	   """)
        return 
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Craps
 	
c.hilfe          Bezeichner der Eigenschaften und Methoden
c.formeln        Berechnungsformeln
c.regeln         Spielregeln
c.spiel(...)  M  Spiel

Synonymer Bezeichner

hilfe    h
""")
        return 
		
