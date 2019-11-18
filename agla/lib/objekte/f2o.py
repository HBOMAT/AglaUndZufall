#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Flaeche2terOrdnung - Klasse  von agla           
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
    pass	
from IPython.display import display, Math

from copy import copy

from sympy.functions.elementary.miscellaneous import sqrt
from sympy import sin, cos, sinh, cosh, asinh, acosh
from sympy.core.symbol import Symbol, symbols 
from sympy.core.sympify import sympify
from sympy.core.numbers import pi, Rational
from sympy.core.containers import Tuple
from sympy.polys.polytools import Poly
from sympy.simplify.simplify import nsimplify
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.flaeche import Flaeche
from agla.lib.objekte.matrix import Matrix
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.funktionen.funktionen import Gleichung, mit_param, is_zahl
from agla.lib.funktionen.graf_funktionen import (_implicit_plot, 
                                                 hex2color)
import agla	
	
	

# Flaeche2terOrdnung - Klasse  
# ---------------------------- 
	
class Flaeche2terOrdnung(AglaObjekt):                                      
    """	
Fläche 2. Ordnung im Raum

**Kurzform**

   **F2O** 

**Erzeugung** 
	
   Fläche2terOrdnung ( *gleichung* ) 
   
   *oder*

   F2O ( *gleichung* ) 
   
**Parameter**

   *gleichung* : Gleichung der Fläche 2. Ordnung in den Variablen *x, y, z*  
   als Zeichenkette '*F(x, y, z) = 0* ' oder als Ausdruck *F(x, y, z)*  
   (rechte Seite wird mit 0 angenommen); die Variablennamen sind zwingend
	
**Vordefinierte Flächen 2. Ordnung**
	
   ``Ellipsoid``                 
   
   ``EinSchaligesHyperboloid``   
   
   ``ZweiSchaligesHyperboloid``  
   
   ``ElliptischesParaboloid``    
   
   ``HyperbolischesParaboloid``
   
   ``ElliptischerZylinder``      
   
   ``HyperbolischerZylinder``    
   
   ``ParabolischerZylinder``
   
   ``DoppelKegel``

    """
	
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            f2o_hilfe(kwargs["h"])		
            return	

        prg = None			
        if kwargs.get('prg'):                         
            prg = kwargs.get('prg')                         
			
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
            if gl.find('x') < 0 and gl.find('y') < 0 and \
                gl.find('z') < 0:
                raise AglaError("eine Gleichung in x, y " + 
                                                   "und z angeben")	
            if gl.find('=') < 0:
                lhs, rhs = gl, 0	
            elif gl.find('=') > 0:
                lhs, rhs = gl[:gl.find('=')], gl[gl.find('=')+1:]
            else:
                raise AglaError("Eingabe überprüfen")	
            try:            				
                lhs, rhs = sympify(lhs), sympify(rhs)
            except SympifyError:
                print('agla: die Eingae ist falsch')	
                return
            if not (is_zahl(lhs) and is_zahl(rhs)):
                raise AglaError("Funktionsausdrücke für beide " +
                                          "Seiten der Gleichung angeben")
            lhs = lhs - rhs 					
            try:
                lhs = nsimplify(lhs)
            except RecursionError:						
                pass					
            gleich = Gleichung(lhs, 0)
			
        x, y, z = symbols("x y z")
        i = gl.find('=')
        if i > 0:
             gl = gl[:i]		
        try:
            sympify(gl)
        except (SyntaxError, NameError):
            print('agla: die Gleichung ist fehlerhaft')
            return
			
        di = dict()
			 
        try:			 
            p = Poly(gl, (x, y, z))
        except:
            print('agla: die Gleichung ist falsch eingegeben')
            return			
        if p.total_degree() != 2:
            print('agla: die Gleichung muss den Grad 2 haben')
            return			
        px = p.subs(y, 0).subs(z, 0)
        py = p.subs(x, 0).subs(z, 0)
        pz = p.subs(x, 0).subs(y, 0)
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
        if pz == 0:
            di['zz'], di['z'] = 0, 0
        else:			
            diz = dict(Poly(pz).all_terms())
            try:
                di['zz'] = diz[(2,)]
            except KeyError:
                di['zz'] = 0
            try:
                di['z'] = diz[(1,)]
            except KeyError:
                di['z'] = 0
				
        p -= (di['xx']*x**2 + di['yy']*y**2 + di['zz']*z**2 
		     + di['x']*x + di['y']*y + di['z']*z + di['f'])
        di['xy'] = p.subs(z, 0) / x / y
        di['xz'] = p.subs(y, 0) / x / z
        di['yz'] = p.subs(x, 0) / y / z

        gleich = Gleichung(Poly(gl).as_expr(), 0)				
        koeff_dict = di
		
        return AglaObjekt.__new__(cls, gleich, koeff_dict, prg)
		               			
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Fläche2terOrdnungSchar(" + ss + ")"
        return "Fläche2terOrdnung"					
		   		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 3

    @property			
    def sch_par(self):              
        """Scharparameter"""
        x, y, z = symbols('x y z')
        return self.imp.free_symbols.difference({x,y,z})
				 
    schPar = sch_par				 
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) != 0	
		
    isSchar = is_schar		
		
    @property
    def M(self):
        """Matrix der Gleichung"""
        di = self.args[1]
        xx, xy, xz, yy, yz, zz = symbols('xx, xy, xz, yy, yz, zz')
        M = ( Vektor(di[xx], di[xy]/2, di[xz]/2) |
              Vektor(di[xy]/2, di[yy], di[yz]/2) |
              Vektor(di[xz]/2, di[yz]/2, di[zz]) )
        return M
       
    m = M
	   
    @property
    def MM(self):
        """Erweiterte Matrix der Gleichung"""
        di = self.args[1]
        xx, xy, xz, yy, yz, zz, x, y, z, f = \
        symbols('xx, xy, xz, yy, yz, zz, x, y, z, f') 
        MM = ( Vektor(di[xx], di[xy]/2, di[xz]/2, di[x]/2) |
              Vektor(di[xy]/2, di[yy], di[yz]/2, di[y]/2) |
              Vektor(di[xz]/2, di[yz]/2, di[zz], di[z]/2) |
              Vektor(di[x]/2, di[y]/2, di[z]/2, di[f]) )
        return MM
		
    mm = MM		
		
    @property
    def gleich(self):                     
        """Gleichung"""
        return self.args[0]

    imp = gleich
	
    @property
    def prg(self):                     
        """Parametergleichung"""
        if not self.args[2]:
            print('agla: die Gleichung ist nicht verfügbar')	
            return			
        x, y, z = symbols('x y z')			
        gl = Gleichung(Vektor(x, y, z), self.args[2])
        return gl  
	
    @property		
    def gleich_m(self):                     
        """Gleichung in Matrixform; nur zur Ausgabe"""
        m, mm = self.M, self.MM
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
        xx = Vektor(x, y, z)		
        vv = 2 * Vektor(mm[0, 3], mm[1, 3], mm[2, 3])
        if vv.x != 0 or vv.y != 0 or vv.z != 0:
            lat1 = '+' + latex(vv.T) + latex(xx)
        else:
            lat1 = ''		
        f = mm[3, 3]	
        if f > 0:
            frei = '+' + str(f)		
        elif f < 0:
            frei = '-' + str(-f)		
        else:
            frei = ''
        lat = latex(xx.T) + latex(m) + latex(xx) + lat1 + frei + '=0'		
        display(Math(lat + '\\quad \\text{oder}'))
        xx = Vektor(x, y, z, 1)		
        lat = latex(xx.T) + latex(mm) + latex(xx) + '=0'		
        display(Math(lat))
		
    gleichM = gleich_m
	
    @property
    def typ(self):                     
        """Flächentyp"""
        m, mm = self.m, self.mm
        if mit_param(m) or mit_param(mm):
            return print('agla: nicht implementiert (Parameter)')		
        delta, Delta = m.D, mm.D
        ss = m[0, 0] + m[1, 1] + m[2, 2]
        tt = ( m[1, 1]*m[2, 2] + m[2, 2]*m[0, 0] + 
               m[0, 0]*m[1, 1] - m[1, 2]**2 - m[2, 0]**2 - 
               m[0, 1]**2 )		
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')			   
        if delta != 0:
            if Delta < 0:
                if ss * delta > 0 and tt > 0:
                    return Symbol('Ellipsoid')
                else:
                    return Symbol('ZweiSchaligesHyperboloid')
            elif Delta > 0:
                if ss * delta > 0 and tt > 0:
                    return Symbol('Imaginaeres Ellipsoid')		
                else:
                    return Symbol('EinSchaligesHyperboloid')
            else:
                if ss * delta > 0 and tt > 0:
                    return Symbol('ImaginaererKegel')
                else:
                    return Symbol('DoppelKegel')				
        else:
            if Delta != 0:
                if Delta < 0 and tt > 0:
                    return Symbol('ElliptischesParaboloid')
                else:
                    return Symbol('HyperbolischesParaboloid')
            else:
                q = self.gleich.lhs
                if q.has(z):
                    if q.has(x):
                        q = q.subs(z, y)
                    else:
                        q = q.subs(z, x)
				
                po = q.as_poly(x, y ,z)
                di0 = po.as_dict()
                
                def eintrag(x, y, z):
                    try:
                        return di0[(x, y, z)]
                    except KeyError:
                        return 0

                di = dict()
                di['xx'] = eintrag(2, 0, 0)
                di['yy'] = eintrag(0, 2, 0)
                di['zz'] = eintrag(0, 0, 2)
                di['xy'] = eintrag(1, 1, 0)
                di['xz'] = eintrag(1, 0, 1)
                di['yz'] = eintrag(0, 1, 1)
                di['x'] = eintrag(1, 0, 0)
                di['y'] = eintrag(0, 1, 0)
                di['z'] = eintrag(0, 0, 1)
                di['f'] = eintrag(0, 0, 0)				
				
                m = ( Vektor(di['xx'], di['xy']/2, di['x']/2) |
                      Vektor(di['xy']/2, di['yy'], di['y']/2) |
                      Vektor(di['x']/2, di['y']/2, di['f']) )
                Delta = m.D
                delta = di['xx'] * di['yy'] - (di['xy']/2)**2 
                if delta != 0:
                    if delta > 0:
                        if Delta != 0:
                            return Symbol('ElliptischerZylinder')
                        else:
                            return Symbol('ImaginaereEbenen')
                    else:
                        if Delta != 0:
                            return Symbol('HyperbolischerZylinder')
                        else:
                            return Symbol('SichSchneidendeEbenen')						
                else:
                    if Delta != 0:
                        return Symbol('ParabolischerZylinder')
                    else: 
                        if (di['x']/2)**2 - di['xx'] * di['f'] > 0:
                            return Symbol('Parallele Ebenen')
                        elif (di['x']/2)**2 - di['xx'] * di['f'] < 0:
                            return Symbol('ImaginaereEbenen')
                        else:
                            return Symbol('DoppelEbene')

    @property
    def in_flaeche(self):                     
        """Konvertierung in Fläche-Objekt"""   
        if self.args[2]:		
            u, w = symbols('u w')		
            return Flaeche(self.args[2], (u, -pi, pi), (w, -pi, pi), imp=str(self.imp.lhs))
        return Flaeche(str(self.gleich))							

    inFlaeche = in_flaeche
	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Fläche 2. Ordnung bei einer Abbildung\n")		
            print("Aufruf   f2o . bild( abb )\n")		                     
            print("             f2o    F2O")
            print("             abb    Abbildung des Raumes R^3\n")	
            return 				
			
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        if not (isinstance(abb, Abbildung) and  abb.dim == 3):
            print("agla: eine Abbildung des Raumes angeben")
            return
        x, y, z, U, V, W = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('U'), \
                         Symbol('V'), Symbol('W')		
        gl = self.gleich.lhs		
        uvw = abb.matrix.inverse * (Vektor(U, V, W) - abb.versch)
        gl = gl.subs({x:uvw.x, y:uvw.y, z:uvw.z})		
        gl = gl.subs({U:x, V:y, W:z})		
        gls = str(gl)
        return F2O(gls)		

    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer F2O-Schar\n")		
            print("Aufruf   F2O . sch_el( wert )\n")		                     
            print("             F2O     Fläche 2. Ordnung")
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
        return Flaeche2terOrdnung(gl)		

    schEl = sch_el
				
		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für F2O"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
		
    def mayavi(self, spez, **kwargs):
        """Grafikelement für F2O mit mayavi"""
				
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                     else spez[1]						
        if not isinstance(flaech_farbe, tuple):
            flaech_farbe = hex2color(flaech_farbe)		
													
        anim = False			
        if spez[3]:
            anim = True        
            aber = spez[3]			
						
        gl = str(self.gleich.lhs)	
        fig = kwargs.get('figure')			
        if not anim:
            plt = _implicit_plot(gl, UMG._sicht_box, fig_handle=fig, 
                     col_isurf=flaech_farbe, col_osurf=flaech_farbe)	
            return plt
        else:
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20							
            gl = str(self.imp.lhs)
            par = self.sch_par.pop()	
            xl, xr, yl, yr, zl, zr = UMG._sicht_box
            Nx, Ny, Nz = 50, 50, 50   
            xx, yy, zz = np.mgrid[xl:xr:eval('{}j'.format(Nx)), \
			         yl:yr:eval('{}j'.format(Ny)), zl:zr:eval('{}j'.format(Nz))]
            gl0 = gl.replace(str(par), str(aber[0]))
            gl0 = gl0.replace('x', 'xx').replace('y', 'yy').replace('z', 'zz')
            scalars = eval(gl0)
            src0 = mlab.pipeline.scalar_field(xx, yy, zz, scalars) 
            plt = mlab.pipeline.iso_surface(src0, color=flaech_farbe, \
                        contours=[-1.e-5])             # Anfangsstellung
            aa = np.linspace(float(aber[0]), float(aber[1]), N)
            scalars = []	
            par = str(par)	
            for cc in aa:	
                cc = str(cc)			
                gl0 = gl.replace(par, cc)
                gl0 = gl0.replace('x', 'xx').replace('y', 'yy').replace('z', 'zz')
                scalars += [eval(gl0)]
            return plt, scalars, N-1
		
    def vispy(self, spez, **kwargs):
        """Grafikelement für F2O mit vispy"""
        pass   		
        
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        f2o_hilfe(3)	
		
    h = hilfe		
		
			
# Benutzerhilfe für Flaeche2terOrdnung

def f2o_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nFläche2terOrdnung - Objekt\n")
        print("Synonymer Name   F2O\n")
        print("Erzeugung     Fläche2terOrdnung( gleichung )\n")
        print("                 gleichung    Gleichung der Fläche 2. Ordnung in den")
        print("                              Variablen x, y, z als Zeichenkette")
        print("                              'F(x, y, z) = 0'   oder als Ausdruck")
        print("                               F(x, y, z) (rechte Seite wird mit 0 an-")
        print("                                           genommen)")
        print("                              (die Variablennamen sind zwingend)\n") 
        print("Zuweisung     f = F2O(...)   (f - freier Bezeichner)\n")
        print("Beispiel")
        print("F2O('z^2 - 3*x*y = 0')    oder")
        print("F2O(z^2 - 3*x*y)\n")
        print("Vordefinierte F2O")
        print("Ellipsoid                 Ellipsoid	")	
        print("EinSchaligesHyperboloid   Einschaliges Hyperboloid")	
        print("ZweiSchaligesHyperboloid  Zweischaliges Hyperboloid	")	
        print("ElliptischesParaboloid    Elliptisches Paraboloid")		
        print("HyperbolischesParaboloid  Hyperbolisches Paraboloid")		
        print("ElliptischerZylinder      Elliptischer Zylinder") 		
        print("HyperbolischerZylinder    Hyperbolischer Zylinder")		
        print("ParabolischerZylinder     Parabolischer Zylinder")	
        print("DoppelKegel               Doppelkegel\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methode (M) für Fläche2terOrdnung\n")
        print("f.hilfe           Bezeichner der Eigenschaften und Methoden")
        print("f.bild         M  Bild bei einer Abbildung")
        print("f.dim             Dimension")
        print("f.gleich          Eingabegleichung") 
        print("f.gleich_m        Gleichung in Matrixform") 
        print("f.imp             = f.gleich") 
        print("f.in_fläche       Konvertierung in Fläche")
        print("f.is_schar        Test auf Schar")        
        print("f.m               Matrix der Gleichung")
        print("f.mm              Erweiterte Matrix der Gleichung")
        print("f.prg             Parametergleichung")
        print("a.sch_el(...)  M  Element einer Schar")
        print("f.sch_par         Parameter einer Schar")	
        print("f.typ             Typ\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("gleich_m  :  gleichM")
        print("in_fläche :  inFläche")
        print("is_schar  :  isSchar")
        print("sch_el    :  schEl")
        print("sch_par   :   schPar\n")
        return			
	
F2O = Flaeche2terOrdnung
	
	

# Vordefinierte F2O
# ------------------

def Ellipsoid(*args, **kwargs):
    """Ellipsoid in Normallage"""
    if kwargs.get("h"): 
        print("\nEllipsoid - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     Ellipsoid( a, b, c )")
        print("                  a, b, c   Parameter in der Gleichung")  
        print("                            (x/a)^2+(y/b)^2+(z/c)^2-1=0\n")		
        return		
    if len(args) == 3:
        a, b, c = args
    else:
        print("agla: drei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b) and is_zahl(c)):
        print("agla : drei Zahlen als Parameter angeben")
        return				 
    a, b, c = sympify(a), sympify(b), sympify(c)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')			
    gl = (x/a)**2 + (y/b)**2 + (z/c)**2 - 1
    prg = Vektor(a*sin(u)*cos(w), b*sin(u)*sin(w), c*cos(u))	
    gls = str(gl)
    return Flaeche2terOrdnung(gls, prg=prg)			
	
def EinSchaligesHyperboloid(*args, **kwargs):
    """EinSchaligesHyperboloid in Normallage"""
    if kwargs.get("h"): 
        print("\nEinSchaligesHyperboloid - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     EinSchaligesHyperboloid( a, b, c )")
        print("                  a, b, c   Parameter in der Gleichung")  
        print("                            (x/a)^2+(y/b)^2-(z/c)^2-1=0\n")		
        return		
    if len(args) == 3:
        a, b, c = args
    else:
        print("agla: drei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b) and is_zahl(c)):
        print("agla : drei Zahlen als Parameter angeben")
        return				 
    a, b, c = sympify(a), sympify(b), sympify(c)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')			
    gl = (x/a)**2 + (y/b)**2 - (z/c)**2 - 1
    gls = str(gl)
    prg = Vektor(a*cosh(w)*cos(u), b*cosh(w)*sin(u), c*sinh(w))	
    return Flaeche2terOrdnung(gls, prg=prg)			

def ZweiSchaligesHyperboloid(*args, **kwargs):
    """ZweiSchaligesHyperboloid in Normallage"""
    if kwargs.get("h"): 
        print("\nZweiSchaligesHyperboloid - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     ZweiSchaligesHyperboloid( a, b, c )")
        print("                  a, b, c   Parameter in der Gleichung")  
        print("                            -(x/a)^2-(y/b)^2+(z/c)^2-1=0\n")		
        return		
    if len(args) == 3:
        a, b, c = args
    else:
        print("agla: drei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b) and is_zahl(c)):
        print("agla : drei Zahlen als Parameter angeben")
        return				 
    a, b, c = sympify(a), sympify(b), sympify(c)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')		
    gl = -(x/a)**2 - (y/b)**2 + (z/c)**2 - 1
    gls = str(gl)
    prg = Vektor(a*sinh(w)*cos(u), b*sinh(w)*sin(u), c*cosh(w))		
    return Flaeche2terOrdnung(gls, prg=prg)			

def ElliptischesParaboloid(*args, **kwargs):
    """ElliptischesParaboloid in Normallage"""
    if kwargs.get("h"): 
        print("\nElliptischesParaboloid - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     ElliptischesParaboloid( a, b )")
        print("                  a, b   Parameter in der Gleichung")  
        print("                         (x/a)^2+(y/b)^2-2*z=0\n")		
        return		
    if len(args) == 2:
        a, b = args
    else:
        print("agla: zwei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b)):
        print("agla : zwei Zahlen als Parameter angeben")
        return				 
    a, b = sympify(a), sympify(b)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')				
    gl = (x/a)**2 + (y/b)**2 - 2*z
    prg = Vektor(a*u*cos(w), b*u*sin(w), 1/2*u**2)	
    gls = str(gl)
    return Flaeche2terOrdnung(gls, prg=prg)			
	
def HyperbolischesParaboloid(*args, **kwargs):
    """HyperbolischesParaboloid in Normallage"""
    if kwargs.get("h"): 
        print("\nHyperbolischesParaboloid - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     HyperbolischesParaboloid( a, b )")
        print("                  a, b   Parameter in der Gleichung")  
        print("                         (x/a)^2-(y/b)^2-2*z=0\n")		
        return		
    if len(args) == 2:
        a, b = args
    else:
        print("agla: zwei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b)):
        print("agla : zwei Zahlen als Parameter angeben")
        return				 
    a, b = sympify(a), sympify(b)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')				
    gl = (x/a)**2 - (y/b)**2 - 2*z
    prg = Vektor(a*u, b*w, 1/2*(u**2-w**2))	
    gls = str(gl)
    return Flaeche2terOrdnung(gls, prg=prg)			
	
def ElliptischerZylinder(*args, **kwargs):
    """ElliptischerZylinder in Normallage"""
    if kwargs.get("h"): 
        print("\nElliptischerZylinder - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     ElliptischerZylinder( a, b )")
        print("                  a, b   Parameter in der Gleichung")  
        print("                         (x/a)^2+(y/b)^2-1=0\n")		
        return		
    if len(args) == 2:
        a, b = args
    else:
        print("agla: zwei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b)):
        print("agla : zwei Zahlen als Parameter angeben")
        return				 
    a, b = sympify(a), sympify(b)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')				
    gl = (x/a)**2 + (y/b)**2 - 1
    prg = Vektor(a*cos(u), b*sin(u), w)	
    gls = str(gl)
    return Flaeche2terOrdnung(gls, prg=prg)			
		
def HyperbolischerZylinder(*args, **kwargs):
    """HyperbolischerZylinder in Normallage"""
    if kwargs.get("h"): 
        print("\nHyperbolischerZylinder - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     HyperbolischerZylinder( a, b )")
        print("                  a, b   Parameter in der Gleichung")  
        print("                         (x/a)^2-(y/b)^2-1=0\n")		
        return		
    if len(args) == 2:
        a, b = args
    else:
        print("agla: zwei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b)):
        print("agla : zwei Zahlen als Parameter angeben")
        return				 
    a, b = sympify(a), sympify(b)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')				
    gl = (x/a)**2 - (y/b)**2 - 1
    gls = str(gl)
    prg = Vektor(a*cosh(u), b*sinh(u), w)	
    return Flaeche2terOrdnung(gls, prg=prg)			
		
def ParabolischerZylinder(*args, **kwargs):
    """ParabolischerZylinder in Normallage"""
    if kwargs.get("h"): 
        print("\nParabolischerZylinder - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     ParabolischerZylinder( a )")
        print("                  a   Parameter in der Gleichung")  
        print("                      (x/a)^2-2*y=0\n")		
        return		
    if len(args) == 1:
        a = args[0]
    else:
        print("agla: einen Parameter angeben")	
        return				
    if not is_zahl(a):
        print("agla : eine Zahl als Parameter angeben")
        return				 
    a = sympify(a)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')				
    gl = (x/a)**2 - 2*y
    prg = Vektor(u, 1/(2*a**2)*u**2, w)	
    gls = str(gl)
    return Flaeche2terOrdnung(gls, prg=prg)			
		
def DoppelKegel(*args, **kwargs):
    """DoppelKegel in Normallage"""
    if kwargs.get("h"): 
        print("\nDoppelKegel - F2O-Objekt    im Raum R^3\n")
        print("Erzeugung     DoppelKegel( a, b, c )")
        print("                  a, b, c   Parameter in der Gleichung")  
        print("                            (x/a)^2+(y/b)^2-(z/c)^2=0\n")		
        return		
    if len(args) == 3:
        a, b, c = args
    else:
        print("agla: drei Parameter angeben")	
        return				
    if not (is_zahl(a) and is_zahl(b) and is_zahl(c)):
        print("agla : drei Zahlen als Parameter angeben")
        return				 
    a, b, c = sympify(a), sympify(b), sympify(c)
    x, y, z, u, w = Symbol('x'), Symbol('y'), Symbol('z'), Symbol('u'), \
                   Symbol('w')			
    gl = (x/a)**2 + (y/b)**2 - (z/c)**2
    prg = Vektor(a*w*cos(u), b*w*sin(u), c*w)	
    gls = str(gl)
    return Flaeche2terOrdnung(gls, prg=prg)			
	
		