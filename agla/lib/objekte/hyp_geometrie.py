#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Klassen der hyperbolischen Geometrie von agla           
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



# Inhalt (Klassen):
#
#   hPunkt		Hyperbolischer Punkt
#   hGerade		Hyperbolische Gerade
#   hStrahl     Hyperbolischer Strahl
#   hStrecke	Hyperbolische Strecke
#   hKreis		Hyperbolischer Kreis
#   hDreieck	Hyperbolisches Dreieck



import importlib

from math import sqrt
from numpy import inf
import numpy as np

from IPython.display import display, Math

from sympy.abc import *
from sympy.core.symbol import Symbol
from sympy.core.sympify import sympify
from sympy.core.numbers import Rational, Float, pi, I, oo, zoo
from sympy.core.numbers import oo as inf
from sympy.functions.elementary.miscellaneous import sqrt
from sympy import (sin, sinh, cosh, acosh, conjugate, re, 
     im, atan, exp, Abs, Add, Min)
from sympy.core.function import diff
from sympy.solvers.solvers import solve, nsolve
from sympy.core.evalf import N	 
from sympy.printing.latex import latex
from sympy import expand 		
import sympy

# Einbeziehung von SymEngine (Probe)
try:
    import symengine as se
    from symengine import Symbol as  sesymbol				
    from symengine import sqrt as sesqrt				
    from symengine import Abs as seabs	
    SYMENGINE = True	
except ImportError:
    se = sympy
    sesymbol = Symbol
    sesqrt = sqrt
    seabs = Abs	
    SYMENGINE = False	

from agla.lib.objekte.basis import AglaObjekt
from sympy.core.containers import Tuple
from sympy.polys.polytools import Poly
from sympy.simplify.simplify import simplify, nsimplify

from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.ebene import Ebene, xy_ebene
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis, EinhKreis2
from agla.lib.objekte.kurve import Kurve
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, kollinear,
   sing, cosg, tang, arccosg, arctang, loese, einfach, grad, rad, Abstand)
from agla.lib.funktionen.abb_funktionen import drehung, spiegelung
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.objekte.umgebung import UMG	
import agla	
	


# Funktionen / Hilfsfunktionen	
# ----------------------------
			
			
			
# Punkt -> komplexe	Zahl	
def v2c(A):
    if isinstance(A, Vektor):
        return A.x + A.y*I
    return A.e.x + A.e.y*I
    
# komplexe Zahl	-> Punkt
def c2v(z):
    return Vektor(re(z), im(z), simpl=False) 
		
# float-Umwandlung
def to_float(x):
    if isinstance(x, hPunkt):
        vv = x.e.dez	
        return hPunkt(vv)	
    if mit_param(x):
        return N(re(x))
    return float(re(x))	

# hPunkt -> komplexe Zahl
def hp2c(hp):
    p = hp.e
    return float(p.x) + float(p.y)*1j
	
	
# Cayley-Transformation / [Agricola S156]
# ---------------------------------------

def cayley(z):       # Inneres des Einheitskreises --> obere Halbebene
    if z == 0:
        return I
    elif z == I:
         return inf
    elif z == inf:
        return -I
    return (1-z*I) / (z-I)

def cayley_inv(z):   # Cayley-Inverse:  obere Halbebene --> Inneres des 
                     # Einheitskreises
    if z == I:
        return 0
    if z == -I:
        return inf
    if z == inf:
        return I
    return (1+z*I) / (z+I)

# Real- und Imaginärteil der Cayley-Transformationen
def re_cayley(z):
    if z in (I, 1j):
        return oo	
    x, y = re(z), im(z)
    return float(2*x / (x**2 + y**2 - 2*y + 1))

def im_cayley(z):
    if z in (I, 1j):
        return oo	
    x, y = re(z), im(z)
    return float((-x**2 - y**2 + 1) / (x**2 + y**2 - 2*y + 1))
            
def re_cayley_inv(z):
    if z in (-I, -1j):
        return 0	
    x, y = re(z), im(z)
    return float(2*x / (x**2 + y**2 + 2*y + 1))     

def im_cayley_inv(z):
    if z in (-I, -1j):
        return 0	
    x, y = re(z), im(z)
    return float((x**2 + y**2 - 1) / (x**2 + y**2 + 2*y + 1))
 	
	
# Test auf Randpunkt	
# ------------------

def is_rand_pkt(hp):
    if not hp._mod in ('D', 'D3'):
        return False
    if hp.exakt:
        if einfach(hp.e.betrag**2) == 1:
            return True	
        else:
            return False
    if mit_param(hp):
        return None	
    g = 1 - 1e-8
    return hp.e.betrag.n() > g
	

# Nummerische Gleichheit	
# ----------------------
	
def gleich(x, y):
    g = 1e-8
    if is_zahl(x):
        u, w = abs(re(abs(x-y))), abs(im(abs(x-y)))
        return u < g and w < g
    elif isinstance(x, (Vektor, hPunkt)):
        w = x.abstand(y)
        return w < g


# float-Schnitt zweier Kreise
# ---------------------------

def schnitt_kreis_kreis_float(kreis1, kreis2):
    chordale = N((kreis1.gleich - kreis1.radius**2).lhs - 
               (kreis2.gleich - kreis2.radius**2).lhs)
    L = loese(chordale, x)   
    L = dict({x : N(L[x])})
    gl = N((kreis1.gleich-kreis1.r**2).lhs.subs(L)) 
    po = Poly(gl, y)
    p = float(po.coeff_monomial(y**2))
    q = float(po.coeff_monomial(y))
    r = float(po.coeff_monomial(1))
    y1 = 1/2/p*(-q + np.sqrt(-4*p*r+q**2))
    y2 = -1/2/p*(q + np.sqrt(-4*p*r+q**2))
    x1 = L[x].subs(y, y1)
    x2 = L[x].subs(y, y2)
    return Vektor(x1, y1, simpl=False), Vektor(x2, y2, simpl=False)	
	
	
# float-TrägerKreis
# -----------------
	
def traeger_kreis_float(A, B, objekt='hGerade'):

    # Berechnung im E+ -Modell, Überführung in das D-Modell
    # unter Benutzung der Cayley-Transformationen  
	#
    #       D <--> E+  : Inneres der Einheitskreisscheibe <--> obere Halbebene 
    #
    # D-Ebene : z = x + yi
    #
    # E+ -Ebene: w = r + si

    zA = hp2c(A)                         
    xA, yA = re(zA), im(zA)               
    rA = re_cayley(zA)        
    sA = im_cayley(zA)     
    wA = rA + sA * 1j
    zB = hp2c(B)
    xB, yB = re(zB), im(zB)
    rB = re_cayley(zB)
    sB = im_cayley(zB)	
    wB = rB + sB * 1j  
    # spezielle Behandlung von w = zoo 
    if cayley(zA) == zoo or cayley(zB) == zoo:
        if cayley(zB) == zoo:
            wA, wB = wB, wA		
            sA, sB = sB, sA		
        m = Symbol('m', real=True)   # gesuchter Mittelpunkt auf der r-Achse
        # Gleichung (s.u.)
        gl = (m-wA)*conjugate(m-wA) - (m-wB)*conjugate(m-wB) 
        L = loese(gl)  
        m = L[m]		
        ME = Vektor(m, 0)
        rE = m
        kE = Kreis(ME, rE)
        if objekt in ('hGerade', 'hStrahl'):
            # 2 Punkte auf kE; gehen in Randpunkte in D über
            wP, wQ = [m + rE*np.exp(t * 1j) for t in (0, np.pi)]
            xP, xQ = [re_cayley_inv(z) for z in [wP, wQ]] 
            yP, yQ = [im_cayley_inv(z) for z in [wP, wQ]]
            return kE, Vektor(xP, yP, simpl=False), Vektor(xQ, yQ, simpl=False)
        elif objekt == 'hStrecke':		
            return kE
	    
    # wM = m  - der Kreismittelpunkt liegt auf der reellen (r-) Achse
    #
    # Gleichung für m: Abstand(wM, wA)^2 = Abstand(wM, wB)^2 
    #
    #                  gl = m*(-2*rA + 2*rB) + rA**2 + sA**2 - rB**2 - sB**2
    #
    # wird hier 'von Hand' gelöst

    t0 = float((rA**2 + sA**2 - rB**2 - sB**2) / (2*rA - 2*rB))
    
    rE = np.sqrt((t0 - rA)**2 + sA**2)    
    ME = Vektor(t0, 0, simpl=False)	
    kE = Kreis(ME, rE)
    
    # 3 Punkte auf kE; P und Q gehen in Randpunkte in D über
    wP, wQ, wR = [t0 + rE*np.exp(t * 1j) for t in (0, np.pi, np.pi/2)]
    xP, xQ, xR = [re_cayley_inv(z) for z in [wP, wQ, wR]] 
    yP, yQ, yR = [im_cayley_inv(z) for z in [wP, wQ, wR]]
      
    a00 = -2*xP + 2*xQ; a01 = -2*yP + 2*yQ
    a10 = -2*xP + 2*xR; a11 = -2*yP + 2*yR
    b0 = xP**2 - xQ**2 + yP**2 - yQ**2
    b1 = xP**2 - xR**2 + yP**2 - yR**2
    a = np.array([[a00, a01], [a10, a11]])
    b = np.array([-b0, -b1])
    L = np.linalg.solve(a, b)
    
    ME = Vektor(L[0], L[1], simpl=False)
    rE = float(Abstand(ME, Vektor(xP, yP)))
    kE = Kreis(ME, rE)
        
    if objekt in ('hGerade', 'hStrahl'):		
        return kE, Vektor(xP, yP, simpl=False), Vektor(xQ, yQ, simpl=False)
    elif objekt == 'hStrecke':		
        return kE
	
	
# Parameterwert für einen Kreispunkt
# ----------------------------------
	
def par_wert(kreis, punkt):   # Kreis, Punkt auf ihm
    vv = np.array([float(punkt.x - kreis.mitte.x), float(punkt.y - kreis.mitte.y)])
    gr = 1e-8
    x = 0 if np.abs(vv[0]) < gr else vv[0]
    y = 0 if np.abs(vv[1]) < gr else vv[1]
    wi = np.arccos(vv[0] / np.sqrt(vv[0]**2 + vv[1]**2))   # Winkel mit Vektor(1, 0)
    wi = wi*180 / np.pi
    if vv[1] >= 0:
        return wi
    return 360 - wi
		
		
# Funktionen zur Transformation der Modelle	
# -----------------------------------------
	
# D - EinheitsKreisScheiben-Modell
# D3 - D in der xy-Ebene des R^3
# H - HyperboloidHalbSchalen-Modell	

# aktuell wirken die Funktionen nur auf Punkte

# D --> H	                         
def D2H(*p, **kwargs):
    if kwargs.get("h"):
        print("\nAbbildung D-Modell -> H-Modell (hyperbolische Geometrie)\n")
        print("Aufruf      D2H( hpunkt )\n")
        print("                hpunkt   hyperbolischer Punkt im D-Modell\n")
        return	
    if len(p) != 1:
        print('agla: hyperbolischen Punkt im D-Modell angeben')		
        return	
    p = p[0]		
    if isinstance(p, hPunkt) and p._mod == 'D':
        b = p.e.x**2 + p.e.y**2 
        return hPunkt( 2*p.e.x / (1-b), 2*p.e.y / (1-b), (1+b) / (1-b) )
    if isinstance(p, Vektor):
        b = p.x**2 + p.y**2
        return Vektor( 2*p.x / (1-b), 2*p.y / (1-b), (1+b) / (1-b), simpl=False )
    print('agla: hyperbolischen Punkt im D-Modell angeben')		

# D --> D3	
def D2D3(*p, **kwargs):
    if kwargs.get("h"):
        print("\nAbbildung D-Modell -> D3-Modell (hyperbolische Geometrie)\n")
        print("Aufruf      D2D3( hpunkt )\n")
        print("                hpunkt   hyperbolischer Punkt im D-Modell\n")
        return	
    if len(p) != 1:
        print('agla: hyperbolischen Punkt im D-Modell angeben')		
        return	
    p = p[0]		
    if isinstance(p, hPunkt) and p._mod == 'D':
        return hPunkt( p.e.x, p.e.y, 0 )
    if isinstance(p, Vektor):
        return Vektor(p.x, p.y, 0)	
    print('agla: hyperbolischen Punkt im D-Modell angeben')		

# D3 --> H
def D32H(*p, **kwargs):
    if kwargs.get("h"):
        print("\nAbbildung D3-Modell -> H-Modell (hyperbolische Geometrie)\n")
        print("Aufruf      D32H( hpunkt )\n")
        print("                hpunkt   hyperbolischer Punkt im D3-Modell\n")
        return	
    if len(p) != 1:
        print('agla: hyperbolischen Punkt im D3-Modell angeben')		
        return	
    p = p[0]		
    if isinstance(p, hPunkt) and p._mod == 'D3':
        b = p.e.x**2 + p.e.y**2
        return hPunkt( 2*p.e.x / (1-b), 2*p.e.y / (1-b), (1+b) / (1-b) )
    print('agla: hyperbolischen Punkt im D3-Modell angeben')		

# D3 --> D	
def D32D(*p, **kwargs):
    if kwargs.get("h"):
        print("\nAbbildung D3-Modell -> D-Modell (hyperbolische Geometrie)\n")
        print("Aufruf      D32D( hpunkt )\n")
        print("                hpunkt   hyperbolischer Punkt im D3-Modell\n")
        return	
    if len(p) != 1:
        print('agla: hyperbolischen Punkt im D3-Modell angeben')		
        return	
    p = p[0]		
    if isinstance(p, hPunkt) and p._mod == 'D3':
        return hPunkt( p.e.x , p.e.y )
    print('agla: hyperbolischen Punkt im D3-Modell angeben')	

# H --> D	
def H2D(*p, **kwargs):
    if kwargs.get("h"):
        print("\nAbbildung H-Modell -> D-Modell (hyperbolische Geometrie)\n")
        print("Aufruf      H2D( hpunkt )\n")
        print("                hpunkt   hyperbolischer Punkt im H-Modell\n")
        return	
    if len(p) != 1:
        print('agla: hyperbolischen Punkt im H-Modell angeben')		
        return	
    p = p[0]		
    if isinstance(p, hPunkt) and p._mod == 'H':
        return hPunkt( p.e.x / (1 + p.e.z), p.e.y / (1 + p.e.z) )
    print('agla: hyperbolischen Punkt im H-Modell angeben')	

# H --> D3	
def H2D3(*p, **kwargs):
    if kwargs.get("h"):
        print("\nAbbildung H-Modell -> D3-Modell (hyperbolische Geometrie)\n")
        print("Aufruf      H2D3( hpunkt )\n")
        print("                hpunkt   hyperbolischer Punkt im H-Modell\n")
        return	
    if len(p) != 1:
        print('agla: hyperbolischen Punkt im H-Modell angeben')		
        return	
    p = p[0]		
    if isinstance(p, hPunkt) and p._mod == 'H':
        return hPunkt( p.e.x / (1 + p.e.z), p.e.y / (1 + p.e.z), 0 )
    print('agla: hyperbolischen Punkt im H-Modell angeben')	


# Funktionen für SymEngine und numpy
# ----------------------------------
		
# Betrag mit SymEngine ('D', 'D3')
def sebetrag(p):
    x, y = p.args[:2]
    if not SYMENGINE:	
        return sqrt(x**2 + y**2)	
    b = se.sympify(x)**2 + se.sympify(y)**2
    return se.sqrt(b)
	
# hPunkt -> numpy	
def h2np(hp):
    return np.array(hp.args)

# Betrag mit numpy ('D', 'D3')	
def npbetrag(hp):
    from math import sqrt
    if type(hp) is hPunkt:
        hp = h2np(hp)
    return sqrt(hp.dot(hp))

# sigma-Form mit SymEngine ('H')
def sesigma(hp1, hp2):
    if not SYMENGINE:	
        x1, y1, z1 = hp1.e.komp
        x2, y2, z2 = hp2.e.komp
        sigma = -x1*x2 - y1*y2 + z1*z2
        return sympify(sigma)	
    else:	
        x1, y1, z1 = [se.sympify(k) for k in hp1.args]
        x2, y2, z2 = [se.sympify(k) for k in hp2.args]
        sigma = -x1*x2 - y1*y2 + z1*z2
        return se.sympify(sigma)	

# sigma-Form mit numpy ('H')
def npsigma(hp1, hp2):
    x1, y1, z1 = h2np(hp1)
    x2, y2, z2 = h2np(hp2)
    sigma = float(-x1*x2 - y1*y2 + z1*z2)
    return np.arccosh(sigma)


	
	
# hPunkt - Klasse   
# ---------------

class hPunkt(AglaObjekt):                                      
    """
hyperbolischer Punkt

**Erzeugung** 
	
   hPunkt ( *x, y* ) *bzw.*
   
   hPunkt ( *x+yi* ) mittels komplexer Zahlen

      hyperbolischer Punkt im D-Modell   *oder*
   
   hPunkt ( *x, y, 0* ) *bzw.*
   
   hPunkt ( *x, y, 'D3' | 'd3'* )  
   
      hyperbolischer Punkt im D3-Modell;  :math:`x^2+y^2 < 1` *oder*
	  
   hPunkt ( *x, y, 'H' | 'h'* ),  *x, y*  beliebige reelle Zahlen *bzw.*
   
   hPunkt( *x, y, z* )     :math:`-x^2-y^2+z^2 = 1, z > 0`
                      hier sind *x* und *y* günstig als ganz bzw. rational 
                      anzugeben und *z* als :math:`sqrt(1 + x^2 + y^2)`

      hyperbolischer Punkt im H-Modell
	   
**Zusatz** `exakt=ja`   
        
    Die (euklidischen) Koordinaten des Punktes werden exakt gespeichert   
     
**Parameter**

   *x, y* bzw. *x, y, z* sind die euklidischen Koordinaten eines Punktes; sie können
   auch als *Vektor(x, y)* (D-Modell) bzw. *Vektor(x, y, z)* (H-Modell) angegeben 
   werden
   
   Ist bei der Erzeugung eines Punktes im D-Modell als drittes Argument `p` 
   angegeben, werden *x* und *y* als Polarkoordinaten *r* und *phi* (in Grad) 
   interpretiert
      
Die Randpunkte der Einheitskreisscheibe im D- und D3-Modell werden aus
technischen Gründen ebenfalls als hyperbolische Punkte betrachtet  

Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die
symbolische Berechnung kann mit der Angabe ``exakt=ja`` bzw. mittels der 
Systemvariablen ``UMG.EXAKT`` erreicht werden
  
    """   
		
		
    def __new__(cls, *args, h=None, exakt=False):  
		
        if h in (1, 2, 3):                         
            hPunkt_hilfe(h)		
            return	
								
        exakt = exakt or UMG.EXAKT
		
        try:
            if len(args) not in (1, 2, 3):		
                raise AglaError("1-3 Argumente angeben")
            if len(args) == 1:
                a = sympify(args[0])
                ok = False				
                if isinstance(a, Add) and a.has(I):
                    ok = True
                if not ok: 
                    if not (isinstance(a, (int, float, Rational, Float, \
                        complex)) or a.is_complex or isinstance(a, Vektor) and \
                        a.dim in (2, 3)):
                        raise AglaError("den Punkt als komplexe Zahl oder seine " + \
                             "Koordinaten einzeln bzw. als Vektor angeben")
                if isinstance(a, Vektor):
                    if a.dim == 2:
                        args = sympify(a.x), sympify(a.y)
                    else:					
                        args = sympify(a.x), sympify(a.y), sympify(a.z)	
                else:
                   args = re(a), im(a)				
            x, y = args[:2]
            if not (is_zahl(x) and is_zahl(y)): 			
                raise AglaError("die ersten beiden Argumente müssen Zahlen sein")
            if len(args) == 3:
                if type(args[2]) == str and not args[2] in ('d3', 'D3', 'h', 
				                                            'H', 'p', 'pol'):
                    print('agla: die Angabe zum Modell ist falsch')															              
                    return
                if args[2] in ('p', 'pol'):
                    if not mit_param(x) and (x < 0 or x > 1):
                        raise AglaError("r muss zwischen 0 und 1 liegen")				
                    xx = nsimplify(N(x*cosg(y), 12), rational=True)
                    yy = nsimplify(N(x*sing(y), 12), rational=True); print('000', xx, yy)
                    x, y = xx, yy
            z = None			
            spar = set() 
            if mit_param(x):
                spar = spar.union(x.free_symbols)			
            if mit_param(y):
                spar = spar.union(y.free_symbols)			
            if len(args) == 3 and args[2] not in ('D3', 'd3', 'H', 'h', 'p', \
                                                               'pol'):
                z = args[2]	
                if mit_param(z):
                    spar = spar.union(z.free_symbols)
            if len(args) == 2 or (len(args) == 3 and args[2] in (0, 'D3', 'd3')):
                txt = "kein Punkt der Einheitskreisscheibe"	
                if not (mit_param(x) or mit_param(y)):
                    if x**2+y**2 > 1+1e-8:
                        raise AglaError(txt)
                if not mit_param(x) and abs(x) > 1+1e-8:
                        raise AglaError(txt)
                if not mit_param(y) and abs(y) > 1+1e-8:
                        raise AglaError(txt)         				
                if len(args) == 2:
                    args_neu = x, y	
                else:					
                    args_neu = x, y, 0					
            elif len(args) == 3 and args[2] in ('p', 'pol', 'h', 'H'):
                if args[2] in ('p', 'pol'):			
                    args_neu = x, y	
                else:
                    args_neu = x, y, sqrt(1 + x**2 + y**2)	
            else:
                z = args[2]			
                if not is_zahl(z): 			
                    raise AglaError("für das dritte Argument Zahl angeben")				
                if not mit_param([x, y, z]):
                    if exakt:				
                        x, y, z = nsimplify(x), nsimplify(y), nsimplify(z)
                        if float(abs(nsimplify(-x**2 - y**2 + z**2 - 1))) > 1e-8:	
                            raise AglaError("kein Punkt der Hyperboloidschale")
                    else:	
                        if float(abs(-x**2 - y**2 + z**2 - 1)) > 1e-8:	
                            raise AglaError("kein Punkt der Hyperboloidschale")					
                args_neu = x, y, z	
            if exakt:				
                if len(args_neu) == 2:	
                    a = nsimplify(args_neu[0]), nsimplify(args_neu[1])				
                    return AglaObjekt.__new__(cls, se.sympify(a[0]), 					
					                          se.sympify(a[1]))			
                a = nsimplify(args_neu[0]), nsimplify(args_neu[1]), \
				    nsimplify(args_neu[2])				
                return AglaObjekt.__new__(cls, se.sympify(a[0]), 
                                          se.sympify(a[1]), se.sympify(a[2]))	
            a = args_neu
            if len(args_neu) == 2:	
                return AglaObjekt.__new__(cls, to_float(a[0]), to_float(a[1]))					
            return AglaObjekt.__new__(cls, to_float(a[0]), to_float(a[1]), 
			                               to_float(a[2]))					
        except AglaError as e:	
            print('agla:', str(e))
            return			
  			
		
    def __str__(self):  
        par = self.sch_par
		
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "hPunktSchar(" + ss + ")_" + '{' + self._mod +'}'
        return "hPunkt_" + '{' + self._mod +'}'			
				
			
		
# Eigenschaften und Methoden für hPunkt
# -------------------------------------
        
    @property
    def _mod(self):    # interne Eigenschaft
        """Modell"""
        if len(self.args) == 2:		
            return 'D'
        if not self.args[2]:		   
            return 'D3'
        return 'H'
		
    @property
    def mod(self):              
        """Modell"""
        return display(Math(self._mod))
		
    @property
    def dim(self):              
        """Euklidische Dimension"""
        if len(self.args) == 2:		
            return 2
        return 3

    @property
    def exakt(self):
        """Test auf exakte Koordinasten"""
        par = self.sch_par
        fl = float, Float		
        if not par:
            return type(self.args[0]) not in fl and type(self.args[1]) not in fl	
        b0 = any([type(self.args[0].subs(p, 1)) in fl for p in par])
        b1 = any([type(self.args[1].subs(p, 1)) in fl for p in par])	
        if b0 or b1:		
             return False		
        return True
		
    @property
    def sch_par(self):
        """Parameter einer Schar hyperbolischer Punkte"""
        return self.free_symbols
		
    schPar = sch_par		
	
    @property
    def traeger(self):
        """Euklidischer Trägerpunkt"""
        a = self.args	
        if self.exakt:		
            return Vektor(*a)
        return Vektor(*a, simpl=False)
	
    e = traeger
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar	
	
    def abstand(self, *punkt, **kwargs):	
        """hyperbolischer Abstand zu einem anderen Punkt"""
		
        if kwargs.get('h'):
            print("\nHyperbolischer Abstand des Punktes zu einem anderen Punkt\n")		
            print("Aufruf   hpunkt . abstand( hpunkt1 )\n")		                     
            print("             hpunkt      hyperbolischer Punkt\n")
            print("Zusatz       exakt=ja    exakte Berechnung\n")
            return
	
        if len(punkt) != 1:
            print('agla: einen anderen Punkt angeben')
            return
			
        p = punkt[0]			
        if not (isinstance(p, hPunkt) and p._mod == self._mod):
            print("agla: einen hyperbolischen Punkt im " + self._mod + \
                  "-Modell angeben")
            return				  
        if is_rand_pkt(self) or is_rand_pkt(p):
            return inf			
				  
        if self._mod.upper() in ('D', 'D3'):
            if not kwargs.get('exakt') and not mit_param(self) and not mit_param(p):
                diff = h2np(self) - h2np(p)		
                dist = np.arccosh(1 + (2*npbetrag(diff)**2)/((1 -
                        npbetrag(self)**2)*(1- npbetrag(p)**2))) 
                dist = float(dist)					   
            else:						
                diff = self.e - p.e						
                dist = se.acosh(1 + (2*sebetrag(diff)**2)/((1 - 
                       sebetrag(self)**2)*(1- sebetrag(p)**2)))
                dist = sympify(dist)
            if mit_param(dist):				
                return dist.n()
            return float(dist)				 
        else:
            if not kwargs.get('exakt') and not mit_param([self, p]):
                dist = npsigma(self, p)
                dist = float(dist)					   				
            else:
                dist = sesigma(self, p)
                dist = sympify(dist)				
            return dist				
			

    def schnitt(self, *obj, **kwargs):  
        """Schnitt mit hyperbolischer Geraden"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
				
        if kwargs.get('h'):
            print("\nSchnitt des hyperbolischen Punktes mit einer hyper-")
            print("bolischen Geraden\n")		
            print("Aufruf    hpunkt . schnitt( hgerade )\n")		                     
            print("              hpunkt    hyperbolischer Punkt")
            print("              hgerade   hyperbolische Gerade\n")
            return
				
        try:				
            if len(obj) != 1:
                raise AglaError('ein hyperbolisches Objekt angeben')
            obj = obj[0]
            if mit_param(self) or mit_param(obj):
                raise AglaError('nicht implementiert (Parameter)')
            if not isinstance(obj, hGerade):			 
                raise AglaError("hyperbolische Gerade angeben")
            if mit_param(obj):
                raise AglaError("nicht implementiert (Parameter)")
            if obj._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")            
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        S = obj.schnitt(self)
        return S

		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
        try:
		
            if not self.is_schar or len(self.sch_par) > 1:
                raise AglaError("keine Schar mit einem Parameter")			
		
            if kwargs.get('h'):
                print("\nElement einer Schar von hyperbolischen Punkten\n")		
                print("Aufruf   hpunkt . sch_el( wert )\n")		                     
                print("             hpunkt    hPunkt")
                print("             wert      Wert des Scharparameters")			
                print("\nEs ist nur ein Scharparameter zugelassen\n")    
                return 
			
            if not wert or len(wert) != 1:
                raise AglaError("einen Wert für den Scharparameter angeben")
        except AglaError as e:
            print('agla:', str(e))
            return
			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter \
			         angeben')	
            return		
        if self._mod in ('D', 'D3'):
            if self._mod == 'D':			
                a, b = self.args
            else:					
                a, b = self.args[:2]
            if mit_param(a):
                a = a.subs(p, wert)				 
            if mit_param(b):
                b = b.subs(p, wert)
            if a**2 + b**2 >= 1:
                print("agla: Parameterwert unzulässig")
                return				
            if self._mod == 'D':
                if self.exakt:			
                    return hPunkt(a, b)
                return hPunkt(N(a), N(b), exakt=False)
            else:					
                if self.exakt:			
                    return hPunkt(a, b, 0)
                return hPunkt(N(a), N(b), 0.0, exakt=False)
        else:
            a, b, c = self.args
            if mit_param(a):
                a = a.subs(p, wert)				 
            if mit_param(b):
                b = b.subs(p, wert)
            if mit_param(c):
                c = c.subs(p, wert)	
            if self.exakt:				
                return hPunkt(Vektor(a, b, c))             				 
            return hPunkt(Vektor(N(a), N(b), N(c)), exakt=False)             				 
			
    schEl = sch_el
		
				
    def graf(self, spez, **kwargs):                       
        """Grafikelement für hPunkt"""	
		
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        vv = self.e	
        vv.graf((None, spez[1], spez[2], None))
		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hPunkt_hilfe(3)	
		
    h = hilfe				
			    	
		

# Benutzerhilfe für hPunkt
# ------------------------

def hPunkt_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nhPunkt - Objekt     Hyperbolischer Punkt\n")
        print("Betrachtete Modelle der hyperbolischen Geometrie:\n")	
        print("   D  - EinheitsKreisScheiben-Modell in der Ebene R^2")
        print("   D3 - D-Modell in der xy-Ebene des R^3")
        print("   H  - HyperboloidHalbSchalen-Modell im R^3\n")	
        print("Erzeugung     hPunkt( x, y )    bzw.")
        print("              hPunkt( x + y*I ) mittels komplexer Zahlen\n")
        print("                  hyperbolischer Punkt im D-Modell; x^2+y^2 < 1\n")
        print("       oder   hPunkt( x, y, 0 )   bzw.")
        print("              hPunkt( x, y, 'D3' | 'd3' )\n")
        print("                  hyperbolischer Punkt im D3-Modell;  x^2+y^2 < 1\n")
        print("       oder   hPunkt( x, y, 'H' | 'h' )   x,y  beliebige reelle Zahlen")
        print("              hPunkt( x, y, z )         -x^2-y^2+z^2 = 1, z > 0")
        print("                      hier sind x und y günstig als ganz oder rational") 
        print("                      anzugeben und z als sqrt(1 + x^2 + y^2)\n")
        print("                  hyperbolischer Punkt im H-Modell\n")
        print("              x,y bzw. x,y,z sind die Euklidischen Koordinaten eines ")
        print("              Punktes; sie können auch als Vektor(x, y) (D-Modell) bzw.")
        print("              Vektor(x, y, z) (H-Modell) angegeben werden\n")
        print("              Ist bei der Erzeugung eines Punktes im D-Modell als")
        print("              drittes Argument 'p' angegeben, werden x und y als")
        print("              Polarkoordinaten r und phi (in Grad) interpretiert\n")	
        print("Die Randpunkte der Einheitskreisscheibe im D- und D3-Modell werden ")
        print("aus technischen Gründen ebenfalls als hyperbolische Punkte betrachtet\n") 
        print("Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die")
        print("symbolische Berechnung kann mit der Angabe exakt=ja erreicht werden\n")
        print("Zuweisung     hp = hPunkt(...)   (hp - freier Bezeichner)\n")
        print("Beispiele")
        print("hPunkt( 1/2, 1/3)") 
        print("hPunkt( 1/2 + 1/3*I, exakt=ja)") 
        print("hPunkt( 0.4, -0.25, 'D3' )")
        print("hPunkt( 0.4, -0.25, 'h' )\n")
        print("Gegenwärtig sind außer Punkten keine hyperbolischen Objekte mit")
        print("Parametern möglich\n") 		
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für hPunkt\n")
        print("hp.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("hp.abstand(...)  M  Hyperbolischer Abstand")	
        print("hp.dim              Euklidische Dimension")
        print("hp.e                = hp.träger")
        print("hp.exakt            Test auf exakte Koordinaten")
        print("hp.is_schar         Test auf Schar")
        print("hp.mod              Modell")
        print("hp.schnitt(...)  M  Schnitt mit anderem Objekt")	
        print("hp.sch_el(...)   M  Element einer Schar")
        print("hp.sch_par          Scharparameter")	
        print("hp.träger           Euklidischer Trägerpunkt\n")	
        print("Synonyme Bezeichner\n")
        print("hilfe    :  h")
        print("is_schar :  isSchar")
        print("sch_el   :  schEl")
        print("sch_par  :  schPar\n")		
        return
		
	    	
	
# hGerade - Klasse   
# ----------------
	
class hGerade(AglaObjekt):  

	
    """
  
hyperbolische Gerade

**Erzeugung** 
	
   hGerade ( *hpunkt1, hpunkt2* ) 
	 
**Parameter**

   *hpunkt* : hyperbolischer Punkt
   
Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die
symbolische Berechnung kann mit der Angabe ``exakt=ja`` bzw. mittels der 
Systemvariablen ``UMG.EXAKT`` erreicht werden
   
    """   
	
    def __new__(cls, *args, h=None, exakt=False):  
		
        if h in (1, 2, 3):                         
            hGerade_hilfe(h)		
            return	
								
        exakt = exakt or UMG.EXAKT 
							
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            A, B = args
            if not (isinstance(A, hPunkt) and isinstance(B, hPunkt)): 			
                raise AglaError("zwei hyperbolische Punkte angeben")
            if mit_param([A, B]):
                raise AglaError("nicht implementiert (Parameter)")			
            if not A._mod == B._mod: 			
                raise AglaError("zwei hyperbolische Punkte im selben Modell angeben")
            if A == B:
                raise AglaError("die Punkte müssen verschieden sein")
             						
            if exakt:
                if not (A.exakt and B.exakt):
                    raise AglaError('beide Punkte müssen exakt definiert sein')		
            else:
                if A.exakt:
                    A = to_float(A)			
                if B.exakt:
                    B = to_float(B)			
			
            if A._mod == 'D':  
                return cls._new_hgerade_d(cls, A, B, exakt)
            elif A._mod == 'D3':  
                return cls._new_hgerade_d3(cls, A, B)
            return cls._new_hgerade_h(cls, A, B)
        except AglaError as e:	
            print('agla:', str(e))
            return			


    def _new_hgerade_d(cls, A, B, exakt):  
	
        def schnitt_par(kk):
            S0, S1 = schnitt_kreis_kreis_float(kk, EinhKreis2) 
            t0, t1 = par_wert(kk, S0), par_wert(kk, S1) 
            m0, m1 = min(t0, t1), max(t0, t1)
            ber1 = [m0, m1]		
            if m1 - m0 > 180:		
                ber1 = [m1-360, m0]	
            return ber1, S0, S1		            
				
        AA, BB = A, B							
        A, B = A.e, B.e 
						
        # die Gerade ist ein Durchmesser					
        if A.kollinear(B):
            t = Symbol('t')				
            gg = Gerade(A, Vektor(A, B), t)   # Trägergerade
            pp = gg.pkt(t)
					
            # Geradenparameter für A, B
            ber0 = [0, 1]					
					
            # Geradenparameter für die Endpunkte
            x, y = symbols('x y')					
            gl = (x**2+y**2-1).subs({x:pp.x, y:pp.y})
            L = solve(gl, t, dict=True)		
            if mit_param([A, B]):
                ber1 = None 	
            else:				
                ber1 = [float(L[0][t]), float(L[1][t])]	
                if ber1[1] < ber1[0]:
                    ber1 = [ber1[1], ber1[0]]	
                else:
                    ber1 = [ber1[0], ber1[1]]						
            return AglaObjekt.__new__(cls, gg, AA, BB, ber0, ber1)	

        # Behandlung der Punkte (1,0), (0,1), (-1,0), (0,-1)		
        punkte = [Vektor(1, 0), Vektor(-1, 0), Vektor(0, -1)]
        pp = Vektor(0, 1)			
        if A in punkte and B in punkte:	
            mx = 1 if A.x + B.x > 0 else -1 			
            my = 1 if A.y + B.y > 0 else -1 
            M = Vektor(mx, my)
            kk = Kreis(M, 1)
            ber, R1, R2 = schnitt_par(kk)
        elif A == pp or B == pp:
            if B == pp:
                A, B = B, A
            a = symbols('a', real=True)  
            k = Kreis(Vektor(a, 1), a)
            gleich = k.gleich.lhs - a**2 
            x, y = symbols('x y')				
            gl = gleich.subs({x:B.x, y:B.y})
            L = loese(gl)
            kk = Kreis(Vektor(L[a], 1), L[a])
            ber1, R1, R2 = schnitt_par(kk)  	
            if abs(float(R1.abstand(A))) > 1e-6:
                R1, R2 =  R2, R1				
            if B.x > 0:
                b0, b1 = 180, par_wert(kk, B)
                if b1 > 360:
                    b1 -= 360
            else:					
                b0, b1 = [180, -180+par_wert(kk, B)]
                m0, m1 = 180, par_wert(kk, R2)+180
                if m1 > 360:
                    m1 -= 360					
                ber1 = sorted([m0, m1])
            ber0 = sorted([b0, b1])													
            return AglaObjekt.__new__(cls, kk, AA, BB, ber0, ber1)			
			
        # der Algorithmus basiert auf den MuPAD-Routinen von agla
        gr = 1e-8		
        if abs(abs((A.x)) - abs((B.x))) < gr and abs(A.y - B.y) < gr:            
            AE = c2v(cayley(v2c(A)))
            BE = c2v(cayley(v2c(B)))			
            ME = Vektor(0, 0)
            rE = ME.abstand(AE)
            kE = Kreis(ME, rE)    
            AE = kE.pkt(0)
            BE = kE.pkt(180)
            CE = kE.pkt(90)			
            AD = c2v(cayley_inv(v2c(AE)))
            BD = c2v(cayley_inv(v2c(BE)))
            CD = c2v(cayley_inv(v2c(CE)))
            x, y = symbols('x y')			
            MD = Vektor(x, y)
            gl = MD.abstand(AD).n()**2 - MD.abstand(BD).n()**2, \
                 MD.abstand(AD).n()**2 - MD.abstand(CD).n()**2
            L = loese(gl, dict=True)			
            MD = Vektor(0, L[y])
            rD = MD.abstand(AD)
            kD = Kreis(MD, rD)			
            t0, t1 = par_wert(kD, A), par_wert(kD, B)
            b0, b1 = min(t0, t1), max(t0, t1)
            ber0 = [b0, b1]	
            if b1 - b0 > 180:		
                ber0 = [b1-360, b0]
            t0, t1 = par_wert(kD, AD), par_wert(kD, BD)
            ber1 = sorted([t0, t1])				
            return AglaObjekt.__new__(cls, kD, AA, BB, ber0, ber1)	
		
        # der Algorithmus basiert auf den MuPAD-Routinen von agla		
        a, b = v2c(A), v2c(B)
        z = Symbol('z')
        gl = (1+z*conjugate(z))*(b*conjugate(a)-conjugate(b)*a) + \
             (1+a*conjugate(a))*(z*conjugate(b)-conjugate(z)*b) + \
             (1+b*conjugate(b))*(a*conjugate(z)-conjugate(a)*z)
        po = Poly(gl, z, conjugate(z))
        E = po.coeff_monomial(z*conjugate(z))
        F = po.coeff_monomial(z)
        G = po.coeff_monomial(1)
        if im(E) != 0:
            E, F, G = E/I, F/I, G/I	
        F1, F2 = re(conjugate(2*F)), im(conjugate(2*F))
        M = Vektor(-F1/2/E, -F2/2/E)
        r = Abs(sqrt((F1**2+F2**2-4*E*G)/4/E**2))
        kk = Kreis(M, r)			
        t0, t1 = par_wert(kk, A), par_wert(kk, B)
        b0, b1 = min(t0, t1), max(t0, t1)
        ber0 = [b0, b1]	
        if b1 - b0 > 180:		
            ber0 = [b1-360, b0]
        ber1 = schnitt_par(kk)[0]		
        return AglaObjekt.__new__(cls, kk, AA, BB, ber0, ber1)				
		

    def _new_hgerade_h(cls, A, B):  
        AA, BB = A, B	
        c = AA.abstand(BB)	
        t = Symbol('t')
        A, B = A.e, B.e
        p = sinh(c-t)/sinh(c)*A + sinh(t)/sinh(c)*B
        t0, t1 = 0, c		
        ber = [t0, t1]
        traeger = Kurve(p, (t, t0, t1) )		
        return AglaObjekt.__new__(cls, traeger, AA, BB, ber)				
		
    def _new_hgerade_d3(cls, A, B):
        AA, BB = A, B	
        A, B = D32D(A), D32D(B)    
        g = hGerade(A, B)
        k = g.traeger  
        if isinstance(k, Gerade):
            st, ri = D2D3(k.stuetz), D2D3(k.richt)		
            traeger = Gerade(st, ri)
        else:			
            M = D2D3(k.mitte)	
            traeger = Kreis(xy_ebene, M, k.radius)		
        return AglaObjekt.__new__(cls, traeger, AA, BB, g.args[3], g.args[4])				
            	
		  				
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "hGeradeSchar(" + ss + ")_" + '{' + self._mod +'}'
        return "hGerade_" + '{' + self._mod +'}'

		
		
# Eigenschaften und Methoden für hGerade
# --------------------------------------
		
    @property
    def mod(self):              
        """Modell"""
        return self.args[1].mod
		
    @property
    def exakt(self):    	
        """Test auf exakte Punkte"""
        if self._mod == 'H':
            return False		
        return all([self.args[i].exakt for i in (1, 2)])

    @property
    def _mod(self):    # interne Eigenschaft
        """Modell"""
        return self.args[1]._mod
		
    @property
    def dim(self):              
        """Euklidische Dimension"""
        return self.args[1].dim
    @property
	
    def is_schar(self):
        """Test auf Schar"""
        return False
		
    isSchar = is_schar		
	
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return set()
		
    schPar = sch_par		
	
    @property
    def traeger(self):	
        """Euklidisches Träger-Objekt"""
        return self.args[0]
		
    e = traeger

    @property
    def _traeger_eplus(self):	
        """Euklidischer Kreis oder Gerade im E+ -Modell; interne Eigenschaft
          E+  - obere Halbebene in R^2"""
		  
        # [Agricola S149]		  
        p1, p2 = self.punkte
        z1, z2 = cayley(v2c(p1.e)), cayley(v2c(p2.e))
        E, F, G = symbols('E F G')
        gl0 = E*abs(z)**2 + 2*F*re(z) + G
        gl = [ gl0.subs(z, z1), gl0.subs(z, z2) ]
        L = loese(gl, [E, F, G], dict=True) 
		
        try:
            if not mit_param(L[E]):	
                if abs(L[E]) < 1e-8:  # Gerade
                    E = 0
        except KeyError:
            E = 0
        if E == 0:			
            return Gerade(c2v(z1), Vektor(c2v(z1), c2v(z2), simpl=False))

        try:
            EE = L[E]
        except KeyError:
            EE = 0
        try:
            FF = L[F]
        except KeyError:
            FF = 0
        try:
            GG = L[G]
        except KeyError:
            GG = 0 
        if mit_param(EE) or mit_param(FF):
            E = EE.subs(G, 1)
            F = FF.subs(G, 1)
            G = 1
        else:
            E, F, G = EE, F, GG
        F1, F2 = re(conjugate(2*F)), im(conjugate(2*F))
        return Kreis(Vektor(-F1/2/E, -F2/2/E), sqrt((F1**2+F2**2-4*E*G)/4/E**2), simpl=False)
        	
    @property
    def par(self):	
        """Parameter"""
        return self.args[0].pkt().sch_par.pop()
	
    @property
    def ber(self):	
        """Parameterbereich"""
        if self._mod == 'H':
            return self.args[3]			
        return self.args[4]	

    @property
    def punkte(self):	
        """Erzeugende Punkte"""
        return self.args[1:3] 		
		
    def schnitt(self, *obj, **kwargs):  
        """Schnitt mit anderem hyperbolischen Objekt"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
				
        if kwargs.get('h'):
            print("\nSchnitt der hyperbolischen Geraden mit einem anderen")
            print("hyperbolischen Objekt\n")		
            print("Aufruf    hgerade . schnitt( hobjekt )\n")		                     
            print("              hgerade   hyperbolische Gerade")
            print("              hobjekt   hyperbolische(r) Punkt, Gerade\n")
            return
								
        try:				
            if len(obj) != 1:
                raise AglaError('ein hyperbolisches Objekt angeben')
            obj = obj[0]			 
            if not isinstance(obj, (hPunkt, hGerade)):			 
                raise AglaError("hyperbolische(n) Punkt oder Gerade angeben")
            if mit_param(obj):
                raise AglaError("nicht implementiert (Parameter)")
            if obj._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")            
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        if obj == self:		
            print("agla: die Geraden sind identisch")
            return		

        if self._mod == 'D3':
            AA, BB = self.punkte
            gg = hGerade(D32D(AA), D32D(BB))			
            if isinstance(obj, hPunkt):									
                SS = gg.schnitt(D32D(obj))
                if not SS:
                    return set()				
                return D2D3(SS)					
            CC, DD = obj.punkte			
            g1 = hGerade(D32D(CC), D32D(DD))	
            SS = gg.schnitt(g1)
            if not SS:
                return set()
            return D2D3(SS)				

        if self._mod == 'H':
            AA, BB = self.punkte
            gg = hGerade(H2D(AA), H2D(BB))			
            if isinstance(obj, hPunkt):									
                SS = gg.schnitt(H2D(obj))
                if not SS:
                    return set()				
                return D2H(SS)					
            CC, DD = obj.punkte			
            g1 = hGerade(H2D(CC), H2D(DD))	
            SS = gg.schnitt(g1)
            if not SS:
                return set()
            return D2H(SS)				
			     
        def nullify(v):
            g = 1e-8		
            x = re(v.x) if im (v.x) < g else v.x  
            y = re(v.y) if im (v.y) < g else v.y  
            return Vektor(x, y)			
										 
        if isinstance(obj, hPunkt):   
            k = self.args[0]	
            if isinstance(k, Kreis):			
                if k.schnitt(obj.e, exakt=False):
                    return obj
                return set()
            else:
                aa = float(abs(k.koord.lhs.subs({x:Q.x, y:Q.y})))			
                if aa < 1e-6 or aa == inf:				
                    return obj
                return set()
        elif isinstance(obj, hGerade):   	
            k1, k2 = self.traeger, obj.traeger
            S = k1.schnitt(k2, exakt=False)
            if not S:
                return set()
            elif isinstance(S, Vektor):
                if re(N(S.betrag)) <= 1:				
                    return hPunkt(nullify(S))
                else:					
                    return set()
            elif len(S) == 2:
                S1, S2 = nullify(S[0]), nullify(S[1])
                if re(N(S1.betrag)) <= 1:
                    return hPunkt(S1)
                elif re(N(S2.betrag)) <= 1:
                    return hPunkt(S2)
            else:					
                return set()
                						
		
    def winkel(self, *args, **kwargs):  
        """Winkel mit anderem hyperbolischen Objekt"""
		
        if kwargs.get('h'):
            print("\nWinkel der hyperbolischen Geraden mit einem anderen")
            print("hyperbolischen Objekt in einem gemeinsamen Punkt\n")		
            print("Aufruf    hgerade . winkel( hobjekt, hpunkt )\n")		                     
            print("              hobjekt   hyperbolische(r) Gerade, Strahl, Strecke")
            print("              hpunkt    hyperbolischer Punkt\n")
            print("Es wird nicht geprüft, ob der Punkt auf den beiden Objekten")
            print("liegt\n")
            return
				
        try:				
            if len(args) != 2:
                raise AglaError('hyperbolische(n) Gerade, Strahl, Strecke und Punkt angeben')
            gg, pp = args		 
            if not isinstance(gg, (hGerade, hStrahl, hStrecke)):			 
                raise AglaError("1. Argument hyperbolische(n) Gerade, Strahl oder " + \
	                            "Strecke angeben")
            if not isinstance(pp, hPunkt):			 
                raise AglaError("2. Argument hyperbolischen Punkt " + \
	                            "angeben")
            if gg._mod != self._mod or pp._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")            
        except AglaError as e:
            print('agla:', str(e))
            return	
		
        if gg == self:		
            print("agla: die Ojekte sind identisch")
            return		
		
        if isinstance(gg, (hStrahl, hStrecke)):
            return gg.winkel(self, pp)
			
        if self._mod in ('D', 'D3'):	
		
            if is_rand_pkt(pp):	  
                return 0		
				
            # Berechnung mit Hilfe der Kreistangenten 		
            def tang_vekt(hgerade, hpunkt):
                tr = hgerade.traeger		
                if isinstance(tr, Gerade):
                    return tr.richt			
                vv = hpunkt.e - tr.mitte
                return Vektor(vv.y, -vv.x, simpl=False) 
			
            tv1 = tang_vekt(self, pp)			
            tv2 = tang_vekt(gg, pp)	
            wi = tv1.winkel(tv2)
            if wi > 90:
                wi = 180 - wi		
            return wi		
			
        else:   # 'H'
		
            A = pp		
            B = self.punkte[0]
            if (B.e - A.e).betrag < 1e-8:
                B = self.punkte[1]	
            C = gg.punkte[0]
            if (A.e - C.e).betrag < 1e-8:
                C = gg.punkte[1]	
            c =	A.abstand(B)
            b = A.abstand(C)
            si = - sesigma(	(B.e-A.e*cosh(c)) / sinh(c), (C.e-A.e*cosh(b)) / sinh(b) )
            wi = arccosg(si).n()			
            if wi > 90:
                wi = 180 - wi		
            return wi		
							
	
    def normale(self, *hpunkt, **kwargs): 
        """Normale in einem Punkt der hyperbolischen Geraden"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
				
        if kwargs.get('h'):
            print("\nNormale in einem Punkt der hyperbolischen Geraden\n")
            print("Aufruf    hgerade . normale( hpunkt )\n")		                     
            print("              hgerade   hyperbolische Gerade")
            print("              hpunkt    hyperbolischer Punkt\n")
            return
				
        try:				
            if len(hpunkt) != 1:
                raise AglaError('einen hyperbolischen Punkt angeben')
            hpunkt = hpunkt[0]			 
            if not isinstance(hpunkt, hPunkt):			 
                raise AglaError("hyperbolischen Punkt angeben")
            if mit_param(hpunkt):
                raise AglaError("nicht implementiert (Parameter)")					
            if hpunkt._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")  
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        if self._mod == 'D3':
            P, Q = self.punkte
            P, Q = D32D(P), D32D(Q)
            self = hGerade(P, Q)
            hpunkt = D32D(hpunkt)
            g = self.normale(hpunkt)
            b0, b1 = g.ber			
            P = hPunkt(g.e.pkt(b0+0.25*(b1-b0)))
            Q = hPunkt(g.e.pkt(b0+0.75*(b1-b0)))
            P, Q = D2D3(P), D2D3(Q)   
            return hGerade(P, Q)	
			
        if self._mod == 'H':
            print('agla: lange Rechenzeit')		
            P, Q = self.punkte
            P, Q = H2D(P), H2D(Q)
            self = hGerade(P, Q)
            hpunkt = H2D(hpunkt)
            g = self.normale(hpunkt)
            b0, b1 = g.ber			
            P = hPunkt(g.e.pkt(b0+0.25*(b1-b0)))
            Q = hPunkt(g.e.pkt(b0+0.75*(b1-b0)))
            P, Q = D2H(P), D2H(Q)   
            return hGerade(P, Q)			
			
        if is_rand_pkt(hpunkt):
            print('agla: keine Normale (Randpunkt)')
			
        g = self.traeger		
        if isinstance(g, Gerade):
            if hpunkt.e.abstand(g).n() > 1e-8:
                print('agla: keine Normale (der Punkt liegt nicht auf der Geraden)')	
                return				
            if N(hpunkt.e.betrag) < 1e-8:   # Ursprung
                P = g.pkt(0.5)
                if N(P.abstand(hpunkt.e)) < 1e-8:
                   P = g.pkt(0.3)
                P2 = P.bild(drehung(Vektor(0, 0), 90))
                P1, P2 = hpunkt, hPunkt(P2)
                return hGerade(P1, P2)
			
        kk = self._traeger_eplus        		
        z = N(cayley(hpunkt.args[0] + hpunkt.args[1]*1j))   # Berechnung im E+ -Modell
        if abs(kk.mitte.abstand(c2v(z)).n() - kk.radius.n()) > 1.e-8:
            print('agla: keine Normale (der Punkt liegt nicht auf der Geraden)')	
            return				
		
        a, b = re(z), im(z)
		
        if isinstance(kk, Gerade):
            q1, q2 = a-b, a+b
            p1, p2 = cayley_inv(q1), cayley_inv(q2)
            if re(N(abs(p1-p2))) > 2 - 1e-8:   # die Punkte liegen diametral		
                A1, B1 = hpunkt, hPunkt(0, 0)  
            else:			
                A1 = hPunkt(re(p1), im(p1))
                B1 = hPunkt(re(p2), im(p2))
            return hGerade(A1, B1)
						
        # die Bestimmungsgleichungen für den gesuchten Kreis	
        #    gl = [ (M-a)**2 + b**2 - R**2, (m-a)*(M-a) + b**2 ]
        #         ( (a,b) liegt auf dem Kreis; die Tangentialvektoren in 
        #            diesem Punkt  sind orthogonal	)
        # sind gut per Hand lösbar
		
        m = kk.mitte.x		
        M = N(a - b**2/(m-a))
        R = N(sqrt((M-a)**2 + b**2))
        q1, q2 = M-R, M+R
        p1, p2 = cayley_inv(q1), cayley_inv(q2)
        im1 = im(p1)
        if N(abs(im1)) < 1e-8:
            im1 = 0
        im2 = im(p2)
        if N(abs(im2)) < 1e-8:
            im2 = 0		
        A1 = hPunkt(N(re(p1)), N(im1))
        B1 = hPunkt(N(re(p2)), N(im2))
        return hGerade(A1, B1)
		
		
    def lot(self, *hpunkt, **kwargs):    
        """Lot auf die Gerade von einem Punkt"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
				
        if kwargs.get('h'):
            print("\nLot auf die hyperbolische Gerade von einem Punkt\n")
            print("Aufruf    hgerade . lot( hpunkt )\n")		                     
            print("              hgerade   hyperbolische Gerade")
            print("              hpunkt    hyperbolischer Punkt\n")
            print("Bei der Angabe f=1  Rückgabe des Lotfußpunktes\n")			
            return
				
        try:				
            if len(hpunkt) != 1:
                raise AglaError('einen hyperbolischen Punkt angeben')
            hpunkt = hpunkt[0]			 
            if not isinstance(hpunkt, hPunkt):			 
                raise AglaError("hyperbolischen Punkt angeben")
            if mit_param(hpunkt):
                raise AglaError("nicht implementiert (Parameter)")					
            if hpunkt._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")  
        except AglaError as e:
            print('agla:', str(e))
            return	

        if self._mod == 'D3':
            print('agla: lange Rechenzeit')		
            P, Q = self.punkte
            P, Q = D32D(P), D32D(Q)
            self = hGerade(P, Q)
            hpunkt = D32D(hpunkt)
            g = self.lot(hpunkt)
            if kwargs.get('f'):
                F = self.lot(hpunkt, f=1)
                return D2D3(F)				
            b0, b1 = g.ber			
            P = hPunkt(g.e.pkt(b0+0.25*(b1-b0)))
            Q = hPunkt(g.e.pkt(b0+0.75*(b1-b0)))
            P, Q = D2D3(P), D2D3(Q)   
            return hGerade(P, Q)			

        if self._mod == 'H':
            print('agla: lange Rechenzeit')		
            P, Q = self.punkte
            P, Q = H2D(P), H2D(Q)
            self = hGerade(P, Q)
            hpunkt = H2D(hpunkt)
            g = self.lot(hpunkt)
            if kwargs.get('f'):
                F = self.lot(hpunkt, f=1)
                return D2H(F)				
            b0, b1 = g.ber			
            P = hPunkt(g.e.pkt(b0+0.25*(b1-b0)))
            Q = hPunkt(g.e.pkt(b0+0.75*(b1-b0)))
            P, Q = D2H(P), D2H(Q)   
            return hGerade(P, Q)		

        z1 = cayley(N(hpunkt.e.x + hpunkt.e.y*1j))			
        kk = self._traeger_eplus
        z2 = cayley(N(kk.mitte.x + kk.mitte.y*1j))			
        if isinstance(kk, Gerade):
            d = kk.abstand(hpunkt.e)
        else:			
            d = re(Abs(z1 - z2) - kk.radius)
        if Abs(re(N(d))) < 1e-8:
            print('agla: es kann kein Lot berechnet werden (Geradenpunkt)')
            return			
        if isinstance(kk, Gerade):
            S = kk.schnitt(Gerade(Vektor(0, 0), Vektor(1, 0)))
            R = N(abs(S.x - z1))
            Q1, Q2 = cayley_inv(S.x - R), cayley_inv(S.x + R)
            P1, P2 = hPunkt(re(Q1), im(Q1)), hPunkt(re(Q2), im(Q2))
            if kwargs.get('f'):
                Q = S.x + R*1j
                P = cayley_inv(Q)
                return hPunkt(re(P), im(P))				
            return hGerade(P1, P2)
        m = kk.mitte.x + kk.mitte.y*1j
        r = N(kk.radius)			
        if abs(Abs(z1-m) - r) < 1e-8:
            ta = Gerade(re(z1)-re(m), im(z1)-im(m), -re(m)*(re(z1)-re(m))- \
                                       im(m)*(im(z1)-im(m))-r**2)            		
            S = ta.schnitt(Gerade(Vektor(0, 0), Vektor(1, 0)))
            R = Abs(S.x - z1)		
            Q1, Q2 = cayley_inv(N(S.x - R)), cayley_inv(N(S.x + R))
            P1, P2 = hPunkt(re(Q1), im(Q1)), hPunkt(re(Q2), im(Q2))	
            if kwargs.get('f'):
                return hpunkt				
            return hGerade(P1, P2)
        else:		
            pp = hpunkt
            qq = self.inv(pp)
            z1, z2 = cayley(N(pp.args[0]+pp.args[1]*1j)), \
                           cayley(N(qq.args[0]+qq.args[1]*1j))
            P, Q = Vektor(re(z1), im(z1), simpl=False),  \
			       Vektor(re(z2), im(z2), simpl=False)
            g = Gerade(P, Vektor(P, Q, simpl=False))
            M = 1/2*(P + Q)
            nn = Gerade(M, Vektor(-g.richt.y, g.richt.x))
            S = nn.schnitt(Gerade(Vektor(0, 0), Vektor(1, 0)))
            R = re(N(abs(S.x - z1)))
            if kwargs.get('f'):	
                S = S.einfach.dez	
                R = N(simplify(R))				
                k1 = Kreis(S, R)				
                S = kk.schnitt(k1, exakt=False)
                S1, S2 = S				
                ss = cayley_inv(	S1.x+S1.y*I)
                if abs(N(ss)) < 1:				
                    F = Vektor(N(re(ss)), N(im(ss)), simpl=False)
                else:					
                    ss = cayley_inv(S2.x+S2.y*I)
                    F = Vektor(N(re(ss)), N(im(ss)), simpl=False)
                return hPunkt(F)
            w1, w2 = cayley_inv(S.x + R), cayley_inv(S.x - R)
            PP, QQ = hPunkt(N(re(w1)), N(im(w1))), hPunkt(N(re(w2)), N(im(w2)))
            return hGerade(PP, QQ)   		
				
				
    def inv(self, *obj, **kwargs): 
        """Inversion eines hyperbolischen Objektes an der Geraden"""
		
        if self._mod in ('D3', 'H'):
            print("agla: nur im D-Modell implementiert")	
            return			
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")	
            return			
		
        if kwargs.get('h'):
            print("\nInversion eines hyperbolischen Objektes an der hyperbolischen Geraden\n")
            print("Aufruf    hgerade . inv( hobjekt )\n")		                     
            print("              hgerade   hyperbolische Gerade")
            print("              hobjekt   hyperbolischer Punkt, Gerade, Strecke, Dreieck\n")
            return
				
        try:				
            if len(obj) != 1:
                raise AglaError('ein hyperbolisches Objekt angeben')
            obj = obj[0]			 
            if not isinstance(obj, (hPunkt, hGerade, hStrecke, hDreieck)):			 
                raise AglaError("hyperbolisches Objekt angeben")
            if mit_param(obj):
                raise AglaError("nicht implementiert (Parameter)")					
            if obj._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")  
        except AglaError as e:
            print('agla:', str(e))
            return	

        tr = self.traeger   
        		
        # Berechnung im D-Modell
		
        def inv_punkt(punkt, tr):	
            punkt = punkt.e
            if isinstance(tr, Gerade):
                q = punkt.bild(spiegelung(tr))
                return hPunkt(q)
            g = Gerade(punkt, Vektor(punkt, tr.mitte))
            t = Symbol('t')		
            r = g.pkt(t)	
			
            # [Rosebrock S143]			
            L = solve(N((punkt.abstand(tr.mitte) * r.abstand(tr.mitte) - \
                     tr.radius**2)), dict=True)    					 
            t1, t2 = L[0][t], L[1][t]
            if g.pkt(t1).betrag <= 1:
                return hPunkt(g.pkt(t1), exakt=True)		
            return hPunkt(g.pkt(t2), exakt=True)	

        if isinstance(obj, hPunkt):			
            return inv_punkt(obj, tr)	
        elif isinstance(obj, hGerade):	
            p0, p1 = obj.punkte
            q0, q1 = inv_punkt(p0, tr), inv_punkt(p1, tr)
            return hGerade(q0, q1)
        elif isinstance(obj, hStrecke):		
            p0, p1 = obj.punkte
            q0, q1 = inv_punkt(p0, tr), inv_punkt(p1, tr)
            return hStrecke(q0, q1)
        elif isinstance(obj, hDreieck):
            p0, p1, p2 = obj.punkte
            q0, q1, q2 = inv_punkt(p0, tr), inv_punkt(p1, tr), inv_punkt(p2, tr)
            return hDreieck(q0, q1, q2)
				
    spieg = inv				
		
    def inv_f(self, *args, **kwargs): 
        """Abbildungsfunktion zur Inversion eines hyperbolischen Punktes
             an der Geraden"""
		
        if self._mod in ('D3', 'H'):
            print("agla: nur im D-Modell implementiert")	
            return			
		
        if kwargs.get('h'):
            print("\nAbbildungsfunktion zur Inversion eines hyperbolischen Punktes")
            print("mittels der Geraden\n")		
            print("Aufruf    hgerade . inv_f( /[ hpunkt ] )\n")		                     
            print("              hgerade   hyperbolische Gerade")
            print("              hpunkt    hyperbolischer Punkt\n")
            print("Rückgabe  Wird kein Argument angegeben, wird die Abbildungs-")
            print("          funktion als Funktionsobjekt ausgegeben\n")
            print("          Bei Angabe eines hyperbolischen Punktes wird dessen Bild")
            print("          bei der Abbildung ausgegeben\n") 			
            print("          Bei Angabe von f=1 wird die Funktionsvorschrift")
            print("          als komplexe Funktion in der Variablen z angezeigt,")
            print("          bei fd=1 erfolgt die Anzeige dezimal\n")
            return
        
        try:	
            hpunkt = None		 
            if not len(args) in (0, 1):
                raise AglaError('höchstens ein Argument angeben')
            if len(args) == 1:	
                hpunkt = args[0]			 
                if not isinstance(hpunkt, hPunkt):			 
                    raise AglaError("hyperbolischen Punkt angeben")
                if hpunkt._mod != self._mod:	    				
                    raise AglaError("Punkt und Gerade sind aus verschiedenen Modellen")  
        except AglaError as e:
            print('agla:', str(e))
            return	

        v2c = lambda v: v.x + v.y*I			
        tt = self.traeger   
        if isinstance(tt, Gerade):
            c = v2c(tt.norm * I) 
            f = nsimplify(c*conjugate(z)/conjugate(c))
            F = lambda z: f   
        else:   
            c = v2c(tt.mitte) * (-I)   # /I = -I
            f = nsimplify((c*conjugate(z)+I) / (-I*conjugate(z)+conjugate(c)))
            F = lambda z: f
        if not hpunkt and not kwargs:
            return F			
        if hpunkt: 
            return self.inv(hpunkt)			
        else:			
            if kwargs.get('f'):
                return f	
            if kwargs.get('fd'):
                return N(f)	
	
    invF = inv_f	
	
	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für hGerade"""	
        if self.dim == 3:
            return self.graf3(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für hGerade in R^2"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]			
        k0 = self.traeger
        ber = sorted(self.ber)
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
        t = Symbol('t')
        kk = Kurve(k0.pkt(t), (t, ber[0], ber[1]))
        kk.graf2((None, spez[1], spez[2], None))
	
    def graf3(self, spez, **kwargs):                       
        """Grafikelement für hGerade in R^3"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        t = Symbol('t')															
        p = self.traeger.pkt(t)		
        if self._mod == 'D3':		
            t0, t1 = self.ber	
        else:   # H	
            zo = UMG._sicht_box[-1] 
            ber = solve(p.z - zo) 
            reell = [not im(z) for z in ber]		
            if 	not all(reell) or len(ber) < 2:
                return None		
            t0, t1 = min(ber), max(ber)				
        traeger = Kurve(p, (t, t0, t1) )	
        traeger.mayavi((None, spez[1], spez[2], None))


    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hGerade_hilfe(3)	
		
    h = hilfe		



# Benutzerhilfe für hGerade
# -------------------------

def hGerade_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nhGerade - Objekt     Hyperbolische Gerade\n")
        print("Erzeugung     hGerade( hpunkt1, hpunkt2 )\n")
        print("                  hpunkt   hyperbolischer Punkt\n")
        print("Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die")
        print("symbolische Berechnung kann mit der Angabe  exakt=ja erreicht werden\n")
        print("Zuweisung     hg = hGerade(...)   (hg - freier Bezeichner)\n")
        print("Beispiel")
        print("A = hPunkt(-0.2, 0.5); B = hPunkt(0.4, 0.1)")		
        print("hGerade( A, B )\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für hGerade\n")
        print("hg.hilfe           Bezeichner der Eigenschaften und Methoden")
        print("hg.ber             Parameterbereich")	
        print("hg.dim             Euklidische Dimension")
        print("hg.e               = hg.träger")
        print("hg.exakt           Test auf exakte Berechnung")
        print("hg.inv(...)     M  Inversion eines hyperbolischen Objektes (nur D-Modell)")
        print("hg.inv_f(...)   M  Abb.Funktion zur Inversion eines hyp. Punktes (ebenso)")
        print("hg.lot(...)     M  Lot von einem Punkt")
        print("hg.mod             Modell")
        print("hg.normale(...) M  Normale in einem Geradenpunkt")
        print("hg.par             Parameter")
        print("hg.punkte          Erzeugende Punkte")
        print("hg.schnitt(...) M  Schnitt mit anderem Objekt")	
        print("hg.spieg(...)   M  = hg.inv(...)")
        print("hg.träger          Euklidisches Träger-Objekt")
        print("hg.winkel(...)  M  Winkel mit anderem Objekt\n")	
        print("Synonyme Bezeichner\n")
        print("hilfe :  h")
        print("inv_f :  invF\n")
        return
		
	
	
# hStrahl - Klasse   
# ----------------
	
class hStrahl(AglaObjekt):                                      
    """
   
hyperbolischer Strahl

**Synonym**

   **hHalbGerade**

**Erzeugung** 
	
   hStrahl ( *hpunkt1, hpunkt2* ) 
	 
**Parameter**

   *hpunkt* : hyperbolischer Punkt
   
   einer der Punkte muss Randpunkt sein, der andere nicht
   
Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die
symbolische Berechnung kann mit der Angabe ``exakt=ja`` bzw. mittels der 
Systemvariablen ``UMG.EXAKT`` erreicht werden
   
    """  
	
	
    def __new__(cls, *args, h=None, exakt=False):  
		
        if h in (1, 2, 3):                         
            hStrahl_hilfe(h)		
            return	
								
        exakt = exakt or UMG.EXAKT 
  
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            A, B = args
            if not (isinstance(A, hPunkt) and isinstance(B, hPunkt)): 			
                raise AglaError("zwei hyperbolische Punkte angeben")
            if A._mod in ('D', 'D3'):			
                if not ((is_rand_pkt(A) and not is_rand_pkt(B)) or \
                       (is_rand_pkt(B) and not is_rand_pkt(A))):
                    print('agla: Einer der Punkte muss Randpunkt sein, der andere nicht')		
                    return				
            if mit_param(A) or mit_param(B):
                raise AglaError("nicht implementiert (Parameter)")             			
            if not A._mod == B._mod: 			
                raise AglaError("zwei hyperbolische Punkte im selben Modell angeben")
            if A == B:
                raise AglaError("die Punkte müssen verschieden sein")
            if exakt:
                if not (A.exakt and B.exakt):
                    raise AglaError('beide Punkte müssen exakt definiert sein')		
            else:
                if A.exakt:
                    A = to_float(A)			
                if B.exakt:
                    B = to_float(B)				
        except AglaError as e:	
            print('agla:', str(e))
            return
						
        if A._mod == 'D':		
            gg = hGerade(A, B, exakt=exakt)
            ber = gg.args[3]
            k = gg.traeger			
            return AglaObjekt.__new__(cls, k, A, B, ber)		
        elif A._mod == 'D3':		
            AA, BB = D32D(A), D32D(B)			
            gg = hGerade(AA, BB)
            ber = gg.args[3]
            k = gg.traeger
            M = Vektor(k.mitte.x, k.mitte.y, 0)
            kk = Kreis(xy_ebene, M, k.radius)			
            return AglaObjekt.__new__(cls, kk, A, B, ber)					
        else:
            c = A.abstand(B)	
            t = Symbol('t')
            p = sinh(c-t)/sinh(c)*A.e + sinh(t)/sinh(c)*B.e
            t0, t1 = 0, c		
            ber = [t0, t1]
            traeger = Kurve(p, (t, t0, t1) )		
            return AglaObjekt.__new__(cls, traeger, A, B, ber)				
			        		
				
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "hStrahlSchar(" + ss + ")_" + '{' + self._mod + '}'
        return "hStrahl_" + '{' + self._mod + '}'			
		
		
# Eigenschaften und Methoden für hStrahl
# --------------------------------------
		
    @property		
    def exakt(self):        
        """Test auf exakte Punkte"""
        return all([self.args[i].exakt for i in (1, 2)])
		
    @property		
    def mod(self):              
        """Modell"""
        return self.args[1].mod

    @property
    def _mod(self):    
        """Modell"""
        return self.args[1]._mod
			
    @property
    def dim(self):              
        """Euklidische Dimension"""
        return self.args[1].dim
		
    @property
    def is_schar(self):
        """Parameter einer Schar"""
        return False
		
    isSchar = is_schar		
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return set()

    schPar = sch_par
	
    @property
    def gerade(self):	
        """hyperbolische Trägergerade"""
        A, B = self.args[1:3]
        return hGerade(A, B)		
		
    @property
    def traeger(self):	
        """Euklidisches Träger-Objekt"""
        return self.gerade.traeger	
		
    e = traeger

    @property
    def par(self):	
        """Parameter"""
        return self.args[0].pkt().sch_par.pop()
	
    @property
    def ber(self):	
        """Parameterbereich"""
        ber = self.args[3]	
        return [float(ber[0]), float(ber[1])] 		

    @property
    def punkte(self):	
        """Erzeugende Punkte"""
        return self.args[1:3] 		
			

    def normale(self, *punkt, **kwargs):       
        """Normale in einem Strahlpunkt"""
		
        if kwargs.get('h'):
            print("\nNormale in einem Punkt des hyperbolischen Strahls\n")		
            print("Aufruf    hstrahl . normale( hpunkt )\n")		                     
            print("              hstrahl   hyperbolischer Strahl")
            print("              hpunkt    hyperbolischer Punkt\n")
            return
				
        try:				
            if not len(punkt) == 1:
                raise AglaError('einen hyperbolischen Punkt angeben')
            p = punkt[0]
            if not isinstance(p, hPunkt):
                raise AglaError('einen hyperbolischen Punkt angeben')
            if p._mod != self._mod:
                raise AglaError('der Punkt muss im selben Modell sein')
            if mit_param(p):
                raise AglaError('nicht implementiert (Parameter)')
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        if self._mod in ('D', 'D3') and is_rand_pkt(p):
            print("agla: keine Normale (Randpunkt)")
            return	
        if self._mod == 'H':
            print("agla: keine Prüfung, ob der Punkt auf dem Strahl liegt")
			
        g = self.gerade
        return g.normale(p)
				
		
    def winkel(self, *args, **kwargs):
        """Winkel mit anderem hyperbolischen Objekt"""
		
        if kwargs.get('h'):
            print("\nWinkel des hyperbolischen Strahls mit einem anderen hyperboli-")
            print("schen Objekt in einem gemeinsamen Punkt\n")		
            print("Aufruf    hstrahl . winkel( hobjekt, hpunkt )\n")		                     
            print("              hstrahl    hyperbolischer Strahl")
            print("              hobjekt    hyperbolische(r) Gerade, Strahl, Strecke")
            print("              hpunkt     hyperbolischer Punkt\n")
            print("Es wird nicht geprüft, ob der Punkt zu den beiden Objekten")
            print("gehört\n")
            return
				
        try:				
            if len(args) != 2:
                raise AglaError('hyperbolische(n) Gerade, Strahl, Strecke und Punkt angeben')
            ss, pp = args		 
            if not isinstance(ss, (hGerade, hStrahl, hStrecke)):			 
                raise AglaError("1. Argument hyperbolische Gerade, Strahl oder Strecke" + \
	                            "angeben")
            if not isinstance(pp, hPunkt):			 
                raise AglaError("2. Argument hyperbolischen Punkt " + \
	                            "angeben")
            if mit_param(ss) or mit_param(pp):
                raise AglaError("nicht implementiert (Parameter)")    			
            if ss._mod != self._mod or pp._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")            
        except AglaError as e:
            print('agla:', str(e))
            return
			
        if ss == self:		
            print("agla: die Strahlen sind identisch")
            return
			
        if self._mod in ('D', 'D3') and is_rand_pkt(pp):
            return 0
						
        if isinstance(ss, (hStrahl, hStrecke)):
            g1, g2 = self.gerade, ss.gerade
        else:			
            g1, g2 = self.gerade, ss
        wi = g1.winkel(g2, pp).n()		
        if wi > 90:
            wi = 180 - wi		
        return wi		
        
		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für hStrahl"""	
        if self.dim == 3:
            return self.graf3(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für hStrahl in R^2"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        k0 = self.args[0]		
        if isinstance(k0, Gerade):
            A, B = self.args[1:3]		
            kk = Strecke(A.e, B.e)       		
        else:	
            ber = self.args[3]
            kk = k0.bogen(ber[0], ber[1])
        kk.graf2((None, spez[1], spez[2], None))
		
    def graf3(self, spez, **kwargs):                       
        """Grafikelement für hStrahl in R^3"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        t = Symbol('t')															
        p = self.traeger.pkt(t)		
        if self._mod == 'D3':		
            t0, t1 = self.ber	
        else:   # H	
            zo = UMG._sicht_box[-1] 
            ber = solve(p.z - zo) 
            reell = [not im(z) for z in ber]		
            if 	not all(reell) or len(ber) < 2:
                return None		
            t0, t1 = min(ber), max(ber)				
        traeger = Kurve(p, (t, t0, t1) )	
        traeger.mayavi((None, spez[1], spez[2], None))
															
																
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hStrahl_hilfe(3)	
		
    h = hilfe		

	
def hStrahl_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nhStrahl - Objekt     Hyperbolischer Strahl\n")
        print("Erzeugung     hStrahl( hpunkt1, hpunkt2 )\n")
        print("                  hpunkt   hyperbolischer Punkt\n")
        print("                  einer der Punkte muss Randpunkt sein, der")
        print("                  andere nicht\n")
        print("Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die")
        print("symbolische Berechnung kann mit der Angabe  exakt=ja erreicht werden\n")		
        print("Zuweisung     hs = hStrahl(...)   (hs - freier Bezeichner)\n")
        print("Beispiel")
        print("A = hPunkt(-0.2, 0.5); B = hPunkt(0.4, sqrt(1-0.4^2))")		
        print("hStrahl( A, B )\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für hStrahl\n")
        print("hs.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("hs.ber               Parameterbereich")
        print("hs.dim               Euklidische Dimension")
        print("hs.e                 = hs.träger")
        print("hs.exakt             Test auf exakte Berechnung")
        print("hs.gerade            hyperbolische Trägergerade")
        print("hs.mod               Modell")
        print("hs.normale(...)   M  Normale in einem Strahlpunkt")
        print("hs.punkte            Erzeugende Punkte")
        print("hs.träger            Euklidisches Träger-Objekt")
        print("hs.winkel(...)    M  Winkel mit anderem Objekt\n")	
        print("Synonymer Bezeichner\n")
        print("hilfe      :  h\n")
        return

			
		
# hStrecke - Klasse   
# -----------------
	
class hStrecke(AglaObjekt):                                      
    """
   
hyperbolische Strecke

**Erzeugung** 
	
   hStrecke ( *hpunkt1, hpunkt2* ) 
	 
**Parameter**

   *hpunkt* : hyperbolischer Punkt
      
Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die
symbolische Berechnung kann mit der Angabe ``exakt=ja`` bzw. mittels der 
Systemvariablen ``UMG.EXAKT`` erreicht werden
	  
    """   
	
	
    def __new__(cls, *args, h=None, exakt=False):  
		
        if h in (1, 2, 3):                         
            hStrecke_hilfe(h)		
            return	
								
        exakt = exakt or UMG.EXAKT 
 
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            A, B = args
            if not (isinstance(A, hPunkt) and isinstance(B, hPunkt)): 			
                raise AglaError("zwei hyperbolische Punkte angeben")
            if mit_param(A) or mit_param(B):
                raise AglaError("nicht implementiert (Parameter)")             			
            if not A._mod == B._mod: 			
                raise AglaError("zwei hyperbolische Punkte im selben Modell angeben")
            if A == B:
                raise AglaError("die Punkte müssen verschieden sein")
				
            if exakt:
                if not (A.exakt and B.exakt):
                    raise AglaError('beide Punkte müssen exakt definiert sein')		
            else:
                if A.exakt:
                    A = to_float(A)			
                if B.exakt:
                    B = to_float(B)							
        except AglaError as e:	
            print('agla:', str(e))    
            return
			
        if A._mod == 'D':		
            if is_rand_pkt(A) or is_rand_pkt(B):	
                print("agla: keine hyperbolische Strecke mit diesen Endpunkten (Randpunkt/e)")
                return		
            gg = hGerade(A, B, exakt=exakt)
            ber = gg.args[3]
            k = gg.traeger			
            return AglaObjekt.__new__(cls, k, A, B, ber)				
        elif A._mod == 'D3':
            AA, BB = D32D(A), D32D(B)
            ss = hStrecke(AA, BB)
            ber = ss.args[3]
            tr = ss.traeger
            if isinstance(tr, Gerade):
                st, ri = D2D3(tr.stuetz), D2D3(tr.richt)
                traeger = Gerade(st, ri) 
            else:				      
                M = D2D3(tr.mitte)
                traeger = Kreis(xy_ebene, M, tr.radius)			
            return AglaObjekt.__new__(cls, traeger, A, B, ber)							
        else:
            c = A.abstand(B)	
            t = Symbol('t')
            p = sinh(c-t)/sinh(c)*A.e + sinh(t)/sinh(c)*B.e
            t0, t1 = 0, c		
            ber = [t0, t1]
            traeger = Kurve(p, (t, t0, t1) )		
            return AglaObjekt.__new__(cls, traeger, A, B, ber)				
		
	
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "hStreckeSchar(" + ss + "_" + '{' + self._mod + '}'
        return "hStrecke_" + '{' + self._mod + '}'			
		
		
# Eigenschaften und Methoden für hStrecke
# ---------------------------------------
		
    @property		
    def mod(self):              
        """Modell"""
        return self.args[1].mod

    @property
    def _mod(self):    # interne Eigenschaft
        """Modell"""
        return self.args[1]._mod
		
    @property
    def exakt(self):         
        """Test auf exakte Erzeugung"""
        return self.args[1].exakt
					
    @property
    def dim(self):              
        """Euklidische Dimension"""
        return self.args[1].dim
		
    @property
    def is_schar(self):
        """Parameter einer Schar"""
        return False
		
    isSchar = is_schar		
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return set()

    schPar = sch_par
	
    @property
    def gerade(self):	
        """hyperbolische Trägergerade"""
        A, B = self.args[1:3]
        return hGerade(A, B)		
		
    @property
    def traeger(self):	
        """Euklidisches Träger-Objekt"""
        return self.gerade.traeger	
		
    e = traeger

    @property
    def par(self):	
        """Parameter"""
        return self.args[0].pkt().sch_par.pop()
	
    @property
    def ber(self):	
        """Parameterbereich"""
        ber = self.args[3]	
        return [float(ber[0]), float(ber[1])] 		

    @property
    def punkte(self):	
        """Erzeugende Punkte"""
        return self.args[1:3] 		
		
    @property
    def laenge(self):	
        """Länge"""
        p1, p2 = self.args[1:3]		
        return p1.abstand(p2) 		

    @property
    def mitte(self):	
        """Mittelpunkt"""
        if self._mod == 'D':	
           ms = self.mitt_senkr
           return self.gerade.schnitt(ms)	
        elif self._mod == 'D3':
            AA, BB = self.punkte
            A, B = D32D(AA), D32D(BB)			
            ss = hStrecke(A, B)
            M = ss.mitte
            return D2D3(M)					
        else:
            AA, BB = self.punkte
            A, B = H2D(AA), H2D(BB)			
            ss = hStrecke(A, B)
            M = ss.mitte
            return D2H(M)			
									
    @property		
    def mitt_senkr(self, **kwargs):
        """Mittelsenkrechte"""		
		
        if self._mod == 'D3':
            AA, BB = self.punkte
            A, B = D32D(AA), D32D(BB)
            ss = hStrecke(A, B)
            ms = ss.mitt_senkr 	
            b0, b1 = ms.ber
            P = hPunkt(ms.traeger.pkt(b0+0.25*(b1-b0)))			
            Q = hPunkt(ms.traeger.pkt(b0+0.75*(b1-b0)))
            PP, QQ = D2D3(P), D2D3(Q)	
            return hGerade(PP, QQ)		
		
        if self._mod == 'H':
            AA, BB = self.punkte
            A, B = H2D(AA), H2D(BB)
            ss = hStrecke(A, B)
            ms = ss.mitt_senkr 	
            b0, b1 = ms.ber
            P = hPunkt(ms.traeger.pkt(b0+0.25*(b1-b0)))			
            Q = hPunkt(ms.traeger.pkt(b0+0.75*(b1-b0)))
            PP, QQ = D2H(P), D2H(Q)	
            return hGerade(PP, QQ)		
		
        p1, p2 = self.args[1:3]	
        if is_rand_pkt(p1) or is_rand_pkt(p2):
            print("agla: der Mittelpunkt ist nicht definiert (Randpunkt/e)")
            return	
        # nach [Lind S28] 
        z1, z2 = cayley(v2c(p1)), cayley(v2c(p2))
        if abs(im(z1) - im(z2)) < 1e-8:   # Fall y1 == y2 nach Lind
            x = 1/2*(re(z1)+re(z2))
            PP, QQ = Vektor(x, 0, simpl=False), Vektor(x, 3, simpl=False)					  
        else:                             # Fall y1 != y2
            x1, y1 = re(z1), im(z1)
            x2, y2 = re(z2), im(z2)			
            a = (x2*y1 - x1*y2) / (y1 - y2)	
            r = re(N(sqrt(y1*y2*((x1-x2)**2/(y1-y2)**2 + 1))))			
            PP, QQ = Vektor(a-r, 0, simpl=False), Vektor(a+r, 0, simpl=False)  			
        PP, QQ = hPunkt(c2v(cayley_inv(v2c(PP)))), \
			      hPunkt(c2v(cayley_inv(v2c(QQ))))
        return hGerade(PP, QQ)
		
    mittSenkr = mitt_senkr		


    def normale(self, *punkt, **kwargs):       
        """Normale in einem Streckenpunkt"""
		
        if kwargs.get('h'):
            print("\nNormale in einem Punkt der hyperbolischen Strecke\n")		
            print("Aufruf    hstrecke . normale( hpunkt )\n")		                     
            print("              hstrecke   hyperbolische Strecke")
            print("              hpunkt     hyperbolischer Punkt\n")
            return
				
        try:				
            if not len(punkt) == 1:
                raise AglaError('einen hyperbolischen Punkt angeben')
            p = punkt[0]
            if not isinstance(p, hPunkt):
                raise AglaError('einen hyperbolischen Punkt angeben')
            if p._mod != self._mod:
                raise AglaError('der Punkt muss im selben Modell sein')
            if mit_param(p):
                raise AglaError('nicht implementiert (Parameter)')
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        if p.e.betrag == 1:
            print("agla: in diesem Punkt ist keine Normale definiert")
            return		
        g = self.gerade
        return g.normale(p)
				
		
    def winkel(self, *args, **kwargs):
        """Winkel mit anderem hyperbolischem Objekt"""
		
        if kwargs.get('h'):
            print("\nWinkel der hyperbolischen Strecke mit einem anderen hyperboli-")
            print("schen Objekt in einem gemeinsamen Punkt\n")		
            print("Aufruf    hstrecke . winkel( hobjekt, hpunkt )\n")		                     
            print("              hstrecke   hyperbolische Strecke")
            print("              hobjekt    hyperbolische(r) Gerade, Strahl, Strecke")
            print("              hpunkt     hyperbolischer Punkt\n")
            print("Es wird nicht geprüft, ob der Punkt auf den beiden Objekten liegt\n")
            return
				
        try:				
            if len(args) != 2:
                raise AglaError('hyperbolische Strecke/Gerade und Punkt angeben')
            ss, pp = args		 
            if not isinstance(ss, (hStrecke, hStrahl, hGerade)):			 
                raise AglaError("1. Argument hyperbolische(n) Gerade, Strahl, Strecke" + \
	                            "angeben")
            if not isinstance(pp, hPunkt):			 
                raise AglaError("2. Argument hyperbolischen Punkt " + \
	                            "angeben")
            if mit_param(ss) or mit_param(pp):
                raise AglaError("nicht implementiert (Parameter)")    			
            if ss._mod != self._mod or pp._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")            
        except AglaError as e:
            print('agla:', str(e))
            return	
		
        if ss == self:		
            print("agla: die Strecken sind identisch")
            return
						
        if isinstance(ss, (hStrahl, hStrecke)):
            g1, g2 = self.gerade, ss.gerade
        else:			
            g1, g2 = self.gerade, ss
        wi = g1.winkel(g2, pp).n()
        if wi > 90:
            wi = 180 - wi		
        return wi		
        
		
    def wink_halb(self, *args, **kwargs):  
        """Winkelhalbierende mit anderer hyperbolischer Strecke"""
		
        if kwargs.get('h'):
            print("\nWinkelhalbierende der hyperbolischen Strecke mit einer ")
            print("anderen hyperbolischen Strecke in einem gemeinsamen ")
            print("Endpunkt\n")		
            print("Aufruf    hstrecke . wink_halb( hstrecke1, hpunkt )\n")		                     
            print("              hstrecke   hyperbolische Strecke")
            print("              hpunkt     hyperbolischer Punkt\n")
            print("Es wird nicht geprüft, ob der Punkt Endpunkt beider ")
            print("Strecken ist\n")
            return
				
        try:				
            if len(args) != 2:
                raise AglaError('hyperbolische Strecke und Punkt angeben')
            ss, PP = args		 
            if not isinstance(ss, hStrecke):			 
                raise AglaError("1. Argument hyperbolische Strecke " + \
	                            "angeben")
            if not isinstance(PP, hPunkt):			 
                raise AglaError("2. Argument hyperbolischen Punkt " + \
	                            "angeben")
            if mit_param(ss) or mit_param(PP):
                raise AglaError("nicht implementiert (Parameter)")    			
            if ss._mod != self._mod or PP._mod != self._mod:	    				
                raise AglaError("die Objekte sind aus verschiedenen Modellen")    
            p1, p2 = self.punkte	
            p3, p4 = ss.punkte	
            if p1.e.betrag == 1 or p2.e.betrag == 1 or p3.e.betrag == 1 \
                or p4.e.betrag == 1:
                raise AglaError("keine Winkelhalbierende (ein Endpunkt ist Randpunkt)")    			
        except AglaError as e:
            print('agla:', str(e))
            return	
		
        if self._mod == 'D3':
            print('agla: lange Rechenzeit')
            P = D32D(PP)			
            S1 = hStrecke(D32D(p1), D32D(p2))
            S2 = hStrecke(D32D(p3), D32D(p4))
            wh = S1.wink_halb(S2, P)
            if not wh:
                return			
            b0, b1 = wh.args[3]
            if isinstance(wh.e, Gerade):		
                P = D2D3(wh.punkte[1])
                if P.e == Vektor(0, 0, 0):
                    P = D2D3(wh.punkte[0])				
                Q = Vektor(-P.e.x, -P.e.y, 0)   # Gegenpunkt zum Erzwingen einer Geraden
                Q = hPunkt(Q)				
                return hGerade(P, Q)				
            A = hPunkt(wh.traeger.pkt(b0+0.25*(b1-b0)))			
            B = hPunkt(wh.traeger.pkt(b0+0.75*(b1-b0)))	
            A, B = D2D3(A), D2D3(B)			
            return hGerade(A, B)
					
        if self._mod == 'H':
            print('agla: lange Rechenzeit')
            P = H2D(PP)			
            S1 = hStrecke(H2D(p1), H2D(p2))
            S2 = hStrecke(H2D(p3), H2D(p4))
            wh = S1.wink_halb(S2, P)
            b0, b1 = wh.args[3]			
            A = hPunkt(wh.traeger.pkt(b0+0.25*(b1-b0)))			
            B = hPunkt(wh.traeger.pkt(b0+0.75*(b1-b0)))	
            A, B = D2D3(A), D2D3(B)			
            return hGerade(A, B)
			
        def nullify(A):  
            if not mit_param(A.e):
                x = 0 if (abs(N(A.e.x))) < 1e-8 else N(A.e.x)
                y = 0 if (abs(N(A.e.y))) < 1e-8 else N(A.e.y)
                return hPunkt(x, y)
            return A	
			
        s1, s2, P = self, ss, PP
        if s1 == s2:
            print('agla: die Strecken fallen zusammen')
            return
    		
        if (p1 != P and p2 != P) or (p3 != P and p4 != P):
            print("agla: der Punkt ist kein gemeinsamer Endpunkt")
            return
  
        if gleich(p1, P) and gleich(p3, P):
            OO, AA, BB, SS, TT = p1, p2, p4, p2, p4
        elif gleich(p1, P) and gleich(p4, P):    
            OO, AA, BB, SS, TT = p1, p2, p3, p2, p3
        elif gleich(p2, P) and gleich(p3, P):    
            OO, AA, BB, SS, TT = p2, p1, p4, p1, p4
        elif gleich(p2, P) and gleich(p4, P):
            OO, AA, BB, SS, TT = p2, p1, p3, p1, p3
       
        k1 = s1.gerade._traeger_eplus
        k2 = s2.gerade._traeger_eplus
        OO = c2v(cayley(v2c(OO.e)))
		
        # Berechnung im E+ -Modell [Lind S29]		
        if isinstance(k1, Kreis) and isinstance(k2, Kreis):
            if gleich(k1.radius, k2.radius):
                fall = 1   # Fig.14 bei Lind
            else:
                fall = 3   # Fig.16
        else:
            fall = 2       # Fig.15
		
        if fall == 1:
            x1, x2 = k1.mitte.x, k2.mitte.x
            Q1, Q2 = OO, Vektor((x1+x2)/2, 0, simpl=False)
            P1, P2 = hPunkt(c2v(cayley_inv(v2c(Q1)))), \
                    hPunkt(c2v(cayley_inv(v2c(Q2))))
            P1, P2 = nullify(P1), nullify(P2)
            gg = hGerade(P1, P2)
            g1 = hGerade(SS, TT)  # Gegenseite
            if gg.schnitt(g1):
                return gg 
            return gg.normale(P) 
    
        elif fall == 2:
            z0 = v2c(OO)
            x1 = k1.mitte.x + k1.radius if isinstance(k1, Kreis) else \
                 k2.mitte.x + k2.radius
            r = abs(z0-x1)
            kk = Kreis(Vektor(x1, 0, simpl=False), r)
            PP = kk.pkt(0)
            Q1, Q2 = OO, PP.dez
            P1, P2 = hPunkt(c2v(cayley_inv(v2c(Q1)))), \
                    hPunkt(c2v(cayley_inv(v2c(Q2))))
            gg = hGerade(P1, P2)
            g1 = hGerade(SS, TT)  # Gegenseite
            if gg.schnitt(g1):
                return gg 
            return gg.normale(P)
         
        elif fall == 3:
            z0 = v2c(OO)
            x1 = k1.mitte.x + k1.radius 
            x2 = k2.mitte.x + k2.radius
            a = (abs(z0)**2 - x1*x2) / (2*re(z0) - (x1+x2))
            r = abs(z0-a)
            kk = Kreis(Vektor(a, 0, simpl=False), r)
            PP = Vektor(a+r, 0, simpl=False)
            Q1, Q2 = OO, PP.dez
            P1, P2 = hPunkt(c2v(cayley_inv(v2c(Q1)))), \
                    hPunkt(c2v(cayley_inv(v2c(Q2))))
            gg = hGerade(P1, P2)
            g1 = hGerade(SS, TT)  # Gegenseite
            if gg.schnitt(g1):
                return gg 
            return gg.normale(P)
    
    winkHalb = wink_halb		
		

    def graf(self, spez, **kwargs):                       
        """Grafikelement für hStrecke"""	
        if self.dim == 3:
            return self.graf3(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für hStrecke in R^2"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        k0 = self.args[0]		
        if isinstance(k0, Gerade):
            A, B = self.args[1:3]		
            kk = Strecke(A.e, B.e)       		
        else:	
            ber = self.args[3]
            kk = k0.bogen(ber[0], ber[1])
        kk.graf2((None, spez[1], spez[2], None))
		
    def graf3(self, spez, **kwargs):                       
        """Grafikelement für hStrecke in R^3"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        t = Symbol('t')															
        p = self.traeger.pkt(t)		
        if self._mod == 'D3':		
            t0, t1 = self.ber	
        else:   # H	
            zo = UMG._sicht_box[-1] 
            ber = solve(p.z - zo) 
            reell = [not im(z) for z in ber]		
            if 	not all(reell) or len(ber) < 2:
                print('agla: Sichtbox - z-Bereich vergrößern')			
                return None	
            t0, t1 = self.ber			
        traeger = Kurve(p, (t, t0, t1) )	
        traeger.mayavi((None, spez[1], spez[2], None))
						
			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hStrecke_hilfe(3)	
		
    h = hilfe		

	
def hStrecke_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nhStrecke - Objekt     Hyperbolische Strecke\n")
        print("Erzeugung     hStrecke( hpunkt1, hpunkt2 )\n")
        print("                  hpunkt   hyperbolischer Punkt\n")
        print("Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die")
        print("symbolische Berechnung kann mit der Angabe  exakt=ja erreicht werden\n")		
        print("Zuweisung     hs = hStrecke(...)   (hs - freier Bezeichner)\n")
        print("Beispiel")
        print("A = hPunkt(-0.2, 0.5); B = hPunkt(0.4, 0.1)")		
        print("hStrecke( A, B )\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für hStrecke\n")
        print("hs.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("hs.ber               Parameterbereich")
        print("hs.dim               Euklidische Dimension")
        print("hs.e                 = hs.träger")
        print("hs.exakt             Test auf exakte Berechnung")
        print("hs.gerade            hyperbolische Trägergerade")
        print("hs.länge             Länge")
        print("hs.mitte             Mittelpunkt")
        print("hs.mitt_senkr        Mittelsenkrechte")
        print("hs.mod               Modell")
        print("hs.normale(...)   M  Normale in einem Streckenpunkt")
        print("hs.punkte            Erzeugende Punkte")
        print("hs.träger            Euklidisches Träger-Objekt")
        print("hs.winkel(...)    M  Winkel mit anderem Objekt")	
        print("hs.wink_halb(...) M  Winkelhalbierende mit anderer Strecke\n") 
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("mitt_senkr :  mittSenkr")
        print("wink_halb  :  winkHalb\n")
        return

				
		

# hKreis - Klasse   
# -----------------
	
class hKreis(AglaObjekt):                                      
    """
   
hyperbolischer Kreis

**Erzeugung** 
	
   hKreis ( *mitte, radius* ) 
	 
**Parameter**

   *mitte* : hyperbolischer Punkt - Mittelpunkt
   
   *radius* : Radius  

Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die
symbolische Berechnung kann mit der Angabe ``exakt=ja`` bzw. mittels der 
Systemvariablen ``UMG.EXAKT`` erreicht werden
      
    """   

	
    def __new__(cls, *args, h=None, exakt=False):  
			
        if h in (1, 2, 3):                         
            hKreis_hilfe(h)		
            return	
			
        exakt = exakt or UMG.EXAKT			
			
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            M, r = args
            if not (isinstance(M, hPunkt) and is_zahl(r)): 			
                raise AglaError("einen hyperbolischen Punkt und einen Radius angeben")
            if is_rand_pkt(M):				
                raise AglaError("der Kreis existiert nicht (Randpunkt)")
            if mit_param(M) or mit_param(r):				
                raise AglaError("nicht implementiert (Parameter)")				
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        if M._mod == 'D3':
            kk = hKreis(D32D(M), r)
            tr = kk.traeger
            traeger = Kreis(xy_ebene, D2D3(tr.mitte), tr.r)            			
            return AglaObjekt.__new__(cls, traeger, M, r)				

        if M._mod == 'H':
            MM = H2D(M)
            kk = hKreis(MM, r)
            t = Symbol('t')			
            PP = kk.traeger.pkt(t)
            p = D2H(PP)			
            ku = Kurve(p, (t, 0, 360))
            return AglaObjekt.__new__(cls, ku, M, r)				
											
        if exakt:
            if not M.exakt or isinstance(r, (float, Float)):
                print('agla: Mittelpunkt und Radius müssen exakt definiert sein')	
                return				
        else:
            if M.exakt:
                M = to_float(M)			
            r = float(r)
			
        return AglaObjekt.__new__(cls, M, r)				
		        		
				
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "hKreisSchar(" + ss + ")_" + '{' + self._mod + '}'
        return "hKreis_" + '{' + self._mod + '}'			
		
		
# Eigenschaften und Methoden für hKreis
# -------------------------------------
			
    @property
    def mod(self):              
        """Modell"""
        m = self.args[0]		
        if isinstance(m, hPunkt):		
            return m.mod
        return self.args[1].mod
				
    @property
    def _mod(self):              
        """Modell"""
        m = self.args[0]		
        if isinstance(m, hPunkt):		
            return m._mod
        return self.args[1]._mod
		
    @property
    def exakt(self):         
        """Test auf exakte Erzeugung"""
        return self.mitte.exakt
		
    @property
    def dim(self):              
        """Euklidische Dimension"""
        return self.args[0].dim
		
    @property
    def is_schar(self):
        """Parameter einer Schar"""
        return False
		
    isSchar = is_schar		
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return set()

    schPar = sch_par
			
    @property		
    def mitte(self):              
        """Mittelpunkt"""
        m = self.args[0]		
        if isinstance(m, hPunkt):		
            return m
        return self.args[1]
			
    M = mitte
    m = mitte
	
    @property		
    def radius(self):              
        """Radius"""
        return self.args[-1]  

    r = radius
	
    @property		
    def traeger(self):              
        """Euklidisches Träger-Objekt"""
        
        if self._mod in ('D3', 'H'):
            return self.args[0]
			
        # aus der Umstellung der Kreisgleichung		
        M = self.mitte.e
        if M.x == 0 and M.y == 0:
            R = tanh(self.radius/2)	
            return Kreis(M, R)
        R = self.radius
        a = 1 - M.betrag**2; 
        A = 2 - a + a*cosh(R)
        C = a - a*cosh(R) + 2*M.betrag**2  
        mx = float(2*M.x / A)
        my = float(2*M.y / A)
        r = float(sqrt(mx**2 + my**2 - C / A))
        kr = Kreis(Vektor(mx, my), r, simpl=False)
        return kr 		

    e = traeger		
	
    @property		
    def laenge(self):              
        """Länge"""
        return 2 * pi * sinh(self.radius)		
    def laenge_(self, **kwargs):              
        """Länge; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nkein Argument - Länge (dezimal)")
            print("f=1  - Formel\n")
            return			
        if kwargs.get('f'):
            txt = 'L' + '=' + '2 \\pi \\sinh ( r ) \quad\quad r - Radius'
            display(Math(txt))
            return	
        return N(self.laenge)	
		
    umfang = laenge		
    umfang_ = laenge_
    Laenge = laenge_
    Umfang = laenge_	

    @property		
    def flaeche(self):              
        """Flächeninhalt"""
        return 4 * pi * sinh(self.radius/2)**2	
    def flaeche_(self, **kwargs):              
        """Flächeninhalt; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nkein Argument - Fläche (dezimal)")
            print("f=1  - Formel\n")
            return			
        if kwargs.get('f'):
            txt = 'A' + '=' + '4 \\pi \\sinh^2(r\,/\,2) \quad\quad r - Radius'
            display(Math(txt))
            return	
        return N(self.flaeche)			
		
    Flaeche = flaeche_

	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für hKreis"""	
        if self.dim == 3:
            return self.graf3(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für hKreis in R^2"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        kk = self.traeger
        kk.graf2((None, spez[1], spez[2], None))
		
    def graf3(self, spez, **kwargs):                       
        """Grafikelement für hKreis in R^3"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        traeger = self.traeger
        traeger.mayavi((None, spez[1], spez[2], None))
				
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hKreis_hilfe(3)	
		
    h = hilfe		
		
		
def hKreis_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nhKreis - Objekt     Hyperbolischer Kreis\n")
        print("Erzeugung     hKreis( mitte, radius )\n")
        print("                  mitte    hyperbolischer Punkt")
        print("                  radius   Radius\n")
        print("Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die")
        print("symbolische Berechnung kann mit der Angabe  exakt=ja erreicht werden\n")		
        print("Zuweisung     hk = hKreis(...)   (hk - freier Bezeichner)\n")
        print("Beispiel")
        print("hKreis( hPunkt(0.2, 0.3), 2 )\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für hKreis\n")
        print("hk.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("hk.dim              Euklidische Dimension")
        print("hk.e                = hk.träger")
        print("hk.exakt            Test auf exakte Berechnung")
        print("hk.fläche           Flächeninhalt")
        print("hk.fläche_(...) M   ebenso, zugehörige Methode")
        print("hk.länge            Länge")
        print("hk.länge_(...)  M   ebenso, zugehörige Methode")
        print("hk.mitte            Mittelpunkt")
        print("hk.M                = hk.mitte")
        print("hk.m                = hk.mitte")
        print("hk.mod              Modell")
        print("hk.radius           Radius")
        print("hk.r                = hk.radius")
        print("hk.träger           Euklidisches Träger-Objekt")
        print("hk.umfang           = hk.länge")
        print("hk.umfang_(...)  M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe   :  h")
        print("fläche_ :  Fläche")
        print("länge_  :  Länge")
        print("umfang_ :  Umfang\n")
        return


		
# hDreieck - Klasse   
# -----------------
	
class hDreieck(AglaObjekt):                                      
    """
   
hyperbolisches Dreieck

**Erzeugung** 
	
   hDreieck ( *hpunkt1, hpunkt2, hpunkt3* ) 
	 
**Parameter**

   *hpunkt* : hyperbolischer Punkt 
         
Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die
symbolische Berechnung kann mit der Angabe ``exakt=ja`` bzw. mittels der 
Systemvariablen ``UMG.EXAKT`` erreicht werden
		 
    """   
	
    def __new__(cls, *args, h=None, exakt=False):  
			
        if h in (1, 2, 3):                         
            hDreieck_hilfe(h)		
            return	
			
        exakt = exakt or UMG.EXAKT			
			
        try:
            if len(args) != 3:
                raise AglaError("drei Argumente angeben")
            A, B, C = args
            if not (isinstance(A, hPunkt) and isinstance(B, hPunkt) and \
               isinstance(C, hPunkt)): 			
                raise AglaError("drei hyperbolische Punkte angeben")
            if mit_param(A) or mit_param(B) or mit_param(C):				
                raise AglaError("nicht implementiert (Parameter)")
            if not (A._mod == B._mod and A._mod == C._mod): 			
                raise AglaError("drei hyperbolische Punkte im selben Modell angeben")								
            if A == B or A == C:
                raise AglaError("die Punkte müssen verschieden sein")
            gr = 1e-8		
            if not (A.e.abstand(B.e) > gr and A.e.abstand(C.e) > gr and 
			        B.e.abstand(C.e) > gr):	
                raise AglaError("die Punkte liegen auf einer hyperbolischen Geraden")
        except AglaError as e:	
            print('agla:', str(e))
            return
		
        if A._mod == 'H':
            sa = hStrecke(B, C)
            sb = hStrecke(C, A)
            sc = hStrecke(A, B)
            return AglaObjekt.__new__(cls, A, B, C, (sa, sb, sc))				

        if exakt:
            if not (A.exakt and B.exakt and C.exakt):
               print('agla: die Punkte müssen exakt definiert sein')
               return			   
        else:
            if A.exakt:
                A = to_float(A)			
            if B.exakt:
                B = to_float(B)			
            if C.exakt:
                C = to_float(C)			
        if is_rand_pkt(B) and is_rand_pkt(C):
            sa = hGerade(B, C, exakt=exakt)
        elif (is_rand_pkt(B) and not is_rand_pkt(C)) or \
            (not is_rand_pkt(B) and is_rand_pkt(C)):
            sa = hStrahl(B, C, exakt=exakt)
        else:			
            sa = hStrecke(B, C, exakt=exakt)			
        if is_rand_pkt(A) and is_rand_pkt(C):
            sb = hGerade(A, C, exakt=exakt)
        elif (is_rand_pkt(A) and not is_rand_pkt(C)) or \
            (not is_rand_pkt(A) and is_rand_pkt(C)):
            sb = hStrahl(A, C, exakt=exakt)
        else:			
            sb = hStrecke(A, C, exakt=exakt)
        if is_rand_pkt(A) and is_rand_pkt(B):
            sc = hGerade(A, B, exakt=exakt)
        elif (is_rand_pkt(A) and not is_rand_pkt(B)) or \
            (not is_rand_pkt(A) and is_rand_pkt(B)):
            sc = hStrahl(A, B, exakt=exakt)
        else:			
            sc = hStrecke(A, B, exakt=exakt)			
			
        return AglaObjekt.__new__(cls, A, B, C, (sa, sb, sc))				
			
			
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "hDreieckSchar(" + ss + ")_" + self._mod
        return "hDreieck_" + self._mod			
		
		
# Eigenschaften und Methoden für hDreieck
# ---------------------------------------
			
    @property
    def mod(self):              
        """Modell"""
        return self.args[0].mod

    @property
    def _mod(self):              
        """Modell"""
        return self.args[0]._mod
		
    @property
    def exakt(self):     
        """Test auf exakte Punkte"""
        return all([self.args[i].exakt for i in (0, 1, 2)])
				
    @property
    def is_schar(self):
        """Parameter einer Schar"""
        return False
		
    isSchar = is_schar		

    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return set()

    schPar = sch_par
			
    @property
    def dim(self):              
        """Euklidische Dimension"""
        return self.args[0].dim
		
    @property
    def punkte(self):
        """Eckpunkte"""
        return self.args[:3]

    @property
    def laengen(self):
        """Seitenlängen"""
        A, B, C = self.args[:3]        		
        return N(B.abstand(C)), N(A.abstand(C)), N(A.abstand(B))	
	
    @property
    def umfang(self):
        """Umfang"""
        A, B, C = self.args[:3]        		
        return N(B.abstand(C) + A.abstand(C) + A.abstand(B))	
	
    @property
    def seiten(self):
        """Seiten"""
        return self.args[3]	
	
    @property
    def winkel(self):
        """Innenwinkel"""
        p1, p2, p3 = self.punkte
        if is_rand_pkt(p1) or is_rand_pkt(p2) or is_rand_pkt(p2): 
            print("agla: nicht implementiert (Randpunkt/e)")		
            return			
        a, b, c = self.laengen
        # Berechnung nach dem 	Seitenkosinussatz
        wia = arccosg((cosh(b)*cosh(c)-cosh(a))/(sinh(b)*sinh(c)))
        wib = arccosg((cosh(a)*cosh(c)-cosh(b))/(sinh(a)*sinh(c)))
        wic = arccosg((cosh(a)*cosh(b)-cosh(c))/(sinh(a)*sinh(b)))
        rea = float(wia) if not mit_param(wia) else wia
        reb = float(wib) if not mit_param(wib) else wib
        rec = float(wic) if not mit_param(wic) else wic
        return rea, reb, rec	
		
    @property
    def wink_summe(self):
        """Innenwinkelsumme"""
        p1, p2, p3 = self.punkte
        if is_rand_pkt(p1) or is_rand_pkt(p2) or is_rand_pkt(p2): 
            print("agla: nicht implementiert (Randpunkt/e)")
            return			
        wia, wib, wic = self.winkel
        return wia + wib + wic
		
    winkSumme = wink_summe		

    @property
    def flaeche(self):
        """Flächeninhalt"""
        p1, p2, p3 = self.punkte
        if is_rand_pkt(p1) or is_rand_pkt(p2) or is_rand_pkt(p2): 
            print("agla: nicht implementiert (Randpunkt/e)")
            return 			
        wi = self.winkel        		
        return N((180 - (wi[0]+wi[1]+wi[2])) * pi / 180)		
		
    @property
    def inkreis(self):
        """Inkreis"""
        A, B, C = self.punkte
        if self._mod == 'H':
            A, B, C = H2D(A), H2D(B), H2D(C)		
            d = hDreieck(A, B, C)
            k = d.inkreis
            M, r = k.mitte, k.radius			
            return hKreis(D2H(M), r)
			
        if any([is_rand_pkt(p) for p in (A, B, C)]): 
            print("agla: nicht implementiert (Randpunkt/e)")	
            return			
        ss = self.seiten
        wh1 = ss[1].wink_halb(ss[2], A)		
        wh2 = ss[0].wink_halb(ss[2], B)	
        M = wh1.schnitt(wh2)
        ll = self.laengen
        a, b, c = ll[0], ll[1], ll[2]
        wa = ss[0].winkel(ss[1], C) 
        tr = tang(wa/2)*sin(1/2*(a+b+c)/I-c/I) 
        R = N(abs(atan(tr)))
        return hKreis(M, R)		
						
    @property
    def umkreis(self):
        """Umkreis"""
        A, B, C = self.punkte
        if self._mod == 'H':
            A, B, C = H2D(A), H2D(B), H2D(C)		
            d = hDreieck(A, B, C)
            k = d.umkreis
            if not k:
                return			
            M, r = k.mitte, k.radius			
            return hKreis(D2H(M), r)
		
        if any([is_rand_pkt(p) for p in (A, B, C)]): 
            print("agla: kein Umkreis (Randpunkt/e)")		
            return 
        sc = hStrecke(A, B)
        sb = hStrecke(A, C)
        msc = sc.mitt_senkr
        msb = sb.mitt_senkr
        M = msc.schnitt(msb)
        if not M:
            print('agla: der Umkreis existiert nicht')
            return			
        r = M.abstand(A)		
        return hKreis(M, r)

    @property
    def exzess(self):
        """Exzeß"""
        p1, p2, p3 = self.punkte
        if is_rand_pkt(p1) or is_rand_pkt(p2) or is_rand_pkt(p2): 
            print("agla: nicht implementiert (Randpunkt/e)")	
            return			
        w = 180 - self.wink_summe		
        return w
		
    defekt = exzess		
		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für hDreieck"""	
        if self.dim == 3:
            return self.graf3(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für hDreieck in R^2"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        ss = self.seiten
        ( ss[0].graf2((None, spez[1], spez[2], None)),
          ss[1].graf2((None, spez[1], spez[2], None)),
          ss[2].graf2((None, spez[1], spez[2], None)) )
		  
    def graf3(self, spez, **kwargs):                       
        """Grafikelement für hDreieck in R^3"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        ss = self.seiten
        ( ss[0].graf3((None, spez[1], spez[2], None)),
          ss[1].graf3((None, spez[1], spez[2], None)),
          ss[2].graf3((None, spez[1], spez[2], None)) )
		  
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften"""
        hDreieck_hilfe(3)	
		
    h = hilfe				

	
def hDreieck_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften")
        return
		   
    if h == 2:
        print("\nhDreieck - Objekt     Hyperbolisches Dreieck\n")
        print("Erzeugung     hDreieck( hpunkt1, hpunkt2, hpunkt3 )\n")
        print("                  hpunkt   hyperbolischer Punkt\n")
        print("Die Berechnungen erfolgen standardmäßig nummerisch (nicht exakt), die")
        print("symbolische Berechnung kann mit der Angabe  exakt=ja erreicht werden\n")		
        print("Zuweisung     hd = hDreieck(...)   (hd - freier Bezeichner)\n")
        print("Beispiel")
        print("A = hPunkt(-0.2, 0.5); B = hPunkt(0.4, 0.1); C = hPunkt(-0.5, -0.6)")		
        print("hDreieck( A, B, C)\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften für hDreieck\n")
        print("hd.hilfe           Bezeichner der Eigenschaften")
        print("hd.defekt          = hd.exzeß")
        print("hd.dim             Euklidische Dimension")
        print("hd.exakt           Test auf exakte Berechnung")
        print("hd.exzeß           Exzeß (in Grad)")
        print("hd.fläche          Flächeninhalt")
        print("hd.inkreis         Inkreis")
        print("hd.längen          Seitenlängen")
        print("hd.mod             Modell")
        print("hd.punkte          Eckunkte")
        print("hd.seiten          Seiten")	
        print("hd.umfang          Umfang")
        print("hd.umkreis         Umkreis")
        print("hd.winkel          Innenwinkel")	
        print("hd.wink_summe      Innenwinkelsumme\n")	
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("wink_summe :  winkSumme\n")
        return
	
	
		
	 	