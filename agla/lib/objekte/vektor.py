#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Vektor - Klasse  von agla           
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
    from vispy import app, scene
import matplotlib.pyplot as plt

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.function import expand
from sympy.core.evalf import N
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.containers import Tuple
from sympy.matrices import Matrix as SympyMatrix
from sympy.simplify import simplify, nsimplify
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.numbers import Integer, Float
from sympy.core.symbol import symbols, Symbol
from sympy.printing.latex import latex
            
from agla.lib.objekte.basis import AglaObjekt
from agla.lib.funktionen.funktionen import (cos, cosg, acosg, is_zahl, 
     wert_ausgabe, mit_param, einfach)								
from agla.lib.funktionen.graf_funktionen import _arrow, _arrow2, \
    _funkt_sympy2numpy
from agla.lib.objekte.ausnahmen import AglaError
import agla


	
# Vektor - Klasse	
# ---------------
	       
class Vektor(AglaObjekt):             
    """
	
Vektor im *n*-dimensionalen Euklidischen Raum 

**Synonym**

   **Punkt** (Punkte werden mit ihren Ortsvektoren identifiziert)

**Kurzform**

   **v** (reservierter Bezeichner)

**Erzeugung** 
	
  Vektor ( *komponente1, komponente2, ...* ) *oder*

   v ( *komponente1, komponente2, ...* ) *bzw.*
   
   Vektor ( *vektor1, vektor2* ) *oder*
   
   v ( *vektor1, vektor2* )    

       Bei Angabe von zwei Vektoren wird der Differenzvektor erzeugt
   
**Parameter**

   *komponente* : nummerischer Ausdruck
		
   *vektor* : Vektor
   				
   ``float``- und ``Float``-Komponenten werden standardmäßig in rationale  
   Zahlen umgewandelt. Die Umwandlung entfällt bei Angabe von `simpl=nein` 
   als letztem Argument. Ebenso wird nicht konvertiert, wenn mit der  
   Anweisung ``UMG.SIMPL = nein`` die Umgebungsvariable ``UMG.SIMPL`` 
   global eingestellt wurde

|
 
**Operatoren**

   +--------+-----------------------------------------------+   
   | ``+``  | Addition von zwei Vektoren                    |
   +--------+-----------------------------------------------+   
   | ``-``  | Negation / Subtraktion von Vektoren           |
   +--------+-----------------------------------------------+   
   | ``*``  | Multiplikation eines Vektors mit einem Skalar |
   +--------+-----------------------------------------------+   
   | ``/``  | Division eines Vektors durch einen Skalar     |
   +--------+-----------------------------------------------+   
   | ``*``  | Skalarprodukt von zwei Vektoren               |
   +--------+-----------------------------------------------+   
   | ``°``  | ebenso                                        |
   +--------+-----------------------------------------------+   
   | ``><`` | Vektorprodukt von zwei Vektoren (nur im Raum) |
   +--------+-----------------------------------------------+   
   | ``|``  | Verketten von zwei Vektoren                   |
   +--------+-----------------------------------------------+   
    
|
	
**Vordefinierte Vektoren** im Raum und in der Ebene
   
   ``O``  :  Nullvektor/Ursprung im Raum  

   ``O2`` :  Nullvektor/Ursprung in der Ebene 
 
   ``X``  :  Allgemeiner Vektor/Punkt im Raum  

   ``X2`` :  Allgemeiner Vektor/Punkt in der Ebene  
	
|
	
	"""
	
    printmethod = '_latex'
    
    def __new__(cls, *args, **kwargs):        
		
        h = kwargs.get('h')
        if h in (1, 2, 3, 4):   
            vektor_hilfe(h)		
            return	
        if kwargs.get('simpl') == False:
            simpl = False
        else:	
            simpl = UMG.SIMPL
			
        try:
            if not args:
                raise AglaError('mindestens 2 Komponenten angeben')                
            if isinstance(args[0], (tuple, Tuple, list)):
                komp = Tuple(*args[0])
            elif isinstance(args[0], Vektor):
                if len(args) == 1:
                    return args[0]
                elif isinstance(args[1], Vektor) and len(args) == 2:
                    vv = Vektor([args[1].args[i] - args[0].args[i] \
                                   for i in range(len(args[1].args))])								   
                    return vv
                else:
                    raise AglaError('hier sind nur ein oder zwei Vektoren möglich')                			
                komp = args[0].args
            else:
                komp = Tuple(*args)

            if len(komp) < 2:
                txt = "ein Vektor muss mindestens zwei Komponenten haben"
                raise AglaError(txt)                			
            komp1 = []			
            for c in komp:
                if not is_zahl(c):
                    raise AglaError('die Komponenten müssen Zahlen sein')
                komma = True if str(c).find('.') >= 0 else False					
                if not mit_param(c) and komma and simpl:
                    try:
                        cc = nsimplify(simplify(c))
                        if abs(N(c) - N(cc)) > 1e-8:   # wegen Unsicherheit
                            raise RecursionError       # von nsimplify 						
                        komp1 += [cc]
                    except (RecursionError, TypeError):
                        komp1 += [simplify(c)] 					
                else:					
                    komp1 += [c]
		
            return AglaObjekt.__new__(cls, *komp1)
		
        except AglaError as e:
            print('agla:', str(e))
            return			
					
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            return "Vektorschar(" + str([el for el in par]) + ")"
        return "Vektor"			
		
    def _latex(self, printer):	
        lat = latex(self.vektor2sympy)
        lat = lat.replace('[', '(').replace(']', ')')		
        return lat

    def __hash__(self):
        return super(Vektor, self).__hash__()	

		
		

# Eigenschaften
# -------------

    @property                      
    def vektor2sympy(self):                          
        """Konvertierung in eine Sympy-Matrix"""
        spalte = [ [k] for k in self.komp ] 
        return SympyMatrix(spalte)

    @property                      
    def dim(self):
        """Anzahl der Komponenten (Dimension) des Vektors"""
        return len(self.args)	

    @property
    def x(self):
        """Erste Komponente des Vektors (Dimension 2 oder 3)"""
        try:
            if self.dim <= 3:
                return self.args[0]
            raise AglaError('der Vektor muss 2 oder 3 Komponenten haben')	
        except AglaError as e:
            print('agla:', str(e))
		
    @property
    def y(self):
        """Zweite  Komponente des Vektors (Dimension 2 oder 3)"""
        try:
            if self.dim <= 3:
                return self.args[1]
            raise AglaError('der Vektor muss 2 oder 3 Komponenten haben')
        except AglaError as e:			
            print('agla:', str(e))

    @property
    def z(self):
        """Dritte Komponente des Vektors (Dimension 3)"""
        try:
            if self.dim == 3:
                return self.args[2]
            raise AglaError('nur für Vektoren im Raum R^3 definiert')
        except AglaError as e:
            print('agla:', str(e))		
			
    @property
    def komp(self):
        """Komponenten des Vektors / Koordinaten des Punktes"""
        return self.args

    @property
    def koord(self):
        """Koordinaten des Punktes, der dem Vektor entspricht"""
        return self.komp

    @property
    def O(self): 
        """Nullvektor in der Dimension des Vektors"""		 
        return Vektor([0] * self.dim)

    @property
    def betrag(self):
        """Betrag des Vektors"""
        return sqrt(self * self)	
    def betrag_(self, **kwargs):
        """Betrag des Vektors; Dezimaldarstellung"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        b = self.betrag
        d = kwargs.get('d')
        return wert_ausgabe(b, d)
		
    Betrag = betrag_		
    laenge = betrag		
    laenge_ = betrag_		
    Laenge = betrag_		
		
    @property
    def einh_vekt(self):
        """Einheitsvektor in Richtung des Vektors"""
        ev = self / self.betrag
        ev = Vektor(ev.komp, simpl=False)
        return ev
		
    einhVekt = einh_vekt
	
    @property
    def dez(self):                                    
        """Dezimaldarstellung"""
        li = [N(k) for k in self.komp]
        return Vektor(*li, simpl=False)
    def dez_(self, *n, **kwargs):                                
        """Dezimaldarstellung"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Stellen\n')
            return 		
        d = kwargs.get('d')
        li = []
        for k in self.komp:
            if d:
                li.append(N(k, d))
            else:
                li.append(N(k))
        return Vektor(*li, simpl=False)
		
    Dez = dez_		
		
    @property
    def zeil(self):                           
        """Zeilenvektor """
        komp = []
        for i in range(self.dim):
            komp += [self.komp[i]]        
        return _ZeilenVektor(*komp)
		
    T = zeil		
	 
    @property
    def d(self):                           
        """Ableitungsvektor für eine Variable"""
        try:
            par = self.free_symbols
            if len(par) > 1:
                txt = "mehr als eine Variable, diff-Methode benutzen"
                raise AglaError(txt)
            elif len(par) > 0:
                x = list(par)[0]
                return Vektor([k.diff(x) for k in self.komp])
            else:
                return self.O
        except AglaError  as e:
            print('agla:', str(e))		
			
    @property						
    def einfach(self):
        """Vereinfachung des Vektors"""
        li = [einfach(k) for k in self.komp]
        return Vektor(li)

    @property
    def punkt_ausg(self):
        """Ausgabe als Punkt"""
        if self.dim <= 3:
            if self.dim == 2:
                return display(Math(latex(('\\left( \,' + latex(self.x) + 
				         '\, | \,' + latex(self.y) + '\, \\right)'))))
            else:
                return display(Math('\\left(\,' + latex(self.x) + '\\left|\,' + 
                      latex(self.y) + '\, \\right|' +
                      latex(self.z) + '\,' + '\\right)'))						   
        else:
            print('agla: nicht implementiert')
            return			

    def punkt_ausg_(self, **kwargs):
        """Ausgabe als Punkt; zugehörige Methode; intern
        bei s=1 wird der latex-string zurückgegeben		
         """
        if self.dim <= 3:
            if self.dim == 2:
                if kwargs.get('s'):		
                    return latex(('\\left( \,' + latex(self.x) + '\, | \,' 
				         + latex(self.y) + '\, \\right)'))                
                return self.punkt_ausg
            else:
                if kwargs.get('s'):		
                    return '\\left(\,' + latex(self.x) + '\\left|\,' + \
                          latex(self.y) + '\, \\right|' + \
                          latex(self.z) + '\,' + '\\right)'						   
                return self.punkt_ausg
        else:
            print('agla: nicht implementiert')
            return			
		
    punktAusg = punkt_ausg
	
    @property
    def is_schar(self):                                       
        """Test auf eine Schar von Vektoren mit einem Parameter"""	      
        return len(self.sch_par) == 1  

    isSchar = is_schar		
				
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return self.free_symbols

    schPar = sch_par		
		
		
# Methoden
# --------

    def abstand(self, *other, **kwargs):
        """Abstand des Punktes zu einem anderen Objekt"""
		
        if kwargs.get('h'):
            print("\nAbstand des Punktes zu einem anderen Objekt\n")		
            print("Aufruf   punkt . abstand( objekt )\n")		
            print("             punkt    Punkt")
            print("             objekt   Punkt, Gerade, Ebene, Kugel (im Raum R^3)")
            print("                      Punkt, Gerade (in der Ebene R^2)")
            print("                      Punkt (Dimension > 3)\n")
            print("Rückgabe 0, wenn punkt in objekt enthalten bzw. identisch ist\n")
            print("Zusatz       d=n   Dezimaldarstellung")
            print("                   n - Anzahl der Nachkomma-/Stellen\n")
            return 

        try:			
            if not other:
                raise AglaError('Punkt, Gerade, Ebene oder Kugel angeben')
            if len(other) != 1:
                raise AglaError('nur ein anderes Objekt angeben')
            other = other[0]  
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
            if other.dim == 3:				
                if not isinstance(other, (Vektor, Gerade, Ebene, Kugel)):       
                    raise AglaError('Punkt, Gerade, Ebene oder Kugel angeben')
            elif other.dim == 2:					
                if not isinstance(other, (Vektor, Gerade)):       
                    raise AglaError('Punkt oder Gerade angeben')
            else:					
                if not isinstance(other, Vektor):       
                    raise AglaError('Punkt angeben')
					
            if isinstance(other, Vektor):
                if self.dim == other.dim:
                    wert = sqrt(expand(sum([(x-y)**2 
				                 for x, y in zip(self.komp, other.komp)]))) 
                    d = kwargs.get('d')							 
                    if not isinstance(d, (Integer, int)):
                        return wert
                    if d <= 0:
                        return wert					
                    if mit_param(wert):
                        if d:
                            return N(wert, d)
                        else:							
                            return wert
                    if kwargs.get('d'):
                        wert = float(wert)
                        if d:
                            return eval(format(wert, ".%df" % d))
                        return eval(format(wert))
                    return wert
                raise AglaError('die Punkte haben unterschiedliche Dimension')
            else: 
                if self.dim in [2, 3]:                       
                    wert = other.abstand(self)
                    d = kwargs.get('d')
                    if not isinstance(d, (Integer, int)):
                        return wert
                    if d <= 0:
                        return wert					
                    if mit_param(wert):
                        if d:					
                            return N(wert, d)
                        return N(wert)
                    wert = float(wert)
                    if d:					
                        return eval(format(wert, ".%df" % d))
                    return eval(format(wert))
        except AglaError as e:
            print('agla:', str(e))
            return
		
						 
    def bild(self, *abb, **kwargs):                           
        """Bild bei einer Abbildung"""
		
        if self.dim not in (2, 3):
             return
			 
        if kwargs.get('h'):
            print("\nBildvektor/-punkt bei einer Abbildung\n")		
            print("Aufruf   vektor . bild( abbildung )\n")		
            print("             vektor      Vektor/Punkt")
            print("             abbildung   Abbildung des Raumes R^3")
            print("                         oder der Ebene R^2\n")
            print("Nur in R^2 und R^3 verfügbar\n")
            return 
			
        try:			
            if len(abb) != 1:
                raise AglaError('eine Abbildung angeben')	
            abb = abb[0]	
            if abb.dim != self.dim:
                raise AglaError('die Abbildung muß die Dimension %i haben' % self.dim)		
            bild = abb.matrix * self + abb.versch
            return bild
        except AglaError as e:
            print('agla ', str(e))

		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Vektor"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Vektor in R^3 mit mayavi"""	
        				
        pkt_farbe = UMG._default_pkt_farbe if spez[1] == 'default' \
                                                   else spez[1]		
        pkt_staerke = UMG._default_pkt_staerke if spez[2] == 'default' \
                                                   else spez[2][0]
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' \
                                                   else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' \
                                                   else spez[2][1]
		
        vektor = False		
        if spez[0]:
            vektor = True	
            q = spez[0]
            if q.dim != 3:
                return AglaError('die Vektoren/Punkte haben unterschiedliche Dimension')				
				
        anim = False			
        if spez[3]:
            anim = True
            aber = spez[3]	
			
        if vektor and anim:
            return None
			
        p = self	
        if not anim:		
            if not vektor:
                return mlab.points3d([float(p.x)], [float(p.y)], [float(p.z)], 
			            scale_factor=pkt_staerke, color=pkt_farbe)		
            else:		
                return _arrow(q.x, q.y, q.z, p.x+q.x, p.y+q.y, p.z+q.z,  
		                    color=lin_farbe, size=lin_staerke)	
        else:
            b_ = Symbol('b_')
            p = p.sch_el(b_)
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20			
            aa = np.linspace(float(aber[0]), float(aber[1]), N) 
            xs, ys, zs = repr(p.x), repr(p.y), repr(p.z)
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
            for bb in aa:
                bb = '(' + str(bb) + ')'
                xa += [eval(xs.replace('b_', bb))]
                ya += [eval(ys.replace('b_', bb))]
                za += [eval(zs.replace('b_', bb))]
            plt = mlab.points3d(xa[0], ya[0], za[0], 
                         scale_factor=pkt_staerke, color=pkt_farbe) 
            return plt, (xa[1:], ya[1:], za[1:]), N-1		

			
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Vektor in R^3 mit vispy"""	
		
        pass		
				
		
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Vektor in R^2 mit matplotlib"""	
			
        from numpy import (pi, sqrt, sin, cos, tan, exp, log, sinh, cosh, tanh,
             arcsin, arccos, arctan, arcsinh, arccosh, arctanh)				   

        pkt_farbe = UMG._default_pkt_farbe2 if spez[1] == 'default' \
		                                             else spez[1]		
        pkt_staerke = UMG._default_pkt_staerke2 if spez[2] == 'default' \
		                                             else spez[2][2]
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' \
		                                             else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' \
		                                             else spez[2][3]
        vektor = False		
        if spez[0]:
            vektor = True	
            q = spez[0]
            if q.dim != 2:
                return AglaError('die Vektoren/Punkte haben unterschiedliche Dimension')		
				
        anim = False			
        if spez[3]:
            anim = True
            aber = spez[3]	
			
        if vektor and anim:
            return None
        p = self	
        if not anim:		
            if not vektor:
                return plt.plot([p.x], [p.y], marker='o',                      
                   markeredgecolor='0.6',  
                   markerfacecolor=pkt_farbe,
                   markersize=pkt_staerke)		
            else:		
                return _arrow2(q.x, q.y, p.x+q.x, p.y+q.y,  
		                    color=lin_farbe, linewidth=lin_staerke)	
        else:
            pass
	   
	   
    def kollinear(self, *args, **kwargs):	
        """Test auf Kollinearität; 
		    für 2- und 3-dimensionale Vektoren bzw. Punkte"""
		
        if kwargs.get('h'):
            print("\nKollinearität von zwei Vektoren bzw. drei Punkten\n")		
            print("Aufruf   vektor . kollinear( vektor1 )\n")
            print("  oder   punkt . kollinear( punkt1, punkt2 )\n")					
            print("             vektor, punkt    Vektor/Punkt\n")
            print("Nur in R^2 und R^3 verfügbar\n")			
            return 
		
        try:		
            if self.dim > 3:
                txt = "nur für Vektoren der Dimension 2 oder 3 verfügbar"
                raise AglaError(txt)
            if not args:
                raise AglaError('mindestens ein Argument angeben')			
            if not all((isinstance(a, Vektor) and a.dim == self.dim) 
		                                                  for a in args):           		
                raise AglaError('nur Vektoren/Punkte (mit gleicher Dimension) erlaubt')
            if len(args) == 1:
                v1, v2 = self, args[0]
            elif len(args) == 2:
                v1, v2 = args[0] - self, args[1] - self
            else:
                raise AglaError('ein oder zwei Argumente angeben')
            if self.dim == 2:
                v1, v2 = Vektor(v1.x, v1.y, 0), Vektor(v2.x, v2.y, 0)
            vp = v1.vp(v2)   	
            vp2 = Vektor(vp.x**2, vp.y**2, vp.z**2)			
            if vp.einfach == v1.O:
                return True
            if vp2.einfach == v1.O:
                return True
            return False
        except AglaError as e:
            print('agla:', str(e))
			

    def komplanar(self, *args, **kwargs):	
        """Test auf Komplanararität;
       		für 3 Vektoren bzw. 4 Punkte im Raum R^3"""
		
        if kwargs.get("h"):
            print("\nKomplanarität von drei Vektoren bzw. vier Punkten\n")		
            print("Aufruf   vektor . komplanar( vektor1, vektor2 )\n")
            print("  oder   punkt . komplanar( punkt1, punkt2, punkt3 )\n")					
            print("             vektor, punkt    Vektor/Punkt\n")
            print("Nur im Raum R^3 verfügbar\n")			
            return 
		
        try:		
            if not args:
                raise AglaError('mindestens zwei Argumente angeben')
            if self.dim != 3:
                txt = "nur für Vektoren der Dimension 3 verfügbar"
                raise AglaError(txt)
            if not all((isinstance(a, Vektor) and a.dim == self.dim) 
		                                             for a in args):
                raise AglaError('nur Vektoren/Punkte (mit gleicher Dimension) ' + \
                              'erlaubt')
            if len(args) == 2:
                v1, v2, v3 = self, args[0], args[1]
            elif len(args) == 3:
                v1, v2, v3 = args[0] - self, args[1] - self, args[2] - self
            else:
                raise AglaError('zwei oder drei Argumente angeben')
            spat_produkt = (v1.vp(v2)).sp(v3)                  
            return einfach(spat_produkt) == 0			
        except AglaError as e:
            print('agla:', str(e))		
		
		
    def kette(self, *args, **kwargs):	                           
        """Verketten von Vektoren zu einer Matrix"""
			   
        if kwargs.get('h'):
            print("\nVerketten von Vektoren zu einer Matrix\n")		
            print("Aufruf   vektor . kette( vektor1, vektor2, ... )\n")
            print("oder     vektor | vektor1 | vektor2 ...\n")
            print("             vektor    Vektor\n")
            return 
		
        try:		
            if not args:
                raise AglaError('mindestens ein Argument angeben')		
            if isinstance(args[0], (tuple, Tuple, list)):
                vekt = Tuple(self, *args[0])
            else:
                vekt = Tuple(self, *args)
            if len(vekt) < 2:
                raise AglaError('zwei oder mehr Vektoren angeben')	
            if not all(isinstance(v, Vektor) for v in vekt):
               raise AglaError('nur Vektoren angeben')
            if not all(v.dim == self.dim for v in vekt):
                raise AglaError('die Vektoren haben unterschiedliche Dimension')			
        except AglaError as e:
            print('agla:', str(e))	
            return			
			
        liste = [ [k for k in v.komp] for v in vekt ]
        m = SympyMatrix(liste)
        return m.T                                  
	
	
    def schnitt(self, *other, **kwargs):
        """Schnitt mit einem anderen Objekt"""
		
        if self.dim > 3:
            return
			
        if kwargs.get('h'):
            print("\nSchnittmenge des Punktes mit einem anderen Objekt\n")		
            print("Aufruf   punkt . schnitt( objekt )\n")		
            print("             punkt     Punkt")
            print("             objekt    im Raum R^3: Punkt, Gerade, Ebene, Kugel,")
            print("                       Strecke, Dreieck, Viereck")
            print("                       in der Ebene R^2: Punkt, Gerade, Strecke,")
            print("                       Kreis, Dreieck, Viereck\n")
            print("Zusatz       l=1   Lageinformationen\n")
            return 
		
        try:	
            if len(other) != 1:
                raise AglaError('ein anderes Objekt angeben')		
            other = other[0]
			
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke	
            Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis	
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
            Dreieck = importlib.import_module('agla.lib.objekte.dreieck').Dreieck	
            Viereck = importlib.import_module('agla.lib.objekte.viereck').Viereck	
			
            if not isinstance(other, (Vektor, Gerade, Ebene, Strecke, Kreis,  
		                       Kugel, Dreieck, Viereck)):
                if self.dim == 3:							   
                   txt = "Punkt, Gerade, Ebene, Kugel, Strecke, Dreieck " +\
        				    "oder Viereck angeben"
                elif self.dim == 2:
                   txt = "Punkt, Gerade, Strecke, Kreis, Dreieck oder " +\
        				    "Viereck angeben"
                else:
                    txt = "nicht implementiert"				
                raise AglaError(txt)
            if self.dim != other.dim:				
                raise AglaError("die Objekte haben unterschiedliche Dimension")
            if mit_param(self) or mit_param(other):
                raise AglaError('nicht implementiert (Parameter)')
        except AglaError as e:
            print('agla:', str(e))	
            return			
			
        if isinstance(other, Vektor):
            if other == self:
                if kwargs.get('l'):
                    return display(Math(latex('\\text{die Punkte sind identisch}')))
                else:
                    return self
            if kwargs.get('l'):
                return display(Math(latex('\\text{die Punkte sind verschieden}')))
            else:
                return set()
        if kwargs.get('l'):
            return other.schnitt(self, l=1)
        else:
            return other.schnitt(self)

		
    def sp(self, *other, **kwargs):       
        """Skalarprodukt zweier Vektoren"""

        if kwargs.get('h'):
            print("\nSkalarprodukt des Vektors mit einem anderen Vektor\n")		
            print("Aufruf   vektor * vektor1     ( Operator * )\n")		            
            print("  oder   vektor ° vektor1     ( Operator ° )\n")		            
            print("  oder   vektor . sp( vektor1 )\n")
            print("             vektor    Vektor\n")
            return 
		
        try:		
            if len(other) != 1:		
                raise AglaError('einen anderen Vektor angeben')
            other = other[0]		
            if isinstance(other, Vektor) and other.dim == self.dim:
                return sum([x*y for x, y in zip(self.komp, other.komp)])
            else: 
                if isinstance(other, Vektor):		
                    raise AglaError('die Vektoren haben unterschiedliche' + \
                                   'Dimension')
                else:
                    txt = ("das Skalarprodukt für %s und %s ist nicht" + \
					           "definiert" % (self, other))			
                    raise AglaError(txt)		
        except AglaError as e:
            print('agla:', str(e))            		
			
			
    def vp(self, *other, **kwargs):  
        """Vektorprodukt zweier Vektoren in R^3"""	
		
        if kwargs.get('h'):
            print("\nVektorprodukt des Vektors mit einem anderen Vektor\n")		
            print("Aufruf   vektor >< vektor1     ( Operator >< )\n")
            print("oder     vektor . vp( vektor1 )\n")
            print("             vektor    Vektor\n")
            print("Nur im Raum R^3 definiert\n")    
            return 

        try:			
            if len(other) != 1:		
                raise AglaError('einen anderen Vektor angeben')
            other = other[0]
            if isinstance(other, Vektor) and self.dim == 3 and other.dim == 3:  
                a, b = self, other
                return Vektor(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, 
			                    a.x*b.y - a.y*b.x)
            else:
                if isinstance(other, Vektor):
                    txt = "die Vektoren haben nicht beide die Dimension 3"
                    raise AglaError(txt)	
                txt = "das Vektorprodukt ist nur für zwei Vektoren im Raum R^3 definiert" 
                raise AglaError(txt)		
        except AglaError as e:
            print('agla:', str(e))		
					
				
    def winkel(self, *other, **kwargs):  
        """Winkel mit anderen Objekten"""	
		
        if self.dim > 3:
            return
			
        if kwargs.get('h'):
            print("\nWinkel des Vektors mit einem anderen Objekt (in Grad)\n")			
            print("Aufruf     vektor . winkel( objekt )\n")
            print("              vektor    Vektor")
            print("              objekt    Vektor, Gerade, Ebene (im Raum R^3)")
            print("                        Vektor, Gerade (in der Ebene R^2)\n")
            print("Zusatz        d=n       Dezimaldarstellung")
            print("                        n - Anzahl der Nachkomma-/Stellen\n")
            return 

        try:	
            if not other:
                raise AglaError('Vektor, Gerade oder Ebene angeben')
            if len(other) != 1:
                raise AglaError('nur ein Objekt angeben')
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene					
            other = other[0]				
            if isinstance(other, Vektor):
                if other.dim != self.dim:
                    txt = "die Vektoren haben unterschiedliche Dimensionen"
                    raise AglaError(txt)
                if self == self.O or other == other.O:
                    raise AglaError('Winkel nicht definiert (Nullvektor)')
                w = self * other / (self.betrag * other.betrag)	
                if N(w) > 1:
                    w = 1				
                elif N(w) < -1:
                    w = -1				
                if mit_param(w):
                    wi = simplify(N(acosg(w)))
                else:
                    wi = N(acosg(w))								
            elif isinstance(other, (Gerade, Ebene)):
                wi = other.winkel(self, d=12)
            else:
                raise AglaError('Vektor, Gerade oder Ebene angeben')
				
            d = kwargs.get('d')
            if not isinstance(d, (Integer, int)) or d < 0:
                return wi
            return wert_ausgabe(wi, d)
			
        except AglaError as e:
            print('agla:', str(e))	
            return			
		
		   
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar mit einem Parameter"""
			
        if kwargs.get('h'):
            print("\nElement einer Schar von Vektoren\n")		
            print("Aufruf   vektor . sch_el( wert )\n")		                     
            print("             vektor    Vektor")
            print("             wert      Wert des Scharparameters\n")			
            print("Es ist nur ein Scharparameter zugelassen\n")    
            return 
        try:					
            if not self.is_schar or len(self.sch_par) > 1:
                raise AglaError('keine Schar mit einem Parameter')					
            if not wert or len(wert) != 1:		
                raise AglaError('einen Wert für den Scharparameter angeben')		
            if len(self.sch_par) != 1:
                raise AglaError('keine Schar mit einem Parameter')
            p = self.sch_par.pop()
            wert = sympify(*wert)
            if not is_zahl(wert):
                raise AglaError('für Scharparameter Zahl oder freien \
				                                      Parameter angeben')	
            return Vektor([k.subs(p, wert) for k in self.komp])
        except AglaError as e:
            print('agla:', str(e))		
	
    schEl = sch_el	

	
    def diff(self, *x, **kwargs):                           
        """Ableitungsvektor für eine Variable (partiell)"""
		 
        if kwargs:
            print("\nPartielle Ableitung eines Vektors mit mehreren Variablen")
            print("nach einer der Variablen\n")			
            print("Aufruf   vektor . diff( var )\n")		                     
            print("             vektor    Vektor")
            print("             var       Variable, nach der abgeleitet wird\n")			
            print("Die Erweiterung der d-Eigenschaft auf mehrere Variable\n")    
            return 
		 
        try:		 
            if len(x) != 1:		 
                raise AglaError('eine Variable angeben')
            x = x[0]
            if not isinstance(x, Symbol):
                raise AglaError('es muss eine Variable angegeben werden')
            return Vektor([k.diff(x) for k in self.komp])
        except AglaError as e:
            print('agla:', str(e))	
            return

	
	
# Operationen
# -----------	
					
    def __add__(self, other):
        try:
            if isinstance(other, Vektor):	
                if other.dim == self.dim:
                    sa, so, sum = self.args, other.args, []
                    for i in range(self.dim):
                       sum += [sa[i] + so[i]]
                    return Vektor(sum)					   
                else:
                    txt = "die Vektoren haben unterschiedliche Dimension"
                    raise AglaError(txt)	
            else:
                raise AglaError('Addition von %s und %s ist nicht möglich' 
			                      % (self, other))
        except AglaError as e:
            print('agla:', str(e))					
						
    def __mul__(self, other): 
        if isinstance(other, Vektor):	
            try:
                if other.dim == self.dim:	
                    return sum([x*y for x, y in zip(self.komp, other.komp)]) 
                txt = "die Vektoren haben unterschiedliche Dimension"				
                raise AglaError(txt)
            except AglaError as e:
                print('agla:', str(e))
        else:
            factor = sympify(other)
            if is_zahl(factor):
                return Vektor([x*factor for x in self.args])	
            else:
                return NotImplemented                              
        		  
    def __rmul__(self, other):
        other = sympify(other)
        try:
            if is_zahl(other):
                return self * other	
            elif isinstance(other, _ZeilenVektor):      
                komp = []
                for i in range(len(other.args)):
                    komp += [other.args[i]]
                v1 = Vektor(*komp)
                return v1.sp(self)
            else:
                raise AglaError('nicht implementiert', type(other))                                  	
        except AglaError as e:
            print('agla:', str(e))
				
    def __neg__(self):
        return Vektor([-x for x in self.args])

    def __sub__(self, other):
        return self + (-other)			

    def __div__(self, divisor):
        divisor = sympify(divisor)
        return Vektor([x/divisor for x in self.args])	

    def __or__(self, other):
        """Überschreiben des Operators '|' zur Verkettung von Vektoren/Matrizen"""         		
        try:
            if isinstance(other, (list, tuple, Tuple)):
                dim1 = other[0].dim
                t = [isinstance(o, Vektor) for o in other]
                if not all(t):
                    print('agla: eine Liste mit Vektoren angeben')
                    return					
            elif isinstance(other, SympyMatrix):
                dim1 = other.dim[0]
            else:
                dim1 = other.dim		
        except AttributeError as e:
            print('agla :  Vektor, Liste von Vektoren oder Matrix angeben')
            return			
        if self.dim != dim1:
            print('agla: die Dimensionen sind unverträglich, ' + \
				                      'Verkettung ist nicht möglich')	
            return	
        if isinstance(other, (list, tuple, Tuple)):			
            return self.kette(*other)	
        elif isinstance(other, SympyMatrix):
            Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix	
            vekt = [self] + other.vekt
            return Matrix(*vekt)			
        return self.kette(other)	

    def __and__(self, other):
        """Überschreiben des Operators '&' zur Berechnung des Vektorproduktes"""	
        try:
            if isinstance(other, Vektor):		
                if other.dim == self.dim:
                    return self.vp(other) 
                else:
                    txt = "die Vektoren haben unterschiedliche Dimension"
                    raise AglaError(txt)			
            else:
                raise AglaError('Vektor im Raum R^3 angeben')
        except AglaError as e:
            print('agla:', str(e))		
		
    __truediv__ = __div__

	
# Indexzugriff (nur lesen)
# ------------------------	
	
    def __getitem__(self, i):
        return self.komp[i]
		 	
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        if self.dim <= 3:		
            vektor_hilfe(3)	
            return
        vektor_hilfe(4)				
		
    h = hilfe					
		
			

# Benutzerhilfe für Vektor
# ------------------------

def vektor_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung, Operatoren")
        print("h=3 - Eigenschaften und Methoden in R^3 und R^2")
        print("h=4 - Eigenschaften und Methoden für dim > 3")
        return		
		
    if h == 2:
        print("\nVektor - Objekt\n")
        print("Kurzname   v\n")		
        print("Repräsentation eines Vektors im n-dimensionalen Euklidischen")
        print("Raum R^n (n>=2)\n")
        print("Synonym       Punkt (Punkte werden mit ihren Ortsvektoren iden-")
        print("                     tifiziert)\n")
        print("Erzeugung     Vektor( komp1, komp2, ... )\n")
        print("                 komp    Komponente (nummerischer Ausdruck)\n")
        print("     oder     Vektor( vekt1, vekt2 )\n")
        print("                 vekt    Vektor; es wird der Differenzvektor der") 
        print("                         beiden Vektoren erzeugt\n")
        print("     Wird mit einem Schlüsselwortparameter simpl=nein angegeben, ") 
        print("     erfolgt keine Umwandlung von float-Komponenten in rationale ")
        print("     Zahlen; das ist auch der Fall, wenn mit der Anweisung")
        print("     UMG.SIMPL = nein die Umgebungsvariable UMG.SIMPL global ein-")
        print("     gestellt wird\n")		
        print("Zuweisung  vek = v(...)   bzw.   vek = Vektor(...)")
        print("                 (v - reservierter, vek - freier Bezeichner)\n")
        print("Operatoren")
        print("  +  : Addition") 
        print("  -  : Negation/Subtraktion") 
        print("  *  : Multiplikation mit einem Skalar")                  
        print("  /  : Division durch einen Skalar")                        
        print("  *  : Skalarprodukt")                                  
        print("  °  : ebenso")                                  
        print("  >< : Vektorprodukt   (nur im Raum R^3)")                
        print("  |  : Verketten mit einem anderen Vektor\n")                   
        print("Beispiele")
        print("a = v(1, 2, 3)  ist identisch mit  a = Vektor(1, 2, 3)")
        print("b = v(4, -2, -5)")
        print("a + b, a - b")
        print("v(a, b) erzeugt den Vektor b-a")
        print("v(1/2, 3/5, 1) ist identisch mit")
        print("               v(Rational(1, 2), Rational(3, 5), 1)")
        print("v(1.33, 4.6)   ist identisch mit v(133/100, 23/5)") 
        print("               (automatische Umwandlung von float-/Float-")
        print("               in Rational-Zahlen, falls nicht mit simpl")
        print("               bzw. UMG.SIMPL verhindert)")
        print("v(sqrt(3), 2*sqrt(5)+1, 1/2*sqrt(2))")
        print("2*a, sqrt(3)*b, 5*a-3*b")
        print("a * b  - Skalarprodukt")
        print("v(1, 2, 3, 4, 5, 6, 7, 8) - Vektor / Punkt im R^8\n")
        print("Vordefinierte Vektoren")   
        print("O    Nullvektor / Ursprung im Raum R^3") 
        print("O2   Nullvektor / Ursprung in der Ebene R^2") 
        print("X    Allgemeiner Vektor / Punkt im Raum R^3") 
        print("X2   Allgemeiner Vektor / Punkt in der Ebene R^2\n") 
        return
		
    if h == 3:
        print("\nEigenschaften und Methoden (M) für Vektoren im Raum R^3 und")
        print("in der Ebene R^2\n")
        print("vek.hilfe                Bezeichner der Eigenschaften und Methoden")
        print("vek.abstand(...)      M  Abstand zu anderen Objekten")              
        print("vek.betrag               Betrag")
        print("vek.betrag_(...)      M  ebenso, zugehörige Methode")
        print("vek.bild(...)         M  Bild bei einer Abbildung")
        print("vek.d                    Ableitungsvektor (eine Variable)")
        print("vek.dez                  Dezimaldarstellung")
        print("vek.dez_(...)         M  ebenso, zugehörige Methode")
        print("vek.diff(...)         M  Ableitungsvektor (mehr als eine Variable)")
        print("vek.dim                  Dimension (Anzahl Komponenten)")
        print("vek.einfach              Vereinfachung eines Vektors")    
        print("vek.einh_vekt            Einheitsvektor")
        print("vek.is_schar             Test auf Schar")
        print("vek.kette(...)        M  Verketten zu einer Matrix")   
        print("vek.kollinear(...)    M  Kollinearität von Vektoren/Punkten")  
        print("vek.komp                 Komponenten")
        print("vek.komplanar(...)    M  Komplanarität von Vektoren/Punkten (nur im Raum R^3)")
        print("vek.koord                Koordinaten  (= vek.komp)")
        print("vek.länge                Länge  (= vek.betrag)")
        print("vek.länge_(...)       M  ebenso, zugehörige Methode")
        print("vek.O                    Nullvektor (in der Dimension des Vektors)")
        print("vek.punkt_ausg           Ausgabe als Punkt")
        print("vek.sch_par              Parameter einer Schar") 
        print("vek.sch_el(...)       M  Element einer Schar")
        print("vek.schnitt(...)      M  Schnittmenge mit anderen Objekten")	
        print("vek.sp(...)           M  Skalarprodukt; Operator * oder °")
        print("vek.vektor2sympy         Konvertierung in eine SympyMatrix")
        print("vek.vp(...)           M  Vektorprodukt; Operator ><   (nur im Raum R^3)")
        print("vek.winkel(...)       M  Winkel mit anderen Objekten")
        print("vek.x                    x-Komponente")
        print("vek.y                    y-Komponente")
        print("vek.z                    z-Komponente   (nur im Raum R^3)")	
        print("vek.zeil                 Zeilenvektor\n")
        print("Synonyme Bezeichner\n")
        print("hilfe       :  h")
        print("betrag_     :  Betrag")
        print("dez_        :  Dez")
        print("einh_vekt   :  einhVekt")
        print("is_schar    :  isSchar")
        print("länge_      :  Länge")
        print("punkt_ausg  :  punktAusg")
        print("sch_el      :  schEl")
        print("sch_par     :  schPar\n")
        return

    if h == 4:
        print("\nEigenschaften und Methoden (M) für Vektoren mit Dimension > 3\n")
        print("vek.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("vek.abstand(...)   M  Abstand zu anderen Vektoren")              
        print("vek.betrag            Betrag")
        print("vek.betrag_(...)   M  ebenso, zugehörige Methode")
        print("vek.d                 Ableitungsvektor (eine Variable)")
        print("vek.dez               Dezimaldarstellung")
        print("vek.dez_(...)      M  ebenso, zugehörige Methode")
        print("vek.diff(...)      M  Ableitungsvektor (mehr als eine Variable)")
        print("vek.dim               Dimension (Anzahl Komponenten)")
        print("vek.einfach           Vereinfachung eines Vektors")    
        print("vek.einh_vekt         Einheitsvektor")
        print("vek.is_schar          Test auf Schar")
        print("vek.kette(...)     M  Verketten zu einer Matrix")   
        print("vek.komp              Komponenten")
        print("vek.koord             = vek.komp")
        print("vek.länge             = vek.betrag (Länge)")
        print("vek.länge_(...)    M  ebenso, zugehörige Methode")
        print("vek.O                 Nullvektor (in der Dimension des Vektors)")
        print("vek.sch_el(...)    M  Element einer Schar")
        print("vek.sch_par           Parameter einer Schar") 
        print("vek.sp(...)        M  Skalarprodukt; Operator * oder °")        
        print("vek.T                 = vek.zeil")
        print("vek.vektor2sympy      Konvertierung in eine Sympy-Matrix")
        print("vek.zeil              Zeilenvektor\n")
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("betrag_    :  Betrag")
        print("dez_       :  Dez")
        print("einh_vekt  :  einhVekt")
        print("is_schar   :  isSchar")
        print("länge_     :  Länge")
        print("sch_el     :  schEl")
        print("sch_par    :  schPar\n")		
        print("Der lesende Zugriff auf die i. Komponente eines Vektors a ")
        print("erfolgt mittels")
        print("\n   a[i]     oder auch     a.komp[i]\n")
        print("Eine Änderung einzelner Komponenten ist nicht möglich\n")
        return
		
		

# Hilfsklasse _ZeilenVektor
# ------------------------

# Zeilenvektor mit n Komponenten; nur zu Darstellungszwecken 
# als Operation ist nur die Multiplikation mit Vektor/Matrix implementiert

class _ZeilenVektor(AglaObjekt):    

    printmethod = '_latex'

    def __new__(self, *args, **kwargs):        
		
        self.komp = args		
        li = []
        for i in range(len(self.komp)):
            li += [is_zahl(self.komp[i])]	
        try:				
            if not all(li):
                raise AglaError('Zahlenwerte angeben')								        
            return AglaObjekt.__new__(self, *self.komp)
        except AglaError as e:			
            print('agla:', str(e))
		
    def __str__(self): 
        m = SympyMatrix([[k for k in self.komp]])	
        return str(m)
		
    def __repr__(self):                                
        m = SympyMatrix([[k for k in self.komp]])	
        return repr(m)

    def _latex(self, printer):	                          
        m = SympyMatrix([[k for k in self.komp]])	        
        return latex(m)
		
    def __mul__(self, other):
        if isinstance(other, (SympyMatrix, Vektor)):
            if isinstance(other, SympyMatrix) and len(self.args) != other.dim[0]:
                print('agla: die Dimensionen sind unverträglich')
                return
            if isinstance(other, Vektor) and len(self.args) != other.dim:
                print('agla: die Dimensionen sind unverträglich')
                return
            m = SympyMatrix([[k for k in self.komp]])
            if isinstance(other, Vektor):
                other = other.vektor2sympy	
                M = m * other
                return M[0, 0]
            M = m * other
            l = [M[0, i] for i in range(M.cols)]			
            return _ZeilenVektor(*l)		
		
    def __rmul__(self, other):
        args = self.args
        komp = [a * other for a in args]
        return _ZeilenVektor(*komp) 		

    
	
# Synonyme
# --------

v = Vektor
Punkt = Vektor



# Vordefinierte Vektoren
# ----------------------

x, y, z = symbols('x y z')
X = Vektor(x, y, z)                                              
X2 = Vektor(x, y)    
O = Vektor(0, 0, 0)
O2 = Vektor(0, 0)

	