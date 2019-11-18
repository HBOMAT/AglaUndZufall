#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  Roulette - Klasse  von zufall           
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



import matplotlib.pyplot as plt
import matplotlib.patches as patches

from sympy import Rational, Integer, nsimplify
from sympy.core.compatibility import iterable
from sympy.printing.latex import latex

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.gleich_verteilung import GleichVerteilung
from zufall.lib.objekte.datenreihe import DatenReihe
from zufall.lib.funktionen.graf_funktionen import verlauf as verlauf_grafik

from zufall.lib.objekte.ausnahmen import ZufallError



# Roulette - Klasse  
# -----------------
	
class Roulette(ZufallsObjekt):                                      
    """
	
Roulette - Spiel
	
**Erzeugung** 

   Roulette( ) 
   		 
    """			
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3, 4):                         
            roulette_hilfe(kwargs["h"])		
            return
  
        cls.colonne1     = {1,4,7,10,13,16,19,22,25,28,31,34} 
        cls.colonne2     = {2,5,8,11,14,17,20,23,26,29,32,35} 			 
        cls.colonne3     = {3,6,9,12,15,18,21,24,27,30,33,36}			
        cls.douze_premier = set(range(1, 13))			 
        cls.douze_milieu  = set(range(13, 25))			
        cls.douze_dernier = set(range(25, 37))			 
        cls.pair         = set(range(2, 37, 2))          
        cls.impair       = set(range(1, 36, 2))			
        cls.rouge        = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}			
        cls.noir         = set(range(1, 37)).difference(cls.rouge)		
        cls.manque       = set(range(1, 19))			
        cls.passe        = set(range(19, 37))			
		
        return ZufallsObjekt.__new__(cls)
					
			
    def __str__(self):  
        return "Roulette"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def omega(self):
        """Ergebnismenge"""	
        return set(range(37))
		
    @property
    def regeln(self):
        """Regeln für Roulettespiel"""	
		
        print("\nRoulette - Glücksspiel\n")
        print("Eine Kugel wird in eine sich drehende Scheibe geworfen. Sie landet in ") 
        print("einem der Felder 0 bis 36, die auf der Scheibe in bunter Reihenfolge")
        print("angeordnet sind (Gewinnfeld)\n")
        print("Auf dem Spielbrett setzt man Spielmarken (Chips) und gewinnt, wenn die ") 
        print("Vorhersage eintrifft, das heißt, wenn das Gewinnfeld durch die getrof-")
        print("fene Wahl erfaßt wird; zu den Setzmöglichkeiten siehe Hilfeseite\n")
        print("Wenn die Vorhersage nicht eintrifft, ist der gesetzte Chip verloren ") 
        print("Das entspricht einer Gewinnquote von -1 : 1\n")
        return		
		
    @property
    def brett(self):
        """Spielbrett / -tisch (Abbildung)"""			
		
        def pline(x, y):
            return plt.plot(x, y, color=(0,0,0), lw=0.8)

        def prot(x, y, t):
            return ax.text(x, y, t, fontsize=9, horizontalalignment='center', 
                  verticalalignment='center', color=(1,0,0), 
                  fontname='Times New Roman')

        def pblack(x, y, t):
            return ax.text(x, y, t, fontsize=9, horizontalalignment='center', 
                   verticalalignment='center', color=(0,0,0),
                   fontname='Times New Roman')

        def punt(x, y):
            ax.text(x, y, '12', fontsize=6, horizontalalignment='center', 
                  verticalalignment='center', color=(0,0,0),
                   fontname='Times New Roman')

        dx, dy = 1.5, 1.5
        fig = plt.figure(figsize=(3, 4))
        ax = fig.add_subplot(1, 1, 1)
        ax.spines['top'].set_visible(False)		
        ax.spines['bottom'].set_visible(False)		
        ax.spines['right'].set_visible(False)		
        ax.spines['left'].set_visible(False)		
        ax.set_xticks([])
        plt.axes().xaxis.set_ticks_position('none')
        ax.set_yticks([])
        plt.axes().yaxis.set_ticks_position('none')
        plt.xlim(0, 10*dx)
        plt.ylim(-0.1, 15*dy)
        pline([3*dx, 6*dx, 6*dx, 3*dx, 3*dx], [0, 0, 14*dy, 14*dy, 0])
        pline([4*dx, 4*dx], [dy, 13*dy])
        pline([5*dx, 5*dx], [dy, 13*dy])
        for i in range(1, 14):
            pline([3*dx, 6*dx], [i*dy, i*dy])
        pline([0, 0], [2*dy, 12*dy])
        pline([9*dx, 9*dx], [2*dy, 12*dy])
        pline([3*dx, 0], [dy, 2*dy])
        pline([3*dx, 0], [2*dy, 3*dy])
        pline([6*dx, 9*dx], [dy, 2*dy])
        pline([6*dx, 9*dx], [2*dy, 3*dy])
        pline([0, 3*dx], [12*dy, 13*dy])
        pline([9*dx, 6*dx], [12*dy, 13*dy])
        pline([0, 9*dx], [5*dy, 5*dy])
        pline([0, 9*dx], [9*dy, 9*dy])
        pline([2*dx, 2*dx], [1.35*dy, 2.3*dy])
        pline([7*dx, 7*dx], [1.35*dy, 2.3*dy])
        pline([dx, dx], [1.7*dy, 2.65*dy])
        pline([8*dx, 8*dx], [1.7*dy, 2.65*dy])
        ax.add_patch(patches.RegularPolygon(
            (1.7*dx, 3.7*dy), 4, 0.6*dx, color=(0,0,0)))
        ax.add_patch(patches.RegularPolygon(
            (7.4*dx, 3.7*dy), 4, 0.6*dx, facecolor=(1,0,0)))
        ax.text(4.5*dx, 13.4*dy, '0', fontsize=9, horizontalalignment='center', \
               verticalalignment='center', color=(0,1,0))
        prot(3.5*dx, 12.4*dy, '1')
        pblack(4.5*dx, 12.4*dy, '2')
        prot(5.5*dx, 12.4*dy, '3')
        pblack(3.5*dx, 11.4*dy, '4')
        prot(4.5*dx, 11.4*dy, '5')
        pblack(5.5*dx, 11.4*dy, '6')
        prot(3.5*dx, 10.4*dy, '7')
        pblack(4.5*dx, 10.4*dy, '8')
        prot(5.5*dx, 10.4*dy, '9')
        pblack(3.5*dx, 9.4*dy, '10')
        pblack(4.5*dx, 9.4*dy, '11')
        prot(5.5*dx, 9.4*dy, '12')
        pblack(3.5*dx, 8.4*dy, '13')
        prot(4.5*dx, 8.4*dy, '14')
        pblack(5.5*dx, 8.4*dy, '15')
        prot(3.5*dx, 7.4*dy, '16')
        pblack(4.5*dx, 7.4*dy, '17')
        prot(5.5*dx, 7.4*dy, '18')
        prot(3.5*dx, 6.4*dy, '19')
        pblack(4.5*dx, 6.4*dy, '20')
        prot(5.5*dx, 6.4*dy, '21')
        pblack(3.5*dx, 5.4*dy, '22')
        prot(4.5*dx, 5.4*dy, '23')
        pblack(5.5*dx, 5.4*dy, '24')
        prot(3.5*dx, 4.4*dy, '25')
        pblack(4.5*dx, 4.4*dy, '26')
        prot(5.5*dx, 4.4*dy, '27')
        pblack(3.5*dx, 3.4*dy, '28')
        pblack(4.5*dx, 3.4*dy, '29')
        prot(5.5*dx, 3.4*dy, '30')
        pblack(3.5*dx, 2.4*dy, '31')
        prot(4.5*dx, 2.4*dy, '32')
        pblack(5.5*dx, 2.4*dy, '33')     
        prot(3.5*dx, 1.4*dy, '34')
        pblack(4.5*dx, 1.4*dy, '35')
        prot(5.5*dx, 1.4*dy, '36')  
        pblack(0.5*dx, 2.4*dy, 'P')    
        pblack(8.5*dx, 2.4*dy, 'P')   
        punt(0.7*dx, 2.13*dy)
        punt(8.7*dx, 2.13*dy)
        pblack(1.35*dx, 2.07*dy, 'M')    
        pblack(7.35*dx, 2.07*dy, 'M')   
        punt(1.72*dx, 1.85*dy)
        punt(7.72*dx, 1.85*dy)    
        pblack(2.45*dx, 1.75*dy, 'D')    
        pblack(6.45*dx, 1.75*dy, 'D')   
        punt(2.75*dx, 1.48*dy)
        punt(6.75*dx, 1.48*dy)   
        pblack(1.5*dx, 10.5*dy, 'Passe')
        pblack(7.5*dx, 10.5*dy, 'Manque')
        pblack(1.5*dx, 7*dy, 'Pair')
        pblack(7.5*dx, 7*dy, 'Impair')
       
        plt.show()

    tisch = brett
	
    @property
    def formeln(self):
        """Berechnungsformeln"""	
	
        def dm(x):
            return display(Math(x))		
		
        print(' ')		
        dm('\mathrm{Gewinnerwartung\;beim\; Roulette - Spiel}')
        print(' ')	
        dm('\mathrm{Gewinnerwartung\; bei\; einer\; Setzmöglichkeit\; (Chance):}')
        dm('\\qquad GewinnQuote \cdot GewinnWahrscheinlichkeit\, + \, (-1) \cdot VerlustWahrscheinlichkeit')
        dm('\\qquad \mathrm{(\,-1 = Verlustquote\;[gesetzter\;Chip]\,)}')
        dm('\mathrm{Die\; Wahrscheinlichkeiten\; der\; Chancen\; werden\; so\; berechnet:}')		
        dm('\qquad P( Chance ) = (Anzahl\; der\; Zahlen\; in\; der\; Chance)\; / \;37')	
        print(' ')		
        dm('\mathrm{ Erwartung\; bei\; den\; einzelnen\; Chancen: \\qquad (s.a.\; Hilfeseite)}')
        dm('\mathrm{ Chance \\qquad\\qquad\;\; Anzahl \\qquad Erwartung \;\\qquad\\qquad\\quad	\, in\; \% \;zum}')
        dm('\mathrm{\\qquad\\qquad\\qquad\\quad\, Zahlen	\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad	Einsatz}')	
        dm('\mathrm{plein} \;\,\\qquad\\qquad\\quad\\quad\\quad 1 \\quad\\quad	35 \\cdot \\frac{1}{37} - \\frac{36}{37} = -\\frac{1}{37} \\quad\\quad -2.7 \%')		
        dm('\mathrm{a\; cheval} \;\\qquad\\qquad\\quad\\quad 2 \\quad\\quad	17 \\cdot \\frac{2}{37} - \\frac{35}{37} = -\\frac{1}{37} \\quad\\quad -2.7 \%')		
        dm('\mathrm{transversale\; plein} \\quad\\qquad 3 \\quad\\quad	11 \\cdot \\frac{3}{37} - \\frac{34}{37} = -\\frac{1}{37} \\quad\\quad -2.7 \%')		
        dm('\mathrm{carre} \;\,\\qquad\\qquad\\quad\\quad\\quad 4 \\quad\\quad	8 \\cdot \\frac{4}{37} - \\frac{33}{37} = -\\frac{1}{37} \;\,\\quad\\quad -2.7 \%')		
        dm('\mathrm{transversale\; simple} \,\;\\qquad 6 \\quad\\quad	5 \\cdot \\frac{6}{37} - \\frac{31}{37} = -\\frac{1}{37} \;\\quad\\quad -2.7 \%')		
        dm('\mathrm{Kolonne,\; Dutzend} \,\,\\qquad 12 \\quad\\quad	2 \\cdot \\frac{12}{37} - \\frac{25}{37} = -\\frac{1}{37} \;\\quad\\quad -2.7 \%')		
        dm('\mathrm{einfache\; Chancen} \;\;\\qquad 18 \\quad\\quad	1 \\cdot \\frac{18}{37} - \\frac{19}{37} = -\\frac{1}{37} \;\\quad\\quad -2.7 \%')		
        print(' ')		
		
		
    def P(self, *args, **kwargs):
        """Wahrscheinlichkeit eines Ereignisses"""
		
        if kwargs.get('h'):
            print("\nWahrscheinlichkeit eines Ereignisses\n")
            print("Aufruf   r . P( e )\n")		                     
            print("                r    Roulette-Objekt")
            print("                e    Zahl aus {0,...,36} | Menge/Liste/Tupel von Zahlen |")
            print("                     Chance beim einmaligen Spielen (s. Hilfeseite)\n")
            print("  oder   r . P( e, e1 )\n")		                     
            print("Bei der Angabe von zwei Ereignissen wird die bedingte Wahrscheinlich-")
            print("keit P( e | e1 ) berechnet\n")
            print("Beispiele")
            print("r.P( 4 )   r.P( {12} )   r.P( r.colonne1 )")
            print("r.P( { 28, 29, 30 } )    r.P( [28, 29, 30] )")   
            print("r.P( 'r.rouge und r.pair' )") 
            print("r.P( 12, r.rouge )   (bedingte Wahrscheinlichkeit)\n")			
            return			
			
        if len(args) not in (1, 2):
            print('zufall: ein oder zwei Ereignisse angeben')
            return	

        def teil(x):
            if isinstance(x, set):
                return all([y in omega for y in x])
            else:
                if x in omega:
                    return True
                return False
			   
        omega = self.omega		
				  
        if len(args) == 1:
            e = args[0]
            if e == 0:
                pp = Rational(1, 37)			
            elif not e:
                pp = 0			
            elif not iterable(e) and e in omega:					
                pp = Rational(1, 37)
            elif iterable(e):
                if not all([x in omega for x in e]):
                    print('zufall: Elemente der Ergebnismenge angeben')
                    return
                if not len(e) in (1, 2, 3, 4, 6, 12, 18):					
                    print('zufall: 1,2,3,4 oder 6 Zahlen oder benannte Chance angeben')
                    return
                if len(e) == 2:
                    if not set(e) in _a_cheval:
                        print('zufall: keine a_cheval-Chance')
                        return
                elif len(e) == 3:
                    if not set(e) in _transversale_plein:
                        print('zufall: keine transversale_plein-Chance')
                        return
                elif len(e) == 4:
                    if not set(e) in _carre:
                        print('zufall: keine carre-Chance')
                        return
                elif len(e) == 6:
                    if not set(e) in _transversale_simple:
                        print('zufall: keine transversale_simple-Chance')
                        return
                elif len(e) == 12:
                     if not set(e) in [self.colonne1, self.colonne2, self.colonne3, self.douze_premier, \
				           self.douze_milieu, self.douze_dernier]:
                         print('zufall: keine Chance mit 12 Zahlen')
                         return
                elif len(e) == 18:
                     if not set(e) in [self.pair, self.impair, self.rouge, self.noir, self.manque, \
                         self.passe]:
                         print('zufall: keine Chance mit 18 Zahlen')
                         return
                pp = Rational(len(e), 37)					
            elif isinstance(e, str):
                uu, oo, nn = e.find('und'), e.find('oder'), e.find('nicht')			
                try:
                    if uu >= 0:
                        a, b = e[:uu].strip(), e[uu+3:].strip() 					  
                        ia, ib = a.find('.'), b.find('.')
                        a, b = a[ia+1:], b[ib+1:]
                        a, b = 'self.' + a, 'self.' + b						
                        a, b = eval(a), eval(b)
                        if not (teil(a) and teil(b)):
                            print('zufall: Ereignisse bei Roulette angeben')
                            return
                        if isinstance(a, set):							
                            if isinstance(b, set):							
                                ee = a.intersection(b)
                            else:								
                                ee = a.intersection(set([b]))
                        else:	
                            if isinstance(b, set):							
                                ee = set([a]).intersection(b)
                            else:								
                                ee = set([a]).intersection(set([b]))						
                        pp = Rational(len(ee), 37)											
                    elif oo > 0:
                        a, b = e[:oo].strip(), e[oo+3:].strip()					  
                        ia, ib = a.find('.'), b.find('.')
                        a, b = a[ia+1:], b[ib+1:]
                        a, b = 'self.' + a, 'self.' + b						
                        a, b = eval(a), eval(b)
                        if not (teil(a) and teil(b)):
                            print('zufall: Ereignisse bei Roulette angeben')
                            return
                        if isinstance(a, set):							
                            if isinstance(b, set):							
                                ee = a.union(b)
                            else:								
                                ee = a.union(set([b]))
                        else:	
                            if isinstance(b, set):
                                ee = set([a]).union(b)
                            else:								
                                ee = set([a]).union(set([b]))						
                        pp = Rational(len(ee), 37)											
                    elif nn >= 0:
                        a = e[nn+5:].strip()				  
                        ia = a.find('.')
                        a = a[ia+1:]
                        a = 'self.' + a						
                        a = eval(a)
                        if not teil(a):
                            print('zufall: Ereignis bei Roulette angeben')
                            return
                        if isinstance(a, set):							
                           ee = omega.difference(a)
                        else:
                            ee = omega.difference(set([a]))						
                        pp = Rational(len(ee), 37)											
                    else:
                        ee = eval(e)
                        pp = Rational(len(ee), 37)											
                except:
                    print('zufall:', 'Ausdruck überprüfen')
                    return			
            else:
                print('zufall: Ereignis bei Roulette angeben')
                return
							
        elif len(args) == 2: 
            e1, e2 = args	
            if iterable(e1):
                e1 = set(e1)			
            if iterable(e2):
                e2 = set(e2)
            try:			
                if isinstance(e1, set):
                    if isinstance(e2, set):
                        ee = e1.intersection(e2)
                    else:
                        ee = e1.intersection(set([e2]))
                else:
                    if isinstance(e2, set):
                        ee = set([e1]).intersection(e2)
                    else:
                        ee = set([e1]).intersection(set([e2]))
                pp1, pp2 = self.P(ee), self.P(e2)
                pp = nsimplify(pp1 / pp2, rational=True)
            except:
                print('zufall: die Angaben bitte überprüfen')	
                return
            			
        return pp	
		
		
    def spiel(self, *args, **kwargs):
        """Spiel"""
		
        if kwargs.get('h'):
            print("\nSpiel     ( Roulette )\n")
            print("Aufruf    r . spiel( chance /[, m ] )\n")		                     
            print("              r        Roulette-Objekt")
            print("              chance   gesetzte Chance - einzelne Zahl oder Menge von ")
            print("                       1-6 Zahlen aus {0,1,...,36} | r.colonne1 |") 
            print("                       r.colonne2 | r.colonne3 | r.douze_premier |")
            print("                       r.douze_milieu | r.douze_dernier | r.pair |") 
            print("                       r.impair | r.rouge | r.noir | r.manque |") 
            print("                       r.passe")			
            print("              m        Anzahl Spiele; Standard=1\n")			
            print("Zusatz   g=ja   Grafik des Gewinn-Verlaufes")
            print("         m=ja   Grafik des Verlaufes des mittleren Gewinns")
            print("         d=ja   Bei Angabe von m > 1 Rückgabe einer DatenReihe mit dem") 
            print("                Gewinn/Verlust je Spiel")
            print("         gd=ja  Gewinnverlauf + DatenReihe")
            print("         md=ja  Mittlerer Gewinn + DatenReihe\n")
            return			

        try:	  
            if len(args) not in (1, 2):
                raise ZufallError("ein oder zwei Argumente angeben")
            chance = args[0]			
            if not (iterable(chance) or isinstance(chance, (int, Integer))):
                raise ZufallError("einzelne Zahl oder Menge von Zahlen angeben")					
            if isinstance(chance, (int, Integer)):
                if chance not in self.omega:
                    raise ZufallError("Element der Ergebnismenge angeben")					
                chance = set([chance])	
            else:
                chance = set(chance)
                if not all([x in self.omega for x in chance]):
                    raise ZufallError("Element der Ergebnismenge angeben")					
                if len(chance) == 1:
                    if list(chance)[0] not in self.omega:			
                        raise ZufallError("keine gültige Chance")					
                elif len(chance) == 2:
                    if chance not in _a_cheval:			
                        raise ZufallError("keine gültige a_cheval-Chance")					
                elif len(chance) == 3:
                   if chance not in _transversale_plein:			
                        raise ZufallError("keine gültige transversale_plein-Chance")											
                elif len(chance) == 4:
                    if chance not in _carre:			
                        raise ZufallError("keine gültige carre-Chance")					
                elif len(chance) == 6:
                    if chance not in _transversale_simple:			
                        raise ZufallError("keine gültige transversale_simple-Chance")								
                elif len(chance) == 12:
                    if chance not in [self.colonne1, self.colonne2, self.colonne3,
                        self.douze_premier, self.douze_milieu, self.douze_dernier]:			
                        raise ZufallError("keine gültige Chance")					
                elif len(chance) == 18:
                    if chance not in [self.pair, self.impair, self.rouge, self.noir,
                        self.manque, self.passe]:			
                        raise ZufallError("keine gültige Chance")					
                else:
                    raise ZufallError("keine gültige Chance")
					
            m = 1			
            if len(args) == 2:
                m = args[1]			
                if not (isinstance(m, (int, Integer)) and m > 0):			
                    raise ZufallError("für m ganze Zahl > 0 angebem")					
		
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        def dm(x):
            return display(Math(x))
        			
        vv = GleichVerteilung(37)  
        if len(args) == 1 or len(args) == 2 and m == 1:		
            erg = vv.versuch - 1   # die Gleichverteilung ist auf {1,2,...,37} definiert	
            print(' ')			
            dm('\mathrm{Gesetzt\;\, :\;\; }' + latex(chance))		
            dm('\mathrm{Ergebnis:\;\; }' + str(erg))
            txt = '\mathrm{Spiel\;gewonnen}' if erg in chance else '\mathrm{Spiel\;verloren}'			
            dm(txt)		
            print(' ')
            return			
        else:
            gewinn = dict([(1, 35), (2, 17), (3, 11), (4, 8), (6, 5), (12, 2), (18, 1)])		
            sp = vv.stich_probe(m)
            sp = [x-1 for x in sp]			
            dr = [ (gewinn[len(chance)] if x in  chance else -1) for x in sp]

            if kwargs.get('g') or kwargs.get('gd'):
                print(' ')			
                dm('\\qquad\mathrm{Verlauf\;des\;Gewinns,\;aktueller\;Gewinn}')			
                verlauf_grafik(dr, art='summe', xlabel='Anzahl Spiele')
            elif kwargs.get('m') or kwargs.get('md'):	
                pass
                print(' ')			
                dm('\\qquad\mathrm{Verlauf\;des\; mittleren\;Spielgewinnes}') 
                dm('\\qquad\mathrm{grün-theoretischer\; Erwartungswert\;bei\;einem\;Spiel\; (-1/37)}')			
                verlauf_grafik(dr, art='mittel', vergl=float(-1/37), xlabel='Anzahl Spiele')
			
            if not kwargs:			
                L = len(dr)			
                G = dr.count(1)	
                V = L - G
                p = float((G-V)/L * 100)
                print(' ')			
                dm('\mathrm{Gesetzt\;\,\; :  \;\; }' + latex(chance))		
                dm('\mathrm{Gewonnen\;(1):  \;\; }' + str(G))
                dm('\mathrm{Verloren\;(-1):\;\; }' + str(V))
                dm('\mathrm{Gesamt\;\\quad\\quad\,:\; }' + str(G-V) + '=' + '{0:.2f}'.format(p) + '\%')
            if kwargs.get('d') or kwargs.get('gd') or kwargs.get('md'):			
                dm('\mathrm{Rückgabe\; einer\; DatenReihe\; mit \;dem\;Gewinn\,/\,Verlust\;je\;Spiel}')
                print(' ')			
                return DatenReihe(dr)				
            print(' ')			
            
			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        roulette_hilfe(3)	
		
    h = hilfe					
			
		
		
# Benutzerhilfe für Roulette
# --------------------------

def roulette_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        print("h=4 - Ereignisse")
        return
		   
    if h == 2:
        print(""" \
		
Roulette - Objekt
	
Erzeugung    Roulette( )
				 
Zuweisung    r = Roulette()   (r - freier Bezeichner)
	   """)
        return 
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für Roulette
 	
r.hilfe          Bezeichner der Eigenschaften und Methoden
r.brett          Spielbrett (Abbildung)
r.formeln        Berechnungsformeln
r.omega          Ergebnismenge
r.P(...)      M  Wahrscheinlichkeiten beim einmaligen Spielen
r.regeln         Spielregeln
r.spiel(...)  M  Spiel
r.tisch          = s.brett

Synonymer Bezeichner

hilfe   h
""")
        return 
		
    if h == 4:   
        print(""" \
		
Ereignisse (Setzmöglichkeiten, Chancen) beim einmaligen Roulette-
Spiel

(Unbenannte) Ereignisse, die über die Menge der Zahlen angegeben 
werden:
                                                                   Anzahl   Gewinn-
Name                Beschreibung                                   Zahlen    quote                                   
                                                                   
plein               einzelne Zahl               z.B. 3 bzw. {3}         1   35 : 1
a_cheval            zwei angrenzende Zahlen     z.B. {13,16}            2   17 : 1
transversale_plein  Querreihe von drei Zahlen   z.B. {28,29,30}         3   11 : 1
carre               vier Zahlen, deren Felder   z.B. {14,15,17,18}      4    8 : 1
                    in einem Punkt zusammensto-  
                    ßen bzw. die ersten vier 
                    Zahlen 			
transversale_simple zwei benachbarte Querreihen z.B. {7,8 9,10,11,12}   6    5 : 1

Kolonne und Dutzend:
r.colonne1          die linke Reihe             {1,4,7,..,34}          12    2 : 1
r.colonne2          die mittlere Reihe          {2,5,8,..,35} 			 
r.colonne3          die rechte Reihe            {3,6,9,..,36}			
r.douze_premier     das erste Dutzend           {1,2,..,12}			 
r.douze_milieu      das mittlere Dutzend        {13,14,..,24}			
r.douze_dernier     das letzte Dutzend          {25,26,..,36}
			 
Einfache Chancen:
r.pair              die geraden Zahlen außer 0  {2,4,6,..,36}          18    1 : 1
r.impair            die ungeraden Zahlen        {1,3,5,..,35}			
r.rouge             die roten Zahlen            {1,3,7,..36}			
r.noir              die schwarzen Zahlen        {2,4,6,..35}			
r.manque            die erste Hälfte            {1,2,..,18}			
r.passe             die zweite Hälfte           {19,20,..,36}			
	""")
        return 

		
		
# 'Unbenannte' Chancen außer plein		
# --------------------------------		
_a_cheval = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {2, 3}, {1, 4}, {2, 5}, {4, 5}, {3, 6}, \
                  {5, 6}, {4, 7}, {5, 8}, {6, 9}, {7, 8}, {8, 9}, {7, 10}, {8, 11}, {10, 11}, \
                  {9, 12}, {11, 12}, {10, 13}, {11, 14}, {12, 15}, {13, 14}, {13, 16}, \
                  {14, 15}, {14, 17}, {15, 18}, {16, 17}, {17, 18}, {16, 19}, {17, 20}, \
                  {19, 20}, {18, 21}, {19, 22}, {20, 21}, {20, 23}, {22, 23}, {21, 24}, \
                  {22, 25}, {23, 24}, {23, 26}, {25, 26}, {24, 27}, {25, 28}, {26, 27}, \
                  {26, 29}, {28, 29}, {27, 30}, {28, 31}, {29, 30}, {29, 32}, {30, 33}, \
                  {31, 32}, {32, 33}, {31, 34}, {32, 35}, {33, 36}, {34, 35}, {35, 36}]		
_transversale_plein = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}, {13, 14, 15}, \
                  {16, 17, 18}, {19, 20, 21}, {22, 23, 24}, {25, 26, 27}, {28, 29, 30}, \
                  {31, 32, 33}, {34, 35, 36}]	
_carre = [{1, 2, 3, 4}, {1, 2, 4, 5}, {2, 3, 5, 6}, {4, 5, 7, 8}, {5, 6, 8, 9}, \
                  {7, 8, 10, 11}, {8, 9, 11, 12}, {10, 11, 13, 14}, {11, 12, 14, 15}, \
                  {13, 14, 16, 17}, {14, 15, 17, 18}, {16, 17, 19, 20}, {17, 18, 20, 21}, 
                  {19, 20, 22, 23}, {20, 21, 23, 24}, {22, 23, 25, 26}, {23, 24, 26, 27}, \
                  {25, 26, 28, 29}, {26, 27, 29, 30}, {28, 29, 31, 32}, {29, 30, 32, 33}, \
                  {31, 32, 34, 35}, {32, 33, 35, 36}]				  
_transversale_simple = [{1, 2, 3, 4, 5, 6}, {4, 5, 6, 7, 8, 9}, {7, 8, 9, 10, 11, 12}, \
                  {10, 11, 12, 13, 14, 15}, {13, 14, 15, 16, 17, 18}, {16, 17, 18, 19, 20, 21}, \
                  {19, 20, 21, 22, 23, 24}, {22, 23, 24, 25, 26, 27}, {25, 26, 27, 28, 29, 30}, \
                  {28, 29, 30, 31, 32, 33}, {31, 32, 33, 34, 35, 36}]				  
		
	
