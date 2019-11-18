#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Kugel - Klasse  von agla           
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
    from vispy.geometry import create_sphere
    from vispy.scene import STTransform

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.simplify import simplify, nsimplify
from sympy.abc import r, s, t
from sympy.solvers.solvers import solve
from sympy.functions.elementary.miscellaneous import sqrt
from sympy import sin, cos, Max, Min
from sympy.core.symbol import Symbol, symbols
from sympy.printing import latex
from sympy.core.numbers import Integer, Rational, pi

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, X
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, Gleichung, 
     ja, Ja, nein, Nein, mit, ohne, loese, wert_ausgabe)
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.funktionen.graf_funktionen import hex2color, _funkt_sympy2numpy
import agla
	
	
	
# Kugel - Klasse
# --------------
	
class Kugel(AglaObjekt):    
    """
	
Kugel im Raum
	
**Erzeugung** 

   Kugel ( *mitte, radius* )
   	
**Parameter**	
	
   *mitte* :    Mittelpunkt
   
   *radius* :  Radius  	
	
    """
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):             
            kugel_hilfe(kwargs["h"])		
            return	
			
        try:			
            if len(args) != 2:
                raise AglaError("Mittelpunkt und Radius angeben")
            mitte, radius = args
            try:
                b = bool(radius <= 0)
            except TypeError:
                b = False			
            if not is_zahl(radius) or b:
                raise AglaError("für Radius Zahlenwert > 0 angeben")
            radius = sympify(radius)
            try:			
                radius = nsimplify(radius)
            except RecursionError:
                pass			
            if not isinstance(mitte, Vektor):
                raise AglaError("für Mittelpunkt Punkt im Raum angeben")
            if mitte.dim != 3: 
                raise AglaError("für Mittelpunkt Punkt im Raum angeben") 
        except AglaError as e:
            print('agla:', str(e))
            return	
        return AglaObjekt.__new__(cls, mitte, radius)
			
		
    def __str__(self):  
        par = self.sch_par
        if par:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Kugelschar(" + ss + ")"
        return "Kugel"	
	
		
# Eigenschaften	
# -------------
		
		
    @property			
    def in_flaeche(self):              
        """Konvertierung in Fläche-Objekt"""
        Flaeche = importlib.import_module('agla.lib.objekte.flaeche').Flaeche	
        u, w, x, y, z = symbols('u w x y z')		
        r, m = self.radius, self.mitte	
        f = Flaeche( (r*cos(u)*cos(w), r*cos(u)*sin(w), r*sin(u) ), 
                   (u, -pi/2, pi/2), (w, 0, 2*pi), 
                   imp = repr((x-m.x)**2 + (y-m.y)**2 + (z-m.z)**2 - r**2))
        return f

    inFlaeche= in_flaeche		
		
    @property
    def sch_par(self):              
        """Scharparameter"""
        ret = self.args[0].free_symbols.union(self.args[1].free_symbols)
        if len(self.args) == 3:
            ret = ret.union(self.args[2].free_symbols)		
        return ret
		
    schPar = sch_par		
		
    @property
    def dim(self):
        """Dimension"""
        return 3

    @property
    def is_schar(self):
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		
	
    @property
    def gleich(self):
        """Gleichung; nur zur Ausgabe"""
        p = self.mitte
        x, y, z = symbols('x y z')				
        gl = Gleichung((x - p.x)**2 +  (y - p.y)**2 + (z - p.z)**2, \
                self.radius**2)
        return gl	
    def gleich_(self, *args, **kwargs): 
        """Gleichung; zugehörige Methode"""
        if kwargs.get('h'):
            if not mit_param(self):
                print('\nAngabe (x, y) oder [x, y] - Rückgabe der/des zum Punkt')
                print('        der xy-Ebene gehörenden Kugelpunkte/-es\n')
            print('Angabe eines Punktes - Auswertung der Gleichung in diesem\n')
            return	
        if len(args) != 1:
            print('agla: ein Tupel/eine Liste oder einen Punkt angeben')
            return			
        args = args[0]
        x, y, z = symbols('x y z')				
        m = self.mitte
        gleich = (x - m.x)**2 +  (y - m.y)**2 + (z - m.z)**2 - \
                self.radius**2
        if type(args) in (tuple, list, Tuple):
            if len(args) != 2 or not is_zahl(args[0]) or not is_zahl(args[1]):
                print('agla: zwei Zahlen angeben')
                return
            if mit_param(self) or mit_param(args[0]) or mit_param(args[1]):
                print('agla: nicht implementiert (Parameter)')
                return				
            gl = gleich.subs(x, args[0]).subs(y, args[1])
            ll = loese(gl)
            if len(ll) == 1:
                return Vektor(args[0], args[1], ll[0][z])
            else:
                if ll[0][z].is_real:
                    p0 = Vektor(args[0], args[1], ll[0][z])
                    p1 = Vektor(args[0], args[1], ll[1][z])
                    return p0, p1
                else:
                    return set()				
        if isinstance(args, Vektor):
            if args.dim != 3:
                print('agla: Punkt im Raum oder ein Tupel/Liste angeben')
                return				
            gl = gleich.subs(x, args.x).subs(y, args.y).subs(z, args.z)
            if simplify(gl) == 0:
                display(Math('\\text{die Gleichung ist erfüllt}'))
            else:
                if mit_param(gl):
                    display(Math('\\text{Die Gleichung ist erfüllt für die Lösung von}'))
                    lat = latex(gl) + latex('=') + latex(0)
                    display(Math(lat))
                    return
                display(Math('\\text{die Gleichung ist nicht erfüllt}'))
            return
        else:
            print('agla: einen Punkt im Raum angeben')	
            return			

    Gleich = gleich_
	
    @property
    def mitte(self):
        """Mittelpunkt"""
        return self.args[0]

    M = mitte
    m = mitte	
		
    @property
    def o_flaeche(self):
        """Oberflächeninhalt"""
        f = 4 * pi * self.radius**2
        if not f.free_symbols:
            return f
        return f
    def o_flaeche_(self, **kwargs):
        """Oberflächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'A' + '=' + '4 \pi r^2, \quad r - Radius'
            display(Math(txt))
            return			
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkommastellen')
            print('f=1 - Formel\n')
            return
        f = self.o_flaeche
        d = kwargs.get('d')		
        return wert_ausgabe(f, d)

    oFlaeche  = o_flaeche 	
    oFlaeche_ = o_flaeche_ 	
    O_flaeche = o_flaeche_	
    flaeche = o_flaeche
    flaeche_ = o_flaeche_
    Flaeche = o_flaeche_
     	
    @property
    def radius(self):
        """Radius"""
        return self.args[1]
    def radius_(self, **kwargs):
        """Radius; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        r = self.radius
        d = kwargs.get('d')
        return wert_ausgabe(r, d)

    r = radius		
    Radius = radius_
    r_ = radius_	
	
    @property
    def volumen(self):
        """Volumen"""
        vol = Rational(4, 3) * pi * self.radius**3
        return vol
    def volumen_(self, **kwargs):
        """Volumen; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'V' + '=' + '\\frac{4}{3} \pi r^3, \quad r - Radius'
            display(Math(txt))
            return			
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen\n')
            print('f=1 - Formel\n')
            return
        vol = self.volumen
        d = kwargs.get('d')
        return wert_ausgabe(vol, d)
		
    Volumen = volumen_		
	
		
# Methoden
# --------
	 
    def abstand(self, *objekt, **kwargs):
        """Abstand zu anderen Objekten"""
		
        if kwargs.get('h'):
            print("\nAbstand der Kugel zu einem anderen Objekt\n")		
            print("Aufruf   kugel . abstand( objekt )\n")		                     
            print("             kugel    Kugel")
            print("             objekt   Punkt, Gerade, Ebene, Kugel\n")
            print("Zusatz       d=n      Dezimaldarstellung")
            print("                      n - Anzahl der Nachkomma-/Stellen\n")			
            return 
					
        try:					
            if mit_param(self):
                raise AglaError('nicht implementiert (Parameter))')
            if len(objekt) != 1:
                raise AglaError('ein Objekt angeben') 
            objekt = objekt[0]
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            if (not type(objekt) in [Vektor, Gerade, Ebene, Kugel] or 
                                                 objekt.dim != 3):		
                raise AglaError("Punkt, Gerade, Ebene oder Kugel im Raum " + \
				                 "angeben")
            if mit_param(objekt):
                raise AglaError('nicht implementiert (Parameter))')
        except AglaError as e:
            print('agla:', str(e))
            return			
			
        if isinstance(objekt, Vektor):
            if objekt.abstand(self.mitte) > self.radius:
                wert = objekt.abstand(self.mitte) - self.radius
                try:
                    wert = nsimplify(wert) 
                except RecursionError:
                    pass				
            elif simplify(objekt.abstand(self.mitte)) < self.radius:
                wert = nsimplify(-(self.radius - objekt.abstand(self.mitte)))
                try:
                    wert = nsimplify(wert) 				
                except RecursionError:
                    pass							
            else:
               wert = 0				
        elif isinstance(objekt, Gerade) or isinstance(objekt, Ebene):
            d = self.mitte.abstand(objekt)
            try:
                d = nsimplify(d) 				
            except RecursionError:
                pass										
            if abs(d) <= self.radius:
                wert = 0
            else:
                wert = abs(d) - self.radius
        elif isinstance(objekt, Kugel):
            d = self.mitte.abstand(objekt.mitte)            
            try:
                d = nsimplify(d) 				
            except RecursionError:
                pass										
            if d > self.radius + objekt.radius:
                wert = d - (self.radius + objekt.radius)
            elif d < self.radius + objekt.radius:	
                r1 = Max(self.radius, objekt.radius)
                r2 = Min(self.radius, objekt.radius)
                if d + r2 >= r1:
                    wert = 0
                else:
                    wert = r1 -(d + r2)
            else:
                wert = 0	
			
        d =  kwargs.get('d')
        if not isinstance(d, (Integer, int)) or d < 0:
            return wert
        return wert_ausgabe(wert, d)
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Kugel bzw. Sphäre bei einer Abbildung\n")		
            print("Aufruf   kugel . bild( abb )\n")		                     
            print("             kugel   Kugel")
            print("             abb     Abbildung\n")			
            return 				
			
        try:			
            if len(abb) != 1:
                raise AglaError("eine Abbildung angeben")
            abb = abb[0]
            Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix	
            Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
            if not (type(abb) is Abbildung and abb.dim == 3):
                raise AglaError("eine Abbildung des Raumes angeben")
            m = abb.matrix
            m1 = Matrix(Vektor(1, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 1))
            if abs(m.D) == 1 or m == m1 * m[0, 0]:
                mitte1 = self.mitte.bild(abb)
                if m == m1 * m[0, 0]:
                    return Kugel(mitte1, m[0, 0] * self.radius)
                else:
                    return Kugel(mitte1, self.radius)
            else:
                raise AglaError("nicht implementiert (Determinante)")
        except AglaError as e:
            print('agla:', str(e))
            return
			
						
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Kugel"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)

    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Kugel mit mayavi"""
		
        # kwarg 'gitter = True'
								
        gitter = None	
        if len(spez) > 4:
            for s in spez[4]:
                s.replace(' ', '')
                if 'gitter' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper():				
                        gitter = (18, 18)	
                    else:
                        gitter = eval(s[s.find('=')+1:])                    					
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                      else spez[1]	
        if not isinstance(flaech_farbe, tuple):
            flaech_farbe = hex2color(flaech_farbe)		

        anim = False			
        if spez[3]:
            anim = True
            aber = spez[3][:2]
		
        m = self.mitte		
        if not anim:				
            r = float(self.radius)
            pi, cos, sin = np.pi, np.cos, np.sin
            phi, theta = np.mgrid[0:pi:101j, 0:2*pi:101j]
            x = float(self.mitte.x) + r * sin(phi) * cos(theta)
            y = float(self.mitte.y) + r * sin(phi) * sin(theta)
            z = float(self.mitte.z) + r * cos(phi)
            plt = [mlab.mesh(x, y, z, color=flaech_farbe)]
            if not gitter:
                return plt			
            else:
                nu, nw = 24, 18
                phi = np.arange(0.0, pi, 2 * pi/nu)
                theta = np.arange(0.0, 2 * pi + pi/400, pi/200)
                for p in phi[1:]:
                    x1 = float(self.mitte.x) + r * sin(p) * cos(theta)
                    y1 = float(self.mitte.y) + r * sin(p) * sin(theta)
                    z1 = np.full(x1.shape, float(self.mitte.z) + r * cos(p))
                    mlab.plot3d(x1, y1, z1, color = (0.7, 0.7, 0.7), \
                    line_width=0.001, opacity=1, tube_radius=None)
                phi = np.arange(0.0, pi + pi/400, 2 * pi/200)
                theta = np.arange(0.0, 2 * pi + pi/nw, 2 * pi/nw)
                for t in theta[1:]:
                    x1 = float(self.mitte.x) + r * sin(phi) * cos(t)
                    y1 = float(self.mitte.y) + r * sin(phi) * sin(t)
                    z1 = np.full(x1.shape, float(self.mitte.z) + r * cos(phi))
                    plt += [mlab.plot3d(x1, y1, z1, color = (0.7, 0.7, 0.7), \
                               line_width=0.001, opacity=1, tube_radius=None)]
                return plt	 
						
        else:
            from sympy import sin, cos	
            from numpy import pi			
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20
            r = self.radius				
            b_, u, w = symbols('b_ u w')	
            p = Vektor(r*cos(u)*cos(w) + m.x, r*sin(u)*cos(w) + m.y, r*sin(w) + m.z)
            par = p.free_symbols.difference({u, w})			
            p = p.subs(par.pop(), b_)			
            uu, uo =  0.0, float(2*pi)		
            wu, wo =  float(-pi/2), float(pi/2)		
            aa = np.linspace(float(aber[0]), float(aber[1]), N)  		
            u, w = np.mgrid[uu:uo:101j, wu:wo:101j]
            xs, ys, zs = repr(p.x), repr(p.y), repr(p.z)
            xa, ya, za = [], [], []
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
            for bb in aa:
                bb = '(' + str(bb) + ')'
                xa += [eval(xs.replace('b_', bb))]
                ya += [eval(ys.replace('b_', bb))]
                za += [eval(zs.replace('b_', bb))]
            opacity = 1				
            plt = mlab.mesh(xa[0], ya[0], za[0], opacity=opacity, color=flaech_farbe)
            return plt, (xa[1:], ya[1:], za[1:]), N-1				
			
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Kugel mit vispy"""
		
        pass		
		
			
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")			
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Kugel-Schar\n")		
            print("Aufruf   kugel . sch_el( wert )\n")		                     
            print("             kugel    Kugel")
            print("             wert     Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für Scharparameter Zahl oder freien Parameter ' + \
			        'angeben')	
            return
        try:
            wert = nsimplify(wert) 				
        except RecursionError:
            pass													
        mitte = self.mitte
        if mitte.has(p):
            mitte = mitte.sch_el(wert)
        radius = self.radius.subs(p, wert)
        return Kugel(mitte, radius)			
	
    schEl = sch_el		
		
		
    def schnitt(self, *objekt, **kwargs):
        """Schnitt mit anderen Objekten"""
        
        if kwargs.get('h'):
            print("\nSchnitt der Kugel mit einem anderen Objekt\n")		
            print("Aufruf   kugel . schnitt( objekt )\n")		                     
            print("             kugel    Kugel")
            print("             objekt   Punkt, Gerade, Ebene, Kugel\n")
            print("Zusatz       l=1   Lageinformationen\n")			
            return 
		
        try:		
            if mit_param(self):
                raise AglaError("nicht implementiert (Parameter)")		
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")
            objekt = objekt[0]
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            if (not type(objekt) in [Vektor, Gerade, Ebene, Kugel] or 
                                                       objekt.dim != 3):
                raise AglaError("Punkt, Gerade, Ebene oder Kugel im Raum " + \
				        "angeben")
            if  mit_param(objekt):
                raise AglaError("nicht implementiert (Parameter)")
        except AglaError as e:
            print('agla:', str(e))
            return
			
        x, y, z = symbols('x y z')				
        p = self.mitte
        gleich = (x - p.x)**2 + (y - p.y)**2 + (z - p.z)**2 - self.radius**2
        if isinstance(objekt, Vektor):
            q = objekt
            gl = gleich.subs(x, q.x).subs(y, q.y).subs(z, q.z)
            if simplify(gl) == 0:
                if kwargs.get('l'):				           
                    display(Math('\\text{der Punkt liegt auf der }' + \
					              '\\text{Kugeloberfläche}'))
                    return
                return q
            if kwargs.get('l'):
                if p.abstand(objekt) > self.radius: 			
                    display(Math('\\text{der Punkt liegt außerhalb der }' + \
				              '\\text{Kugel und ihrer Oberfläche}'))
                else:
                    display(Math('\\text{der Punkt liegt innerhalb der }' + \
				              '\\text{Kugel}'))				
                return				
            return set()
			
        elif isinstance(objekt, Gerade):
            q = objekt.pkt(objekt.par)
            gl = gleich.subs(x, q.x).subs(y, q.y).subs(z, q.z)
            li = solve(gl, objekt.par)
            if len(li) == 1:
                if kwargs.get('l'):
                    display(Math('\\text{die Gerade berührt die Kugel ' +
                         'im Punkt mit  }' + str(objekt.par) + 
						     ' = ' + str(li[0]) + '\\:\:\\text{(Tangente)}'))
                    return
                return objekt.pkt(li[0]).einfach
            elif len(li) == 2:
                if not li[0].is_real:
                     if kwargs.get('l'):
                         display(Math('\\text{die Gerade schneidet die ' +
						                'Kugel nicht}' + 
										'\:\: \\text{(Passante)}'))
                         return						 
                     return set()
                else:			
                    if kwargs.get('l'):
                        display(Math('\\text{die Gerade schneidet die ' +
						          'Kugel in den beiden ' +
                              'Punkten mit}'))
                        display(Math(str(objekt.par) + '_1 = ' + latex(li[0]) +
						           ',\:\: ' + \
                                str(objekt.par) + '_2 = ' + latex(li[1]) + 
								     '\:\:\:\: \\text{(Sekante)}'))
                        return
                    return objekt.pkt(li[0]).einfach, objekt.pkt(li[1]).einfach
				 
        elif isinstance(objekt, Ebene):
            Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis	
            d = abs(objekt.abstand(self.mitte))
            if d > self.radius:
                if kwargs.get('l'):
                    display(Math('\\text{die Ebene schneidet die Kugel ' +
      					'nicht}'))
                    return					
                return set()
            elif d < self.radius:
                r = sqrt(self.radius**2 - d**2)                
                g = Gerade(self.mitte, objekt.norm)
                m = g.schnitt(objekt)
                if kwargs.get('l'):
                    display(Math('\\text{die Ebene schneidet die Kugel ' +
					   'in einem Kreis}'))
                    return
                return Kreis(objekt, m, r)
            else:
                g = Gerade(self.mitte, objekt.norm)
                b = g.schnitt(objekt)
                if kwargs.get('l'):
                    display(Math('\\text{die Ebene berührt die Kugel }' +
					   '\\text{im Punkt}' + b.punkt_ausg_(s=1) ))
                    return													     
                return b
			
        elif isinstance(objekt, Kugel):
            if objekt.radius == self.radius and objekt.mitte == self.mitte:
                if kwargs.get('l'):
                    display(Math('\\text{die Kugeln sind identisch}'))
                    return					
                return self
            elif objekt.radius < self.radius:
                r0, r1 = objekt.radius, self.radius
                stuetz = self.mitte
                vv = Vektor(self.mitte, objekt.mitte)
            else:
                r0, r1 = self.radius, objekt.radius
                stuetz = objekt.mitte
                vv = Vektor(objekt.mitte, self.mitte)
            d = abs(objekt.mitte.abstand(self.mitte))
            if not (r1 - r0 <= d <= r1 + r0):
                if kwargs.get('l'):
                    display(Math('\\text{die Kugeln schneiden sich nicht}'))
                    return					
                return set()
            else:	   	
			    # aus der Geometrie des Drachenvierecks wird ein Ebenenpunkt
                # gewonnen	(Schnittpunkt der Diagonalen)			 
                p = stuetz + vv.einh_vekt * (r1**2 - r0**2 + d**2) / (2*d)
                s = self.schnitt(Ebene(p, vv))
                if kwargs.get('l'):
                    if type(s) is Vektor:
                        display(Math('\\text{die Kugeln berühren sich ' + 
						    'im Punkt}' + s.punkt_ausg_(s=1)))
                        return						 
                    else:
                        display(Math('\\text{die Kugeln schneiden sich ' +
						    'in einem Kreis}'))
                        return						    
                return s				
				        			
		
    def tangenten(self, *objekt, **kwargs):
        """Tangenten"""
		
        if kwargs.get('h'):
            print("\nTangenten an die Kugel\n") 
            print("von einem Punkt außerhalb oder von einem Punkt der")
            print("Kugeloberfläche\n")		
            print("Aufruf   kugel . tangenten( punkt )\n")		                     
            print("             kugel   Kugel")
            print("             punkt   Punkt\n")	
            print("Rückgabe   bei einem Punkt außerhalb:")
            print("           Berührkreis; seine Trägerebene ist die")
            print("               Polarebene  kugel.tangenten(punkt).ebene")
            print("           bei einem Kugelpunkt:")
            print("           Tangentialebene\n")			
            return 				
				
        try:
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis	
            if mit_param(self):
                raise AglaError('nicht implementiert (Parameter)')				
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")
            p = objekt[0]
            m = self.mitte
            vv = Vektor(p, m)
            if not (isinstance(p, Vektor) and p.dim == 3):
                raise AglaError("Punkt angeben")
            if mit_param(p):
                raise AglaError('nicht implementiert (Parameter)')		
            if p.abstand(m) < self.radius:
                raise AglaError("innerer Punkt der Kugel, keine Tangenten")
            elif p.abstand(m) > self.radius:
                # Tangentialkegel
                # Polarebene
                pe = Ebene(vv.x, vv.y, vv.z, (-vv.sp(m) + self.radius**2))
                g = Gerade(self.mitte, vv)
                q = g.schnitt(pe)
                # Berührkreis
                r = sqrt(self.radius**2 - 
			          Vektor(self.mitte, q).sp(Vektor(self.mitte, q)))
                bk = Kreis(pe, q, r) 
                return bk
            else:
                # Tangentialebene
                return Ebene(p, vv)
			
        except AglaError as e:		
            print('agla:', str(e))			
            return

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        kugel_hilfe(3)	
		
    h = hilfe					
			
		
						
# Benutzerhilfe für Kugel
# -----------------------

def kugel_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nKugel - Objekt\n")
        print("Erzeugung einer Kugel im Raum R^3:\n")
        print("             Kugel( mitte, radius )\n")
        print("                 mitte    Mittelpunkt")
        print("                 radius   Radius\n")
        print("Zuweisung    k = Kugel(...)   (k - freier Bezeichner)\n")
        print("Beispiele")
        print("Kugel(v(1, 2, 3), 3)")
        print("Kugel(O, r)\n")
        return
		
    if h == 3:
        print("\nEigenschaften und Methoden (M) für Kugel\n")
        print("k.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("k.abstand(...)    M  Abstand zu anderen Objekten")
        print("k.bild(...)       M  Bild bei einer Abbildung")
        print("k.dim                Dimension")
        print("k.fläche             = o_fläche")
        print("k.fläche_(...)       = o_fläche_")
        print("k.gleich             Gleichung")
        print("k.gleich_(...)    M  ebenso, zugehörige Methode")
        print("k.in_fläche          Konvertierung in Fläche")
        print("k.is_schar           Test auf Schar")
        print("k.mitte              Mittelpunkt")
        print("k.M                  = k.mitte")
        print("k.o_fläche           Oberflächeninhalt")
        print("k.o_fläche_(...)  M  ebenso, zugehörige Methode")
        print("k.radius             Radius")
        print("k.radius_(...)    M  ebenso, zugehörige Methode")
        print("k.r                  = k.radius")
        print("k.r_(...)         M  = k.radius_")
        print("k.sch_el(...)     M  Element einer Schar")
        print("k.sch_par            Parameter einer Schar")
        print("k.schnitt(...)    M  Schnittmenge mit anderen Objekten")
        print("k.tangenten(...)  M  Tangenten")
        print("k.volumen            Volumen") 
        print("k.volumen_(...)   M  ebenso, zugehörige Methode\n") 
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("fläche_   :  Fläche")
        print("gleich_   :  Gleich")
        print("in_fläche :  inFläche")
        print("is_schar  :  isSchar")
        print("o_fläche  :  oFläche")
        print("radius_   :  Radius")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")
        print("volumen_  :  Volumen\n")
        return
    		
			
			