#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  ZufallsGroesse - Klasse  von zufall           
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

from scipy.stats import rv_discrete

from sympy.core.numbers import (Integer, Rational, Float, Zero, One, 
    NegativeOne, Half, Pi, E)
from sympy import Add, Mul, Pow, Mod
from sympy.core.symbol import Symbol
from sympy.core.relational import (GreaterThan, StrictGreaterThan, LessThan, 
    StrictLessThan)
from sympy import sympify, sqrt, nsimplify
from sympy import floor
from sympy.printing.latex import latex
from sympy.core.compatibility import iterable

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.datenreihe import DatenReihe 
from zufall.lib.funktionen.graf_funktionen import (balken1, polygon_zug, 
    vert_funktion, verlauf, balken_plus_balken, poly_plus_poly, balken_plus_stetig)

from zufall.lib.objekte.ausnahmen import ZufallError

import zufall
	
	

# ZufallsGroesse - Klasse  
# ------------------------
	
class ZufallsGroesse(ZufallsObjekt):                                      
    """

Zufallsgröße

**Kurzname** **ZG**
	
**Erzeugung** 
	
   ZG( *verteilung* )

**Parameter**
 
   *verteilung* : *Liste/Tupel* | *dictionary* 
				 
      Elemente der Liste sind 2-elementige Listen/Tupel, 
      die die Zuordnung Wert - Wahrscheinlichkeit bzw.  
      Häufigkeit/Zahl > 0  beinhalten;
      In einem dictionary erfolgt die Zuordnung als
      zahl : zugeordnete_zahl
	  
      Ist die Summe der zugeordneten Zahlen ungleich 1, wird  
      eine Wahrscheinlichkeitsverteilung durch Normieren 
      erzeugt
	  
    """
		
		
    def __new__(cls, *args, **kwargs):  
        			
        if kwargs.get("h") in (1, 2, 3):                         
            zufalls_groesse_hilfe(kwargs["h"])		
            return	
				
        zahlen = (Integer, int, Float, float, Rational, One, Zero, NegativeOne, Half, 
			       Mul, Add, Pow, Mod)

        kontrolle = True				   
        if kwargs.get('kontrolle') == False:
            kontrolle = kwargs.get('kontrolle')
		
        try:						
            if len(args) != 1:
                raise ZufallError("ein Argument angeben")
            arg = args[0]
            if not isinstance(arg, (list, dict)):
                raise ZufallError("eine Liste oder ein dictionary angeben")
            if isinstance(arg, list):			
                if not all(map(lambda x: isinstance(x, (list, tuple)) and len(x) == 2, arg)):				
                    raise ZufallError("die Listenelemente müssen 2-elementige Listen/Tupel sein")
                if not all(map(lambda x: isinstance(x[0], (int, Integer)) and type(x[1]) in zahlen, arg)):				
                    raise ZufallError("die Elemente der inneren Listen müssen Zahlen sein")
                vert = dict(arg)
            else:
                if not all(map(lambda x: isinstance(x, (int, Integer)), arg.keys())):				
                    raise ZufallError("die Schlüsselwerte des dictionary müssen ganze Zahlen sein")
                if not all(map(lambda x: type(x) in zahlen, arg.values())):				
                    raise ZufallError("die Werte des dictionary müssen Zahlen sein")
                vert = arg	
            if kontrolle:		          			
                vv = []
                for k in vert:
                    if isinstance(vert[k], Rational):
                        vv += [[k, vert[k]]]
                    else:
                        try:					
                            vv += [[k, nsimplify(vert[k])]]		
                        except RecursionError:
                            vv += [[k, vert[k]]]						
                vert = dict(vv)
                s = (sum([vert[k] for k in vert]))
                if s != 1:
                    for k in vert:
                        vert[k] = vert[k] / s			
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        if kwargs.get('parameter'):
            parameter = kwargs.get('parameter')
        else:
            parameter = None		
        return ZufallsObjekt.__new__(cls, vert, parameter)

			
    def __str__(self):  
        return "ZufallsGroesse"	

		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def omega(self):
        """Ergebismenge"""	
        di = self._vert	
        return set([k for k in di if di[k]])
		
    @property
    def n_omega(self):
        """Größe der Ergebnismenge"""	
        return len(self.omega)

    nOmega = n_omega
		
    @property
    def erw(self):
        """Erwartungswert"""	
        ve = self._vert
        return sum([k*ve[k] for k in ve])		
    def erw_(self, *args, **kwargs):
        """Erwartungswert; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n   Darstellung dezimal mit n Kommastellen\n")
            return			
        d = kwargs.get('d')
        e = self.erw		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(e), ".%df" % d))			
        return float(e)       
		
    Erw = erw_
	
    @property
    def var(self):
        """Varianz"""	
        ve, e = self._vert, self.erw	
        return sum([(k - e)**2*ve[k] for k in ve])		
    def var_(self, *args, **kwargs):
        """Varianz; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Kommastellen")
            print("         b=ja   Begriffe\n")
            return
        if kwargs.get('b'):
            print("\nEs sind auch die Begriffe  Varianzwert, mittleres Abweichungsquadrat,")
            print("Streuungsquadrat oder Dispersion gebräuchlich\n")
            return			
        d = kwargs.get('d')
        v = self.var		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(v), ".%df" % d))			
        return float(v)       

    Var = var_		
		
    @property
    def sigma(self):
        """Standardabweichung"""	
        return sqrt(self.var)
    def sigma_(self, *args, **kwargs):
        """Standardabweichung; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Kommastellen\n")
            return
        d = kwargs.get('d')
        s = self.sigma		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(s), ".%df" % d))			
        return float(s)       

    Sigma = sigma_		
		   
    @property
    def _vert(self): 
        """Wahrscheinlichkeitsverteilung als internes dict"""	
        return self.args[0]			
            	
    @property				
    def vert(self):
        """Wahrscheinlichkeitsverteilung"""	
        return self._vert			
    def vert_(self, s=None, p=None, sp=None, **kwargs):		
        """Wahrscheinlichkeitsverteilung; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz")
            print("p=ja  - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben")
            print("d=n   - ebenso, dezimal mit n Kommastellen")
            print("s=ja  - Spaltenausgabe")
            print("sp=ja - ebenso, Prozentwerte")
            print("sd=n  - ebenso, dezimal mit n Kommastellen\n")
            return			
        di = self._vert
        di1 = dict()
        d = kwargs.get('d')			
        sd = kwargs.get('sd')			
        if p or d or sp or sd:
            if sd:
                d = sd
            if d and	not (isinstance(d, (int, Integer)) and (1 < d <= 12)):
                print("zufall: für d einen Wert aus [2, 12] angeben")
                return				
            for k in di.keys():
                if p or sp:
                    di1[k] = eval(format(float(100*di[k]), ".2f"))	
                elif d or sd:
                    di1[k] = eval(format(float(di[k]), ".%df" % d))
        if s or sp or sd:
            if sp or sd:
                di = di1			
            kk = list(di.keys()) 
            try:
                kk.sort()	
            except TypeError:
                pass			
            for k in kk:		
                display(Math(latex(k) + '\\quad ' + latex(di[k])))	
            print(' ')			
            return			
        elif d or p:
            return di1
        return di			
		
    Vert = vert_
	
    @property		
    def _vert_kum(self):
        """Kumulierte Wahrscheinlichkeitsverteilung; internes dict"""	
        di = self._vert
        ll, sum = [], 0	
        kk = list(di.keys())
        kk.sort()		
        for k in kk:
            sum += di[k]		
            ll += [(k, sum)]
        return dict(ll)			
		
    @property				
    def vert_kum(self):
        """Kumulierte Wahrscheinlichkeitsverteilung"""	
        return self._vert_kum
    def vert_kum_(self, s=None, p=None, sp=None, **kwargs):		
        """Kumulierte Wahrscheinlichkeitsverteilung; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz")
            print("p=ja  - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben")
            print("d=n   - ebenso, dezimal mit n Kommastellen")
            print("s=ja  - Spaltenausgabe")
            print("sp=ja - ebenso, Prozentwerte")
            print("sd=n  - ebenso, dezimal mit n Kommastellen\n")
            return			
        di = self._vert_kum
        di1 = dict()
        d = kwargs.get('d')			
        sd = kwargs.get('sd')			
        if p or d or sp or sd:
            if sd:
                d = sd
            if d and	not (isinstance(d, (int, Integer)) and (1 < d <= 12)):
                print("zufall: für d einen Wert aus [2, 12] angeben")
                return				
            for k in di.keys():
                if p or sp:
                    di1[k] = eval(format(float(100*di[k]), ".2f"))	
                elif d or sd:
                    di1[k] = eval(format(float(di[k]), ".%df" % d))     
        if s or sp or sd:
            if sp or sd:
                di = di1	
            kk = list(di.keys()) 
            kk.sort()			
            for k in kk:		
                display(Math(latex(k) + '\\quad ' + latex(di[k])))	
            print(' ')			
            return			
        elif d or p:
            return di1
        return di			
	
    vertKum = vert_kum
    VertKum = vert_kum_
		
    @property	
    def hist(self):
        """Histogramm"""
        daten = self._vert
        balken1(daten, typ='W', titel='$\mathrm{Wahrscheinlichkeitsverteilung - Histogramm}$' + '\n')
    def hist_(self, *args, **kwargs):
        """Histogramm; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   p=ja   Polygonzug-Diagramm")
            print("Angabe einer Zufallsgröße | Datenreihe - Vergleich mit anderer Verteilung\n")
            return			
        if kwargs.get('p'):
            self.poly_zug
            return			
        daten = self._vert
        if not args:
            balken1(daten, typ='W', titel='$\mathrm{Wahrscheinlichkeitsverteilung - Histogramm}$' + '\n ')
            return
        if len(args) != 1:
            print("zufall: nur ein Argument angeben")
            return
        arg = args[0]			
        nv = importlib.import_module('zufall.lib.objekte.normal_verteilung')
        ev = importlib.import_module('zufall.lib.objekte.exponential_verteilung')
        NormalVerteilung = nv.NormalVerteilung
        ExponentialVerteilung = ev.ExponentialVerteilung         		
        if not isinstance(arg, (ZufallsGroesse, DatenReihe, NormalVerteilung, ExponentialVerteilung)):			
            print("zufall: Zufallsgröße oder Datenreihe angeben")
            return
        if isinstance(arg, (NormalVerteilung, ExponentialVerteilung)):	
            balken_plus_stetig(daten, arg, typ='W', 
                titel='$\mathrm{Wahrscheinlichkeitsverteilung - Histogramm}$' + '\n') 	
            return			
        if isinstance(arg, DatenReihe) and not arg.is_ganz:	
            print("zufall: Klasseneinteilung vornehmen")
            return			
        daten2 = arg._vert			
        if isinstance(arg, ZufallsGroesse):			
            typ2 = 'W'
            titel = '$\mathrm{Vergleich\; von\; Wahrscheinlickeitsverteilungen}$' + '\n' \
                   + '$\mathrm{hell - Ausgangs-, dunkel - Vergleichsverteilung}$' + '\n'			
        else:
            typ2 = 'R'		
            titel = '$\mathrm{Vergleich\; Wahrsch.-\; und\; Häufigk.-Verteilung}$' + '\n' + \
                   '$\mathrm{gelb \;- Wahrsch.,\; grün\; -\; relative\; Häufigkeiten}$\n'			
        balken_plus_balken	(daten, daten2, typ1='W', typ2=typ2, titel=titel, ) 	
		
    Hist = hist_
		
    @property	
    def hist_kum(self):
        """Histogramm der kumulierten Wahrscheinlichkeiten"""
        daten = self._vert_kum
        balken1(daten, typ='W', titel='$\mathrm{Kumulierte\; Wahrscheinlichkeiten - Histogramm}$' + '\n', 
              ylabel='$P\,(X \,\\leq \, k)$')

    histKum = hist_kum	
	
    @property	
    def poly_zug(self):
        """Polygonzug"""
        daten = self._vert
        polygon_zug(daten, typ='W', titel='$\mathrm{Wahrscheinlichkeitsverteilung - Polygonzug}$' + '\n')
    def poly_zug_(self, *args, **kwargs):
        """Polygonzug; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   hi=ja   Histogramm")
            print("Angabe einer Zufallsgröße | Datenreihe - Vergleich mit anderer Verteilung\n")
            return			
        if kwargs.get('hi'):
            self.hist
            return			
        daten = self._vert
        if not args:
            self.poly_zug
            return
        if len(args) != 1:
            print("zufall: nur ein Argument angeben")
            return
        arg = args[0]			
        if not isinstance(arg, (ZufallsGroesse, DatenReihe)):			
            print("zufall: Zufallsgröße oder Datenreihe angeben")
            return
        daten2 = arg._vert			
        if isinstance(arg, ZufallsGroesse):			
            typ2 = 'W'
            titel = '$\mathrm{Vergleich\; von\; Wahrscheinlickeitsverteilungen}$' + '\n' + \
                   '$\mathrm{hell - Ausgangs-, dunkel - Vergleichsverteilung}$\n'			
        else:
            typ2 = 'R'		
            titel = '$\mathrm{Vergleich\; Wahrsch.-\, und\; Häufigk.-Verteilung}$\n' + \
                   '$\mathrm{gelb - Wahrsch., grün - rel. Häufigkeiten}$\n'			
        poly_plus_poly	(daten, daten2, typ1='W', typ2=typ2, titel=titel, ) 	

    polyZug = poly_zug
    PolyZug = poly_zug_

    @property	
    def graf_F(self):
        """Graf der Verteilungsfunktion"""
        vert_funktion(self, typ='W', titel='$\mathrm{Verteilungsfunktion}$\n ')
	
    grafF = graf_F
	
    def F(self, *args, **kwargs):
        """Verteilungsfunktion"""
        if kwargs.get('h'):
            print("\nVerteilungsfunktion\n")		
            print("Aufruf   zg . F( wert )\n")		                     
            print("              zg    Zufallsgröße")
            print("              wert  Zahl\n")
            print("Zusatz   d=n    Darstellung dezimal mit n Kommastellen\n")			
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        wert = sympify(args[0])
        if not isinstance(wert, (int, Integer, Rational, float, Float)):			
            print('zufall: einen Zahlenwert angeben')
            return
        vert_kum = self._vert_kum
        if wert < min(self._vert.keys()):
            erg = 0
        elif wert >= max(self._vert.keys()):
            erg = 1
        else:			
            try:
                erg = vert_kum[floor(wert)]	
            except KeyError:
                i = 0                				
                while True:
                    w = list(vert_kum.keys())[i]
                    if w > wert:
                        erg = vert_kum[list(vert_kum.keys())[i-1]]	
                        break						
                    i += 1				
        d = kwargs.get('d')
        erg = nsimplify(erg)		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(erg), ".%df" % d))			
        return erg      
	
    @property	
    def versuch(self):
        """Versuch"""
        xk = [float(x) for x in list(self._vert.keys())] 
        pk = [float(x) for x in list(self._vert.values())]
        X = rv_discrete(name='X', values=(xk, pk))		
        return X.rvs()

    wurf = versuch
	
    def stich_probe(self, *args, **kwargs):
        """Stichprobe"""
        if kwargs.get('h'):
            print("\nStichprobe\n")		
            print("Aufruf   zg . stich_probe( m )\n")		                     
            print("             zg   Zufallsgröße")
            print("             m    Umfang (Anzahl Versuche)\n")
            print("Zusatz   d=ja   Rückgabe als DatenReihe\n")
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        m = sympify(args[0])
        if not isinstance(m, (int, Integer)) and m > 0:			
            print('zufall: ganze Zahl > 0 angeben')
            return
        xk = [float(x) for x in list(self._vert.keys())]
        pk = [float(x) for x in list(self._vert.values())]
        X = rv_discrete(name='X', values=(xk, pk))		
        ll = X.rvs(size=m)
        def f(x):
            if x - int(x) == 0.0:
                return int(x)
            return x
        ll = [f(x) for x in ll]		
        if kwargs.get('d'):		
            print('Rückgabe einer DatenReihe')				
            return DatenReihe(ll)		
        return ll
		
    stichProbe = stich_probe
	
	
    def P(self, *args, **kwargs):
        """Wahrscheinlichkeit eines Ereignisses"""
		
        if kwargs.get('h'):
            print("\nWahrscheinlichkeit eines Ereignisses\n")
            print("Aufruf   zg . P( e )\n")		                     
            print("              zg     Zufallsgröße")
            print("              e      Ereignis:")   
            print("                     elem | Liste/Tupel/Menge von Elementen von") 
            print("                            zg.omega |")
            print("                     X = elem |")
            print("                     elem rel X | X rel elem |")
            print("                     abs( X - elem ) rel zahl |")
            print("                     'elem rel X rel elem'  (als Zeichenkette)")		
            print("                     (der Bezeichner X ist zwingend)")
            print("              elem   Element von zg.omega")
            print("              rel    Relation:  < | <= | > | >=")
            print("              zahl   reelle Zahl\n")
            print("  oder   zg . P( e, e1)")		                     
            print("              e1     Ereignis   Element | Liste/Tupel/Menge von")
            print("                     Elementen von zg.omega\n")
            print("Bei der Angabe von zwei Ereignissen wird die bedingte Wahrscheinlichkeit")
            print("P( e | e1 ) berechnet\n")						
            print("Zusatz   p=ja   Darstellung als Prozentwert")			
            print("         d=n    Darstellung dezimal mit n Kommastellen")			
            print("         g=ja   grafische Darstellung\n")			
            print("Beispiele ")
            print("zg.P( 3 )         zg.P( { 3, 4, 7, 8 } )     zg.P( X = 3 )")
            print("zg.P( X < 8 )     zg.P( X >= 3 )             zg.P( abs(X-3) > 2.5 )")
            print("zg.P( '3 <= X < 7' )    ( Z e i c h e n k e t t e )")	
            print("zg.P( {2, 5, 7}, {2, 8} )   oder")	
            print("zg.P( [2, 5, 7], [2, 8] )   bedingte Wahrscheinlichkeit\n")	
            return			
			
        if len(args) not in (1, 2) and not kwargs.get('X'):
            print('zufall: ein oder zwei Ereignisse angeben')
            return			
        omega = list(self.omega)
        _x = kwargs.get('X')
        pp = None
        if _x is not None:
            if _x not in omega:
                print('zufall: Element aus der Ergebnismenge angeben')
                return
            erg = [_x]
        elif isinstance(args[0], (int, Integer)):
            el = args[0]
            if not el in omega:
                print('zufall: Element aus der Ergebnismenge angeben')
                return 
            erg = [el]
        else:
            arg = args[0]
            if isinstance(arg, (set, list, tuple)):
                erg = list(arg)
                test = map(lambda x: x in omega, erg)
                if not all(test):				
                    print('zufall: Elemente aus der Ergebnismenge angeben')
                    return
            else:
                X = Symbol('X')
                if str(arg).find('abs') >= 0 or str(arg).find('Abs') >= 0:
                    try:				
                        erg = [i for i in omega if arg.subs(X, i)]
                    except Exception:
                        print('zufall: Anweisung überprüfen')
                        return											
                elif isinstance(arg, (GreaterThan, StrictGreaterThan, LessThan,
                     StrictLessThan)):
                    k = arg.args[1]
                    if not isinstance(k, (int, Integer)):
                        print('zufall: ganze Zahl angeben')
                        return						
                    if isinstance(arg, StrictGreaterThan):
                        if k > self.n_omega:
                            pp = 0
                        elif k < 0:
                            pp = 1
                        pp = 1 - self._vert_kum[k]	
                        erg = [i for i in omega if i > k]						
                    elif isinstance(arg, GreaterThan):
                        pp = self.P(X > k) + self.P(k)										
                        erg = [i for i in omega if i >= k]						
                    elif isinstance(arg, StrictLessThan):
                        if k > self.n_omega:
                            pp = 1
                        elif k < 1:
                            pp = 0
                        pp = self._vert_kum[k-1]															
                        erg = [i for i in omega if i < k]						
                    elif isinstance(arg, LessThan):
                        pp = self.P(X < k) + self.P(k)										
                        erg = [i for i in omega if i <= k]						
                else:    # " 2 < X <= 6 "
                    try:				
                        erg = [i for i in omega if eval(arg.replace('X', str(i)))]
                    except Exception:
                        print('zufall: Anweisung überprüfen')
                        return	
        if pp is None:
            pp = 0
            for k in erg:
                pp += self._vert[k] 
							
        if len(args) == 2: 
            if isinstance(args[0], str) and isinstance(eval(args[0]), (int, Integer)):
                e = eval(args[0])
                if not e in omega:
                    print('zufaall: Element aus der  Ergebnismenge angeben')	
                    return
                erg = [e]			
            eig1 = args[1]
            if not iterable(eig1):
                eig1 = [eig1]	
            pp1 = self.P(eig1)
            if pp1 is None:			 
                return				
            erg, eig1 = set(erg), set(eig1)
            eig2 = erg.intersection(eig1)	
            pp2 = self.P(eig2)
            if pp1 == 0:
                print('zufall: Division durch 0 ist nicht erlaubt')
                return				
            pp = nsimplify(pp2 / pp1, rational=True)			
		
        if kwargs.get('p'):
            return eval(format(float(100*pp), ".2f"))			
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(pp), ".%df" % d))			
        if kwargs.get('g'):		
            balken1(self._vert, typ='W', titel='$\mathrm{Wahrscheinlichkeit = \
			                       Inhalt\; der\; dunklen\; Fläche}$\n', mark=erg)	
            return			
        return pp	
		
		
    def relh2p(self, *args, **kwargs):
        """Stabilisierung der relativen Häufigkeiten"""
		
        if kwargs.get('h'):
            print("\nStabilisierung der relativen Häufigkeiten\n")
            print("Aufruf   zg . relh2p( e, m )\n")		                     
            print("              zg     Zufallsgröße")
            print("              e      Ereignis   Element | Liste|Tupel|Menge von Elementen")
            print("                                der Ergebnismenge")
            print("              m      Anzahl Versuche\n")
            print("Zusatz   d=ja   Rückgabe einer Datenreihe mit den Versuchsausgängen")
            print("                1-Ereignis ist eingetreten / 0-Ereignis ist nicht")
            print("                eingetreten\n") 
            print("relh2p = 'rel'ative 'H'äufigkeit 'to' 'P' (Wahrscheinlichkeit)\n")
            return	
			
        om = self.omega
        if len(args) != 2:
            print('zufall: zwei Argumente angeben')
            return
        e, m = args
        if isinstance(e, (list, tuple, set)):	
            if not all(map(lambda x: x in om, e)):
                print('zufall: kein Ereignis aus Elementen der Ergebnismenge')
                return
        else:	
            if not e in om:
                print('zufall: kein Element der Ergebnismenge')
                return
        if not isinstance(m, (int, Integer)) and m > 0:
            print('zufall: für Anzahl Versuche ganze Zahl > 0 angeben')
            return
        p = float(self.P(e))
        X = rv_discrete(name='X', values=([1, 0], [p, 1-p]))		
        daten = X.rvs(size=m)
        if m < 5:
            print('zufall: die Anzahl der Versuche muss > 4 sein')	
            return				
        print(' ')
        print("Stabilisierung der relativen Häufigkeiten eines Ereignisses\n")		
        print("Es werden die relativen Häufigkeiten eines Ereignisses bei wachsender Ver-")
        print("suchsanzahl dargestellt\n")
        print("grüne Linie: theoretische Wahrscheinlichkeit des Ereignisses")
        print(' ')		
        verlauf(daten, vergl=p, art='mittel', xlabel='$Anzahl\; Versuche$')
        if kwargs.get('d'):
            def f(x):
                if int(x) - x == 0.0:
                    return int(x)
                return x
            daten = [f(x) for x in daten]				
            print("Rückgabe DatenReihe\n")			
            return DatenReihe(daten)			
		
				
    def quantil(self, *args, **kwargs):
        """"""
        if kwargs.get('h'):
            print("\nQuantile\n")		
            print("Aufruf   zg . quantil( q )\n")		                     
            print("             zg    Zufallsgröße")
            print("             q     Zahl aus [0,1]\n")
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        pp = args[0]
        if not isinstance(pp, (int, Integer, float, Float, Rational)):			
            print('zufall: Zahl aus [0,1] angeben')
            return			
        if not (0 <= pp <= 1):			
            print('zufall: Zahl aus [0,1] angeben')
            return
        pp = float(pp)	
        kve = self._vert_kum
        qq = 0
        k = 0
        if pp == 0.0:
            return 0
        if pp == 1.0:
            return len(kve)-1
        while qq < pp:
            try:		
                qq = kve[k]
            except KeyError:
                pass			
            k += 1		
        return k-1		
		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        zufalls_groesse_hilfe(3)	
		
    h = hilfe					
			

			
# Benutzerhilfe für ZufallsGroesse
# --------------------------------

def zufalls_groesse_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
ZufallsGröße - Objekt

Kurzname     ZG
		
Erzeugung    ZufallsGröße( verteilung )

                 verteilung    Liste / dictionary 
				 
                    Elemente der Liste sind 2-elementige Listen/Tupel, 
                    die die Zuordnung Zahl - Wahrscheinlichkeit /  
                    Häufigkeit / Zahl > 0  beinhalten
                    In einem dictionary erfolgt die Zuordnung direkt als
                    zahl : zugeordnete_zahl                    					
                    Ist die Summe der zugeordneten Zahlen ungleich 1, wird  
                    eine Wahrscheinlichkeitsverteilung durch Normieren 
                    erzeugt
				 
Zuweisung     zg = ZG(...)   (zg - freier Bezeichner)

Beispiele
ZG( [ [1, 1/2], [2, 1/6], [3, 1/3] ] )
ZG( [ [1, 6], [2, 2], [3, 4] ] )
ZG( { 1 : 6, 2 : 2,  3 : 4 } )
(die erzeugten Zufallsgrößen sind identisch)
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für ZufallsGröße
 
zg.hilfe               Bezeichner der Eigenschaften und Methoden
zg.erw                 Erwartungswert	
zg.erw_(...)           ebenso, zugehörige Methode	
zg.F(...)           M  Verteilungsfunktion
zg.graf_F              Graf der Verteilungsfunktion
zg.hist                Histogramm
zg.hist_(...)       M  ebenso, zugehörige Methode
zg.hist_kum            Histogramm, kumulierte Wahrscheinlichkeiten
zg.n_omega             Größe der Ergebnismenge 
zg.omega               Ergebnismenge 
zg.P(...)           M  Wahrscheinlichkeit eines Ereignisses
zg.poly_zug            Polygonzug-Diagramm der Wahrscheinlichkeiten
zg.poly_zug_(...)   M  ebenso, zugehörige Methode
zg.quantil(...)     M  Quantile
zg.relh2p           M  Stabilisierung der relativen Häufigkeiten        
zg.sigma               Standardabweichung
zg.sigma_(...)      M  ebenso, zugehörige Methode	
zg.stich_probe(...) M  Stichprobe		
zg.var                 Varianz		
zg.var_(...)        M  ebenso, zugehörige Methode		
zg.versuch             Versuch		
zg.vert                Wahrscheinlichkeitsverteilung		
zg.vert_(...)       M  ebenso, zugehörige Methode		
zg.vert_kum            kumulierte Wahrscheinlichkeitsverteilung
zg.vert_kum_(...)   M  ebenso, zugehörige Methode		

Synonyme Bezeichner

hilfe        h
erw_         Erw	
graf_F       grafF
hist_        Hist
hist_kum     histKum
n_omega      nOmega
poly_zug     polyZug
poly_zug_    PolyZug
sigma_       Sigma
stich_probe  stichProbe
var_         Var
vert_        Vert
vert_kum     vertKum
vert_kum_    VertKum
""")		
        return
	
	
ZG = ZufallsGroesse
		


		