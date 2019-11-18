#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Kurve2terOrdnung - Klasse  von agla           
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



from copy import copy
import importlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from IPython.display import display, Math

from sympy import sqrt, sin, cos, sinh, cosh, asinh, acosh, Abs, sign 
from sympy.core.evalf import N	 
from sympy.core.sympify import sympify 
from sympy.core.symbol import Symbol, symbols 
from sympy.solvers.solvers import solve
from sympy.polys.polytools import Poly
from sympy.core.containers import Tuple
from sympy.simplify.simplify import simplify, nsimplify
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.matrix import matrix2vektor
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (Gleichung, mit_param, is_zahl, 
    determinante)
from agla.lib.funktionen.graf_funktionen import rgb2hex			
from agla.lib.objekte.umgebung import UMG	
import agla	
	

	
# Kurve2terOrdnung - Klasse
# --------------------------	
	
class Kurve2terOrdnung(AglaObjekt):                                      
    """	
Kurve 2. Ordnung in der Ebene

**Kurzform**

   **K2O** 

**Synonym**

   **KegelSchnitt** 

**Erzeugung** 
	
   Kurve2terOrdnung ( *gleichung* ) 
   
   *oder*

   K2O ( *gleichung* ) 
      
**Parameter**

   *gleichung* : Gleichung der Kurve 2. Ordnung in den Variablen *x, y* als 
   Zeichenkette '*F(x, y) = 0* ' oder als Ausdruck *F(x, y)*  (rechte Seite 
   wird mit 0 angenommen); die Variablennamen sind zwingend
	
    """
				
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            k2o_hilfe(kwargs["h"])		
            return	
						
        if len(args) != 1:
            print("agla: ein Argument angeben")
            return			
        gl = args[0]
        if not isinstance(gl, (str, Gleichung)): 
             if not isinstance(gl, Gleichung):		
                 gl = str(gl)	
        if isinstance(gl, Gleichung):
            gl = str(gl.lhs)
        else:			
            id = gl.find('=')
            if id > 0:
                if sympify(gl[id+1:]) != 0:
                    print("agla: die rechte Seite der Gleichung muss 0 sein")
                    return				
                gl = gl[:id]
        x, y = Symbol('x'), Symbol('y')	
        if gl.find('x') < 0 or gl.find('y') < 0:
            print("agla: die Gleichung muß x und y enthalten")
            return

        try:
            gl = nsimplify(gl)
        except RecursionError:						
            pass					
							
        x, y = Symbol("x"), Symbol("y")			 
        di = dict()
			 
        try:			 
            p = Poly(gl, (x, y))
        except PolynomialError:
            print('agla: die Gleichung ist fehlerhaft')
            return			
        if p.total_degree() != 2:
            print('agla: die Gleichung muss den Grad 2 haben')
            return	
			
        px = p.subs(y, 0)
        py = p.subs(x, 0)
        if px == 0:
            di['f'], di['xx'], di['x'] = 0, 0, 0 
        else:
            dix = dict(Poly(px).all_terms())			
            di['f'] = dix[(0,)]
            try: 
                di['xx'] = dix[(2,)]
            except KeyError:
                di['xx'] = 0
            try:
                di['x'] = dix[(1,)]
            except KeyError:
                di['x'] = 0						
        if py == 0:
            di['yy'], di['y'] = 0, 0
        else:
            diy = dict(Poly(py).all_terms())
            try:
                di['yy'] = diy[(2,)]
            except KeyError:
                di['yy'] = 0
            try:
                di['y'] = diy[(1,)]
            except KeyError:
                di['y'] = 0			
				
        p -= (di['xx']*x**2 + di['yy']*y**2 + di['x']*x + di['y']*y + + di['f'])
        di['xy'] = p / x / y

        gleich = Gleichung(Poly(gl).as_expr(), 0)				
        koeff_dict = di
		
        return AglaObjekt.__new__(cls, gleich, koeff_dict)
		   
		   
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "KegelSchnittSchar(" + ss + ")"
        return "KegelSchnitt"					
		   
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 2
		
    @property
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    @property
    def sch_par(self):              
        """Scharparameter"""
        x, y = symbols('x y')		
        return self.gleich.free_symbols.difference({x, y})       			

    @property
    def M(self):
        """Matrix der Gleichung"""
        di = self.args[1]
        xx, xy, yy, = Symbol('xx'), Symbol('xy'), Symbol('yy')
        m = Vektor(di[xx], di[xy]/2) | Vektor(di[xy]/2, di[yy]) 
        return m
        
    m = M
	
    @property
    def MM(self):
        """Erweiterte Matrix der Gleichung"""
        di = self.args[1]
        xx, xy, yy, x, y, f = symbols('xx, xy, yy, x, y, f') 
        m = Vektor(di[xx], di[xy]/2, di[x]/2) | \
            Vektor(di[xy]/2, di[yy], di[y]/2) | \
            Vektor(di[x]/2, di[y]/2, di[f]) 
        return m
		
    mm = MM
	
    @property
    def gleich(self):                     
        """Gleichung"""
        return self.args[0]
    def gleich_(self, *args, **kwargs):                     
        """Gleichung; zugehörige Methode"""		
        if kwargs.get('h'):	
            print("\nBei Angabe eines x-Wertes Ermittlung der/des dazugehörenden")
            print("Punkte(s) des Kegelschnittes\n")
            return			
        if len(args) != 1:        
            print("agla: einen x-Wert angeben")
            return
        wert = sympify(*args)
        if not is_zahl(wert):
            print("agla: eine Zahl für den x-Wert angeben")
            return		
        x, y = Symbol('x'), Symbol('y')			
        gl = self.gleich.lhs.subs(x, wert)
        L = solve(gl, [y], dict=True)
        if len(L) == 2:		 
            return Vektor(wert, L[0][y]), Vektor(wert, L[1][y]) 
        elif len(L) == 1:		 
            return Vektor(wert, L[0][y]) 
        if len(L) == 0:		 
            return set() 

    Gleich = gleich_			
		
    @property
    def gleich_m(self):                     
        """Gleichung in Matrixform; nur zur Ausgabe"""
        m, mm = self.M, self.MM
        x, y = Symbol('x'), Symbol('y')
        xx = Vektor(x, y)		
        vv = 2 * Vektor(mm[0, 2], mm[1, 2])
        if vv.x != 0 or vv.y != 0:
            lat1 = '+' + latex(vv.T) + latex(xx)
        else:
            lat1 = ''		
        f = mm[2, 2]	
        if f > 0:
            frei = '+' + str(f)		
        elif f < 0:
            frei = '-' + str(-f)		
        else:
            frei = ''
        lat = latex(xx.T) + latex(m) + latex(xx) + lat1 + frei + '=0'		
        display(Math(lat + '\\quad oder'))
        xx = Vektor(x, y, 1)		
        lat = latex(xx.T) + latex(mm) + latex(xx) + '=0'		
        display(Math(lat))
		
    @property
    def typ(self):                     
        """Kurventyp"""
		
        # Bronstein S182 ff
		
        m, mm = self.M, self.MM
        if mit_param(m) or mit_param(mm):
            print('agla: nicht implementiert (Parameter)')
            return			
        delta, Delta = m.D, mm.D
        ss = m[0, 0] + m[1, 1] 
        x, y = Symbol('x'), Symbol('y')		   
        if delta != 0:
            if delta > 0:
                if Delta != 0:
                    if Delta * ss < 0:
                        return Symbol('Ellipse')
                    else:
                        return Symbol('ImaginaereEllipse')
                else:
                    return Symbol('ImaginaereGeraden')
            elif delta < 0:
                if Delta != 0:
                    return Symbol('Hyperbel')
                else:
                    return Symbol('SchneidendeGeraden')
                return					
        elif delta == 0:
            if Delta != 0:
                return Symbol('Parabel')
            elif Delta == 0:
                if not self.gleich.has(x):  # y -> x
                    mm[0, 0], mm[0, 2] = mm[1, 1], mm[1, 2]
                    mm[1, 1], mm[1,2] = 0, 0					
                dd = mm[0, 2]**2 - mm[0, 0] * mm[2, 2]
                if dd > 0:			
                    return Symbol('ParalleleGeraden')
                elif dd == 0:			
                    return Symbol('DoppelGerade')
                elif dd < 0:			
                    return Symbol('ImaginaereGeraden')
                return					
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Kegelschnittes bei einer Abbildung\n")		
            print("Aufruf   k2o . bild( abb )\n")		                     
            print("             k2o    Kegelschnitt")
            print("             abb    Abbildung\n")	
            return 				
			
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        if not (isinstance(abb, Abbildung) and  abb.dim == 2):
            print("agla: eine Abbildung der Ebene angeben")
            return
        x, y, U, V = Symbol('x'), Symbol('y'), Symbol('U'), Symbol('V')		
        gl = self.gleich.lhs		
        uv = abb.matrix.inverse * (Vektor(U, V) - abb.versch)
        gl = gl.subs({x:uv.x, y:uv.y})		
        gl = gl.subs({U:x, V:y})		
        gls = str(gl)
        return K2O(gls)		
		
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer K2O-Schar\n")		
            print("Aufruf   K2O . sch_el( wert )\n")		                     
            print("             K2O     Kurve 2. Ordnung")
            print("             wert    Wert des Scharparameters\n")			
            print("Es ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print("agla: Zahlenwert angeben")
            return
        gl = self.gleich
        gl = gl.subs(p, wert)
        return Kurve2terOrdnung(gl)		

    schEl = sch_el
		
				
    def graf(self, spez, **kwargs):                       
        """Grafikelement für K2O"""
		
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' else \
                                                             spez[2][3]	
        lin_farbe = rgb2hex(lin_farbe)
															 
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:			
            xl, xr, yl, yr = UMG._sicht_box[:4]
            y, x = np.ogrid[yl:yr:100j, xl:xr:100j]  # Reihenfolge!
            gl = self.gleich
            gl = str(N(gl.lhs))
            egl = eval(gl)
            return plt.gca().contour(x.ravel(), y.ravel(), egl, [0], 
                  colors=lin_farbe, linewidths=lin_staerke)
				

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften"""
        k2o_hilfe(3)	
		
    h = hilfe				
				

			
# Benutzerhilfe für Kurve2terOrdnung
# ------------------------------------

def k2o_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nKurve2terOrdnung - Objekt\n")
        print("Erzeugung in der Ebene R^2:\n")
        print("             Kurve2terOrdnung( gleichung )\n")
        print("                 gleichung    Gleichung der Kurve 2. Ordnung in den")
        print("                              Variablen x, y als Zeichenkette")
        print("                              'F(x, y) = 0'  oder als Ausdruck")
        print("                               F(x, y) (rechte Seite wird mit 0 ange-")
        print("                                        nommen)")
        print("                              (die Variablennamen sind zwingend)\n") 
        print("Synonyme Namen   K2O   KegelSchnitt\n")
        print("Zuweisung     k = K2O(...)   (k - freier Bezeichner)\n")
        print("Beispiel")
        print("K2O('x^2 - y^2 + 5*x*y + 2*x = 0')\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoddn (M) für Kurve2terOrdnung\n")
        print("k.hilfe          Bezeichner der Eigenschaften")
        print("k.bild        M  Bild bei einer Abbildung")
        print("k.dim            Dimension")
        print("k.gleich         Eingabegleichung") 
        print("k.gleich_     M  ebenso; zugehörige Methode") 
        print("k.gleich_m       Gleichung in Matrixform") 
        print("k.is_schar       Test auf Schar")
        print("k.M              Matrix der Gleichung")
        print("k.m              = M")
        print("k.MM             Erweiterte Matrix der Gleichung")
        print("k.mm             = MM")
        print("k.sch_el(...) M  Element einer Schar")
        print("k.sch_par        Parameter einer Schar")
        print("k.typ            Typ\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("gleich_   :  Gleich")
        print("gleich_m  :  gleichM")
        print("is_schar  :  isSchar")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar\n")
        return		
     	  
	
K2O = Kurve2terOrdnung
KegelSchnitt = Kurve2terOrdnung
		
	
	
