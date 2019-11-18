#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Parabel - Klasse  von agla           
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
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.evalf import N
from sympy.printing import latex
from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, v, X
from agla.lib.objekte.abbildung import Abbildung
from agla.lib.objekte.k2o import K2O
from agla.lib.objekte.kurve import Kurve
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    ja, Ja, nein, Nein, mit, ohne, sing, cosg, tang, sqrt, Gleichung)
from agla.lib.funktionen.graf_funktionen import rgb2hex			
from agla.lib.objekte.umgebung import UMG	
import agla



# Parabel - Klasse
# ----------------
	
class Parabel(AglaObjekt):                                      
    """
	
Parabel in der Ebene
	
**Erzeugung** 
	
   Parabel ( *p* ) 
   
**Parameter**

   *p* : Parameter in der Gleichung  *y*:sup:`2` = *2px*
      	
    """

	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            parabel_hilfe(kwargs["h"])		
            return	
			
        try:			
            if len(args) != 1:
                txt = "Parameter angeben"
                raise AglaError(txt)
            p = args[0]
            if not is_zahl(p):
                raise AglaError("Zahlenwert angeben")
            if not mit_param(p):
                if p < 0:
                    raise AglaError("positive Zahl angeben")
            try:				
                p = nsimplify(p)	
            except RecursionError:
                pass			
            return AglaObjekt.__new__(cls, p)
        except AglaError as e:
            print('agla:', str(e))
            return			

   
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Parabelschar(" + ss + ")"
        return "Parabel"			

		
# Eigenschaften + Methoden
# ------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return 2
		
    @property
    def p(self):              
        """Parameter in der Gleichung   *y*:sup:`2` = *2px*"""
        return self.args[0]
    
    @property			
    def sch_par(self):              
        """Scharparameter"""
        args = self.args		
        return args[0].free_symbols
	
    schPar = sch_par	

    @property	
    def lin_exz(self):              
        """Lineare Exzentrizität"""        
        return self.p / 2
		
    e = lin_exz
    linExz = lin_exz	

    @property	
    def brenn_ger(self):              
        """Brenn- / Leitgerade""" 
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        return Gerade(1, 0, self.p / 2)

    brennGer = brenn_ger
    leit_ger = brenn_ger
    leitGer = brenn_ger
	
    @property	
    def F(self):              
        """Brennpunkt""" 
        return Vektor(self.p / 2, 0)
	
    f = F	
		
    @property	
    def brenn_punkt(self):              
        """Brennpunkt""" 
        return self.f

    brennPunkt = brenn_punkt
	
    @property	
    def num_exz(self):              
        """Nummerische Exzentrizität"""        
        return 1
		
    eps = num_exz
    numExz = num_exz	
	
    @property		
    def gleich(self):              
        """Gleichung; nur zur Ausgabe"""
        p = self.p
        x, y = Symbol('x'), Symbol('y')		
        lat = latex(y**2) + '=' + latex(2*p*x)
        return display(Math(lat))			
    def gleich_(self, *punkt, **kwargs):              
        """Gleichung; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nBei Einsetzen eines Punktes Auswertung der Gleichung in diesem\n")
            print("Zusatz   g=ja   Bereitstellung der Gleichung als Gleichung-Objekt\n")			
            return
            return
        x, y = Symbol('x'), Symbol('y')	
        p = self.p
        gl = Gleichung(y**2, 2*p*x)
        if kwargs.get('g'):
            return gl	
        gl = gl - 2*p*x
        gl = gl.lhs		
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
        if bool(simplify(gl.subs({x:punkt.x, y:punkt.y})) == 0):
            lat = latex('\\text{die Gleichung ist erfüllt}')
        else:
            lat = latex('\\text{die Gleichung ist nicht erfüllt}')		
        return display(Math(lat))
		
    Gleich = gleich_	
	
    @property
    def in_kurve(self):
        """Konvertierung in Kurve"""
        p = self.p
        t = Symbol("t")
        pp = Vektor(t**2/(2*p), t)		
        Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
        return Kurve(pp, (t, -100, 100))		
		
    inKurve = in_kurve		
		
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar	

    @property		
    def scheitel(self):              
        """Scheitelpunkt"""
        return Vektor(0, 0)
	
    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        t, x, y = Symbol('t'), Symbol('x'), Symbol('y')	
        X = Vektor(x, y)
        p = self.p
        vv = Vektor(t**2/(2*p), t)   
        lat = latex(X) + '=' + latex(vv)
        return display(Math(lat))
		
	
    def pkt(self, *par_wert, **kwargs):
        """Parabelpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt der Parabel\n")		
            print("Aufruf   parabel . pkt( /[ wert ] )\n")		                     
            print("             parabel   Parabel")
            print("             wert      Wert des Parabelparameters\n")		
            print("Rückgabe     bei Angabe eines Parameterwertes:")
            print("             Parabelpunkt, der zu diesem Wert gehört")
            print("             bei leerer Argumentliste oder freiem Bezeichner:") 
            print("             allgemeiner Punkt der Parabel\n") 			
            return 
			
        t = Symbol("t")
        p = self.p
        if not par_wert:
            p = Vektor(t**2/(2*p), t)
            return p
        if len(par_wert) == 1:
            pw = sympify(par_wert[0]) 
            if is_zahl(pw):
                p = Vektor(pw**2/(2*p), pw).einfach
                return p			
            print("agla: Zahl angeben")	
            return			 
        print("agla: einen Parameterwert angeben")
        return
	
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar von Parabeln; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")			
            return
			
        if kwargs.get('h'):
            print("\nElement einer Parabelschar\n")		
            print("Aufruf   parabel . sch_el( wert )\n")		                     
            print("             parabel   Parabel")
            print("             wert      Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        par = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter angeben')	
            return	
        try:			
            wert = nsimplify(wert)
        except RecursionError:
            pass		
        if not mit_param(wert):
            if wert <= 0:
                print("agla: Parameter > 0 angeben")
                return			
        p = self.p.subs(par, wert)
        return Parabel(p)			
	
    schEl = sch_el
		
		
    def tangente(self, *args, **kwargs):
        """Tangente"""
		
        if kwargs.get('h'):
            print("\nTangente in einem Parabelpunkt\n")	
            print("Aufruf   parabel . tangente( punkt )\n")		                     
            print("             parabel   Parabel")
            print("             punkt     Punkt der Parabel\n")			
            return 				
			
        if len(args) != 1:
            print("agla: einen Punkt angeben")
            return
        pkt = args[0]			
        if not isinstance(pkt, Vektor):
            print("agla: einen Punkt der Ebene angeben")
            return
        if pkt.dim != 2:
            print("agla: einen Punkt der Ebene angeben")
            return
        x, y = Symbol('x'), Symbol('y')	
        p = self.p
        gl = Gleichung(y**2 - 2*p*x, 0)
        if simplify(gl.lhs.subs({x:pkt.x, y:pkt.y})) != 0:
            print("agla: Punkt der Parabel angeben")
            return		
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade
        if pkt == Vektor(0, 0):
            ta = Gerade(1, 0, 0)
        else:		
            if pkt.y > 0:		
                ta = Gerade(p/sqrt(2*p*pkt.x), pkt.y-p*pkt.x/sqrt(2*p*pkt.x))
            else:				
                ta = Gerade(-p/sqrt(2*p*pkt.x), (pkt.y+p*pkt.x/sqrt(2*p*pkt.x)))
        return ta					
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Parabel bei einer Abbildung\n")		
            print("Aufruf   parabel . bild( abb )\n")		                     
            print("             parabel   Parabel")
            print("             abb       Abbildung der Ebene R^2\n")	
            print("Es wird ein Kurve2terOrdnung-Objekt erzeugt\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        if not (isinstance(abb, Abbildung) and  abb.dim == 2):
            print("agla: eine Abbildung der Ebene angeben")
            return
        p = self.p
        x, y, U, V = Symbol('x'), Symbol('y'), Symbol('U'), Symbol('V')		
        gl = y**2 - 2*p *x		
        uv = abb.matrix.inverse * (Vektor(U, V) - abb.versch)		
        gl = gl.subs({x:uv.x, y:uv.y})		
        gl = gl.subs({U:x, V:y})		
        gls = str(gl)
        return K2O(gls)		
	
				
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Parabel"""	

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
            x, y = Symbol('x'), Symbol('y')		
            gl = N(y**2 - 2 * self.p * x)	
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
        parabel_hilfe(3)	
		
    h = hilfe					
				
	
	
# Benutzerhilfe für Parabel
# -------------------------

def parabel_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nParabel - Objekt\n")
        print("Erzeugung in der Ebene R^2:\n")
        print("             Parabel( p )\n")
        print("                  p    Parameter in der Gleichung  y^2 = 2px\n")		
        print("Zuweisung    pb = Parabel(...)   (pb - freier Bezeichner)\n")
        print("Beispiel")
        print("Parabel(2)\n")
        return
		
    if h == 3:              
        print("\nEigenschaften und Methoden (M) für Parabel\n")
        print("pb.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("pb.bild(...)      M  Bild bei einer Abbildung")       
        print("pb.brenn_ger         Brenngerade (= pb.leit_ger)")     
        print("pb.brenn_punkt       = pb.F")     
        print("pb.dim               Dimension")
        print("pb.e                 = pb.lin_exz")
        print("pb.eps               = pb.num_exz")
        print("pb.F                 = pb.brenn_punkt")    
        print("pb.gleich            Gleichung")    
        print("pb.gleich_(...)   M  ebenso, zugehörige Methode")    
        print("pb.in_kurve          Konvertierung in Kurve")             
        print("pb.is_schar          Test auf Schar")        
        print("pb.leit_ger          = pb.brenn_ger")
        print("pb.lin_exz           Lineare Exzentrizität")
        print("pb.num_exz           Nummerische Exzentrizität")
        print("pb.p                 Parameter in der Gleichung y^2=2px")
        print("pb.pkt(...)       M  Parabelpunkt")                      
        print("pb.prg               Parametergleichung")
        print("pb.scheitel          Scheitelpunkt")	
        print("pb.sch_par           Parameter einer Schar")	
        print("pb.sch_el(...)    M  Element einer Schar")   
        print("pb.tangente(...)  M  Tangente\n")     
        print("Synonyme Bezeichner\n")
        print("hilfe       :  h")
        print("brenn_ger   :  brennGer")
        print("brenn_punkt :  brennPunkt")
        print("F           :  f")
        print("gleich_     :  Gleich")
        print("in_kurve    :  inKurve")
        print("is_schar    :  isSchar")
        print("leit_ger    :  leitGer")
        print("linExz      :  lin_exz")
        print("num_exz     :  numExz")
        print("sch_par     :  schPar")
        print("sch_el      :  schEl\n")
        return
   	
		
		
