#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  NormalVerteilung - Klasse  von zufall           
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
from scipy.stats import norm
import matplotlib.pyplot as plt

from sympy.core.numbers import Integer, Rational, Float   
from sympy.core.symbol import Symbol
from sympy import sympify
from sympy import sqrt, exp
from sympy.core.relational import (GreaterThan, StrictGreaterThan, LessThan, 
    StrictLessThan)
from sympy.printing.latex import latex

from sympy.stats import Normal, density, P, sample, sample_iter

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.datenreihe import DatenReihe 
from zufall.lib.funktionen.funktionen import is_zahl, mit_param 

from zufall.lib.objekte.ausnahmen import ZufallError
	
	

# NormalVerteilung - Klasse  
# -------------------------
#

class NormalVerteilung(ZufallsObjekt):                                      
    """

Normalverteilung

**Kurzname** **NV**
	
**Erzeugung** 
	
   NV( *mu*, *sigma* )

**Parameter**
 
   *mu* : Erwartungswert

   *sigma* : Standardabweichung   
				 
    """
	
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            normal_verteilung_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 2:
                raise ZufallError("zwei Argumente angeben")
            mu, sigma = args
            mu, sigma = sympify(mu), sympify(sigma)
            if not is_zahl(mu):
                raise ZufallError("der Erwartungswert muß eine Zahl sein")
            if not is_zahl(sigma):
                raise ZufallError("die Standardabweichung muß eine Zahl sein")
        except ZufallError as e:
            print('zufall:', str(e))
            return
        return ZufallsObjekt.__new__(cls, mu, sigma)

			
    def __str__(self):  
        mu, sigma = self.args
        return 'NormalVerteilung\\left(' + latex(mu) + ',\;' + latex(sigma) + '\\right)'	

		
		
# Eigenschaften + Methoden
# ------------------------


    @property
    def erw(self):
        """Erwartungswert"""	
        return self.args[0]	
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
    mu = erw		
		
    @property
    def sigma(self):
        """Standardabweichung"""				
        return self.args[1]
    def sigma_(self, *args, **kwargs):
        """Standardabweichung; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Stellen\n")
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
        return self.sigma**2	
    def var_(self, *args, **kwargs):
        """Varianz; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz   d=n    Darstellung dezimal mit n Stellen\n")
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
        display(Math('\mathrm{Dichtefunktion} \\qquad\\qquad\; p(x) = \\frac{1}{\\sqrt{2 \\pi} \\sigma }' + \
                  'e^{-\\frac{1}{2} \\left(\\frac{x-\\mu}{\\sigma}\\right) ^2}'))
        display(Math('\mathrm{Verteilungsfunktion} \\qquad\; F(x) = P(X \\le x) = \\Phi \\left(\\frac{x-\\mu}' + \
                  '{\\sigma} \\right)' ))
        display(Math('\\qquad\\qquad \mathrm{mit} \;\;\; \\Phi(x) = \\int_{-\\infty}^x \\phi(t)dt, \;\;\; \\phi(t) = \\frac{1}' + \
                   '{\\sqrt{2 \\pi}} e^{-\\frac{t^2}{2}} \\qquad \mathrm{(Funktionen\: der\: (0,1)-Normalverteilung)}'))
        display(Math('\mathrm{Erwartungswert} \\qquad\\quad\; \\mu'))	
        display(Math('\mathrm{Varianz} \\qquad\\qquad\quad \;\;\;\,\, \\sigma'))	
        display(Math('\mathrm{Aktuelle Werte}\;\;\; \\mu = ' + latex(self.mu) + ', \;\;\; \\sigma = ' + latex(self.sigma)))
        print(' ')		
        
    def dichte(self, *args, **kwargs):
        if kwargs.get('h'):
            print("\nDichtefunktion\n")		
            print("Aufruf   nv . dichte( x )")		                     
            print("             nv    Normalverteilung")
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
        X = Normal('X', self.mu, self.sigma)
        wert = density(X)(x)	
        if mit_param(wert):
            return wert		
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(wert), ".%df" % d))			
        return float(wert)       
        

    @property		
    def graf_D(self):
        """Graf der Dichtefunktion"""	
        if mit_param(self):
            print("zufall: nicht verfügbar (Parameter)")
            return
        X = norm(float(self.mu), float(self.sigma))			
        fig = plt.figure(figsize=(4, 4))		
        ax = fig.add_subplot(1, 1, 1)
        xu, xo = X.ppf(1e-5), X.ppf(1-1e-5)
        x = np.linspace(xu, xo, 100)
        plt.xlim(xu, xo)		
        plt.ylim(0, 1.2 * X.pdf(X.mean()))
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
            print("Aufruf   nv . F( x )\n")		                     
            print("             nv    Normalverteilung")
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
        if isinstance(x, (float, Float)):			
            x = Rational(x)			
        X = Normal('X', self.mu, self.sigma)
        wert = P(X < x)		
        if mit_param(wert):
            return wert		
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(wert), ".%df" % d))			
        return float(wert)       
		
    @property		
    def graf_F(self):
        """Graf der Verteilungsfunktion"""	
        if mit_param(self):
            print("zufall: nicht verfügbar (Parameter)")
            return
        X = norm(float(self.mu), float(self.sigma))			
        fig = plt.figure(figsize=(4, 4))		
        ax = fig.add_subplot(1, 1, 1)
        xu, xo = X.ppf(1e-5), X.ppf(1-1e-5)
        x = np.linspace(xu, xo, 100)
        plt.xlim(xu, xo)
        plt.ylim(0, 1.1)
        ax.plot(x, X.cdf(x), color=(0.956893, 0.643101, 0.376507), linewidth=2.5)   # RGB::SandyBrown    
        plt.title('\nVerteilungsfunktion\n', fontsize=14, loc='left', fontname='Times New Roman')
        plt.xlabel('$x$', fontsize=14, alpha=0.9)
        plt.ylabel('$P(X < x)$', fontsize=12, alpha=0.9)		
        ytickspos = []
        i, dy = 1, 0.2
        while True:
            ytickspos += [i*dy]
            i += 1
            if (i-1)*dy > 1.:
                break           
        yticks = [float(format((i+1)*dy, '.1f')) for i in range(len(ytickspos))]
        plt.yticks(ytickspos, [t for t in yticks if t <= 1])  
        for t in ytickspos:
            plt.plot([xu, xo], [t, t], color=(0.3,0.3,0.3), linewidth=0.3)		
        plt.show()		

    grafF = graf_F
		
    def quantil(self, *args, **kwargs):
        """Quantile"""	
        if kwargs.get('h'):
            print("\nQuantile\n")		
            print("Aufruf   nv . quantil( q )\n")		                     
            print("             nv    Normalverteilung")
            print("             q     Zahl aus [0,1]\n")
            print("Zusatz   d=n   Ausgabe mit n Kommastellen\n")			
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
        X = norm(float(self.mu), float(self.sigma))
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
        X = Normal('X', self.mu, self.sigma)	
        return sample(X)		
		
    def stich_probe(self, *args, **kwargs):
        """Stichprobe"""
        if kwargs.get('h'):
            print("\nStichprobe\n")		
            print("Aufruf   nv . stichprobe( m )\n")		                     
            print("              nv   Normalverteilung")
            print("              m    Umfang (Anzahl Versuche)\n")
            print("Zusatz   d=ja   Rückgabe als DatenReihe")
            print("         s=ja   Übergang zu SciPy (schnelle Berechnung)\n")
            return 
        if len(args) != 1:
            print('zufall: einen Wert angeben')
            return
        m = sympify(args[0])
        if not isinstance(m, (int, Integer)) and m > 0:			
            print('zufall: ganze Zahl > 0 angeben')
            return
        s = kwargs.get('s')
        if s == True:	
            if mit_param(self):
                print('zufall: Übergang zu SciPy nicht möglich (Parameter)')
                return				
            X = norm(float(self.mu), float(self.sigma))
            ll = X.rvs(size=m)
        else:
            X = Normal('X', self.mu, self.sigma)	
            iterator = sample_iter(X, numsamples=m)    # relativ langsam
            ll = list(iterator)
        ll = [float(x) for x in ll]		
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
                if not all(map(lambda x: isinstance(x, (int, Integer, 
                   Rational, float, Float)), ll)):
                    print('zufall: diese Zahlen sind nicht erlaubt, ' + \
					       'dezimal eingeben')
                    return					
                if not (isinstance(li, StrictGreaterThan) and 
                   isinstance(re, StrictLessThan)):				
                    print('zufall: Eingabe überprüfen')	
                    return
                li, re = float(li.args[1]), float(re.args[1])
                if li > re:
                    print('zufall: die linke Zahl muss kleiner als die ' + \
                          'rechte sein')
                    return	
                graf = [li, re, 1]		
                pp = F(re) - F(li)		
			
            else:     # mit abs(...)
                try:
                    a, b = -arg.args[0].args[0].subs(X, 0), arg.args[1]
                    a, b = float(a), float(b)
                    if b < 0:					
                        print('zufall: Ausdruck überprüfen (rechte ' + \
                             'Seite muß >= 0 sein)')
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
            X = norm(float(self.mu), float(self.sigma))
            fig = plt.figure(figsize=(4, 3))
            ax = fig.add_subplot(1, 1, 1)
            xu, xo = X.ppf(1e-5), X.ppf(1-1e-5)
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
                    plt.fill_between(z, yu, yo, color='none', 
                                  edgecolor=(1.0, 0.6, 0.0), 
                                  hatch='xx')
                    zu, zo = graf[1], xo
                z = np.linspace(zu, zo, 100)	     		
                yu, yo = np.zeros(100), X.pdf(z)    					
                plt.fill_between(z, yu, yo, color='none', 
                                  edgecolor=(1.0, 0.6, 0.0), 
                                  hatch='xx')								  
            if len(graf) == 2:								  
                z = np.linspace(zu, zo, 100)	     		
                yu, yo = np.zeros(100), X.pdf(z)
                plt.fill_between(z, yu, yo, color='none', 
                              edgecolor=(1.0, 0.6, 0.0), hatch='xx')
            plt.xlim(xu, xo)		
            plt.ylim(0, 1.2 * X.pdf(X.mean()))
            ax.plot(x, X.pdf(x), color=(0.956893, 0.643101, 0.376507), 
                   linewidth=2.5)   # RGB::SandyBrown    
            plt.title(u'\nWahrscheinlichkeit = Inhalt der markierten Fläche\n', 
                    fontsize=12, 
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
        return pp	
		

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        normal_verteilung_hilfe(3)	
		
    h = hilfe					
		
		
				
# Benutzerhilfe für NormalVerteilung
# ----------------------------------

def normal_verteilung_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
NormalVerteilung - Objekt

Kurzname     NV
		
Erzeugung    NormalVerteilung( mu, sigma )

                 mu       Erwartungswert
                 sigma    Standardabweichung
				 
Zuweisung     nv = NV(...)   (nv - freier Bezeichner)

Beispiel
NV( 3, 2 )
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für NormalVerteilung
 
nv.hilfe               Bezeichner der Eigenschaften und Methoden
nv.dichte(...)      M  Dichtefunktion	
nv.erw                 Erwartungswert	
nv.erw_(...)        M  ebenso, zugehörige Methode	
nv.F(...)           M  Verteilungsfunktion
nv.formeln             Formeln
nv.graf_D              Graf der Dichtefunktion
nv.graf_F              Graf der Verteilungsfunktion
nv.P(...)           M  Wahrscheinlichkeit eines Ereignisses
nv.quantil(...)     M  Quantile
nv.sigma               Standardabweichung
nv.sigma_(...)      M  ebenso, zugehörige Methode
nv.stich_probe(...) M  Stichprobe		
nv.var                 Varianz		
nv.var_(...)        M  ebenso, zugehörige Methode		
nv.versuch             Versuch	

Synonyme Bezeichner

hilfe        h
erw          mu
erw_         Erw	
graf_F       grafF
graf_D       grafD
sigma_       Sigma
stich_probe  stichProbe
var_         Var
	   """)		
        return
	
	
NV = NormalVerteilung
		


	


