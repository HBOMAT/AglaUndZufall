#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Hyperbel - Klasse  von agla           
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
import matplotlib.pyplot as plt
		
from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.simplify.simplify import nsimplify, simplify
from sympy.core.symbol import Symbol
from sympy import sqrt, sin, cos, tan, sinh, cosh
from sympy.core.evalf import N	 
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, v, X
from agla.lib.objekte.abbildung import Abbildung
from agla.lib.objekte.k2o import K2O
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    ja, Ja, nein, Nein, mit, ohne, sing, cosg, tang, Gleichung)
from agla.lib.funktionen.graf_funktionen import rgb2hex			
from agla.lib.objekte.umgebung import UMG	
import agla



# Hyperbel - Klasse
# --------------
	
class Hyperbel(AglaObjekt):                                      
    """
	
Hyperbel in der Ebene
	
**Erzeugung** 
	
   Hyperbel ( */[ mitte, ] a, b )* ) 
   
**Parameter**

   *mitte* : Mittelpunkt; Ursprung, wenn weggelassen
   
   *a, b* :  Halbachsen 
   	
    """

	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            hyperbel_hilfe(kwargs["h"])		
            return	
			
        try:			
            if len(args) == 2:
                a, b = args
                mitte = Vektor(0, 0)							
            elif len(args) == 3:
                mitte, a, b = args
            else:				
                txt = "2 Halbachsen oder Mittelpunkt und 2  Halbachsen angeben"
                raise AglaError(txt)
            if not isinstance(mitte, Vektor):			
                raise AglaError("für Mittelpunkt Punkt der Ebene angeben")
            if mitte.dim != 2:				
                raise AglaError("für Mittelpunkt Punkt der Ebene angeben")
            if not is_zahl(a) or not is_zahl(b):
                raise AglaError("für die Halbachsen Zahlen angeben")
            if not mit_param(a) and not mit_param(b):
                if a < 0 or b < 0:
                    raise AglaError("2 positive Zahlen angeben")
            try:					
                a, b = nsimplify(a), nsimplify(b)
            except RecursionError:
                pass			
            return AglaObjekt.__new__(cls, mitte, a, b)
        except AglaError as e:
            print('agla:', str(e))
            return			

   
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Hyperbelnschar(" + ss + ")"
        return "Hyperbel"			

		
# Eigenschaften + Methoden
# ------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return self.args[0].dim
		
    @property
    def mitte(self):              
        """Mittelpunkt"""
        return self.args[0]
    
    @property	
    def a(self):              
        """Erste Halbachse"""
        return self.args[1]

    @property	
    def b(self):              
        """Zweite Halbachse"""
        return self.args[2]
       	   		
    @property	
    def asympt(self):              
        """Asymptoten"""
        m, a, b = self.args
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        return Gerade(b/a, -1, -b/a*m.x + m.y), Gerade(-b/a, -1, b/a*m.x + m.y) 
		
    @property			
    def sch_par(self):              
        """Scharparameter"""
        args = self.args		
        ret = args[0].free_symbols
        if mit_param(args[1]):
            ret = ret.union(args[1].free_symbols)		
        if mit_param(args[2]):
            ret = ret.union(args[2].free_symbols)		
        return ret
	
    schPar = sch_par	

    @property	
    def lin_exz(self):              
        """Lineare Exzentrizität"""        
        return sqrt(self.a**2 + self.b**2)
		
    e = lin_exz
    linExz = lin_exz	

    @property	
    def brenn_ger(self):              
        """Leit- / Brenngeraden""" 
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        g1 = Gerade(1, 0, -self.mitte.x - self.a**2 / self.e)		
        g2 = Gerade(1, 0, -self.mitte.x + self.a**2 / self.e)		
        return g1, g2

    brennGer = brenn_ger
    leit_ger = brenn_ger
    leitGer = brenn_ger
	
    @property	
    def f1(self):              
        """Erster Brennpunkt""" 
        return Vektor(self.mitte.x + self.e, self.mitte.y)
		
    F1 = f1
	
    @property	
    def f2(self):              
        """Zweiter Brennpunkt""" 
        return Vektor(self.mitte.x - self.e, self.mitte.y)
		
    F2 = f2
	
    @property	
    def brenn_punkt(self):              
        """Brennpunkte""" 
        return self.f1, self.f2
		
    brennPunkt = brenn_punkt
		
    @property	
    def num_exz(self):              
        """Nummerische Exzentrizität"""        
        return simplify(self.e / self.a)
		
    eps = num_exz
    numExz = num_exz	
	
    @property	
    def mitte(self):              
        """Mittelpunkt"""        
        return self.args[0]
	
    @property		
    def gleich(self):              
        """Gleichung; nur zur Ausgabe"""
        m, a, b = self.args
        x, y = Symbol('x'), Symbol('y')	
        x, y = latex((x - m.x)**2), latex((y - m.y)**2)	
        a, b = latex(a**2), latex(b**2)		
        lat = '\\frac{' + x + '}{' + a + '}' + '-' + '\\frac{' + y + \
             '}{' + b + '}' + '=1'
        return display(Math(lat))			
    def gleich_(self, *punkt, **kwargs):              
        """Gleichung; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nBei Einsetzen eines Punktes Auswertung der Gleichung in diesem\n")
            print("Zusatz   g=ja   Bereitstellung der Gleichung als Gleichung-Objekt\n")			
            return
        x, y = Symbol('x'), Symbol('y')	
        m, a, b = self.args
        gl = Gleichung((x - m.x)**2 / a**2 - (y - m.y)**2 / b**2, 1)
        if kwargs.get('g'):
            return gl
        if not punkt:
            self.gleich
            return			
        if len(punkt) != 1:
            print("agla: einen Punkt der Ebene angeben")
            return        		
        punkt = punkt[0]
        if not (isinstance(punkt, Vektor) and punkt.dim == 2):	
            print("agla: einen Punkt der Ebene angeben")
            return
        gl = gl.lhs
        if bool(simplify(gl.subs({x:punkt.x, y:punkt.y})) == 1):
            lat = latex('\\text{die Gleichung ist erfüllt}')
        else:
            lat = latex('\\text{die Gleichung ist nicht erfüllt}')		
        return display(Math(lat))
		
    Gleich = gleich_
	
    @property
    def in_kurve(self):
        """Konvertierung in Kurve"""
        m, a, b = self.args
        t = Symbol("t")
        p1 = Vektor(a*cosh(t), b*sinh(t)) + m		
        p2 = Vektor(-a*cosh(t), b*sinh(t)) + m		
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
        return Kurve(p1, (t, -100, 100)), Kurve(p2, (t, -100, 100))		
        # (getrennte Zweige rechts und links)
		
    inKurve = in_kurve		
		
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar	

    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        t, x, y = Symbol('t'), Symbol('x'), Symbol('y')	
        X = Vektor(x, y)
        m, a, b = self.args
        vv = Vektor(a/cos(t), b*tan(t))   
        if m == Vektor(0, 0):
            lat = latex(X) + '=' + latex(vv)
        else:			
            lat = latex(X) + '=' + latex(vv) + '+' + latex(m)		
        return display(Math(lat))
		
    @property		
    def prg_hf(self):              
        """Parametergleichung anhand von Hyperbelfunktionen; nur zur Ausgabe"""
        t, x, y = Symbol('t'), Symbol('x'), Symbol('y')	
        X = Vektor(x, y)
        m, a, b = self.args
        p1 = Vektor(a*cosh(t), b*sinh(t))   
        p2 = Vektor(-a*cosh(t), b*sinh(t))   
        if m == Vektor(0, 0):
            lat1, lat2 = latex(X) + '=' + latex(p1), latex(X) + '=' + latex(p2)
        else:			
            lat1 = latex(X) + '=' + latex(p1) + '+' + latex(m)		
            lat2 = latex(X) + '=' + latex(p2) + '+' + latex(m)		
        display(Math(lat1)), display(Math(lat2))   # 2 Zweige
		
    prgHf = prg_hf
	
    @property		
    def prg_rf(self):              
        """Parametergleichung anhand von rationalen Funktionen; nur zur Ausgabe"""
        t, x, y = Symbol('t'), Symbol('x'), Symbol('y')	
        X = Vektor(x, y)
        m, a, b = self.args
        p1 = Vektor(a*(t**2+1)/(2*t), b*(t**2-1)/(2*t))   
        p2 = Vektor((-1)*p1.x, p1.y)    
        if m == Vektor(0, 0):
            lat1, lat2 = latex(X) + '=' + latex(p1), latex(X) + '=' + latex(p2)
        else:			
            lat1 = latex(X) + '=' + latex(p1) + '+' + latex(m)		
            lat2 = latex(X) + '=' + latex(p2) + '+' + latex(m)		
        display(Math(lat1)), display(Math(lat2))   # 2 Zweige

    prgRf = prg_rf		
	
    def pkt(self, *par_wert, **kwargs):
        """Hyperbelpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt der Hyperbel (anhand der Parametergleichung prg)\n")		
            print("Aufruf   hyperbel . pkt( /[ wert ] )\n")		                     
            print("             hyperbel   Hyperbel")
            print("             wert       Wert des Hyperbelparameters (in Radian)\n")		
            print("Rückgabe     bei Angabe eines Parameterwertes:")
            print("             Hyperbelpunkt, der zu diesem Wert gehört")
            print("             bei leerer Argumentliste oder freiem Bezeichner:") 
            print("             allgemeiner Punkt der Hyperbel\n") 			
            return 
			
        t = Symbol("t")
        m, a, b = self.args
        if not par_wert:
            p = self.mitte + Vektor(a/cos(t), b*tan(t))
            return p
        if len(par_wert) == 1:
            pw = sympify(par_wert[0]) 
            if is_zahl(pw):
                p = self.mitte + Vektor(a/cos(pw), b*tan(pw)).einfach
                return p			
            print("agla: Zahl angeben")	
            return			 
        print("agla: einen Parameterwert angeben")
        return
	
				
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar von Hyperbeln; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")			
            return
			
        if kwargs.get('h'):
            print("\nElement einer Hyperbelschar\n")		
            print("Aufruf   hyperbel . sch_el( wert )\n")		                     
            print("             hyperbel   Hyperbel")
            print("             wert       Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter angeben')	
            return
        try:			
            wert = nsimplify(wert)
        except RecursionError:
            pass		
        m, a, b = self.args
        if p in m.sch_par:
            m = m.sch_el(wert)
        a = self.a.subs(p, wert)
        b = self.b.subs(p, wert)
        if not mit_param(a) and not mit_param(b) and (a < 0 or b < 0):   
            print('agla: für die Halbachsen 2 positive Zahlen angeben')	
            return	
        return Hyperbel(m, a, b)			
	
    schEl = sch_el
		
		
    def tangente(self, *args, **kwargs):
        """Tangente"""
		
        if kwargs.get('h'):
            print("\nTangente in einem Hyperbelpunkt\n")	
            print("Aufruf   hyperbel . tangente( punkt )\n")		                     
            print("             hyperbel   Hyperbel")
            print("             punkt      Punkt der Hyperbel\n")			
            return 				
			
        if len(args) != 1:
            print("agla: einen Punkt angeben")
            return
        p = args[0]			
        if not isinstance(p, Vektor):
            print("agla: einen Punkt der Ebene angeben")
            return
        if p.dim != 2:
            print("agla: einen Punkt der Ebene angeben")
            return
        x, y = Symbol('x'), Symbol('y')	
        m, a, b = self.args
        gl = Gleichung((x - m.x)**2 / a**2 - (y - m.y)**2 / b**2, 1)
        if simplify(gl.lhs.subs({x:p.x, y:p.y})) != 1:
            print("agla: Punkt der Hyperbel angeben")
            return		
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        ta = Gerade((p.x-m.x) / a**2, -(p.y-m.y) / b**2, \
                       -1 -m.x*(p.x-m.x)/a**2 +m.y*(p.y-m.y)/b**2)
        return ta					
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Hyperbel bei einer Abbildung\n")		
            print("Aufruf   hyperbel . bild( abb )\n")		                     
            print("             hyperbel   Hyperbel")
            print("             abb        Abbildung der Ebene R^2\n")	
            print("Es wird ein Kurve2terOrdnung-Objekt erzeugt\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        if not (isinstance(abb, Abbildung) and  abb.dim == 2):
            print("agla: eine Abbildung der Ebene angeben")
            return
        a, b, m = self.a, self.b, self.mitte
        x, y, U, V = Symbol('x'), Symbol('y'), Symbol('U'), Symbol('V')		
        gl = (x - m.x)**2/a**2 - (y - m.y)**2/b**2 - 1		
        uv = abb.matrix.inverse * (Vektor(U, V) - abb.versch)		
        gl = gl.subs({x:uv.x, y:uv.y})		
        gl = gl.subs({U:x, V:y})		
        gls = str(gl)
        return K2O(gls)		
			
				
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Hyperbel"""	

        from numpy import (pi, sqrt, sin, cos, tan, exp, log, sinh, cosh, tanh,
             arcsin, arccos, arctan, arcsinh, arccosh, arctanh)
        ln = log			 
			
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' else spez[2][3]
        lin_farbe = rgb2hex(lin_farbe)
		
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:
            m, a, b = self.args	
            x, y = Symbol('x'), Symbol('y')			
            gl = N((x - m.x)**2/a**2 - (y - m.y)**2/b**2 - 1)		
            xl, xr, yl, yr = UMG._sicht_box[:4]
            xl, xr, yl, yr = float(xl), float(xr), float(yl), float(yr)
            y, x = np.ogrid[xl:xr:100j, yl:yr:100j]  # Reihenfolge !!!	
            egl = eval(str(gl))
            plt.gca().contour(x.ravel(), y.ravel(), egl, [0], linewidths= \
                                          lin_staerke, colors=lin_farbe)
            return plt.plot([0], [0], 'w', markersize=0.0001)  # dummy plot	 
		
        else:
            xl, xr, yl, yr = UMG._sicht_box[:4]
            xl, xr, yl, yr = float(xl), float(xr), float(yl), float(yr)
            y, x = np.ogrid[xl:xr:100j, yl:yr:100j]  # Reihenfolge !!!	
            gl = str(self.imp.lhs)
            gl = eval(gl)
            if isinstance(lin_farbe, (tuple, Tuple)):
                lin_farbe = rgb2hex(lin_farbe)                  
            plt.gca().contour(x.ravel(), y.ravel(), gl, [0], \
                     linewidths=lin_staerke, colors=lin_farbe)	
            return plt.plot([0], [0], 'w', markersize=0.0001)  # dummy plot	 

				
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        hyperbel_hilfe(3)	
		
    h = hilfe				
				
	
# Benutzerhilfe für Hyperbel
# -----------------------

def hyperbel_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nHyperbel - Objekt\n")
        print("Erzeugung in der Ebene R^2:\n")
        print("             Hyperbel( /[ mitte, ] a, b )\n")
        print("                mitte   Mittelpunkt; Ursprung, wenn weggelassen")		
        print("                a, b    Halbachsen\n")		
        print("Zuweisung     h = Hyperbel(...)   (h - freier Bezeichner)\n")
        print("Beispiele")
        print("Hyperbel(5, 3)")
        print("Hyperbel(v(2, 3), a, 2)\n")
        return
		
    if h == 3:              
        print("\nEigenschaften und Methoden (M) für Hyperbel\n")
        print("h.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("h.a                 Länge der 1. Halbachse")       
        print("h.b                 Länge der 2. Halbachse")       
        print("h.asympt            Asymptoten")       
        print("h.bild(...)      M  Bild bei einer Abbildung")       
        print("h.brenn_ger         = h.leit_ger (Brenngeraden)")     
        print("h.brenn_punkt       Brennpunkte")     
        print("h.dim               Dimension")
        print("h.e                 = h.lin_exz")
        print("h.eps               = h.num_exz")
        print("h.F1                1. Brennpunkt")    
        print("h.f1                = h.F1")    
        print("h.F2                2. Brennpunkt")    
        print("h.f2                = h.F2")    
        print("h.gleich            Gleichung")    
        print("h.gleich_(...)   M  ebenso, zugehörige Methode")    
        print("h.in_kurve          Konvertierung in Kurve (2 Zweige)")             
        print("h.is_schar          Test auf Schar")        
        print("h.leit_ger          Leitgeraden")
        print("h.lin_exz           Lineare Exzentrizität")
        print("h.mitte             Mittelpunkt")
        print("h.num_exz           Nummerische Exzentrizität")
        print("h.pkt(...)       M  Hyperbelpunkt (anhand von h.prg)")                      
        print("h.prg               Parametergleichung")
        print("h.prg_hf            ebenso, mit Hyperbel-F. (2 Zweige)")
        print("h.prg_rf            ebenso, mit rationalen F. (2 Zweige)")
        print("h.sch_par           Parameter einer Schar")	
        print("h.sch_el(...)    M  Element einer Schar")   
        print("h.tangente(...)  M  Tangente\n")     
        print("Synonyme Bezeichner\n")
        print("hilfe       :  h")
        print("brenn_ger   :  brennGer")
        print("brenn_punkt :  brennPunkt")
        print("F1          :  f1")
        print("F2          :  f2")
        print("gleich_     :  Gleich")
        print("in_kurve    :  inKurve")
        print("is_schar    :  isSchar")	
        print("leit_ger    :  leitGer")
        print("lin_exz     :  linExz")
        print("num_exz     :  numExz")
        print("prg_hf      :  prgHf")
        print("prg_rf      :  prgRf")
        print("sch_el      :  schEl")
        print("sch_par     :  schPar\n")
        return
   	
		
		
