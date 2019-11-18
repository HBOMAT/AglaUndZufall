#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  ExponentialVerteilung - Klasse  von zufall           
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
from scipy.stats import expon
import matplotlib.pyplot as plt

from sympy.core.numbers import Integer, Rational, Float   
from sympy.core.symbol import Symbol
from sympy import sympify, nsimplify, Piecewise
from sympy import exp
from sympy.core.relational import (GreaterThan, StrictGreaterThan, LessThan, 
    StrictLessThan)
from sympy.printing.latex import latex

from sympy.stats import Exponential, sample, sample_iter

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.datenreihe import DatenReihe 
from zufall.lib.funktionen.funktionen import is_zahl, mit_param 

from zufall.lib.objekte.ausnahmen import ZufallError
	
	

# ExponentialVerteilung - Klasse  
# ------------------------------
#

class ExponentialVerteilung(ZufallsObjekt):                                      
    """

Exponentialverteilung

**Kurzname** **EV**
	
**Erzeugung** 
	
   EV( *par* )

**Parameter**
 
   *par* : Parameter der Verteilung (Zahl > 0)
   
    """
		
    # interne args:  lambda 
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            exponential_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 1:
                raise ZufallError("ein Argument angeben")
            lamda = args[0]
            lamda = sympify(lamda)
            if not is_zahl(lamda):
                raise ZufallError("der Parameter muß eine Zahl sein")
            lamda = nsimplify(lamda)				
            if lamda <= 0:
                raise ZufallError("der Parameter muß > 0 sein")
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsObjekt.__new__(cls, lamda)

			
    def __str__(self):  
        lamda = self.args[0]
        return "ExponentialVerteilung(" + str(lamda) + ")"

		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def par(self):
        """Parameter"""	
        return self.args[0]
		
    lamda = par		


    @property
    def erw(self):
        """Erwartungswert"""	
        return nsimplify(1 / self.par)	
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
    def sigma(self):
        """Standardabweichung"""				
        return nsimplify(1 / self.par)	
    def sigma_(self, *args, **kwargs):
        """Standardabweichung; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Kommastellen\n")
            return
        d = kwargs.get('d')
        v = self.sigma		
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(v), ".%df" % d))			
        return float(v)       

    Sigma = sigma_		

    @property
    def var(self):
        """Varianz"""				
        return nsimplify(1 / self.par**2)	
    def var_(self, *args, **kwargs):
        """Varianz; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Kommastellen\n")
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
    def formeln(self):
        """Formeln"""
        print(' ')	
        x = Symbol('x')
        lamda = Symbol('lamda')		
        p = Piecewise([0, x<0], [lamda * exp(-lamda * x), x>=0])
        F = Piecewise([0, x<0], [1 - exp(-lamda * x), x>=0])	
        display(Math('\mathrm{Dichtefunktion} \\qquad\\qquad\; p(x) = ' + latex(p) )) 
        display(Math('\mathrm{Verteilungsfunktion} \\qquad\: F(x) = P(X \\le x) = ' + latex(F)  ))
        display(Math('\mathrm{Erwartungswert} \\qquad\;\;\;\;\,\, \\frac{1}{\\lambda}'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad \;\;\;\;\,\;\;\;\; \\frac{1}{\\lambda^2}'))	
        display(Math('\\lambda \,\mathrm{-\, Parameter, \;aktueller\; Wert}\;\;\; \\lambda = ' + latex(self.args[0])))
        print(' ')		
        
    def dichte(self, *args, **kwargs):
        if kwargs.get('h'):
            print("\nDichtefunktion\n")		
            print("Aufruf   ev . dichte( x )")		                     
            print("             ev    Exponentialverteilung")
            print("             x     Zahl\n")
            print("Zusatz   d=n   Ausgbabe  dezimal mit n Kommastellen\n")			
            return 
        if len(args) != 1:
            print('zufall: ein Argumente angeben')
            return
        x = args[0]
        if not is_zahl(x):
            print('zufall: eine Zahl angeben')
            return
        def pp(x):
            p = self.par		
            return Piecewise([p * exp(-p * x), x>=0], [0, x<0])		
        wert = pp(x)	
        if mit_param(wert):
            return wert		
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(wert), ".%df" % d))			
        return wert       
        

    @property		
    def graf_D(self):
        """Graf der Dichtefunktion"""	
        if mit_param(self):
            print("zufall: nicht verfügbar (Parameter)")
            return
        X = expon(loc=0, scale=float(1/self.par))			
        fig = plt.figure(figsize=(4, 4))		
        ax = fig.add_subplot(1, 1, 1)
        xu, xo = 0., float(X.ppf(1-1e-5))
        x = np.linspace(xu, xo, 100)
        plt.xlim(xu, xo)
        plt.ylim(0, float(1.1 * self.par))
        ax.plot(x, X.pdf(x), color=(0.956893, 0.643101, 0.376507), linewidth=2.5)   # RGB::SandyBrown    
        plt.title('\nDichtefunktion\n', fontsize=12, loc='left', fontname='Times New Roman')
        plt.xlabel('$x$', fontsize=14, alpha=0.9)
        plt.ylabel('$p(x)$', fontsize=12, alpha=0.9)
        loc, labels = plt.yticks()		
        for t in loc:
            plt.plot([xu, xo], [t, t], color=(0.3,0.3,0.3), linewidth=0.3)		
        plt.show()		

    grafD = graf_D		
    	
    def F(self, *args, **kwargs):
        """Verteilungsfunktion"""	
        if kwargs.get('h'):
            print("\nVerteilungsfunktion\n")		
            print("Aufruf   ev . F( x )\n")		                     
            print("              ev    Exponentialverteilung")
            print("              x     Zahl\n")
            print("Zusatz   d=n   Ausgbabe  dezimal mit n Kommastellen\n")			
            return 
        if len(args) != 1:
            print('zufall: ein Argumente angeben')
            return
        x = args[0]
        if not is_zahl(x):
            print('zufall: eine Zahl angeben')
            return
        if isinstance(x, (float, Float)):			
            x = Rational(x)			
        def FF(x):
            return Piecewise([1 - exp(-self.par * x), x>=0], [0, x<0])		
        wert = FF(x)		
        if mit_param(wert):
            return wert		
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(wert), ".%df" % d))			
        return wert      
		
    @property		
    def graf_F(self):
        """Graf der Verteilungsfunktion"""	
        if mit_param(self):
            print("zufall: nicht verfügbar (Parameter)")
            return
        X = expon(loc=0, scale=float(1/self.par))			
        fig = plt.figure(figsize=(4, 3))		
        ax = fig.add_subplot(1, 1, 1)
        xu, xo = 0, X.ppf(1-1e-5)
        x = np.linspace(xu, xo, 100)
        plt.xlim(xu, xo)
        plt.ylim(0, 1.1)
        ax.plot(x, X.cdf(x), color=(0.956893, 0.643101, 0.376507), linewidth=2.5)   # RGB::SandyBrown    
        plt.title('\nVerteilungsfunktion\n', fontsize=12, loc='left', \
		    fontname='Times New Roman')
        plt.xlabel('$x$', fontsize=14, alpha=0.9)
        plt.ylabel('$P(X < x)$', fontsize=12, alpha=0.9)		
        ytickspos = []
        i, dy = 1, 0.2
        while True:
            ytickspos += [i*dy]
            i += 1
            if (i-1)*dy > 1.:
                break           
        yticks = [eval(format((i+1)*dy, '.1f')) for i in range(len(ytickspos))]
        plt.yticks(ytickspos, [t for t in yticks if t <= 1])  
        for t in ytickspos:
            plt.plot([xu, xo], [t, t], color=(0.3,0.3,0.3), linewidth=0.3)		
        plt.show()		

    grafF = graf_F		
		
    def quantil(self, *args, **kwargs):
        """Quantile"""	
        if kwargs.get('h'):
            print("\nQuantile\n")		
            print("Aufruf   ev . quantil( q )\n")		                     
            print("              ev    Exponentialverteilung")
            print("              q     Zahl aus [0,1]\n")
            print("Zusatz   d=n   Ausgbabe mit n Kommastellen\n")			
            return 
        if mit_param(self):
            print('zufall: nicht verfügbar (Parameter)')
            return		
        if len(args) != 1:
            print('zufall: ein Argumente angeben')
            return
        q = args[0]
        if not is_zahl(q) or mit_param(q):
            print('zufall: eine Zahl angeben')
            return
        if not 0 <= q <= 1:			
            print('zufall: eine Zahl aus [0,1] angeben')
            return
        X = expon(loc=0, scale=float(1/self.par))			
        wert = X.ppf(float(q))		
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(wert), ".%df" % d))			
        return float(wert)       
		
		
    @property		
    def versuch(self):
        """Versuch"""	
        X = Exponential('X', self.par)	
        return sample(X)		
		
    def stich_probe(self, *args, **kwargs):
        """Stichprobe"""
        if kwargs.get('h'):
            print("\nStichprobe\n")		
            print("Aufruf   ev . stichprobe( m )\n")		                     
            print("              ev   Exponentialverteilung")
            print("              m    Umfang (Anzahl Versuche)\n")
            print("Zusatz   d=ja   Rückgabe als DatenReihe\n")
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        m = sympify(args[0])
        if not isinstance(m, (int, Integer)) and m > 0:			
            print('zufall: ganze Zahl > 0 angeben')
            return
        else:
            X = Exponential('X', self.par)	
            iterator = sample_iter(X, numsamples=m)
            ll = list(iterator)
        if kwargs.get('d'):			
            print('Rückgabe einer DatenReihe')				
            return DatenReihe(ll)		
        return list(ll)	
		
    stichProbe = stich_probe		
		
		
    def P(self, *args, **kwargs):
        """Wahrscheinlichkeit eines Ereignisses"""
		
        if mit_param(self):
             print("zufall: nicht implementiert (Parameter)")	
             return
			 
        if kwargs.get('h'):
            print("\nWahrscheinlichkeit eines Ereignisses\n")
            print("Aufruf   nv . P( e )\n")		                     
            print("              nv     Normalverteilung")
            print("              e      Ereignis:")
            print("                     X rel zahl | zahl rel X |")
            print("                     abs( X - zahl ) rel zahl |")
            print("                     'zahl rel X rel zahl'  (string)")
            print("              rel    Relation:  < | <= | > | >=")
            print("              zahl   reelle Zahl\n")	
            print("Der Bezeichner X für die Zufallsgröße ist zwingend\n")			
            print("Zusatz   p=ja   Darstellung als Prozentwert")			
            print("         d=n    Darstellung dezimal mit n Kommastellen")			
            print("         g=ja   grafische Darstellung\n")			
            print("Beispiele")
            print("nv.P(X < 1.8)     nv.P(X >= 3.4)     nv.P( abs(X-3) > 2.5)")
            print("nv.P( '-2 < X <= 2.5' )    ( Z e i c h e n k e t t e )\n")	
            return	
			
        x = kwargs.get('X')
        if len(args) == 0 and is_zahl(x):
            return 0		       			
        if len(args) != 1:
            print('zufall: ein Argument angeben')
            return
        arg = args[0]
        X = Symbol('X')
        if str(arg).find('X') < 0:
            print('zufall: im Ausdruck ist kein X enthalten')
            return	

        F = self.F	
		
        if isinstance(arg, str) or str(arg).upper().find('ABS') >= 0:   # mit abs
            x = Symbol('x', real=True)
            if isinstance(arg, str):
                try:
                    ss = arg.replace('=', '').replace('X', 'x') 
                    k = ss.find('x')
                    li, re = ss[:k+1], ss[k:]
                except:
                    print('zufall: Eingabe überprüfen')	
                    return
                li, re = eval(li), eval(re)
                ll = [li.args[0], li.args[1], re.args[0], re.args[1]]
                ll = [el for el in ll if el is not x]
                if not all(map(lambda x: isinstance(x, (int, Integer, Rational, float, Float)), ll)):
                    print('zufall: diese Zahlen sind nicht erlaubt, dezimal eingeben')
                    return					
                if not (isinstance(li, StrictGreaterThan) and isinstance(re, StrictLessThan)):				
                    print('zufall: Eingabe überprüfen')	
                    return
                li, re = float(li.args[1]), float(re.args[1])
                if li > re:
                    print('zufall: die linke Zahl muss kleiner als die rechte sein')
                    return	
                graf = [li, re, 1]		
                pp = F(re) - F(li)		
			
            else:     # mit abs(...)
                try:
                    a, b = -arg.args[0].args[0].subs(X, 0), arg.args[1]
                    a, b = float(a), float(b)
                    if b < 0:					
                        print('zufall: Ausdruck überprüfen (rechte Seite muß >= 0 sein)')
                        return		
                    g0, g1 = min(a+b, a-b), max(a+b, a-b)					
                    if isinstance(arg, (LessThan, StrictLessThan)):
                        pp = F(g1) - F(g0)			
                        graf = [g0, g1, 1]					
                    else:
                        pp = F(g0) + 1 - F(g1)			
                        graf = [g0, g1, 2]					
                except:
                    print('zufall: Ausdruck überprüfen')
                    return					
                            						
        else:        # X < 3, X > 3, 3 < X, 3 > X
            a = arg.args[1]
            if isinstance(arg, (LessThan, StrictLessThan)):
                graf = [float(a), '-']
            else:				
                graf = [float(a), '+']
            if isinstance(arg, (LessThan, StrictLessThan)):
                pp = F(float(a))
            else:
                pp = 1 - F(float(a))				
                      
        if kwargs.get('g'):
            import matplotlib.pyplot as plt		
            X = expon(loc=0, scale=float(1/self.par))
            fig = plt.figure(figsize=(4, 3))
            ax = fig.add_subplot(1, 1, 1)
            xu, xo = 0, X.ppf(1-1e-5)
            x = np.linspace(xu, xo, 100)
            if len(graf) == 2:
                if graf[1] == '-':
                    zu, zo = xu, graf[0]
                else:
                    zu, zo = graf[0], xo
            else:
                if graf[2] == 1:	
                    zu, zo = graf[0], graf[1]
                else:
                    zu, zo = xu, graf[0]				
                    z = np.linspace(zu, zo, 100)	     		
                    yu, yo = np.zeros(100), X.pdf(z)    			
                    plt.fill_between(z, yu, yo, color='none', edgecolor=(1.0, 0.6, 0.0), \
                                  hatch='xx')
                    zu, zo = graf[1], xo
                z = np.linspace(zu, zo, 100)	     		
                yu, yo = np.zeros(100), X.pdf(z)    					
                plt.fill_between(z, yu, yo, color='none', edgecolor=(1.0, 0.6, 0.0), \
                                  hatch='xx')								  
            if len(graf) == 2:								  
                z = np.linspace(zu, zo, 100)	     		
                yu, yo = np.zeros(100), X.pdf(z)
                plt.fill_between(z, yu, yo, color='none', edgecolor=(1.0, 0.6, 0.0), hatch='xx')
            plt.xlim(xu, xo)		
            plt.ylim(0, 1.1 * float(self.par))
            ax.plot(x, X.pdf(x), color=(0.956893, 0.643101, 0.376507), linewidth=2.5)   # RGB::SandyBrown    
            plt.title(u'\nWahrscheinlichkeit = Inhalt der markierten Fläche\n', fontsize=12, \
                    fontname='Times New Roman', loc='left')
            plt.xlabel('$x$', fontsize=14, alpha=0.9)
            plt.ylabel('$p(x)$', fontsize=12, alpha=0.9)
            plt.show()
            return			

        if kwargs.get('p'):
            return eval(format(float(100*pp), ".2f"))			
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(pp), ".%df" % d))			
        return float(pp)	
		
				
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        exponential_verteilung_hilfe(3)	
		
    h = hilfe							
		
		
				
# Benutzerhilfe für ExponentialVerteilung
# ---------------------------------------

def exponential_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
ExponentialVerteilung - Objekt

Kurzname     EV
		
Erzeugung    ExponentialVerteilung( p )

                 par   Parameter
				 
Zuweisung     ev = EV(...)   (ev - freier Bezeichner)

Beispiel
EV( 2 )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für ExponentialVerteilung 

ev.hilfe               Bezeichner der Eigenschaften und Methoden	
ev.dichte(...)      M  Dichtefunktion	
ev.erw                 Erwartungswert	
ev.erw_(...)        M  ebenso, zugehörige Methode	
ev.F(...)           M  Verteilungsfunktion
ev.formeln             Formeln
ev.graf_D              Graf der Dichtefunktion
ev.graf_F              Graf der Verteilungsfunktion
ev.lamda               = ev.par; Schreibweise!
ev.P(...)           M  Wahrscheinlichkeit eines Ereignisses
ev.par                 Parameter der Verteilung
ev.quantil(...)     M  Quantile
ev.sigma               Standardabweichung
ev.sigma_(...)      M  ebenso, zugehörige Methode
ev.stich_probe(...) M  Stichprobe		
ev.var                 Varianz		
ev.var_(...)        M  ebenso, zugehörige Methode		
ev.versuch             Versuch		

Synonyme Bezeichner

hilfe         h
erw_          Erw
graf_D        grafD
graf_F        grafF
sigma_        Sigma
stich_probe   stichProbe
var_          Var
	   """)		
        return
	
	
EV = ExponentialVerteilung
		


	


