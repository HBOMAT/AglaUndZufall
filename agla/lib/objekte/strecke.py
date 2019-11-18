#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Strecke - Klasse  von agla           
#  
                                               
#
# This file is part of agla
#
#
# Copyright (c) 2019 Holger Böttcher  hbomat@posteo.de
#
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License
# You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#  



import importlib

import numpy as np
from agla.lib.objekte.umgebung import UMG	
if UMG.grafik_3d == 'mayavi':
    from mayavi import mlab
else:
    from vispy import scene
import matplotlib.pyplot as plt

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.abc import t
from sympy.simplify.simplify import nsimplify, simplify
from sympy.core.symbol import Symbol, symbols
from sympy import Max, N, Interval
from sympy.core.numbers import Integer, Rational, Float

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, loese, 
    wert_ausgabe, identisch)
from agla.lib.funktionen.graf_funktionen import _funkt_sympy2numpy
from agla.lib.objekte.ausnahmen import AglaError
import agla



# Strecke - Klasse 
# ----------------  
	
class Strecke(AglaObjekt):                                      
    """Strecke im Raum und in der Ebene
		
**Erzeugung** 
	
   Strecke ( *punkt1, punkt2*)

**Parameter**

   *punkt* : Punkt; Angabe von Anfangs- und Endpunkt
      
    """
		
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            strecke_hilfe(kwargs["h"])		
            return	
			
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        try:		
            if len(args) != 2:
                raise AglaError("Anfangs- und Endpunkt angeben")
            anf, end = args
            if not (isinstance(anf, Vektor) and (anf.dim == 3 or 
			     anf.dim == 2) and 
		            isinstance(end, Vektor) and end.dim == anf.dim):
                raise AglaError("Anfangs- und Endpunkt angeben")
            if end == anf:
                raise AglaError("die Punkte müssen verschieden sein")
        except AglaError as e:
            print('agla:', str(e))
            return			
        return AglaObjekt.__new__(cls, anf, end)
        
   
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Streckenschar(" + ss + ")"
        return "Strecke"			

		
# Für Strecken in R^3 und R^2 gemeinsame Eigenschaften + Methoden
# ---------------------------------------------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return self.args[0].dim
		
    @property
    def anf(self):
        """Anfangspunkt"""
        return self.args[0]
		
    @property
    def end(self):
        """Endpunkt"""
        return self.args[1]
		
    @property
    def punkte(self):
        """Endpunkte"""
        return self.args[0], self.args[1]
		
    @property
    def mitte(self):              
        """Mittelpunkt"""
        return (self.args[0] + self.args[1]) * Rational(1, 2)
    
    @property	
    def gerade(self):              
        """Trägergerade"""
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        return Gerade(self.anf, Vektor(self.anf, self.end))   

    @property			
    def laenge(self):              
        """Länge"""
        return self.punkte[0].abstand(self.punkte[1])
    def laenge_(self, **kwargs):
        """Länge; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        ll = self.laenge
        d = kwargs.get('d')
        ll = self.laenge
        d = kwargs.get('d')
        return wert_ausgabe(ll, d)

    Laenge = laenge_	
		
    @property			
    def sch_par(self):              
        """Scharparameter"""
        return self.args[0].free_symbols.union(self.args[1].free_symbols)
	
    schPar = sch_par
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1

    isSchar = is_schar
	
    @property
    def in_figur(self):
        """Konvertierung in Figur; nur in der Ebene"""
        if self.dim != 2:
            print("agla: nur in der Ebene R^2 verfügbar")		
            return		
        ecken, kanten  = [self.punkte[0], self.punkte[1]], [[0, 1]]
        Figur = importlib.import_module('agla.lib.objekte.figur').Figur	
        return Figur(ecken, kanten)
	
    inFigur = in_figur		
		
    @property
    def in_koerper(self):
        """Konvertierung in Körper; nur im Raum"""
        if self.dim != 3:
            print("agla: nur im Raum R^3 verfügbar")		
            return		
        ecken, kanten  = [self.punkte[0], self.punkte[1]], [[0, 1]]
        Koerper = importlib.import_module('agla.lib.objekte.koerper').Koerper	
        return Koerper(ecken, kanten)
				
    inKoerper = in_koerper
	
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Streckenschar\n")		
            print("Aufruf   strecke . sch_el( wert )\n")		                     
            print("             strecke    Strecke")
            print("             wert       Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if not wert or len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien ' + \
			       'Parameter angeben')	
            return
        try:			
            wert = nsimplify(wert)
        except RecursionError:	
            pass					
        anf, end = self.punkte
        if anf.has(p):
            anf = anf.sch_el(wert)
        if end.has(p):
            end = end.sch_el(wert)
        return Strecke(anf, end)		

    schEl = sch_el
	
		
    def pkt(self, *wert, **kwargs):
        """Streckenpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt der Strecke\n")		
            print("Aufruf   strecke . pkt( wert )\n")		                     
            print("             strecke   Strecke")
            print("             wert      Wert des Streckenparameters\n")
            print("Rückgabe     bei Angabe eines Parameterwertes aus [0, 1]:")
            print("             Streckenpunkt, der zu diesem Wert gehört")
            print("             bei leerer Argumentliste oder freiem " + \
			       "Bezeichner:")
            print("             allgemeiner Punkt der Strecke\n")
            return
				
        g = self.gerade	
        try:
            if not wert:
                return g.pkt()
            elif isinstance(wert[0], Symbol):
                return g.pkt(wert[0])
            elif len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    raise AglaError('Zahlenwert angeben')				
                if not (0 <= pw <= 1):
                    raise AglaError("Wert aus [0, 1] angeben")
                return g.pkt(pw)			 
            raise AglaError("Parameterwert angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			
	
	
    def teil_punkt(self, *teil_verh, **kwargs):	
        """Teilpunkt"""
		
        if kwargs.get('h'):
            print("\nTeilpunkt der Strecke\n")		
            print("Aufruf   strecke . teil_punkt( k )\n")		                     
            print("             strecke   Strecke")
            print("             k         Teilverhältnis\n")
            return
				
        try:				
            if len(teil_verh) != 1:
                raise AglaError("Teilverhältnis angeben")
            try:				
                tv = nsimplify(sympify(teil_verh[0]))
            except RecursionError:	
                tv = sympify(teil_verh[0])
            if not is_zahl(tv):
                raise AglaError("Zahlenwert angeben")
            if tv == -1:
                raise AglaError("das Teilverhältnis kann nicht -1 sein")	
        except AglaError as e:
            print('agla:', str(e))
            return			
        a, b = self.punkte
        return (a + b * tv) * 1/(1+tv) 
        		
    teilPunkt = teil_punkt
	
				
    def teil_verh(self, *punkt, **kwargs):	
        """Teilverhältnis"""
		
        if kwargs.get('h'):
            print("\nTeilverhältnis der Strecke\n")		
            print("Aufruf   strecke . teil_verh( punkt )\n")		                     
            print("             strecke   Strecke")
            print("             punkt     Punkt der Trägergeraden\n")
            return
		
        try:	
            if len(punkt) != 1:
                raise AglaError("einen Punkt angeben")
            Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
            punkt = punkt[0]
            if (not isinstance(punkt, Vektor) or isinstance(punkt, Vektor) 
		         and punkt.dim != self.punkte[0].dim):
                raise AglaError("einen Punkt der Trägergeraden angeben")
            if punkt == self.punkte[1]:
                raise AglaError('das Teilverhältnis ist für diesen Punkt ' + \
				        'nicht definiert') 
            t = Symbol('t')						
            L = loese(punkt - self.gerade.pkt(t), [t])
            if not L:			
                raise AglaError("einen Punkt der Trägergeraden angeben")
            p, q = punkt.abstand(self.punkte[0]), punkt.abstand(self.punkte[1])            				
            return simplify(p / q)		
        except AglaError as e:
            print('agla:', str(e))
            return
			
    teilVerh = teil_verh
	
		
    def schnitt(self, *objekt, **kwargs):
        """"Schnitt mit anderen Objekten"""
				
        if kwargs.get('h'):
            print("\nSchnitt der Strecke mit einem anderen Objekt\n")		
            print("Aufruf   strecke . schnitt( objekt )\n")		                     
            print("             strecke   Strecke")
            print("             objekt    Punkt, Gerade, Ebene, Strecke  " + \
                 "(im Raum R^3)")		
            print("                       Punkt, Gerade, Strecke  "
                 "(in der Ebene R^2)\n")	
            print("Zusatz       l=1   Lageinformationen\n")
            return
	
        try:	
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")
            objekt = objekt[0]	
            Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            if not type(objekt) in [Vektor, Gerade, Ebene, Strecke]:
                raise AglaError("Punkt, Gerade, Ebene oder Strecke angeben")
            if mit_param(self) or mit_param(objekt):
                raise AglaError('nicht implementiert (Parameter)')
            if objekt.dim != self.dim or not objekt.dim in [2, 3]:
                raise AglaError("Objekt mit der passenden Dimension angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			
        p1, p2 = self.punkte
        ll = self.laenge
        if isinstance(objekt, Vektor):
            if N(objekt.abstand(self.gerade)) > 0:
                if kwargs.get('l'):
                    display(Math('\\text{der Punkt liegt nicht auf ' + \
					   'der Strecke}'))
                    return					
                return set()
            if objekt.abstand(p1) <= ll and objekt.abstand(p2) <= ll:
                if kwargs.get('l'):
                    display(Math('\\text{der Punkt liegt auf der Strecke}'))
                    return				
                return objekt
            else:
                if kwargs.get('l'):
                    display(Math('\\text{der Punkt liegt nicht auf ' + \
					   'der Strecke}'))
                    return				
                return set()
				
        elif (isinstance(objekt, Gerade) 
		     or self.dim == 3 and isinstance(objekt, Ebene)):
            if isinstance(objekt, Gerade):
                objtext = 'Gerade'
            else:
                objtext = 'Ebene'			 
            if p1.abstand(objekt) == 0 and p2.abstand(objekt) == 0:
                if kwargs.get('l'):
                    if isinstance(objekt, Gerade):
                        display(Math('\\text{die Strecke liegt auf der ' + \
						    'Geraden}'))
                    else:
                        display(Math('\\text{die Strecke liegt\ in der ' + \
						    'Ebene}]'))
                    return
                return self
            s = objekt.schnitt(self.gerade)
            if not s:
                if kwargs.get('l'):
                    display(Math('\\text{die Streck schneidet die }' + \
                    objtext + '\\text{ nicht}'))
                    return				
                return set()
            if s.abstand(p1) <= ll and s.abstand(p2) <= ll:
                if kwargs.get('l'):
                    display(Math('\\text{die Strecke schneidet die\ }' + \
					   objtext + '\\text{ im Punkt}'))
                    s.punkt_ausg					
                    return				
                return s
            else:
                if kwargs.get('l'):
                    display(Math('\\text{die Strecke schneidet die }' + \
					   objtext + '\\text{ nicht }'))
                    return				
                return set()
				
        elif isinstance(objekt, Strecke): 
            if objekt == self:
                if kwargs.get('l'):			
                    display(Math('\\text{die Strecken sind ' + \
						        'identisch}'))
                    return
                return self
            q1, q2 = objekt.punkte
            g1, g2 = self.gerade, objekt.gerade
            s, t = symbols('s t')			
            if not identisch(g1, g2):
                if not g1.schnitt(g2):
                    if kwargs.get('l'):
                        display(Math('\\text{die Strecken schneiden ' + \
						    'sich nicht}'))
                        return
                    return set() 	
                else:
                    ss = g1.schnitt(g2)
                    L = loese(g1.pkt(s) - ss)
                    ss1 = L[s]            			
                    L = loese(g2.pkt(s) - ss)
                    ss2 = L[s]            								
                    if (ss1 >= 0 and ss1 <= 1) and (ss2 >= 0 and ss2 <= 1):				
                        if kwargs.get('l'):
                            display(Math('\\text{die Strecken schneiden ' + \
						        'sich in einem Punkt}'))
                            return
                        return ss
                    if kwargs.get('l'):
                            display(Math('\\text{die Strecken schneiden ' + \
						        'sich nicht}'))
                            return
                    return set()
            g = g1					
            s1 = 0            			
            s2 = 1            			
            L = loese(g.pkt(t) - q1) 
            t1 = L[t]           			
            L = loese(g.pkt(t) - q2) 
            t2 = L[t]  
            t1, t2 = sorted([t1, t2])
            s1, s2 = sorted([s1, s2])
            int1, int2 = Interval(s1, s2), Interval(t1, t2)				
            if t1 == s2:
                anf, txt = s2, 'punkt'
            elif t2 == s1:
                anf, txt = s1, 'punkt'
            elif not int1.intersection(int2):
               txt = 'kein'
            elif t1 < s1 and t2 > s2:
                 anf, end, txt = s1, s2, 'strecke'			
            elif s1 < t1 and s2 > t2:
                 anf, end, txt = t1, t2, 'strecke'			
            else:			   
                if t1 in int1 and t2 in int1:
                    anf, end, txt = t1, t2, 'strecke'
                elif t1 in int1 and t2 not in int1:
                    anf, end, txt = t1, s2, 'strecke'
                elif t1 not in int1 and t2 in int1:
                    anf, end, txt = s1, t2, 'strecke'				
                elif s1 in int2 and s2 in int2:
                    anf, end, txt = s1, s2, 'strecke'					
                elif s1 in int2 and s2 not in int2:
                    anf, end, txt = s1, t2, 'strecke'
                elif s1 not in int2 and s2 in int2:
                    anf, end, txt = st, s2, 'strecke'								
            if kwargs.get('l'):
                if txt == 'kein':
                    display(Math('\\text{die Strecken schneiden ' + \
                                 'sich nicht}'))
                elif txt == 'punkt':
                    display(Math('\\text{die Strecken haben einen ' + \
                                 'gemeinsamen Endpunkt}'))
                elif txt == 'strecke':
                    display(Math('\\text{die Strecken haben eine ' + \
                                 'gemeinsame Teilstrecke}'))
                return
            if txt == 'kein':
                return set()
            elif txt == 'punkt': 
                return g.pkt(anf)			
            elif txt == 'strecke':			
                 return Strecke(g.pkt(anf), g.pkt(end))			
						
			
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Strecke bei einer Abbildung\n")		
            print("Aufruf   strecke . bild( abb )\n")		                     
            print("             strecke    Strecke")
            print("             abb        Abbildung\n")			
            return 				
			
        if len(abb) != 1:
             print("agla: eine Abbildung angeben")
             return			 
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == self.dim):
            print("agla: eine Abbildung (mit gleicher Dimension) angeben")
            return
        m = abb.matrix
        if m.det != 0:
            p, q = self.punkte
            p1, q1 = p.bild(abb), q.bild(abb)
            return Strecke(p1, q1)
        else:
            k = self.in_koerper
            return k.bild(abb)

						
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Strecke"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Strecke in R^3 mit mayavi"""	
					
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' \
		              else spez[2][1]

        anim = False	
        if self.is_schar:
            anim = True            
            aber = spez[3]			

        a, b = self.punkte	
        if not anim:			
            x = [float(a.x), float(b.x)]		
            y = [float(a.y), float(b.y)]		
            z = [float(a.z), float(b.z)]	
            return mlab.plot3d(x, y, z, line_width=lin_staerke, 
			                    color=lin_farbe, tube_radius=None)	
        else:			
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20		
            b_, t = symbols('b_ t')					
            ss = self.sch_el(b_)	
            xx, yy, zz = ss.pkt(t).komp
            xs, ys, zs = repr(xx), repr(yy), repr(zz)
            from numpy import sin, cos, tan, abs, log, arcsin, arccos, arctan, \
               sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, exp, pi
            tab = _funkt_sympy2numpy 			   
            for tt in tab:                			
                if tt in xs:			
                    xs = xs.replace(tt, tab[tt]) 
                if tt in ys:			
                    ys = ys.replace(tt, tab[tt]) 
                if tt in zs:			
                    zs = zs.replace(tt, tab[tt]) 
            xa, ya, za = [], [], []            
            aa = np.linspace(float(aber[0]), float(aber[1]), N) 
            typ = (int, Integer, float, Float)			            			
            for bb in aa:
                bb = '(' + str(bb) + ')'
                sx = eval(xs.replace('b_', bb))
                sy = eval(ys.replace('b_', bb))
                sz = eval(zs.replace('b_', bb))
                if isinstance(sx, typ):
                   xa += [[float(sx), float(sx)]]
                else:				   
                   xa += [[float(sx.subs(t, 0)), float(sx.subs(t, 1))]]
                if isinstance(sy, typ):
                    ya += [[float(sy), float(sy)]]
                else:					
                    ya += [[float(sy.subs(t, 0)), float(sy.subs(t, 1))]]
                if isinstance(sz, typ):
                    za += [[float(sz), float(sz)]]
                else:					
                    za += [[float(sz.subs(t, 0)), float(sz.subs(t, 1))]]
            plt = mlab.plot3d(xa[0], ya[0], za[0], line_width=lin_staerke, 
                     color=lin_farbe, tube_radius=None) 						
            return plt, (xa[1:], ya[1:], za[1:]), N-1		
	
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Strecke in R^3 mit vispy"""

        pass		
		
	
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Strecke in R^2"""	
			
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' \
                     else spez[2][3]
		
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:			
            p, q = self.punkte
            x, y = [float(p.x), float(q.x)], [float(p.y), float(q.y)]
            return plt.plot(x, y, linewidth=lin_staerke, color=lin_farbe)      
	
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        strecke_hilfe(3)	
		
    h = hilfe					

	
	
# Benutzerhilfe für Strecke
# --------------------------

def strecke_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nStrecke - Objekt\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")
        print("             Strecke( anf, end )\n")
        print("                 anf   Anfangspunkt")
        print("                 end   Endpunkt\n")
        print("Zuweisung     s = Strecke(...)   (s - freier Bezeichner)\n")
        print("Beispiel")
        print("Strecke(v(1, 2, 3), v(4, 5, 6))\n")
        return
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Strecke\n")
        print("s.hilfe               Bezeichner der Eigenschaften und Methoden")
        print("s.anf                 Anfangspunkt")
        print("s.bild(...)        M  Bild bei einer Abbildung")
        print("s.dim                 Dimension")
        print("s.end                 Endpunkt")
        print("s.gerade              Trägergerade")
        print("s.in_figur            Konvertierung in Figur  (in der Ebene R^2)")
        print("s.in_körper           Konvertierung in Körper  (im Raum R^3)")
        print("s.is_schar            Test auf Schar")
        print("s.länge               Länge")
        print("s.länge_(...)      M  ebenso, zugehörige Methode")
        print("s.mitte               Mittelpunkt")
        print("s.pkt(...)         M  Streckenpunkt")
        print("s.punkte              Endpunkte")
        print("s.sch_el(...)      M  Element einer Schar")
        print("s.sch_par             Parameter einer Schar")
        print("s.schnitt(...)     M  Schnittmenge mit anderen Objekten")
        print("s.teil_punkt(...)  M  Teilpunkt")
        print("s.teil_verh(...)   M  Teilverhältnis\n")
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("in_figur   :  inFigur")
        print("in_körper  :  inKörper")
        print("is_schar   :  isSchar")
        print("länge_     :  Länge")
        print("sch_el     :  schEl")
        print("sch_par    :  schPar")
        print("teil_punkt :  teilPunkt")	
        print("teil_verh  :  teilVerh\n")
        return
   
		