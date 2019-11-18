#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Ellipse - Klasse  von agla           
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
import matplotlib.patches as patches
			
from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.simplify.simplify import nsimplify, simplify
from sympy.core.symbol import Symbol, symbols
from sympy.core.numbers import Integer, pi
from sympy.functions.elementary.miscellaneous import sqrt
from sympy import sqrt, sin, cos
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, v, X
from agla.lib.objekte.abbildung import Abbildung
from agla.lib.objekte.k2o import K2O
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    ja, Ja, nein, Nein, mit, ohne, sing, cosg, sqrt, wert_ausgabe, Gleichung)
from agla.lib.funktionen.graf_funktionen import rgb2hex				
from agla.lib.objekte.umgebung import UMG	
import agla



# Ellipse - Klasse
# --------------
	
class Ellipse(AglaObjekt):                                      
    """
Ellipse in der Ebene
	
**Erzeugung** 
	
   Ellipse ( */[ mitte, ] a, b* ) 
   
**Parameter**

   *mitte* : Mittelpunkt; Ursprung, wenn weggelassen
   
   *a, b* :  Halbachsen 
   	
    """

	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            ellipse_hilfe(kwargs["h"])		
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
            a, b = sympify(a), sympify(b)				
            if not isinstance(mitte, Vektor):			
                raise AglaError("für Mittelpunkt Punkt der Ebene angeben")
            if mitte.dim != 2:				
                raise AglaError("für Mittelpunkt Punkt der Ebene angeben")
            if not is_zahl(a) or not is_zahl(b):
                raise AglaError("Für die Halbachsen Zahlen angeben")
            if not mit_param(a) and not mit_param(b):
                if a < 0 or b < 0:
                    raise AglaError("2 positive Zahlen angeben")				
                if a < b:
                    raise AglaError("1. Halbachse > 2. Halbachse angeben")
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
            return "Ellipsenschar(" + ss + ")"
        return "Ellipse"			

		
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
        return sqrt(self.a**2 - self.b**2)
		
    e = lin_exz
    linExz = lin_exz	

    @property	
    def brenn_ger(self):              
        """Brenn- / Leitgerade""" 
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        g1 = Gerade(1, 0, -self.mitte.x - self.a**2 / self.e)		
        g2 = Gerade(1, 0, -self.mitte.x + self.a**2 / self.e)		
        return g1, g2

    brennGer = brenn_ger
    leit_ger = brenn_ger
    leitGer = brenn_ger
	
    @property	
    def F1(self):              
        """Erster Brennpunkt""" 
        return Vektor(self.mitte.x + self.e, self.mitte.y)
		
    f1 = F1
	
    @property	
    def F2(self):              
        """Zweiter Brennpunkt""" 
        return Vektor(self.mitte.x - self.e, self.mitte.y)
		
    f2 = F2
		
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
        lat = '\\frac{' + x + '}{' + a + '}' + '+' + '\\frac{' + y + \
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
        gl = Gleichung((x - m.x)**2 / a**2 + (y - m.y)**2 / b**2, 1)
        if kwargs.get('g'):
            return gl
        gl = Gleichung((x - m.x)**2 / a**2 + (y - m.y)**2 / b**2, 1)
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
        t = Symbol("t")
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
        return Kurve(self.pkt(t*180/pi), (t, 0, 2*pi))		
		
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
        vv = Vektor(a*cos(t), b*sin(t))   
        if m == Vektor(0, 0):
            lat = latex(X) + '=' + latex(vv)
        else:			
            lat = latex(X) + '=' + latex(vv) + '+' + latex(m)		
        return display(Math(lat))
				
    @property			
    def umfang(self):              
        """Umfang"""
        k = self.in_kurve
        return k.bog_laenge
			
    @property			
    def flaeche(self):              
        """Flächeninhalt"""
        return pi * self.a * self.b
    def flaeche_(self, **kwargs):  
        """Flächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'A' + '=' + '\\pi a b' + '\\quad\\quad a,\, b - Halbachsen'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('                        n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')			
            return
        f = self.flaeche
        d = kwargs.get('d')
        return wert_ausgabe(f, d)
				
    Flaeche = flaeche_				
	
	
    def pkt(self, *par_wert, **kw):
        """Ellipsenpunkt"""
		
        if kw.get('h'):
            print("\nPunkt der Ellipse\n")		
            print("Aufruf   ellipse . pkt( /[ wert ] )\n")		                     
            print("             ellipse   Ellipse")
            print("             wert      Wert des Ellipsenparameters (in Grad)\n")		
            print("Rückgabe     bei Angabe eines Parameterwertes:")
            print("             Ellipsenpunkt, der zu diesem Wert gehört")
            print("             bei leerer Argumentliste oder freiem Bezeichner:") 
            print("             allgemeiner Punkt der Ellipse\n") 			
            return 
			
        t = Symbol("t")
        m, a, b = self.args
        if not par_wert:
            p = self.mitte + Vektor(a*cosg(t), b*sing(t))
            return p
        if len(par_wert) == 1:
            pw = sympify(par_wert[0]) 
            if is_zahl(pw):
                p = self.mitte + Vektor(a*cosg(pw), b*sing(pw)).einfach
                return p			
            print("agla: Zahl zwischen 0 und 360 angeben")	
            return			 
        print("agla: einen Parameterwert angeben")
        return
	
				
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar von Ellipseen; vorerst für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")			
            return
			
        if kwargs.get('h'):
            print("\nElement einer Ellipsenschar\n")		
            print("Aufruf   ellipse . sch_el( wert )\n")		                     
            print("             ellipse   Ellipse")
            print("             wert      Wert des Scharparameters")			
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
        if not mit_param(a) and not mit_param(b) and a < b:   
            print('agla: die 1. Halbachse muss > 2. Halbachse sein')	
            return	
        return Ellipse(m, a, b)			
	
    schEl = sch_el
		
		
    def tangente(self, *args, **kwargs):
        """Tangente"""
		
        if kwargs.get('h'):
            print("\nTangente in einem Ellipsenpunkt\n")	
            print("Aufruf   ellipse . tangente( punkt )\n")		                     
            print("             ellipse   Ellipse")
            print("             punkt     Punkt der Ellipse\n")			
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
        gl = Gleichung((x - m.x)**2 / a**2 + (y - m.y)**2 / b**2, 1)
        if simplify(gl.lhs.subs({x:p.x, y:p.y})) != 1:
            print("agla: Punkt der Ellipse angeben")
            return		
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        ta = Gerade((p.x-m.x) / a**2, (p.y-m.y) / b**2, \
                       -1 -m.x*(p.x-m.x)/a**2 -m.y*(p.y-m.y)/b**2)
        return ta					
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Ellipse bei einer Abbildung\n")		
            print("Aufruf   ellipse . bild( abb )\n")		                     
            print("             ellipse   Ellipse")
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
        a, b, m = self.a, self.b, self.mitte
        x, y, U, V = Symbol('x'), Symbol('y'), Symbol('U'), Symbol('V')		
        gl = (x - m.x)**2/a**2 + (y - m.y)**2/b**2 - 1		
        uv = abb.matrix.inverse * (Vektor(U, V) - abb.versch)		
        gl = gl.subs({x:uv.x, y:uv.y})		
        gl = gl.subs({U:x, V:y})		
        gls = str(gl)
        return K2O(gls)		
	
	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Ellipse"""	

        # 'füll=True' - gefüllte Darstellung; default - ungefülte Darstellung	
		
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' else \
                                                             spez[2][3]
        lin_farbe = rgb2hex(lin_farbe)
		
        fuell = None			
        if len(spez) > 4:
            for s in spez[4]:
                if 'fuell' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper() or '1' in s.upper():
                        fuell = True
		
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:	
            m, a, b  = self.args	
            if not fuell:	
                ellipse = patches.Ellipse((m.x, m.y), 2*float(a), 
                         2*float(b), fill=None, 
                         edgecolor=lin_farbe, linewidth=lin_staerke)
                plt.gca().add_patch(ellipse)
                return plt.plot([0], [0], 'w', markersize=0.0001)  # dummy plot	 
            else:
                ellipse = patches.Ellipse((m.x, m.y), 2*float(a), 
                         2*float(b), facecolor=lin_farbe, 
                         edgecolor=lin_farbe)
                plt.gca().add_patch(ellipse)
                return plt.plot([0], [0], 'w', markersize=0.0001)		 
	
    @property	
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        ellipse_hilfe(3)	
		
    h = hilfe		
	
	
	
# Benutzerhilfe für Ellipse
# -----------------------

def ellipse_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nEllipse - Objekt\n")
        print("Erzeugung in der Ebene R^2:\n")
        print("             Ellipse( /[ mitte, ] a, b )\n")
        print("                mitte   Mittelpunkt; Ursprung, wenn weggelassen")		
        print("                a, b    Halbachsen\n")		
        print("Zuweisung     e = Ellipse(...)   (e - freier Bezeichner)\n")
        print("Beispiele")
        print("Ellipse(5, 3)")
        print("Ellipse(v(2, 3), a, 2)\n")
        return
		
    if h == 3:              
        print("\nEigenschaften und Methoden (M) für Ellipse\n")
        print("e.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("e.a                 Länge der 1. Halbachse")       
        print("e.b                 Länge der 2. Halbachse")       
        print("e.bild(...)      M  Bild bei einer Abbildung")       
        print("e.brenn_ger         Brenngeraden ( = e.leit_ger))")     
        print("e.brenn_punkt       Brennpunkte")     
        print("e.dim               Dimension")
        print("e.e                 = e.lin_exz")
        print("e.eps               = e.num_exz")
        print("e.fläche            Flächeninhalt")
        print("e.fläche_(...)   M  ebenso, zugehörige Methode")
        print("e.F1                1. Brennpunkt")    
        print("e.f1                = e.F1")    
        print("e.F2                2. Brennpunkt")    
        print("e.f2                = e.F2")    
        print("e.gleich            Gleichung")    
        print("e.gleich_(...)   M  ebenso, zugehörige Methode")    
        print("e.in_kurve          Konvertierung in Kurve")             
        print("e.is_schar          Test auf Schar")        
        print("e.leit_ger          Leitgeraden")
        print("e.lin_exz           Lineare Exzentrizität")
        print("e.mitte             Mittelpunkt")
        print("e.num_exz           Nummerische Exzentrizität")
        print("e.pkt(...)       M  Ellipsenpunkt")                      
        print("e.prg               Parametergleichung")
        print("e.sch_el(...)    M  Element einer Schar")   
        print("e.sch_par           Parameter einer Schar")	
        print("e.tangente(...)  M  Tangente")     
        print("e.umfang            Umfang\n")     
        print("Synonyme Bezeichner\n")
        print("hilfe       :  h")
        print("brenn_ger   :  brennGer")
        print("brenn_punkt :  brennPunkt")
        print("fläche_     :  Fläche")
        print("F1          :  f1")
        print("F2          :  f2")
        print("gleich_     :  Gleich")
        print("in_kurve    :  inKurve")
        print("is_schar    :  isSchar")	
        print("leit_ger    :  leitGer")
        print("lin_exz     :  linExz")
        print("num_exz     :  numExz")
        print("sch_el      :  schEl")
        print("sch_par     :  schPar\n")
        return   
   	
		
		
