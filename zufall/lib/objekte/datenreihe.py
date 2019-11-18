#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  DatenReihe - Klasse  von zufall           
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

import numpy as np
from numpy import floor

from IPython.display import display, Math

from sympy.core.numbers import Integer, Rational, Float   
from sympy.core.symbol import Symbol
from sympy import sympify, sqrt, nsimplify, N
from sympy.printing.latex import latex
from sympy.core.compatibility import iterable 

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.funktionen.funktionen import is_zahl 
from zufall.lib.funktionen.graf_funktionen import (balken1, balken2, 
     polygon_zug, vert_funktion, balken_plus_balken, poly_plus_poly,
     balken_plus_stetig)

from zufall.lib.objekte.ausnahmen import ZufallError
import zufall	
	
	

# DatenReihe - Klasse  
# -------------------
	
class DatenReihe(ZufallsObjekt):                                      
    """

Datenreihe

**Kurzname** **DR**
	
**Erzeugung** 
	
   DR( *daten* )

**Parameter**
 
   *daten* : Daten
   
      | *zahl /[, zahl1, ... ]*  | 
      | *{ zahl : wiederh /[, zahl1 : wiederh1, ... ] }*
			 
   *zahl* : reelle Zahl	

   *wiederh* : Anzahl der Wiederholungen   
   
Es werden vorwiegend DatenReihen mit ganzzahligen Elementen betrachtet				
 
    """   
   
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            datenreihe_hilfe(kwargs["h"])		
            return	
						
        try:
            if len(args) == 1:
                if type(*args) == dict:
                    pass				
                elif isinstance(args, (list, tuple)):                			
                    args = args[0]
            daten = []				
            for arg in args:
                if isinstance(arg, (list, tuple)): 
                    if all(map(lambda x: is_zahl(x))):	
                        daten += [el for el in arg]	
                    else:
                        raise ZufallError("es sind nur Zahlen erlaubt")						
                if isinstance(arg, dict): 
                    for a in arg.keys():
                        if not is_zahl(a):
                            raise ZufallError("Schlüssel in dem dictionary muß eine Zahl sein")						
                        if not (isinstance(arg[a], (int, Integer)) and arg[a] >= 0):
                            raise ZufallError("Anzahl der Wiederholungen muss ganz und nicht negativ sein")
                        daten += [a for i in range(arg[a])]						                    				
                else:
                    if is_zahl(arg):
                        daten += [arg]
                    else:						
                        raise ZufallError("es sind nur Zahlen erlaubt")						
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsObjekt.__new__(cls, list(daten))

			
    def __str__(self):  
        return "DatenReihe"
		
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def daten(self):
        """Datenliste"""	
        return self.args[0]	

    @property
    def is_ganz(self):
        """Test auf ganzzahlige Daten"""
        return all(map(lambda x: isinstance(x, (int, Integer)), self.daten))		
		
    isGanz = is_ganz
	
    @property
    def diagr(self):
        """Daten-Balkendiagramm"""	
        dat = self.daten		
        daten = dict( [[i,dat[i]] for i in range(len(dat))])	
        balken2(daten, typ='D', titel='$Daten-Balken-Diagramm$' + '\n ')

    @property		
    def _H(self):
        """Absolute Häufigkeiten als internes dict"""	
        di = dict()
        for d in self.daten:
            try:
                di[d] += 1
            except KeyError:
                di[d] = 1
        return di

    def H(self, *args, **kwargs):
        """Absolute Häufigkeiten"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\nAbsolute Häufigkeit eines Ereignisses in einer DatenReihe\n")
            print("Aufruf   dr . H(  )\n")		                     
            print("              dr          DatenReihe")
            print("              ereignis    elem | Liste/Tupel/Menge von elem's")
            print("              elem        Element von dr.daten\n")
            print("Zusatz   d=ja   Ausgabe aller Häufigkeiten als dictionary")
            print("         s=ja   ebenso, Spaltenausgabe\n")
            return			
        di = self._H
        if kwargs.get('s'):		
            for k in di:
                display(Math(latex(k) + '\\quad' + latex(di[k])))			
            print(' ')
            return
        if kwargs.get('d'):		
            return di
        if len (args) != 1:
             print('zufall: ein Argument angeben')
             return		
        if iterable(args[0]):
            e = list(args[0])
        else:			
            e = [args[0]]
        if not all([x in di.keys() for x in e]):
            print('zufall: Elemente der Datenreihe angeben') 		
            return			
        anzahl = 0
        for el in e:
            anzahl += di[el]		
        return anzahl

    @property		
    def umfang(self):
        """Umfang  / Anzahl Datenelemente"""
        return len(self.daten)
		
    n = umfang		
		
    @property		
    def _vert(self):
        """Relative Häufigkeiten als internes dict"""	
        di = self._H
        n = self.umfang
        di1 = dict()		
        for k in di.keys():
            di1[k] = Rational(di[k], n)
        return di1
		
		
    def hh(self, *args, **kwargs):
        """Relative Häufigkeiten"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\nRelative Häufigkeit eines Ereignisses in einer DatenReihe\n")
            print("Aufruf   dr . hh( ereignis )   (Bezeichner hh wegen h-hilfe)\n")		                     
            print("              dr          DatenReihe")
            print("              ereignis    elem | Liste/Tupel/Menge von elem's")
            print("              elem        Element von dr.daten\n")
            print("Zusatz   p=ja     Ausgabe als Prozentwert")
            print("         d=n      Ausgabe dezimal mit n Kommastellen")			
            print("         ah=ja    Ausgabe aller Häufigkeiten der Datenelemente")
            print("         ap=ja    ebenso, Prozentwerte")
            print("         ad=n     ebenso, Dezimalzahlen")    
            print("         ahd=ja   Rückgabe als dictionary")
            print("         adp=ja   ebenso, Prozentwerte")
            print("         add=n    ebenso, Dezimalzahlen\n	")
            return			
        di = self._vert
        if kwargs.get('ah'):		
            for k in di.keys():
                display(Math(latex(k) + '\\quad' + latex(di[k])))			
            print(' ')
            return
        if kwargs.get('ap'):		
            for k in di.keys():
                display(Math(latex(k) + '\\quad' + latex(format(float(100*di[k]), ".2f"))))			
            print(' ')
            return
        if kwargs.get('ad'):	
            d = kwargs.get('ad')		
            for k in di.keys():                       
                display(Math(latex(k) + '\\quad' + latex(eval(format(float(di[k]), ".%df" % d)))))			
            print(' ')
            return
        if kwargs.get('ahd'):		
            return di
        if kwargs.get('adp'):		
            return self.vert_(p=1)
        if kwargs.get('add'):		
            n = kwargs.get('add')		
            return self.vert_(d=n)
        if len (args) != 1:
             print('zufall: ein Argument angeben')
             return		
        if iterable(args[0]):
            e = list(args[0])
        else:			
            e = [args[0]]
        if not all(map(lambda x: x in di.keys(), e)):
            print('zufall: Elemente der DatenReihe angeben') 		
            return			
        pp = 0
        for el in e:
            pp += di[el]	
        if kwargs.get('p'):
            return eval(format(float(100*pp), ".2f"))	
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(pp), ".%df" % d))						
        return pp
	
    @property
    def vert(self): 
        """Verteilung der relativen Häufigkeiten"""	
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			        
        return self._vert

    vert_rel_h = vert
    vertRelH = vert
	
    def vert_(self, s=None, p=None, sp=None, **kwargs):		
        """Verteilung der relativen Häufigkeiten; zugehörige Methode"""
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\nZusatz")
            print("p=ja  - relative Häufigkeiten werden als Prozentwerte ausgegeben")
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
            kk.sort()			
            for k in kk:		
                display(Math(latex(k) + '\\quad ' + latex(di[k])))	
            print(' ')			
            return			
        elif d or p:
            return di1
        return di			
		
    Vert = vert_	
    vert_rel_h_= vert_
    VertRelH = vert_
		
    @property		
    def _vert_kum(self):
        """Kumulierte relative Häufigkeiten; internes dict"""	
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return					
        di = self._vert
        ll, sum = [], 0	
        keys = list(di.keys())
        keys.sort()		
        for k in keys:
            sum += di[k]		
            ll += [(k, sum)]
        return dict(ll)			
		
    @property				
    def vert_kum(self):
        """Kumulierte Häufigkeitskeitsverteilung"""	
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        return self._vert_kum
    def vert_kum_(self, s=None, p=None, sp=None, **kwargs):		
        """Kumulierte Häufigkeitskeitsverteilung; zugehörige Methode"""
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\nZusatz")
            print("p=ja  - relative Häufigkeiten werden als Prozentwerte ausgegeben")
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
	
	
    def F(self, *args, **kwargs):
        """Empirische Verteilungsfunktion"""
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return	
			
        if kwargs.get('h'):
            print("\nEmpirische Verteilungsfunktion\n")		
            print("Aufruf   dr . F( wert )\n")		                     
            print("               dr    DatenReihe")
            print("               wert  Zahl\n")
            print("Zusatz    d=n    Darstellung als Dezimalzahl mit n Kommastellen")			
            print("          b=ja   Erläuterung des Begriffes\n")			
            return 

        if kwargs.get('b'):
            print("\nDer Wert der empirischen Verteilungsfunktion an einer Stelle x ist der")
            print("Quotient aus der Anzahl der Datenelemente, die kleiner oder gleich x ")
            print("sind und der Anzahl aller Datenelemente\n")			
            return			
			
        import statsmodels
		
        dat = self.daten
        F = statsmodels.distributions.empirical_distribution.ECDF(dat)
        if kwargs.get('alle'):   # internes kwarg
            dat = self.daten
            dat.sort()		
            return F(dat)		
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        wert = sympify(args[0])
        if not isinstance(wert, (int, Integer, Rational, float, Float)):			
            print('zufall: einen Zahlenwert angeben')
            return
        dat.sort()		 
        erg = F(wert)		
        d = kwargs.get('d')			
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(erg, ".%df" % d))			
        return nsimplify(erg)       
		
		
    @property	
    def hist(self):
        """Histogramm der relativen Häufigkeiten"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        daten = self._vert
        balken1(daten, typ='R', titel='$Verteilung\; der\; relativen\; Häufigkeiten - Histogramm$' + '\n')
    def hist_(self, *args, **kwargs):
        """Histogramm; zugehörige Methode"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\nZusatz   p=ja   Polygonzug-Diagramm")
            print("Angabe einer Zufallsgröße | DatenReihe - Vergleich mit anderer Verteilung\n")
            return			
        if kwargs.get('p'):
            self.poly_zug
            return			
        daten = self._vert
        if not args:
            self.hist
            return
        if len(args) != 1:
            print("zufall: nur ein Argument angeben")
            return
        arg = args[0]	
        zg = importlib.import_module('zufall.lib.objekte.zufalls_groesse')
        nv = importlib.import_module('zufall.lib.objekte.normal_verteilung')
        ev = importlib.import_module('zufall.lib.objekte.exponential_verteilung')
        ZufallsGroesse= zg.ZufallsGroesse		
        NormalVerteilung = nv.NormalVerteilung
        ExponentialVerteilung = ev.ExponentialVerteilung         		
        if not isinstance(arg, (ZufallsGroesse, DatenReihe, NormalVerteilung, ExponentialVerteilung)):			
            print("zufall: Zufallsgröße oder DatenReihe angeben")
            return
        if isinstance(arg, NormalVerteilung):	
            balken_plus_stetig	(daten, arg, typ='R', 
                titel='$Vergleich\; mit\; der\; Normalverteilung$' + '\n ') 	
            return			
        elif isinstance(arg, ExponentialVerteilung):	
            balken_plus_stetig	(daten, arg, typ='R', 
                titel='$Vergleich\; mit\; der\; Exponentialverteilung$' + '\n ') 	
            return			
        daten2 = arg._vert			
        if isinstance(arg, ZufallsGroesse):			
            typ2 = 'W'
            titel = '$Vergleich\; von\; Häufigkeits-\; u.\; Wahrsch.-Verteilungen$' + '\n' + \
                   '$grün - rel.\; Häufigkeiten,\; gelb - Wahrscheinlichkeiten$' '\n'			
        else:
            typ2 = 'R'		
            titel = '$Vergleich\; von\; zwei\; relativen\; Häufigkeitsverteilungen$' + '\n' + \
                   '$hell - Ausgangs-, dunkel - Vergleichsverteilung$' + '\n'				   
        balken_plus_balken	(daten, daten2, typ1='R', typ2=typ2, titel=titel) 	
		
    hist_rel_h = hist		
    histRelH = hist		
    Hist = hist_		
				
    @property	
    def hist_kum(self):
        """Histogramm der kumulierten relativen Häufigkeiten"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        daten = self._vert_kum
        balken1(daten, typ='R', titel='$Kumulierte\; relative\; Häufigkeiten - Histogramm$' + '\n ')
		
    histKum = hist_kum		
	
    @property	
    def vert_abs_h(self):
        """Verteilung der absoluten Häufigkeiten"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        return self.H(d=True)
    def vert_abs_h_(self, *args, **kwargs):
        """Verteilung der absoluten Häufigkeiten; zugehörige Methode"""
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\ns=ja   Spaltenausgabe\n")
            return			
        if kwargs.get('s'):
            return self.H(s=True)
        return self.H(d=True)
		
    vertAbsH = vert_abs_h	
    VertAbsH = vert_abs_h_	
		
    @property	
    def hist_abs_h(self):
        """Histogramm der absoluten Häufigkeiten"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        daten = self._H
        balken1(daten, typ='A', titel='$Verteilung\; der\; absoluten\; Häufigkeiten - Histogramm$' + '\n ')

    histAbsH = hist_abs_h		
		
    @property	
    def linien(self):
        """Linien-Daten-Diagramm"""
        if not self.is_ganz:
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        dat = self.daten	
        n = len(dat)		
        daten = dict([[i, dat[i]] for i in range(n)])
        polygon_zug(daten, typ='D', titel='$Daten-Linien-Diagramm$' + '\n ')
				
    @property	
    def poly_zug(self):
        """Polygonzug"""
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        daten = self._vert
        polygon_zug(daten, typ='R', titel='$Relative\; Häufigkeiten - Polygonzug$' + '\n')
    def poly_zug_(self, *args, **kwargs):
        """Polygonzug; zugehörige Methode"""
        if not self.is_ganz:		
            print("zufall: Datenelemente nicht ganzzahlig; eventuell Klasseneinteilung vornehmen")
            return			
        if kwargs.get('h'):
            print("\nZusatz   hi=ja   Histogramm")
            print("Angabe einer Zufallsgröße | DatenReihe - Vergleich mit anderer Verteilung\n")
            return			
        if kwargs.get('hi'):
            self.hist
            return			
        daten = self._vert
        if not args:
            s
            return
        if len(args) != 1:
            print("zufall: nur ein Argument angeben")
            return
        arg = args[0]	
        zg = importlib.import_module('zufall.lib.objekte.zufalls_groesse')
        ZufallsGroesse= zg.ZufallsGroesse		
        if not isinstance(arg, (ZufallsGroesse, DatenReihe)):			
            print("zufall: Zufallsgröße oder DatenReihe angeben")
            return
        daten2 = arg._vert			
        if isinstance(arg, ZufallsGroesse):			
            typ2 = 'W'
            titel = '$Vergleich\; von\; Häufigkeits- u.\; Wahrsch.-Verteilungen$' + '\n' + \
                   '$grün - rel. Häufigkeiten,\; gelb - Wahrscheinlichkeiten$' + '\n'			
        else:
            typ2 = 'R'		
            titel = '$Vergleich\; von\; zwei\; relativen\; Häufigkeitsverteilungen$' + '\n' + \
                   '$hell - Ausgangs-,\; dunkel - Vergleichsverteilung$' + '\n'				   
        poly_plus_poly	(daten, daten2, typ1='R', typ2=typ2, titel=titel) 	
		
    polyZug = poly_zug				
    PolyZug = poly_zug_				
				
				
    @property	
    def graf_F(self):
        """Graf der empirischen Verteilungsfunktion"""
        vert_funktion(self, typ='D', titel='$Empirische\; Verteilungsfunktion$' + '\n ')
				
    grafF = graf_F
	
    @property	
    def mittel(self):
        """Arithmetischer Mittelwert"""
        sum = 0
        for x in self.daten:
            sum += x
        wert = sum / self.n			
        if self.is_ganz:
            return nsimplify(wert)		
        return wert		
    def mittel_(self, **kwargs):
        """Arithmetischer Mittelwert; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Kommastellen")
            print("         f=ja   Berechnungsformel\n")
            return 
        if kwargs.get('f'):
            print(' ')		
            lat = '\\overline {x} = \\frac{1}{n} \sum\limits_{i=1}^{n}x_i'		
            display(Math(lat))
            display(Math('x_i - Elemente, \\quad n - Umfang\: der\: DatenReihe'))
            print(' ')			
            return		
        d = kwargs.get('d')
        erg = self.mittel		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(erg), ".%df" % d))			
        return N(erg)       
		
    Mittel = mittel_		
		
    @property	
    def var(self):
        """Varianz"""
        mittel = self.mittel
        sum = 0		
        for x in self.daten:
            sum += (x - mittel)**2
        return sum / self.n		
    def var_(self, **kwargs):
        """Varianz; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   d=n     Darstellung dezimal mit n Kommastellen")
            print("         a=ja    Berechnung mit 1/(n-1)")
            print("         ad=ja   ebenso, Darstellung dezimal")
            print("         f=ja    Berechnungsformeln\n")
            return 
        if kwargs.get('a'):
            sum = self.n * self.var
            return sum / (self.n-1)
        if kwargs.get('ad'):
            n = self.n		
            sum = n * self.var
            return float(sum / (n-1))
        if kwargs.get('f'):
            print(' ')		
            lat = 'Varianz = s^2 = \sum\limits_{i=1}^{m} h(x_i)\:(x_i  - \\overline{x})^2'		
            display(Math(lat))
            display(Math('x_i - verschiedene\; Elemente\; der\; DatenReihe, \\quad h(x_i) - deren\;' +
                  u'relative\; Häufigkeiten'))
            display(Math('\\overline{x} - arithmetisches\; Mittel'))
            display(Math("Dieser\; Wert\; kann\; auch\; so\; erhalten\; werden:"))				  
            lat = 's^2 = \\frac{1}{n} \sum\limits_{i=1}^{n} (x_i  - \\overline{x})^2'		
            display(Math(lat))
            display(Math('x_i - Elemente, \\quad n - Umfang\; der\; DatenReihe'))
            display(Math("Bei\; Angabe\; des\; Zusatzes\; a\; wird\; diese\; Formel\; benutzt"))
            lat = 's^2 = \\frac{1}{n-1} \sum\limits_{i=1}^{n} (x_i  - \\overline{x})^2'		
            display(Math(lat))
            print(' ')			
            return		
        d = kwargs.get('d')
        erg = self.var		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(erg), ".%df" % d))			
        return erg       
			
    Var = var_
	
    @property	
    def s(self):
        """Standardabweichung"""
        return sqrt(self.var)		
    def s_(self, **kwargs):
        """Standardabweichung; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Kommastellen")
            print("         b=ja    Berechnung\n")
            return 
        if kwargs.get('b'):
            print("\nDie Standardabweichung ist die Quadratwurzel aus der Varianz der")
            print("DatenReihe\n")
            return						
        d = kwargs.get('d')
        erg = self.s		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(erg), ".%df" % d))			
        return erg       
			
    S = s_
	
    @property	
    def spann_weite(self):
        """Spannweite"""
        return self.max - self.min		
    def spann_weite_(self, **kwargs):
        """Spannweite; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   b=ja    Berechnung\n")
            return 
        if kwargs.get('b'):
            print("\nDie Spannweite ist die Länge des Intervalls")
            print("[ kleinster Wert der DatenReihe, größter Wert der DatenReihe ]\n")
            return	
        return self.spann_weite			
	
    spannWeite = spann_weite
    SpannWeite = spann_weite_
				
    def quantil(self, *args, **kwargs):
        """Quantile"""
        if kwargs.get('h'):
            print("\nQuantil\n")		
            print("Aufruf   dr . quantil( p )\n")		                     
            print("             dr    DatenReihe")
            print("             p     Zahl aus [0,1]\n")
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        pp = args[0]
        if not isinstance(pp, (int, Integer, float, Float, Rational)):			
            print('zufall: Zahl aus [0,1] angeben')
        if not (0 <= pp <= 1):			
            print('zufall: Zahl aus [0,1] angeben')
            return
        pp = float(pp)	
        from scipy.stats.mstats import mquantiles
        qq = mquantiles(self.daten, [pp])[0]	
        q1 = floor(qq)
        if qq == q1: 		
            return q1
        return qq			

    @property	
    def o_quartil(self):
        """Oberes Quartil"""
        return self.quantil(Rational(3/4))		
    def o_quartil_(self, **kwargs):
        """Oberes Quartil; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   b=ja    Berechnung\n")
            return 
        if kwargs.get('b'):
            print("\nDas obere Quartil ist der Quantilwert für p = 3/4\n")		
            return 
        return self.o_quartil						
		
    oQuartil = o_quartil
    OQuartil = o_quartil_
		
    @property	
    def u_quartil(self):
        """Unteres Quartil"""
        return self.quantil(Rational(1/4))		
    def u_quartil_(self, **kwargs):
        """Unteres Quartil; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   b=ja    Berechnung\n")
            return 
        if kwargs.get('b'):
            print("\nDas untere Quartil ist der Quantilwert für p = 1/4\n")		
            return 
        return self.u_quartil			

    uQuartil = u_quartil
    UQuartil = u_quartil_
	
    @property	
    def halb_weite(self):
        """Halbweite"""
        dat = self.daten
        return self.o_quartil - self.u_quartil		
    def halb_weite_(self, **kwargs):
        """Halbweite; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   e=ja    Erläuterung\n")
            return 
        if kwargs.get('e'):
            print("\nDie Halbweite ist die Länge des Intervalls")
            print("[ unteres Quartil der DatenReihe, oberes Quartil der DatenReihe ]\n")
            return
        return self.halb_weite			
	
    halbWeite = halb_weite	
    HalbWeite = halb_weite_
	
    @property	
    def median(self):
        """Median"""
        n, dat = self.n, self.daten
        dat.sort()	
        m = n/2
        if	 n/2-floor(n/2) != 0.0:
            return dat[int(m)]        		
        return Rational(1, 2)*(dat[int(m)] + dat[int(m)-1])        
    def median_(self, **kwargs):
        """Median; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   b=ja    Berechnung\n")
            return 
        if kwargs.get('b'):
            print("\nDer Median wird auch Zentralwert genannt; ein oft verwendetes Symbol ist")			
            display(Math('\\tilde{x}'))	
            print("Bei 2n+1 Datenelementen ist er gleich dem (n+1). Datenelement in der")
            print("nach der Größe geordneten DatenReihe, für 2n Datenelemente ist es das")
            print("arithmetische Mittel aus dem n. und dem (n+1). Datenelement\n")
            return
        return self.median			
		
    Median = median_			
				
    @property	
    def modal(self):
        """Modalwert(e)"""
        di = self._H
        m = max(di.values())
        liste = []
        for k in di.keys():
            if di[k] == m:
                liste += [k]
        return liste, m				
    def modal_(self, **kwargs):
        """Modalwert(e); zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   r=ja    relative Häufigkeit")
            print("         rd=ja   ebenso, dezimal")
            print("         e=ja    Erläuterung\n")
            return 
        if kwargs.get('e'):
            print("\nErläuterung der Ausgabe:")
            print("Die Liste enthält den/die Modalwert(e), dann folgt die absolute bzw. ")
            print("relative Häufigkeit\n")
            return
        if kwargs.get('r'):
            m = self.modal		
            return m[0], nsimplify(m[1]/self.n) 			
        if kwargs.get('rd'):
            m = self.modal		
            return m[0], float(m[1]/self.n) 						
        return self.modal			
		
    Modal = modal_			

    def korr_koeff(self, *args, **kwargs):
        """Korrelationskoeffizient"""
        if kwargs.get('h'):
            print("\nKorrelationskoeffizient für zwei  DatenReihen\n")		
            print("Aufruf   dr . korr_koeff( dr1 )\n")		                     
            print("              dr    DatenReihe\n")
            return 
					
        if len(args) != 1:
            print("zufall: andere DatenReihe als Argument angeben")		
            return
        dr1, dr2 = self, args[0]
        if not isinstance(dr2, DatenReihe):
            print("zufall: andere DatenReihe als Argument angeben")		
            return
        if dr1.n != dr2.n:
            print("zufall: die DatenReihen müssen gleichen Umfang haben")		
            return		
        d1 = np.array([float(x) for x in dr1.daten])		
        d2 = np.array([float(x) for x in dr2.daten])		
        from numpy import corrcoef
        cc = corrcoef(d1, d2)			
        return cc[0, 1]		
	
    korrKoeff = korr_koeff
	
    def streu_diagr(self, *args, **kwargs):
        """Streudiagramm mit Regressionsgerade"""
        if kwargs.get('h'):
            print("\nStreudiagramm mit Regressionsgerade für zwei DatenReihen\n")		
            print("Aufruf   dr . streu_diagr( dr1 )\n")		                     
            print("              dr    DatenReihe\n")
            print("Zusatz   g=ja   Gleichung der Regressionsgeraden\n")			
            return 					
        if len(args) != 1:
            print("zufall: andere DatenReihe als Argument angeben")		
            return
        dr1, dr2 = self, args[0]
        if not isinstance(dr2, DatenReihe):
            print("zufall: andere DatenReihe als Argument angeben")		
            return
        if dr1.n != dr2.n:
            print("zufall: die DatenReihen müssen gleichen Umfang haben")		
            return	
        # aus dem Internet			
        import numpy as np
        import matplotlib.pyplot as plt		
        x = np.array(dr1.daten)
        A = np.array([x, np.ones(len(x))])
        y = np.array(dr2.daten)
        w = np.linalg.lstsq(A.T, y)[0]   # Parameter berechnen
        print(' ')	
        plt.close('all')		
        fig = plt.figure(figsize=(4, 3))
        x1, x2 = min(x), max(x)
        plt.xlim(x1-0.05*(x2-x1), x2 + 0.05*(x2-x1))		
        y1, y2 = min(y), max(y)
        plt.ylim(y1-0.05*(y2-y1), y2 + 0.05*(y2-y1))		
        if kwargs.get('g'):
            display(Math('\\text{Gleichung der Regressionsgeraden}'))		
            display(Math('y =' + latex(w[0]) + '\; x +' + latex(w[1])))
        line = w[0]*x + w[1]
        plt.plot(x, line, 'r-', linewidth=1.5)
        plt.plot(x, y,'o', color=(0,0,0), markersize=3.0)		
        plt.title('$\mathrm{Streudiagramm}$\n', fontsize=10.5, 
                 loc='left', fontname='Times New Roman', color=(0.2, 0.2, 0.2))
        plt.xlabel('$x$', fontsize=11)
        plt.ylabel('$y$', fontsize=11)
        for tick in plt.gca().xaxis.get_major_ticks():
            tick.label1.set_fontsize(10)
            tick.label1.set_color((0.5,0.5, 0.5))
            tick.label1.set_fontname('Times New Roman')
        for tick in plt.gca().yaxis.get_major_ticks():
            tick.label1.set_fontsize(10)	
            tick.label1.set_color((0.5, 0.5, 0.5))
            tick.label1.set_fontname('Times New Roman')
        for pos in ('top', 'bottom', 'right', 'left'): 			
            plt.gca().spines[pos].set_linewidth(0.5)		
        plt.show()
		
    streuDiagr = streu_diagr
	
    @property		
    def box_plot(self):
        """Boxplot-Diagramm """
        import numpy as np
        import matplotlib.pyplot as plt		
        print(' ')		
        dat = np.array([float(x) for x in self.daten])
        plt.close('all')		
        fig = plt.figure(1, figsize=(4, 3))
        ax = fig.add_subplot(111)		
        m, M = np.min(dat), np.max(dat)
        mm = max(abs(m), abs(M))
        d = 0.1*abs(abs(M) - abs(m))		
        plt.ylim(m-d, M+d)
        plt.boxplot(dat, 0, 'r')
        plt.title('$Boxplot-Diagramm\; der\; DatenReihe$' + '\n', fontsize=10.5, 
                 fontname='Times New Roman', loc='left', color=(0.2, 0.2, 0.2))
        ax.set_xticklabels([])		
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(9)	
            tick.label1.set_fontname('Times New Roman')
            tick.label1.set_color((0.2, 0.2, 0.2))
        for pos in ('top', 'bottom', 'right', 'left'): 			
            ax.spines[pos].set_linewidth(0.5)	
			
        plt.show()		
    def box_plot_(self, *args, **kwargs):
        """Boxplot-Diagramm; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   e=ja   Erläuterungen zum Diagramm\n")	
            return			
        if kwargs.get('e'):
            print("\nDargestellt sind:\n")		                     
            print("maximaler Wert der DatenReihe (obere dunkle Linie)")
            print("oberes Quartil (obere Grenze des inneren Kastens)")		
            print("Median (rote Linie)")			
            print("unteres Quartil (untere Grenze des inneren Kastens)")		
            print("minimaler Wert der DatenReihe (untere dunkle Linie)")
        self.box_plot		

    boxPlot = box_plot
    BoxPlot = box_plot_

	
    @property		
    def violin_plot(self):
        """Violinplot-Diagramm"""
        import numpy as np
        import matplotlib.pyplot as plt
        print(' ')		
        dat = [float(x) for x in self.daten]
        plt.close('all')		
        fig = plt.figure(1, figsize=(4, 3))
        ax = fig.add_subplot(111)		
        m, M = np.min(dat), np.max(dat)
        d = 0.1*abs(abs(M) - abs(m))		
        plt.ylim(m-d, M+d)
        plt.violinplot(dat, showextrema=True, showmeans=True, showmedians=True)
        plt.title('$Violinplot-Diagramm\; der\; DatenReihe$' + '\n', fontsize=10.5, 
                 fontname='Times New Roman', loc='left', color=(0.2, 0.2, 0.2))
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(9)	
            tick.label1.set_fontname('Times New Roman')
            tick.label1.set_color((0.2, 0.2, 0.2))
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(9)	
            tick.label.set_fontname('Times New Roman') 
            tick.label1.set_color((0.2, 0.2, 0.2))
        for pos in ('top', 'bottom', 'right', 'left'): 			
            ax.spines[pos].set_linewidth(0.5)
			
        plt.show()		
    def violin_plot_(self, *args, **kwargs):
        """Violinplot-Diagramm; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz   e=ja   Erläuterungen zum Diagramm\n")	
            return			
        if kwargs.get('e'):
            print("\nDargestellt sind:\n")		                     
            print("Maximaler und minimaler Wert, Mittelwert, Median der DatenReihe")
            print("(schwarze bzw. rote horizontale Linien)\n")
            print("Die Grafik dazwischen vermittelt ein Bild der Wahrscheinlichkeits-")
            print("verteilung auf der Grundlage einer Kerndichteschätzung")			
        self.violin_plot		
		
    violinPlot = violin_plot
    ViolinPlot = violin_plot_
	
    def klassen(self, *args, **kwargs):
        """KLasseneinteilung"""
        if kwargs.get('h'):
            print("\nKLasseneinteilung / Gruppierung der Daten\n")		
            print("Aufruf   dr . klassen( anzahl )\n")		                     
            print("             anzahl   Anzahl Klassen\n")
            print("Die Klassen haben gleiche Breite und folgen unmittelbar aufeinander\n")			
            print("Die zurückgegebene DatenReihe beinhaltet für alle Datenelemente den") 
            print("Index der Klasse, in der das Datenelement liegt\n")
            print("Zusatz   g=ja      Ausgabe der Klassengrenzen")
            return 					
        if len(args) != 1:
            print('zufall: ein Argument angeben')
            return			
        anzahl = args[0]	
        if not isinstance(anzahl, (int, Integer)) and anzahl > 0:
            print('zufall: die Anzahl der Klassen muß ganz und positiv sein')
            return			
        daten = self.daten
        if anzahl > len(daten):
            print('zufall: die Anzahl der Klassen soll nicht größer als die Anzahl der Daten sein')
            return			
        anf = min(daten)
        b = self.spann_weite / anzahl		
        klass = [[anf + i*b, anf + (i+1)*b] for i in range(anzahl)]
		
        def ss(s):
            return ' ' * (4-len(str(s)))  		
			
        if kwargs.get('g'):
            print('Klasse  Grenzen')
            for i in range(len(klass)):
                print(ss(i) + str(i), '  ', klass[i])
            return
        di =  dict([[i, 0] for i in range(anzahl)])
        m = max(daten)		
        for d in daten:
            nr = int(floor( (d-anf) / b ) )   
            if d == m:
                nr -=1			
            di[nr] += 1 
        return DatenReihe(di) 		

    @property		
    def max(self):  
        """größter Wert"""
        return np.max(self.daten)		
		
    @property		
    def min(self):  
        """kleinster Wert"""
        return np.min(self.daten)		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        datenreihe_hilfe(3)	
		
    h = hilfe					
	
		
		
# Benutzerhilfe für DatenReihe
# ----------------------------

def datenreihe_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
DatenReihe - Objekt

Kurzname     DR
		
Erzeugung    DatenReihe( daten )       
          
                 daten	   zahl /[, zahl1, ... ]  | 
                           { zahl : wiederh /[, zahl1 : wiederh1, ... ] }
                 wiederh   Anzahl der Wiederholungen von zahl

Es werden vorwiegend DatenReihen mit ganzzahligen Elementen betrachtet				
 
Zuweisung     dr = DR(...)   (dr - freier Bezeichner)

Beispiele
DR( 2, 5, 8, 2, 5, 2 )
DR( {2:4, 1:6, 6:3}, 4, 7 )
DR( 2.24, 1.67, 5.45, 3.34, 2.40 )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für DatenReihe
 
dr.hilfe                Bezeichner der Eigenschaften und Methoden
dr.box_plot             Boxplot-Daten-Diagramm		
dr.box_plot_(...)    M  ebenso, zugehörige Methode
dr.daten                Daten-Liste
dr.diagr                Balken-Diagramm der Daten
dr.F(...)            M  empirische Verteilungsfunktion
dr.graf_F               Graf der empirischen Verteilungsfunktion
dr.hh(...)           M  relative Häufigkeiten
dr.H(...)            M  absolute Häufigkeiten
dr.halb_weite           Halbweite
dr.halb_weite_(...)  M  ebenso, zugehörige Methode
dr.hist                 Histogramm der relativen Häufigkeiten
dr.hist_(...)        M  ebenso, zugehörige Methode
dr.hist_abs_h           Histogramm der absoluten Häufigkeiten
dr.hist_kum             Histogramm der kumulierten rel. Häufigkeiten
dr.hist_rel_h           = dr.hist
dr.is_ganz              Test auf ganzzahlige Daten		
dr.klassen           M  KLasseneinteilung
dr.korr_koeff        M	 Korrelationskoeffizient für zwei DatenReihen
dr.linien               Linien-Diagramm der Daten
dr.max                  größter Wert
dr.min                  kleinster Wert
dr.mittel               Arithmetischer Mittelwert
dr.mittel_(...)      M  ebenso, zugehörige Methode
dr.modal                Modalwert(e)
dr.modal_(...)       M  ebenso, zugehörige Methode
dr.n                    = dr.umfang
dr.o_quartil            oberes Quartil
dr.o_quartil_(...)   M  ebenso, zugehörige Methode
dr.poly_zug             Polygonzug-Diagramm der relativen Häufigkeiten
dr.quantil(...)      M  Quantile          
dr.s                    Standardabweichung
dr.s_(...)           M  ebenso, zugehörige Methode
dr.spann_weite          Spannweite
dr.spann_weite_      M  ebenso, zugehörige Methode
dr.streu_diagr       M  Streudiagramm mit Regr.Gerade für zwei DatenReihen
dr.umfang               Umfang / Anzahl Elemente
dr.u_quartil            unteres Quartil
dr.u_quartil_(...)   M  ebenso, zugehörige Methode
dr.var                  Varianz
dr.var_(...)         M  ebenso, zugehörige Methode
dr.vert                 Verteilung der relativen Häufigkeiten
dr.vert_(...)        M  ebenso, zugehörige Methode	
dr.vert_abs_h           Verteilung der absoluten Häufigkeiten
dr.vert_abs_h_(...)  M  ebenso, zugehörige Methode
dr.vert_kum             Verteilung der kumulierten relativen Häufigkeiten
dr.vert_kum_(...)    M  ebenso, zugehörige Methode
dr.vert_rel_h           = dr.vert
dr.vert_rel_h_(...)  M  = dr.vert_
dr.violin_plot          Violinplot-Daten-Diagramm
dr.violin_plot_(...) M  ebenso, zugehörige Methode

Synonyme Bezeichner

h              hilfe
box_plot       boxPlot
box_plot_      BoxPlot
graf_F         grafF
halb_weite     halbWeite
halb_weite_    HalbWeite
hist_          Hist
hist_abs_h     histAbsH
hist_kum       histKum
hist_rel_h     histRelH
is_ganz        isGanz
korr_koeff     korrKoeff
mittel_        Mittel
o_quartil      oQuartil
o_quartil_     OQuartil
poly_zug       polyZug
poly_zug_      PolyZug
modal_         Modal
s_             S
spann_weite    spannWeite
spann_weite_   SpannWeite
streu_diagr    streuDiagr
u_quartil      uQuartil
u_quartil_     UQuartil
var_           Var
vert_          Vert
vert_abs_h     vertAbsH
vert_abs_h_    VertAbsH
vert_kum       vertKum
vert_kum_      VertKum
vert_rel_h     vertRelH
vert_rel_h_    VertRelH
violin_plot    violinPlot
violin_plot_   ViolinPlot
	   """)		
        return
	
	
DR = DatenReihe



		
		