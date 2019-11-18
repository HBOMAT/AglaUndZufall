#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Kreis - Klasse  von agla           
#                                                 
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
                                             



import importlib, copy

import numpy as np
from agla.lib.objekte.umgebung import UMG	
if UMG.grafik_3d == 'mayavi':
    from mayavi import mlab
else:
    from vispy import scene	
import matplotlib.pyplot as plt
import matplotlib.patches as patches
			
from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.simplify.simplify import nsimplify, simplify
from sympy.core.symbol import Symbol, symbols
from sympy.core.numbers import Float, Integer, Rational, pi, I
from sympy.solvers.solvers import solve
from sympy.core.function import expand
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.evalf import N
from sympy import sin, cos, Abs
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, v, X
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    ja, Ja, nein, Nein, mit, ohne, sing, cosg, Gleichung, loese, wert_ausgabe)
from agla.lib.funktionen.graf_funktionen import _funkt_sympy2numpy 	
import agla                 

import importlib
Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene


# Kreis - Klasse
# --------------
	
class Kreis(AglaObjekt):                                      
    """Kreis im Raum und in der Ebene
	
**Erzeugung** 

   Kreis ( *ebene, mitte, radius* )
   
      (im Raum)   
 
   Kreis ( *mitte, radius* )
   
      (in der Ebene)   
	  
**Parameter**	
	
   *ebene* :    Trägerebene
   
   *mitte* :    Mittelpunkt
   
   *radius* :   Radius  	
	
**Vordefinierte Kreise**

   ``EinhKreis`` :   Einheitskreis im Raum

   ``EinhKreis2`` :  Einheitskreis in der Ebene
	
    """
	
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            kreis_hilfe(kwargs["h"])		
            return	
			
        try:			
            if not 2 <= len(args) <= 3:
                txt = "Trägerebene (nur in R^3), Mittelpunkt und Radius angeben"
                raise AglaError(txt)
            if len(args) == 2:
                a1, a2 = args
                a2 = sympify(a2)
                if not (isinstance(a1, Vektor) and a1.dim == 2 and is_zahl(a2)):
                    raise AglaError("Trägerebene (in R^3), " + \
                         "Mittelpunkt und Radius angeben")
                return AglaObjekt.__new__(cls, a1, a2)
            else:
                a0, a1, a2 = args
                a2 = sympify(a2)
                if not (isinstance(a0, Ebene) and isinstance(a1, Vektor) and 
			             a1.dim == 3 and is_zahl(a2)):
                    raise AglaError("Trägerebene, Mittelpunkt und Radius " + \
                         "angeben")
                if not mit_param(a1.abstand(a0)) and a1.abstand(a0) > 0:
                    raise AglaError("der Mittelpunkt muß in der Ebene liegen")
                try:					
                    a2 = nsimplify(a2)
                except RecursionError:	
                    pass				
                return AglaObjekt.__new__(cls, a1, a2, a0)
        except AglaError as e:
            print('agla:', str(e))
            return			

   
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Kreisschar(" + ss + ")"
        return "Kreis"			

		
# Für Kreise in R^3 und R^2 gemeinsame Eigenschaften + Methoden
# -------------------------------------------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return self.args[0].dim
		
    @property
    def mitte(self):              
        """Mittelpunkt"""
        return self.args[0]

    M = mitte
    m = mitte
	 
    @property	
    def radius(self):              
        """Radius"""
        return self.args[1]
    def radius_(self, **kwargs):  
        """Radius; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        r = self.radius
        d = kwargs.get('d')
        return wert_ausgabe(r, d)

    r = radius		
    Radius = radius_
    r_ = radius_	
	
    @property			
    def umfang(self):              
        """Umfang"""
        return 2 * pi * self.radius
    def umfang_(self, **kwargs):  
        """Umfang; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'U' + '=' + '2 \\pi r \quad\quad r - Radius'
            display(Math(txt))
            return			
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('                        n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')			
            return
        u = self.umfang
        d = kwargs.get('d')
        return wert_ausgabe(u, d)

    laenge = umfang
    laenge_ = umfang_
    Laenge = umfang_	
    Umfang = umfang_
	
    @property			
    def flaeche(self):              
        """Flächeninhalt"""
        return pi * self.radius**2
    def flaeche_(self, **kwargs):  
        """Flächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'A' + '=' + '\\pi r^2 \quad\quad r - Radius'
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
	
    @property		
    def ebene(self):               
        """Trägerebene; nur im Raum"""
        if self.dim != 3:
            print('agla: nur im Raum R^3 verfügbar')		
            return 
        return self.args[2]		
		
    @property			
    def sch_par(self):              
        """Scharparameter"""
        ret = self.args[0].free_symbols.union(self.args[1].free_symbols)
        if self.dim == 3:
            ret |= self.args[2].stuetz.free_symbols
            ret |= self.args[2].norm.free_symbols
        return ret
	
    schPar = sch_par	
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar	
		
    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        x, y, z, t = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('t')		
        if self.dim == 3:		
            v1 = self.ebene.richt[0]
            v2 = -v1.vp(self.ebene.norm)
            v1 = v1.einh_vekt
            v2 = v2.einh_vekt
            t0 = latex(Vektor(x, y, z)) + '='
        else:
            v1 = Vektor(1, 0)
            v2 = Vektor(0, 1)	
            t0 = latex(Vektor(x, y)) + '='			
        r = self.radius
        t1 = latex(self.mitte) + '+'		
        t2 = latex(r*cos(t)) + latex(v1) + '+'
        t3 = latex(r*sin(t)) + latex(v2)
        return display(Math(t0 + t1 + t2 + t3))
		
    @property		
    def gleich(self):              
        """Gleichung"""
        x, y, z, t = symbols('x y z t')		
        if self.dim == 3:
            v1 = self.ebene.richt[0]
            v2 = -v1.vp(self.ebene.norm)
            v1 = v1.einh_vekt
            v2 = v2.einh_vekt
            r = self.radius
            gl = Gleichung(Vektor(x, y, z), self.mitte + r*cos(t)*v1 + \
                          r*sin(t)*v2)
        else:
            m = self.mitte
            r = self.radius
            gl = Gleichung((x - m.x)**2 + (y - m.y)**2, r**2)
        return gl			
    def gleich_(self, *punkt, **kwargs):              
        """Gleichung; zugehörige Methode"""
        if self.dim == 3:
            print("agla: nur in der Ebene R^2 verfügbar")		
            return
        if kwargs.get('h'):
            print('\nBei Einsetzen eines Punktes Auswertung der Gleichung in diesem\n')
            return
        if not 0 < len(punkt) < 2:
            print("agla: einen Punkt der Ebene angeben")
            return        		
        punkt = punkt[0]
        if not (isinstance(punkt, Vektor) and punkt.dim == 2):	
            print("agla: einen Punkt der Ebene angeben")
            return
        gl = self.gleich.lhs
        x, y = Symbol('x'), Symbol('y')		
        if bool(simplify(gl.subs({x:punkt.x, y:punkt.y})) == self.radius**2):
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
	

    def bogen(self, *bereich, **kwargs):
        """Kreisbogen"""
		
        if kwargs.get('h'):
            print("\nKreisbogen\n")		
            print("Aufruf     kreis . bogen( par_unt, par_ob )\n")		                     
            print("               kreis     Kreis")
            print("               par_unt   untere und obere Bereichsgren-")	
            print("               par_ob    zen des Parameters (in Grad)\n")
            return 

        bereich = sympify(bereich)
        if not (isinstance(bereich, Tuple) and len(bereich) == 2):  
            print("agla: untere und obere Bereichsgrenze angeben")
            return			
        if not (is_zahl(bereich[0]) and is_zahl(bereich[1])):			
            print("agla: zwei Zahlenwerte angeben")
            return
        t = Symbol('t')
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
        return Kurve(self.pkt(t), (t, bereich[0], bereich[1]))
	
	
    def pkt(self, *par_wert, **kwargs):
        """Kreispunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt des Kreises\n")		
            print("Aufruf   kreis . pkt( /[ wert ] )\n")		                     
            print("             kreis    Kreis")
            print("             wert     Wert des Kreisparameters (in Grad)\n")		
            print("Rückgabe   bei Angabe eines Parameterwertes:")
            print("           Kreispunkt, der zu diesem Wert gehört")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           allgemeiner Punkt des Kreises\n") 			
            return 
			
        dim = 3 if self.dim == 3 else 2
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        r  = self.radius
        if dim == 2:
            m = self.mitte
            m = Vektor(m.x, m.y, 0)			
            self = Kreis(Ebene(0, 0, 1, 0), m, r)		
        v1 = self.ebene.richt[0].einh_vekt
        v2 = -v1.vp(self.ebene.norm).einh_vekt
        t = Symbol("t", real=True)
        if not par_wert:
            if dim == 2:
                px = self.mitte.x + r*cosg(t) * v1.x + r*sing(t) * v2.x
                py = self.mitte.y + r*cosg(t) * v1.y + r*sing(t) * v2.y
                return Vektor(px, py)
            else:				
                px = self.mitte.x + r*cosg(t) * v1.x + r*sing(t) * v2.x
                py = self.mitte.y + r*cosg(t) * v1.y + r*sing(t) * v2.y				
                pz = self.mitte.z + r*cosg(t) * v1.z + r*sing(t) * v2.z				
                return Vektor(px, py, pz)
        if len(par_wert) == 1:
            pw = par_wert[0]
            if is_zahl(pw):
                if  dim == 2:
                    px = self.mitte.x + r*cosg(pw) * v1.x + r*sing(pw) * v2.x
                    py = self.mitte.y + r*cosg(pw) * v1.y + r*sing(pw) * v2.y
                    return Vektor(px, py)				                     					 
                px = self.mitte.x + r*cosg(pw) * v1.x + r*sing(pw) * v2.x
                py = self.mitte.y + r*cosg(pw) * v1.y + r*sing(pw) * v2.y				
                pz = self.mitte.z + r*cosg(pw) * v1.z + r*sing(pw) * v2.z				
                return Vektor(px, py, pz)
            print("agla: Zahl zwischen 0 und 360 angeben")	
            return			 
        print("agla: einen Parameterwert angeben")
        return
		

    def sch_el(self, *wert, **kwargs):
        """Element einer Schar von Kreisen; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")			
            return
			
        if kwargs.get('h'):
            print("\nElement einer Kreisschar\n")		
            print("Aufruf   kreis . sch_el( wert )\n")		                     
            print("             kreis    Kreis")
            print("             wert     Wert des Scharparameters")			
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
        if self.dim == 3:		
            ebene = self.ebene
            if p in ebene.sch_par:
                ebene = ebene.sch_el(wert)
        mitte = self.mitte
        radius = self.radius
        if p in mitte.sch_par:
            mitte = mitte.sch_el(wert)
        radius = self.radius.subs(p, wert)
        if not mit_param(radius) and radius < 0:   
            print('agla: der Radius kann nicht negativ sein')	
            return	
        if self.dim == 3:		
            return Kreis(ebene, mitte, radius)			
        return Kreis(mitte, radius)			
	
    schEl = sch_el


    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Kreises bei einer Abbildung\n")		
            print("Aufruf   kreis . bild( abb )\n")		                     
            print("             kreis    Kreis")
            print("             abb      Abbildung\n")
            print("Ist die Determinante der Abbildung  ungleich +/-1, wird ein")
            print("Kurve-Objekt erzeugt\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
        Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix	
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == self.dim):
            print("agla: eine Abbildung (mit gleicher Dimension) angeben")
            return
        m = abb.matrix
        if self.dim == 3:		
            m1 = Matrix(Vektor(1, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 1))			
            dd = simplify(m.D)
            if not mit_param(dd) and abs(abs(dd)-1) < 1e-6 or m == m1 * m[0, 0]:
                bebene = self.ebene.bild(abb)
                bmitte = self.mitte.bild(abb) 
                r = self.radius
                if m == m1 * m[0, 0]:
                    r = r * m[1, 1]
                return Kreis(bebene, bmitte, r)  
            t = Symbol('t')
            p = self.pkt(t*180/pi)
            q = p.bild(abb)
            return Kurve(q, (t, 0, 2*pi))
        else:		
            dd = simplify(m.D)
            if not mit_param(dd) and abs(abs(dd)-1) < 1e-6:
                bmitte = self.mitte.bild(abb) 
                r = self.radius
                return Kreis(bmitte, r)  
            t = Symbol('t')
            p = self.pkt(t*180/pi)
            q = p.bild(abb)
            return Kurve(q, (t, 0, 2*pi))

	
    def tangente(self, *args, **kwargs):
        """Tangenten"""
		
        if kwargs.get('h'):
            print("\nTangente in einem Kreispunkt oder von einem")	
            print("Punkt außerhalb (in der Ebene R^2)\n")			
            print("Aufruf   kreis . tangente( punkt )\n")		                     
            print("             kreis    Kreis")
            print("             punkt    Kreispunkt oder Punkt außerhalb\n")			
            return 				
			
        if self.dim != 2:
            print("agla: nur in der Ebene R^2 verfügbar")
            return
			
        if len(args) != 1:
            print("agla: einen Punkt angeben")
            return
        p = args[0]			
        if not isinstance(p, Vektor) and p.dim == 2:
            print("agla: einen Punkt der Ebene angeben")
            return
        if not (mit_param(self) or mit_param(p)):
            if N(p.abstand(self.mitte)) < N(self.radius):
                print("agla: innerer Punkt des Kreises, keine Tangente")
                return		
        m, r = self.mitte, self.radius
        x, y = Symbol('x'), Symbol('y')
        Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
        gl = self.gleich.lhs.subs({x:p.x, y:p.y}) - r**2		
        if mit_param(self) or mit_param(p):	
            if gl != 0:
                print("nur für Punkte auf dem Kreis implementiert")
                return
        if not simplify(gl):
            ta = Gerade(p.x-m.x, p.y-m.y, -m.x*(p.x-m.x)-m.y*(p.y-m.y)-r**2)
        else:
            L = solve([self.gleich.lhs-r**2, (x-m.x)*(p.x-m.x)+(y-m.y)*\
                     (p.y-m.y)-r**2]) 
            q1, q2 = Vektor(L[0][x], L[0][y]), Vektor(L[1][x], L[1][y])
            ta = Gerade(p, Vektor(p, q1)), Gerade(p, Vektor(p, q2))
        return ta			

		
    def schnitt(self, *objekt, **kwargs):
        """Schnitt mit einem anderen Objekt"""
		
        if kwargs.get('h'):
            print("\nSchnitt mit einem anderen Objekt (in der Ebene R^2)\n")			
            print("Aufruf   kreis . schnitt( objekt )\n")		                     
            print("             kreis    Kreis")
            print("             objekt   Punkt, Gerade, Kreis\n")
            print("Zusatz       l=ja        Lageinformationen")
            print("             exakt=nein  näherungsweise Berechnung\n")			
            return 
			
        if self.dim != 2:
            print("agla: nur in der Ebene R^2 verfügbar")
            return
			
        try:		
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")
            objekt = objekt[0]
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            if (not isinstance(objekt, (Vektor, Gerade, Kreis)) or 
                                                       objekt.dim != 2):
                raise AglaError("Punkt, Gerade oder Kreis in der Ebene " + \
				        "angeben")
        except AglaError as e:
            print('agla:', str(e))
            return
		
        exakt = True
        if kwargs.get('exakt') == False:
            exakt = False
        x, y = Symbol('x'), Symbol('y')
        p = self.mitte
        px, py	 = p.x, p.y
        try:	
            px, py = nsimplify(p.x), nsimplify(p.y)
        except RecursionError:
            pass	
			
        gleich = (x - px)**2 + (y - py)**2 - self.radius**2
		
        if isinstance(objekt, Vektor):
            q = objekt
            gl = gleich.subs({x:q.x, y:q.y})
            if exakt:
                erfuellt = bool(simplify(gl) == 0)		
            else:				
                erfuellt = bool(abs(simplify(gl)) < 1e-6)
            if erfuellt:
                if kwargs.get('l'):				           
                    display(Math('\\text{der Punkt liegt auf dem ' + \
					              'Kreis}'))
                    return
                return q
            if kwargs.get('l'):
                display(Math('\\text{der Punkt liegt nicht auf dem ' + \
				              'Kreis}'))
                return				
            return set()
			
        if isinstance(objekt, Gerade):
            if len(self.sch_par.union(objekt.sch_par)) > 1:			
                print("agla: nicht implementiert (Parameter)")
                print("Mittels  mit Eigenschaften versehenen Parametern")
                print("(z.B. p=Symbol('p', real=True) per Hand probieren\n")
                return				
            # die Berechnungen werden 'per Hand' durchgeführt (Zeit)		
            x, y = Symbol('x', real=True), Symbol('y', real=True)
            z = x+y*I			
            m, r = self.args
            a = m.x + m.y*I   # Mittelpunkt			
            st, ri = objekt.stuetz, objekt.richt	
            t = Symbol('t', real=True)			
            g = st.x + t*ri.x + (st.y + t*ri.y)*1j
            L = solve([abs(g-a) - r], [t], rational=True, dict=True)  			
            if not L:
                if kwargs.get('l'):				           
                    display(Math('\\text{die Gerade schneidet den  Kreis }' + \
					              '\\text{nicht}'))
                    return
                return set()
            elif len(L) == 1:
                if kwargs.get('l'):				           
                    display(Math('\\text{die Gerade berührt den Kreis }' + \
					              '\\text{in einem  Punkt}]'))
                    return
                q = objekt.pkt(L[0][t])					
                return q
            elif len(L) == 2:
                if kwargs.get('l'):				           
                    display(Math('\\text{die Gerade schneidet den Kreis }' + \
					              '\\text{in zwei Punkten}'))
                    return
                p, q = objekt.pkt(L[0][t]), objekt.pkt(L[1][t])					
                return p, q
					               				
        if isinstance(objekt, Kreis):
            if len(self.sch_par.union(objekt.sch_par)) > 1:			
                print("agla: nicht implementiert (Parameter)")
                print("Mittels  mit Eigenschaften versehenen Parametern")
                print("(z.B. p=Symbol('p', real=True) interaktiv versuchen\n")
                return				
            x, y = Symbol('x', real=True), Symbol('y', real=True)
            m1, r1 = self.args
            m2, r2 = objekt.args
            if m1.x==m2.x and m1.y==m2.y and r1==r2:
                if kwargs.get('l'):				           
                    display(Math('die\: Kreise\: sind\: identisch '))
                    return
                return self  
            gl = [(x-m1.x)**2 + (y-m1.y)**2 - r1**2, (x-m2.x)**2 + (y-m2.y)**2 - r2**2]
            if exakt:			
                L = loese(gl, [x, y], rational=True, dict=True)
            else:
                gl1, gl2 = N(gl[0]), N(expand(gl[1] - gl[0]))
                try:
                    L = loese(gl2, x, dict=True)
                    if L:
                        gl = gl1.subs(x, L[x])
                        L = loese(gl, y, dict=True)
                except KeyError:
                    L = loese(gl2, y, dict=True)
                    if L:                    					
                        gl = gl1.subs(y, L[y])
                        L = loese(gl, x, rational=True, dict=True)                    					
            if not L:
                if kwargs.get('l'):				           
                    display(Math('die\: Kreise\: schneiden\: sich \: nicht\: '))
                    return
                return set()
            if len(L) == 1:
                if kwargs.get('l'):				           
                    display(Math('die\: Kreise\: berühren\: sich \: ' + \
					              'in \:einem \: Punkt'))
                    return
                if exakt:					
                    q = Vektor(L[0][x], L[0][y])
                else:	
                    try:				
                        xx = L[x]
                        gl = gl2.subs(x, xx)						
                        L = loese(gl, y, rational=True, dict=True) 
                        yy = L[y]						
                        q = Vektor(xx, yy, simpl=False)
                    except KeyError:						
                        yy = L[y]
                        gl = gl2.subs(y, yy)
                        L = loese(gl, x, rational=True, dict=True) 
                        xx = L[x]						
                        q = Vektor(xx, yy, simpl=False)
                return q
            else:				
                if kwargs.get('l'):				           
                    display(Math('die\: Kreise\: schneiden\: sich \: ' + \
					              'in \:zwei \: Punkten'))
                    return	
                if exakt:         
                    p = Vektor(L[0][x], L[0][y], simpl=False)
                    q = Vektor(L[1][x], L[1][y], simpl=False)
                else:
                    try:				
                        xx = L[0][x], L[1][x]
                        gl = gl2.subs(x, xx[0])						
                        L = loese(gl, y, rational=True, dict=True) 
                        yy = [L[y]]
                        gl = gl2.subs(x, xx[1])						
                        L = loese(gl, y, rational=True, dict=True) 
                        yy += [L[y]]
                        p, q = Vektor(xx[0], yy[0]), Vektor(xx[1], yy[1])
                    except KeyError:						
                        yy = L[0][y], L[1][y]
                        gl = gl2.subs(y, yy[0])						
                        L = loese(gl, x, rational=True, dict=True) 
                        xx = [L[x]]
                        gl = gl2.subs(y, yy[1])						
                        L = loese(gl, x, rational=True, dict=True) 
                        xx += [L[x]]
                        p, q = Vektor(xx[0], yy[0]), Vektor(xx[1], yy[1])
                    if N(p.abstand(q))**2 < 1e-8:
                        return p					
                return p, q			   
		
			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Kreis"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)			
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Kreis in R^3 mit mayavi"""	
		
        # 'füll=ja / '  - gefüllte Darstellung; default - ungefülte Darstellung	
        # 'radius=wert'  - Radius für Darstellung als Röhre	
					
        fuell, radius = None, None		
        if len(spez) > 4:
            for s in spez[4]:
                if 'fuell' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper() or '1' in s.upper():
                        fuell = True
                if 'radius' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper():				
                        radius = 0.02	
                    else:
                        radius = eval(s[s.find('=')+1:])                    					
		
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
			
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3][:2]
			
        n = 100			
        v1 = self.ebene.richt[0]
        v2 = v1.vp(self.ebene.norm)
        v1 = v1.einh_vekt
        v2 = v2.einh_vekt
        m = self.mitte
        r  = self.radius
        #sin, cos, sqrt, pi = np.sin, np.cos, np.sqrt, np.pi
        if not anim:		
            v1x, v1y, v1z = float(v1.x), float(v1.y), float(v1.z)		
            v2x, v2y, v2z = float(v2.x), float(v2.y), float(v2.z)		
            t = np.linspace(0.0, 2*np.pi, n)
            mx, my, mz = float(m.x), float(m.y), float(m.z)		
            r  = float(r)
            x = r*np.cos(t)*v1x + r*np.sin(t)*v2x + mx
            y = r*np.cos(t)*v1y + r*np.sin(t)*v2y + my
            z = r*np.cos(t)*v1z + r*np.sin(t)*v2z + mz
            if not fuell:				
                return mlab.plot3d(x, y, z, line_width=lin_staerke,  
                      color=lin_farbe, tube_radius=radius)  
            else:
                flaech_farbe = lin_farbe
                x = np.r_[mx, x]
                y = np.r_[my, y]
                z = np.r_[mz, z]
                dreiecke = [(0, i, i + 1) for i in range(1, n)]
                return mlab.triangular_mesh(x, y, z, dreiecke, color= \
                      flaech_farbe)
        else:
            print('agla: lange Rechenzeiten')		
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20		
            b, _t = Symbol('b'), Symbol('_t')		
            kk = self.sch_el(b)
            p = kk.pkt(_t * 180 / pi)
            tt = np.linspace(0.0, 2*np.pi, n)
            xx, yy, zz = [], [], []			
            typ = (int, Integer, float, Float)			            			
            for s in tt:
                if isinstance(p.x, typ):			
                    xx += [p.x]
                else:					
                    xx += [p.x.subs(_t, s)] 
                if isinstance(p.y, typ):			
                    yy += [p.y]
                else:					
                    yy += [p.y.subs(_t, s)] 
                if isinstance(p.z, typ):			
                    zz += [p.z]
                else:					
                    zz += [p.z.subs(_t, s)]
            aa = np.linspace(float(aber[0]), float(aber[1]), N)
            xa, ya, za = [], [], []
            for bb in aa:
                if not fuell:
                    xa += [[float(x.subs(b, bb) if not isinstance(x, typ) 
                                                     else x) for x in xx]]					  
                    ya += [[float(y.subs(b, bb) if not isinstance(y, typ) 
                                                     else y) for y in yy]]						  
                    za += [[float(z.subs(b, bb) if not isinstance(z, typ) 
                                                     else z) for z in zz]]						  
                else:
                    return None
            plt = mlab.plot3d(xa[0], ya[0], za[0], line_width=lin_staerke, 
			                 color=lin_farbe, tube_radius=None)							 
            return plt, (xa[1:], ya[1:], za[1:]), N-1		

			
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Kreis in R^3 mit vispy"""	
		
        pass

		
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Kreis in R^2"""	

        # 'fuell=True' - gefüllte Darstellung; default - ungefülte Darstellung	
		
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' else \
                                                             spez[2][3]
		
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
            m, r  = self.mitte.dez, self.radius.n()	
            if not fuell:	
                kreis = patches.Circle((m.x, m.y), r, fill=None, 
                         edgecolor=lin_farbe, linewidth=lin_staerke)
                plt.gca().add_patch(kreis)
                return plt.plot([0], [0], 'w', markersize=0.0001)  # dummy plot	 
            else:
                kreis = patches.Circle((m.x, m.y), r, facecolor=lin_farbe, 
                         edgecolor=lin_farbe)
                plt.gca().add_patch(kreis)
                return plt.plot([0], [0], 'w', markersize=0.0001)		 
	
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        kreis_hilfe(3)	
		
    h = hilfe					

	
	
# Benutzerhilfe für Kreis
# -----------------------

def kreis_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nKreis - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Kreis( ebene, mitte, radius )\n")
        print("                 ebene    Trägerebene")
        print("                 mitte    Mittelpunkt")
        print("                 radius   Radius\n")
        print("Erzeugung in der Ebene R^2:\n")
        print("             Kreis( mitte, radius )\n")
        print("Zuweisung     k = Kreis(...)   (k - freier Bezeichner)\n")
        print("Beispiele")
        print("Kreis(xy_ebene, v(1, 2, 0), 3)")
        print("Kreis(v(1, 2), r)\n")
        return
		
    if h == 3:              
        print("\nEigenschaften und Methoden (M) für Kreis\n")
        print("k.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("k.bild(...)      M  Bild bei einer Abbildung")       
        print("k.bogen(...)     M  Kreisbogen  (= k.in_kurve.stueck)")     
        print("k.dim               Dimension")
        print("k.ebene             Trägerebene  (im Raum R^3)")
        print("k.fläche            Flächeninhalt")
        print("k.fläche_(...)  M   ebenso, zugehörige Methode")
        print("k.gleich            Gleichung des Kreises")    
        print("k.gleich_(...)   M  ebenso, zugehörige Methode (in R^2)")    
        print("k.in_kurve          Konvertierung in Kurve")             
        print("k.is_schar          Test auf Schar")        
        print("k.länge             = k.umfang")     
        print("k.länge_(...)   M   ebenso, zugehörige Methode")     
        print("k.M                 = k.mitte")
        print("k.mitte             Mittelpunkt")
        print("k.pkt(...)       M  Kreispunkt")                      
        print("k.prg               Parametergleichung")
        print("k.radius            Radius")
        print("k.radius_(...)   M  ebenso, zugehörige Methode")
        print("k.r                 = k.radius")
        print("k.r_(...)        M  = k.radius_")
        print("k.sch_par           Parameter einer Schar")	
        print("k.sch_el(...)    M  Element einer Schar")   
        print("k.schnitt(...)   M  Schnitt mit anderem Objekt (in R^2)")     
        print("k.tangente(...)  M  Tangenten  (in der Ebene R^2)")     
        print("k.umfang            Umfang")     
        print("k.umfang_(...)   M  ebenso, zugehörige Methode\n")     
        print("Synonyme Bezeichner\n")
        print("hilfe    :  h")
        print("fläche_  :  Fläche")
        print("gleich_  :  Gleich")
        print("in_kurve :  inKurve")
        print("is_schar :  isSchar")
        print("länge_   :  Länge")
        print("m        :  mitte")
        print("radius_  :  Radius")
        print("sch_el   :  schEl")
        print("sch_par  :  schPar")
        print("umfang_  :  Umfang\n")
        print("Vordefinierte Kreise")
        print("EinhKreis    Einheitskreis im Raum R^3")
        print("EinhKreis2   Einheitskreis in der Ebene R^2\n")
        return
   	
	
		
# Vordefinierte Kreise
# --------------------		

EinhKreis = Kreis(Ebene(0, 0, 1, 0), Vektor(0, 0, 0), 1)
	
EinhKreis2 = Kreis(Vektor(0, 0), 1)		
