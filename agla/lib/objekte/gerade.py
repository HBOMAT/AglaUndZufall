#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Gerade - Klasse  von agla           
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
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.simplify.simplify import simplify, nsimplify
from sympy.core.symbol import Symbol, symbols 
from sympy.solvers.solvers import solve
from sympy.core.evalf import N	 
from sympy.core.function import expand
from sympy import Min, Max
from sympy.polys.polytools import Poly
from sympy.printing import latex
from sympy.core.numbers import Integer, Float

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, kollinear, 
     Gleichung, orthogonal, loese, wert_ausgabe)
from agla.lib.funktionen.graf_funktionen import hex2color, _funkt_sympy2numpy
from agla.lib.objekte.ausnahmen import AglaError
import agla

	

# Gerade - Klasse  
# ---------------                                   
                                 
class Gerade(AglaObjekt):    
    """Gerade im Raum und in der Ebene
	
**Erzeugung im Raum und in der Ebene** 

   Gerade ( *stütz, richt /[, par ]* )

   *oder* 
	
   Gerade ( *schar /[, par ]* ) 
	
**Erzeugung nur in der Ebene** 

   Gerade ( *m, n* )
   
   *oder*

   Gerade ( *a, b, c* )
   
**Parameter**	
	
   *stütz* :    Stützvektor
	  
   *richt* :    Richtungsvektor
   
   *par* :      Geradenparameter; *t* falls nicht angegeben

   *schar*:    
      | Punkteschar, die eine Gerade bildet
      | *par* muss bei mehr als einem Parameter in *schar* 
        angegeben werden   

   *m, n* :     Koeffizienten der Gleichung  *y=mx+n*
				
   *a, b, c* :     Koeffizienten der Gleichung  *ax+by+c=0*
	
	
**Vordefinierte Geraden**
   
``x_achse`` : *x* -Achse im Raum 

``y_achse`` : ebenso, *y* -Achse

``z_achse`` : ebenso, *z* -Achse  

``x_achse2`` : *x* -Achse in der Ebene

``y_achse2`` : ebenso, *y* -Achse
		
    """
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3, 4):                         
            gerade_hilfe(kwargs["h"])		
            return	
			
        try:	

		     # Erzeugen einer Geraden in R^2	
            if is_zahl(args[0]):
                if len(args) == 2:
                    if not is_zahl(args[1]):
                        raise AglaError("zwei oder drei Zahlen angeben")
                    a = -nsimplify(sympify(args[0]))
                    b = 1					 
                    c = -nsimplify(sympify(args[1]))
                elif len(args) == 3:
                    if not (is_zahl(args[1]) and is_zahl(args[2])):
                        raise AglaError("zwei oder drei Zahlen angeben")
                    a = nsimplify(sympify(args[0]))
                    b = nsimplify(sympify(args[1]))					 
                    c = nsimplify(sympify(args[2]))
                else:            
                    raise AglaError("zwei oder drei Zahlen angeben")
                t = Symbol('t')					
                return AglaObjekt.__new__(cls, a, b, c, t)
                 							 	
            # Erzeugen einer Geraden in R^3 aus einer Punktmenge mit Parametern
            if (len(args) == 1 and isinstance(args[0], Vektor)) or \
               (len(args) == 2 and isinstance(args[0], Vektor) and not \
               isinstance(args[1], Vektor)):
                p = args[0] 	
                if not p.free_symbols:
                    raise AglaError("zwei Vektoren oder Vektor mit Parameter(n) angeben")
                pars = p.free_symbols				
                if len(args) == 2:				
                    par	= args[1]
                    if not par.free_symbols:					
                         raise AglaError("der angegebene Parameter ist nicht frei")
                    if not par in pars:					
                         raise AglaError("der angegebene Parameter ist im Vektor nicht vorhanden")
                else:	
                    if len(pars) > 1:				
                         raise AglaError("einen Parameter explizit angeben")
                    par = pars.pop()	
                stuetz, richt = list(), list() 			
                for k in p.komp:
                    if not k.is_polynomial:
                        raise AglaError("Komponenten müssen Polynome sein")
                    if Poly(k, par).degree() > 1:
                        txt = "der Parameter darf höchstens in 1. Potenz auftreten"
                        raise AglaError(txt)
                    li = Poly(k, par).all_coeffs()				
                    stuetz += [li[-1]]				
                    if len(li) == 2:
                        richt += [li[0]]
                    else:
                        richt += [0]	
                stuetz = Vektor([nsimplify(k) for k in stuetz])				
                richt = Vektor([nsimplify(k) for k in richt])				
                return AglaObjekt.__new__(cls, stuetz, richt, par)
	   
		     # Erzeugen einer Geraden in R^3 und R^2 über Stütz- und Richtungsvektor
            if len(args) < 2 or len(args) > 3:
                txt = "Stütz-, Richtungsvektor und evtl. Geradenparameter angeben"
                raise AglaError(txt)		
            if not (isinstance(args[0], Vektor) and isinstance(args[1], Vektor) and
		         args[0].dim == args[1].dim):
                raise AglaError("zwei Vektoren mit gleicher Dimension angeben")
            stuetz = args[0]		
            richt = args[1]
            if richt == Vektor(0, 0, 0) or richt == Vektor(0, 0):
                raise AglaError('der Nullvektor kann nicht Richtungsvektor sein')			
            if len(args) == 3:
                if isinstance(args[2], Symbol):
                    parameter = args[2]	
                else:
                    raise AglaError("der Bezeichner muss frei sein")	
                if parameter in stuetz.free_symbols | richt.free_symbols:
                    raise AglaError("der Parameter ist in den Vektoren enthalten")			
            else: 
                parameter = Symbol("t")                   
            if stuetz.dim in (2, 3):	
                sx, sy, rx, ry = [nsimplify(e) for e in (stuetz.x, stuetz.y, 
                                richt.x, richt.y)]
                if stuetz.dim == 3:	
                    sz, rz = nsimplify(stuetz.z), nsimplify(richt.z)
                    stuetz, richt = Vektor(sx, sy, sz), Vektor(rx, ry, rz)
                else:					
                    stuetz, richt = Vektor(sx, sy), Vektor(rx, ry)
                stuetz = Vektor([nsimplify(k) for k in stuetz.komp])
                richt = Vektor([nsimplify(k) for k in richt.komp])   
                return AglaObjekt.__new__(cls, stuetz, richt, parameter)
            else:
                txt = "Geraden sind nur in R^2 und R^3 erzeugbar"
                raise AglaError(txt)

        except AglaError as e:
            print('agla:', str(e))
            return			
   
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Geradenschar(" + ss + ")"
        return "Gerade"			

				 
# Für Geraden in R^3 und R^2 gemeinsame Eigenschaften + Methoden
# --------------------------------------------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        a = self.args[0]
        if isinstance(a, Vektor) and a.dim == 3:
            return 3
        return 2
		
    @property
    def stuetz(self):              
        """Stützvektor"""
        a = self.args[0]
        if self.dim == 3:
            return a
        if isinstance(a, Vektor):
            return a
        a, b, c = self.args[:3]
        if b:
            return Vektor(0, nsimplify(-c / b))
        return Vektor(nsimplify(-c / a), 0)
		
    auf_pkt = stuetz
    aufPkt = stuetz		
            
    @property	
    def richt(self):              
        """Richtungsvektor"""
        a = self.args[0]
        if self.dim == 3:
            return self.args[1]
        if isinstance(a, Vektor):
            return self.args[1]
        return Vektor(self.args[1], -self.args[0])
				
    @property	
    def norm(self):              
        """Normalenvektor"""
        if self.dim == 3:
            print('agla: nur für Geraden in R^2 definiert')		
            return 
        ri = self.richt
        return Vektor(-ri.y, ri.x)
		
    @property			
    def par(self):              
        """Parameter der Geraden"""
        return self.args[-1]

    @property			
    def sch_par(self):              
        """Scharparameter"""
        return self.stuetz.free_symbols.union(self.richt.free_symbols)
	
    schPar = sch_par	
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		
		
    @property		
    def punkte(self):              
        """Zwei Geradenpunkte"""
        return self.stuetz, self.stuetz + self.richt		
    def punkte_(self, **kwargs): 
        if kwargs.get('h'):
            print("\nAusgabe: Punkte mit den Parameterwerten 0 und 1\n")
            return
        return self.pkt(0), self.pkt(1)			
		
    Punkte = punkte_
	
    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
        if self.dim == 3:		
            t0 = latex(Vektor(x, y, z)) + latex('=')
        else:
            t0 = latex(Vektor(x, y)) + latex('=')		
        t1 = latex(self.stuetz) + latex('+')
        t2 = latex(self.par) + '\,' + latex(self.richt)
        return display(Math(t0 + t1 + t2)) 
    def prg_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""
        if kwargs.get('h'):
            print('\nAngabe eines Punktes - Auswertung der Gleichung in diesem\n')
            return	
        try:			
            if len(punkt) != 1:
                raise AglaError('einen Punkt angeben')
            punkt = punkt[0]
            if not isinstance(punkt, Vektor):
                raise AglaError('einen Punkt angeben')			
            if punkt.dim == self.dim:
                _r = Symbol('_r')			
                p = self.pkt(_r)
                ll = loese(p - punkt, _r)
                if not ll:
                    lat = latex('\\text{die Gleichung ist nicht erfüllt}')
                    return display(Math(lat))
                else:
                    lat = latex('\\text{die Gleichung ist erfüllt }') + \
                          latex('[') + latex(self.par) + latex('=') + \
                          latex(ll[_r]) + latex(']')	
                    return display(Math(lat))
            else:
                raise AglaError('der Punkt hat nicht die richtige Dimension')			
        except AglaError as e:
            print('agla:', str(e))
            return			

    Prg = prg_			
			
    gleich = prg
    gleich_ = prg_	
    Gleich = prg_	
		
    @property		
    def koord(self):              
        """Koordinatengleichung"""
        if self.dim == 3:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        x, y = Symbol('x'), Symbol('y')
        arg = self.args
        if not isinstance(arg[0], Vektor): 
            a, b, c = arg[:3]
            gl = Gleichung(a*x + b*y + c, 0)		
        else:
            st, ri = arg[:2]		
            n = Vektor(-ri.y, ri.x)
            gl = Gleichung(n.x*x + n.y*y - n.sp(st), 0)		
        return gl
    def koord_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""
        if self.dim == 3:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        if kwargs.get('h'):
            print('\nAngabe eines Punktes - Auswertung der Gleichung in diesem\n')
            return	
        try:			
            if len(punkt) != 1:
                raise AglaError('einen Punkt angeben')
            punkt = punkt[0]
            if not isinstance(punkt, Vektor):
                raise AglaError('einen Punkt angeben')			
            if isinstance(punkt, Vektor) and punkt.dim == self.dim:
                _r = Symbol('_r')				
                p = self.pkt(_r)
                ll = loese(p - punkt, _r)
                if not ll:
                    lat = latex('\\text{die Gleichung ist nicht erfüllt}')
                    return display(Math(lat))
                else:
                    lat = latex('\\text{die Gleichung ist erfüllt}') 
                    return display(Math(lat))
            else:					
                raise AglaError('einen Punkt der Ebene angeben')
        except AglaError as e:
            print('agla:', str(e))
            return			

    Koord = koord_
	
    @property
    def nf(self):
        """Gleichung in Normalenform; nur zur Ausgabe"""
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        x, y = Symbol('x'), Symbol('y')	
        lat = latex('\\left[') + latex(Vektor(x, y)) +'-' + \
		       latex(self.stuetz) + latex('\\right]') + latex('\circ') + \
			    latex(self.norm) + latex('=') + latex(0) 
        return display(Math(lat))
    def nf_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""	
        if self.dim == 3:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        if kwargs.get('h'):
            print('\nAngabe eines Punktes - Auswertung der Gleichung in diesem')
            print('k = 1 - Ausgabe der Koordinatengleichung\n')
            return	
        if kwargs.get('k'):
            return self.koord	
        try:			
            if len(punkt) != 1:
                raise AglaError("einen Punkt angeben")
            punkt = punkt[0]
            if isinstance(punkt, Vektor) and punkt.dim == 2:
                x, y = Symbol('x'), Symbol('y')
                gl = (Vektor(x, y) -self.stuetz) * self.norm      
                gl = gl.subs({x:punkt.x, y:punkt.y})
                if simplify(gl) == 0:
                    lat = latex('\\text{die Gleichung ist erfüllt}')				
                    return display(Math(lat))
                else:
                    lat = latex('\\text{die Gleichung ist nicht erfüllt}')				
                    return display(Math(lat))
                return
            else:
                raise AglaError("Punkt im Raum angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			

    Nf = nf_
	
    @property			
    def hnf(self):
        """Hessesche Normalenform; nur zur Ausgabe"""
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        x, y = Symbol('x'), Symbol('y')	
        lat = latex('\\left[') + latex(Vektor(x, y)) +'-' + \
		       latex(self.stuetz) + latex('\\right]') + latex('\circ') + \
              (latex(1/self.norm.betrag) if self.norm.betrag != 1 else '') \
			    + latex(self.norm) + latex('=') + latex(0) 
        return display(Math(lat))
		
    @property		
    def fkt(self):              
        """Funktionsgleichung; nur zur Ausgabe"""
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        x, y = Symbol('x'), Symbol('y')
        arg = self.args
        if not isinstance(arg[0], Vektor): 
            a, b, c = arg[:3]
        else:
            st, ri = self.args[:2]
            n = Vektor(-ri.y, ri.x)			
            a, b, c = n.x, n.y, - n.sp(st)
        if not b:
            print('agla: die Funktionsgleichung ist nicht definiert')
            return
        gl = Gleichung(y, nsimplify(expand((-a*x - c) / b)))		
        return gl
    def fkt_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        if kwargs.get('h'):
            print('\nAngabe eines Punktes - Auswertung der Gleichung in diesem\n')
            return	
        try:			
            if len(punkt) != 1:
                raise AglaError('einen Punkt angeben')
            punkt = punkt[0]
            if not isinstance(punkt, Vektor):
                raise AglaError('einen Punkt angeben')			
            if isinstance(punkt, Vektor) and punkt.dim == self.dim:
                _r = Symbol('_r')			
                p = self.pkt(_r)
                ll = loese(p - punkt, _r)
                if not ll:
                    lat = latex('\\text{die Gleichung ist nicht erfüllt}')
                    return display(Math(lat))
                else:
                    lat = latex('\\text{die Gleichung ist erfüllt}') 
                    return display(Math(lat))
            else:					
                raise AglaError('einen Punkt der Ebene angeben')
        except AglaError as e:
            print('agla:', str(e))
            return
			
    Fkt = fkt_
	
    @property
    def anstieg(self):
        """Anstieg"""	
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        args = self.args
        m = None
        if not isinstance(args[0], Vektor):	
            if args[1]:
                m = -args[0] / args[1]			
                try:					
                    m = nsimplify(m)
                except RecursionError:
                    pass					
        else:	
            ri = args[1]		
            if ri.x:
                m = ri.y / ri.x			
                try:					
                    m = nsimplify(m)
                except RecursionError:
                    pass					
        if m is not None:
            return m		
        print('agla: der Anstieg ist nicht definiert')
		
    m = anstieg		
		
		
    @property
    def y_abschn(self):
        """Abschnitt auf der *y* -Achse"""	
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        args = self.args
        n = None
        if not isinstance(args[0], Vektor):		
            if args[1]:
                n = -args[2] / args[1]			
                try:					
                    n = nsimplify(n)
                except RecursionError:
                    pass					
        else:
            st, ri = args[:2]		
            if ri.x:
                n = st.y - st.x / ri.x * ri.y
                try:					
                    n = nsimplify(n)
                except RecursionError:
                    pass					
        if n is not None:
            return n		
        print('agla: der Abschnitt auf der y-Achse ist nicht definiert')
		
    n = yAbschn = y_abschn
	
    @property
    def aagl(self):
        """Achsenabschnittsgleichung"""
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return			
        args = self.args
        if args[2]:
            x, y = Symbol('x'), Symbol('y')			
        args = self.args
        gl = None
        if not isinstance(args[0], Vektor): 
            if args[2]:		
                a = -args[0] / args[2]
                b = -args[1] / args[2]	
                try:
                    a, b = nsimplify(a), nsimplify(b)		
                except RecursionError:
                    pass					
                gl = Gleichung(a*x + b*y, 1) 
        else:
            st, ri = args[:2]		
            n = Vektor(-ri.y, ri.x)
            if n.sp(st):		
                a = n.x / n.sp(st)		
                b = n.y / n.sp(st)			
                try:
                    a, b = nsimplify(a), nsimplify(b)		
                except RecursionError:
                    pass					
                gl = Gleichung(a*x + b*y, 1) 
        if gl is None:          			
            display(Math('\\text{die Achsenabschnittsgleichung ist nicht definiert}'))
        return gl			
	
		
    @property		
    def spur_xy(self):
        """Spur in der *xy* - Ebene"""	
        if self.dim != 3:
            print('agla: nur für Geraden in R^3 definiert')		
            return		
        xy_ebene = importlib.import_module('agla.lib.objekte.ebene').xy_ebene	
        return self.schnitt(xy_ebene)
		
    spurXY = spur_xy		
		
    @property		
    def spur_xz(self):
        """Spur in der *xz* - Ebene"""	
        if self.dim != 3:
            print('agla: nur für Geraden in R^3 definiert')		
            return		
        xz_ebene = importlib.import_module('agla.lib.objekte.ebene').xz_ebene	
        return self.schnitt(xz_ebene)

    spurXZ = spur_xz		
		
    @property				
    def spur_yz(self):
        """Spur in der *yz* - SEbene"""	
        if self.dim != 3:
            print('agla: nur für Geraden in R^3 definiert')		
            return		
        yz_ebene = importlib.import_module('agla.lib.objekte.ebene').yz_ebene	
        return self.schnitt(yz_ebene)  		
		
    spurYZ = spur_yz		
			
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
        try:
		
            if not self.is_schar or len(self.sch_par) > 1:
                raise AglaError("keine Schar mit einem Parameter")			
		
            if kwargs.get('h'):
                print("\nElement einer Schar von Geraden\n")		
                print("Aufruf   gerade . sch_el( wert )\n")		                     
                print("             gerade    Gerade")
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
        stuetz = Vektor([k.subs(p, wert) for k in self.stuetz.komp])
        richt = Vektor([k.subs(p, wert) for k in self.richt.komp])		
        return Gerade(stuetz, richt, self.par)			
		
    schEl = sch_el
	
		
    def abstand(self, *objekt, **kwargs):	
        """Abstand zu einem anderen Objekt"""
		
        if kwargs.get('h'):
            print("\nAbstand der Geraden zu einem anderen Objekt\n")		
            print("Aufruf   gerade . abstand( objekt )\n")		                     
            print("             gerade    Gerade")
            print("             objekt    Punkt, Gerade, Ebene, Kugel  (im Raum R^3)")		
            print("                       Punkt, Gerade  (in der Ebene R^2)\n")		
            print("Rückgabe 0, wenn gerade und objekt sich schneiden\n")		
            print("Zusatz       d=n   Dezimaldarstellung")
            print("                   n - Anzahl der Nachkomma-/Stellen\n")
            return
	
        if len(objekt) != 1:
            print('agla: ein Objekt angeben')
            return
			
        objekt = objekt[0]
        if	 self.dim == 3:
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel
            if not isinstance(objekt, (Vektor, Gerade, Ebene, Kugel)):			
                print('agla: Punkt, Gerade, Ebene oder Kugel angeben')
                return			
			
            if isinstance(objekt, Vektor):   # Gerade - Punkt
                q = self.stuetz
                m = self.richt.einh_vekt
                wert = sqrt(((objekt - q) * (objekt - q) - \
                                        (m * (objekt - q))**2))
            elif isinstance(objekt, Gerade):   # Gerade - Gerade
                if objekt.dim == 3:
                    if objekt.richt.kollinear(self.richt):     
                        if objekt.stuetz.abstand(self) == 0:   
                            wert = 0
                        else:                                
                            wert = objekt.stuetz.abstand(self)
                    else:
                        if objekt.schnitt(self):
                            wert = 0
                        else: 
                            e = Ebene(objekt.stuetz, objekt.richt, self.richt)
                            wert = self.stuetz.abstand(e)	
                else:
                    print('agla: die Gerade hat nicht die richtige Dimension')
                    return					
            else:
                wert = objekt.abstand(self)
				
        if self.dim == 2:
            if not isinstance(objekt, (Vektor, Gerade)):
                print('agla: Punkt oder Gerade angeben')
                return				
            st, ri = self.stuetz, self.richt
            st, ri = Vektor(st.x, st.y, 0), Vektor(ri.x, ri.y, 0)
            g3 = Gerade(st, ri)			
            if isinstance(objekt, Vektor):
                o3 = Vektor(objekt.x, objekt.y, 0)	
            else:
                if objekt.dim != 2:			
                    print('agla: die Gerade hat nicht die richtige Dimension')
                    return					
                st, ri = objekt.stuetz, objekt.richt
                st, ri = Vektor(st.x, st.y, 0), Vektor(ri.x, ri.y, 0)
                o3 = Gerade(st, ri)
            wert = g3.abstand(o3)				
                			
        d = kwargs.get('d')
        if not isinstance(d, (Integer, int)) or d < 0:
            return wert
        return wert_ausgabe(wert, d)
			
			
    def bild(self, *abb, **kwargs):	
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBildgerade bei einer Abbildung\n")		
            print("Aufruf   gerade . bild( abb )\n")		                     
            print("             gerade    Gerade")
            print("             abb       Abbildung\n")		
            return
	
        try:	
            if len(abb) != 1:
                raise AglaError("eine Abbildung angeben")
            abb = abb[0]
            Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
            if not isinstance(abb, Abbildung):
                raise AglaError("eine Abbildung angeben")			
            if abb.dim != self.dim:
                raise AglaError("die Dimensionen sind unterschiedlich")		
        except AglaError as e:
            print('agla:', str(e))
            return
        p, q = self.punkte
        p1 = abb.matrix*p + abb.versch
        q1 = abb.matrix*q + abb.versch
        if p1 != q1:
            return Gerade(p1, Vektor(p1, q1))
        else:
            return p1					
		

    def graf(self, spez, **kwargs):                       
        """Grafikelement für Gerade"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Gerade in R^3 mit mayavi"""			
				
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
		              spez[2][1]
					  
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]	
			
        xl, xr, yl, yr, zl, zr = [x for x in list(UMG._sicht_box)]				
        def par_werte(gerade):
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            eb = [ Ebene(1,0,0,-xl), Ebene(1,0,0,-xr), Ebene(0,1,0,-yl), 
		            Ebene(0,1,0,-yr), Ebene(0,0,1,-zl), Ebene(0,0,1,-zr) ]
            x, y, z, t = Symbol("x"), Symbol("y"), Symbol("z"), Symbol('t')
            p = gerade.pkt(t)
            li = []
            for e in eb:
                gl = e.koord_(Vektor(0,0,0), ausgabe=False).subs(x, p.x).\
                        subs(y, p.y).subs(z, p.z)
                if  gl.lhs.has(t):
                    li1 = solve(gl.lhs)
                    li += [[li1[0], gerade.pkt(li1[0])]]
            li1 = []				
            for el in li:
                p = el[1].dez
                if (xl<=p.x<=xr) and (yl<=p.y<=yr) and (zl<=p.z<=zr):
                    li1 += [el[0]]
            tmin, tmax = Min(*li1), Max(*li1)
            return tmin, tmax
			
        if not anim:			
            tmin, tmax = par_werte(self)
            p, q = self.pkt(tmin), self.pkt(tmax)
            x, y, z = [float(p.x), float(q.x)], [float(p.y), float(q.y)], \
                     [float(p.z), float(q.z)] 
            return mlab.plot3d(x, y, z, line_width=lin_staerke, 
                            color=lin_farbe, tube_radius=None)      
        else:
		
            # Da mlab.plot3d(..., extent=...) nicht funktioniert, müssen für jeden 
            # Wert aus dem Parameterbereich die Schnittpunkte der Geraden mit den 
            # Ebenen, die die Sichtbox begrenzen, berechnet werden
			
            print('agla: lange Rechenzeit')
			
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20						
            aa = np.linspace(float(aber[0]), float(aber[1]), N)  
            xa, ya, za = [], [], []
            x, y, z, b_, t = symbols('x y z b_ t')			
            gg = self.sch_el(b_)			
            xx, yy, zz = gg.pkt(t).komp
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
            ebenen = [x-xl, x-xr, y-yl, y-yr, z-zl, z-zr]
            i, tol = 0, 1e-6
            typ = (int, Integer, float, Float)			
            for bb in aa:
                bb = '(' + str(bb) + ')'
                sx = eval(xs.replace('b_', bb))
                sy = eval(ys.replace('b_', bb))
                sz = eval(zs.replace('b_', bb))
                tt = []
                for e in ebenen:
                    gl = e.subs([(x, sx), (y, sy), (z, sz)])
                    L = loese(gl)
                    if L:					
                        tt += [L[t]]			
                tt = [s for s in tt if 
                     xl-tol<=(sx if isinstance(sx, typ) else sx.subs(t, s))<=
                                                             xr+tol and 
	                  yl-tol<=(sy if isinstance(sy, typ) else sy.subs(t, s))<=
                                                             yr+tol and 
                     zl-tol<=(sz if isinstance(sz, typ) else sz.subs(t, s))<=
                                                                zr+tol]	
                if not tt:
                    xa += [[0, 0]]				
                    ya += [[0, 0]]				
                    za += [[0, 0]]
                    i += 1					 					
                    continue				
                tmin = Min(*tt)
                tmax = Max(*tt)		
                if isinstance(sx, typ):		
                    xa += [[float(sx), float(sx)]]
                else:					
                    xa += [[float(sx.subs(t, tmin)), float(sx.subs(t, tmax))]]
                if isinstance(sy, typ):		
                    ya += [[float(sy), float(sy)]]
                else:					 
                    ya += [[float(sy.subs(t, tmin)), float(sy.subs(t, tmax))]]
                if isinstance(sz, typ):		
                    za += [[float(sz), float(sz)]]
                else:					
                    za += [[float(sz.subs(t, tmin)), float(sz.subs(t, tmax))]]
            plt = mlab.plot3d(xa[0], ya[0], za[0], line_width=lin_staerke, 
                     color=lin_farbe, tube_radius=None) 
            return plt, (xa[1:], ya[1:], za[1:]), N-1	
					 		
							
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Gerade in R^3 mit vispy"""	
		
        pass		
				
			
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Gerade in R^2"""	
						
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else \
		            spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' \
		              else spez[2][3]
		
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:			
            tmin, tmax = -1000, 1000
            p, q = self.pkt(tmin), self.pkt(tmax)
            x, y = [float(p.x), float(q.x)], [float(p.y), float(q.y)]
            return plt.plot(x, y, linewidth=lin_staerke, 
                            color=lin_farbe)      	
		
	
    def schnitt(self, *objekt, **kwargs):
        """"Schnitt mit anderen Objekten"""
				
        if kwargs.get('h'):
            print("\nSchnitt der Geraden mit einem anderen Objekt\n")		
            print("Aufruf   gerade . schnitt( objekt )\n")		                     
            print("             gerade    Gerade")
            print("             objekt    Punkt, Gerade, Ebene, Kugel, Strecke, ")
            print("                       Dreieck, Viereck " + \
			       "im Raum R^3)")
            print("                       Punkt, Gerade, Strecke, Kreis ")
            print("                                              " + \
			      "in der Ebene R^2")
            print("Zusatz       l=1   Lageinformationen\n")			
            return
			
        Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke	
		
        if self.dim == 3: 	
		
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel
            Dreieck = importlib.import_module('agla.lib.objekte.dreieck').Dreieck	
            Viereck = importlib.import_module('agla.lib.objekte.viereck').Viereck	
			
            try:	
                if not objekt:
                    raise AglaError("ein Objekt angeben")
                if len(objekt) != 1:
                    raise AglaError('ein Objekt angeben')					
                objekt = objekt[0]	
                if not isinstance(objekt, (Vektor, Gerade, Ebene, Kugel, \
				         Strecke, Dreieck, Viereck)):
                    raise AglaError("Vektor, Gerade, Ebene, Kugel, " + \
					         "Strecke, Dreieck oder Viereck angeben")
                if self.dim != objekt.dim:
                    raise AglaError("die Objekte haben unterschiedliche Dimension")      				
            except AglaError as e:		
                print('agla:', str(e))
                return
            if isinstance(objekt, Vektor):
                t = Symbol('t')				
                L = loese(self.pkt(t) - objekt) 				
                if L:
                    if kwargs.get('l'):
                        lat = latex('\\text{der Punkt liegt auf der Geraden}')		
                        display(Math(lat))					
                        return 
                    return objekt
                if kwargs.get('l'):
                    lat = latex('\\text{der Punkt liegt nicht auf der ' + \
					'Geraden}')		
                    display(Math(lat))					
                    return 
                return set()
            elif isinstance(objekt, Gerade):
                r, s = Symbol("r"), Symbol("s")
                p, q = objekt.pkt(r), self.pkt(s)
                try:
                    di = solve([p.x - q.x, p.y -  q.y, p.z - q.z], [r, s])
                except RuntimeError:
                    from sympy import N
                    di = solve([N(p.x - q.x), N(p.y -  q.y), \
                               N(p.z - q.z)], [r, s])				
                if not di:                   
                    if kwargs.get('l'):
                        if kollinear(self.richt, objekt.richt):
                            zusatz = '\\text{parallel}'
                        else:
                            zusatz = '\\text{windschief}'
                        lat = latex('\\text{die Geraden schneiden sich }') + \
					             latex('\\text{nicht, sie sind }' + zusatz)						
                        display(Math(lat))
                        return					
                    return set()             
                elif len(di)  == 1:
                    if kwargs.get('l'):
                        lat = latex('\\text{die Geraden sind identisch}')
                        display(Math(lat))
                        return					
                    return self
                if kwargs.get('l'):
                    lat = latex('\\text{die Geraden schneiden sich im }') + \
                          latex('\\text{Punkt}')
                    pp = objekt.pkt(di[r])
                    lat1 = pp.punkt_ausg_(s=1)
                    lat2 = latex('[\:') + latex(self.par) + latex('=') + \
						      latex(di[s]) + latex('\:]')
                    display(Math(lat + lat1 + '\:\:' + lat2))
                    return				
                return objekt.pkt(di[r])       
            else:
                if kwargs.get('l'):
                    return objekt.schnitt(self, l=1)		
                return objekt.schnitt(self)		
				
        elif self.dim == 2: 
           		
            Kreis = importlib.import_module('agla.lib.objekte.kreis').Kreis	
            st, ri = self.stuetz, self.richt	
            g3 = Gerade(Vektor(st.x, st.y, 0), Vektor(ri.x, ri.y, 0))		
            try:	
                if not objekt:
                    raise AglaError("Vektor, Gerade, Strecke oder Kreis angeben")
                if len(objekt) != 1:
                    raise AglaError('ein Objekt angeben')					
                objekt = objekt[0]	
                if mit_param(self) or mit_param(objekt) and isinstance(objekt, 
                    (Strecke, Kreis)):
                    print('agla: nicht implementiert (Parameter)')
                    return				
                if not isinstance(objekt, (Vektor, Gerade, Strecke, Kreis)):
                    raise AglaError("Vektor, Gerade, Strecke  oder Kreis angeben")		     
                if self.dim != objekt.dim:
                    raise AglaError("die Objekte haben unterschiedliche Dimension")      				
            except AglaError as e:		
                print('agla:  ', str(e))
                return
            if isinstance(objekt, Vektor):
                if objekt.dim != 2:
                    print("agla: der Vektor hat nicht die richtige Dimension")
                    return					
                o3 = Vektor(objekt.x, objekt.y, 0)
                ss = g3.schnitt(o3)		
                if ss:
                    if kwargs.get('l'):
                        lat = latex('\\text{der Punkt liegt auf der Geraden}')		
                        display(Math(lat))					
                        return 				
                    return Vektor(ss.x, ss.y)
                if kwargs.get('l'):
                    lat = latex('\\text{der Punkt liegt nicht auf }' + \
                               '\\text{der Geraden}')		
                    display(Math(lat))					
                    return 				
                return set()	
            elif isinstance(objekt, Gerade):
                if objekt.dim != 2:
                    print("agla: die Gerade hat nicht die richtige Dimension")
                    return	
                st, ri = objekt.stuetz, objekt.richt	
                st, ri = Vektor(st.x, st.y, 0), Vektor(ri.x, ri.y, 0)                					            
                o3 = Gerade(st, ri)  
                ss = g3.schnitt(o3)   
                if isinstance(ss, Vektor):
                    ss2 = Vektor(ss.x, ss.y)				
                    if kwargs.get('l'):
                        lat = latex('\\text{die Geraden schneiden sich }'+ \
                             '\\text{im Punkt}')		   
                        lat1 = ss2.punkt_ausg_(s=1)
                        display(Math(lat + lat1))					
                        return 								
                    return ss2
                elif isinstance(ss, Gerade):
                    if kwargs.get('l'):
                        lat = latex('\\text{die Geraden sind identisch}')		
                        display(Math(lat))					
                        return 								
                    return self
                if kwargs.get('l'):
                    lat = latex('\\text{die Geraden schneiden sich nicht}')		
                    display(Math(lat))					
                    return 								
                return set()					
            elif isinstance(objekt, Strecke):
                if objekt.dim != 2:
                    print("agla: die Strecke hat nicht die richtige Dimension")
                    return	
                p1, p2 = objekt.punkte
                p1, p2 = Vektor(p1.x, p1.y, 0), Vektor(p2.x, p2.y, 0)
                o3 = Strecke(p1, p2)
                ss = g3.schnitt(o3)
                if isinstance(ss, Vektor):
                    if kwargs.get('l'):
                        lat = latex('\\text{die Strecke schneidet die }' + \
                             '\\text{Gerade in einem Punkt}')		
                        display(Math(lat))					
                        return 								
                    return Vektor(ss.x, ss.y)
                elif isinstance(ss, Strecke):
                    if kwargs.get('l'):
                        lat = latex('\\text{die Strecke liegt auf der }' + \
                             '\\text{Geraden}')		
                        display(Math(lat))					
                        return 								
                    p1, p2 = ss.punkte
                    p1, p2 = Vektor(p1.x, p1.y), Vektor(p2.x, p2.y)					
                    return Strecke(p1, p2)
                if kwargs.get('l'):
                    lat = latex('\\text{die Strecke schneidet die }' + \
                         '\\text{Gerade nicht}')		
                    display(Math(lat))					
                    return 								
                return set()					
            elif isinstance(objekt, Kreis):
                if kwargs.get('l'):
                    return objekt.schnitt(self, l=1)				
                return objekt.schnitt(self)
                				
				
    def winkel(self, *objekt, **kwargs):
        """Winkel mit einem anderen Objekt"""
					
        if kwargs.get('h'):
            print("\nWinkel der Geraden mit einem anderen Objekt (in Grad)\n")		
            print("Aufruf   gerade . winkel( objekt )\n")		                     
            print("             gerade    Gerade")
            print("             objekt    Vektor, Gerade, Ebene  (im Raum R^3)")
            print("                       Vektor, Gerade  (in der Ebene R^2)\n")
            print("Bei objekt=Gerade Rückgabe des Winkels zwischen den beiden")
            print("Richtungsvektoren (unabhängig von der Lage)\n")
            print("Zusatz       d=n   Dezimaldarstellung")
            print("                   n - Anzahl der Nachkomma-/Stellen\n")
            return 
		
        if len(objekt) != 1:
            print("agla: ein Objekt angeben")
            return			
        objekt = objekt[0]
        if objekt == Vektor(0, 0, 0) or objekt == Vektor(0, 0):
            print('agla: der Winkel ist nicht definiert (Nullvektor)')
            return
			
        if self.dim == 3:
            Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
            if isinstance(objekt, Vektor):	
                wi = self.richt.winkel(objekt)
            elif isinstance(objekt, Gerade):
                wi = self.richt.winkel(objekt.richt)
            elif isinstance(objekt, Ebene):
                wi = objekt.winkel(self)		
            else:
                print('agla: Vektor, Gerade oder Ebene angeben')
                return
            if not mit_param(wi):				
                if wi > 90:
                    wi = 180 - wi				
        else:
            if not isinstance(objekt, (Vektor, Gerade)):
                print('agla: Vektor oder Gerade angeben')
                return			
            if objekt.dim != 2:
                print('agla: der Vektor bzw. die Gerade hat nicht die ' + \
				        'richtige Dimension')
                return
            st, ri = self.stuetz, self.richt
            st, ri = Vektor(st.x, st.y, 0), Vektor(ri.x, ri.y, 0)
            g3 = Gerade(st, ri)
            if isinstance(objekt, Vektor):
                o3 = Vektor(objekt.x, objekt.y, 0)
            else:
                st, ri = objekt.stuetz, objekt.richt
                st, ri = Vektor(st.x, st.y, 0), Vektor(ri.x, ri.y, 0)
                o3 = Gerade(st, ri)			
            wi = g3.winkel(o3)
			
        d = kwargs.get('d')
        if not isinstance(d, (Integer, int)) or d < 0:
            return wi
        return wert_ausgabe(wi, d)
		
		
    def proj(self, *ebene, **kwargs):	
        """Projektion auf eine Ebene"""
		
        if self.dim != 3:
            print('agla: nur für Geraden in R^3 definiert')		
            return			
		
        if kwargs.get('h'):
            print("\nProjektion der Geraden auf eine Ebene\n")		
            print("Aufruf   gerade . proj( ebene )\n")		                     
            print("             gerade    Gerade")
            print("             ebene     Ebene\n")
            return
	
        if len(ebene) != 1:
            print("agla: eine Ebene angeben")
            return			
        ebene = ebene[0]
        p = self.schnitt(ebene)
        if p:
            if isinstance(p, Gerade):
                return self
            if orthogonal(self, ebene):
                return p
            q = self.punkte[0]
            if q == p:
                q = self.punkte[1]
            g = Gerade(q, ebene.norm)
            s = g.schnitt(ebene)
            return Gerade(p, Vektor(p, s))
        elif self.abstand(ebene) == 0:
            return self
        p, q = self.punkte[0], self.punkte[1]
        g1, g2 = Gerade(p, ebene.norm), Gerade(q, ebene.norm)
        s1, s2 = g1.schnitt(ebene), g2.schnitt(ebene)	
        return Gerade(s1, Vektor(s1, s2))

	
    def pkt(self, *wert, **kwargs):
        """Geradenpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt der Geraden\n")		
            print("Aufruf    gerade . pkt( /[ wert ] )\n")		                     
            print("              gerade   Gerade")
            print("              wert     Wert des Geradenparameters\n")
            print("Rückgabe      bei Angabe eines Parameterwertes:") 
            print("              Geradenpunkt, der zu diesem Wert gehört")
            print("              bei leerer Argumentliste oder freiem " + \
			       "Bezeichner:") 
            print("              allgemeiner Punkt der Geraden\n") 			
            return

        if not wert:
            return self.stuetz + self.richt * self.par
        if len(wert) == 1:
             pw = sympify(wert[0])
             if not is_zahl(pw):
                 print('agla: Zahlenwert oder freien Bezeichner angeben')
                 return			
             return self.stuetz + self.richt * pw			 
        print("agla: einen Parameterwert angeben")
        return		
		
		    
    def normale(self, *arg, **kwargs):
        """Normale in einem Geradenpunkt"""
		
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return
			
        if kwargs.get('h'):
            print("\nNormale in einem Geradenpunkt\n")		
            print("Aufruf    gerade . normale( /[ punkt | wert ] )\n")		                     
            print("              gerade   Gerade")
            print("              punkt    Geradenpunkt")
            print("              wert     Wert des Geradenparameters\n")
            print("Rückgabe      bei Angabe eines Punktes oder Parameterwertes:") 
            print("              Normale im (zugehörigen) Geradenpunkt")
            print("              bei leerer Argumentliste oder freiem " + \
			       "Bezeichner:") 
            print("              Normale im allgemeinen Geradenpunkt\n") 			
            return
			
        if len(arg) > 1:
            raise AglaError('nur ein Argument angeben')
            return			
        if arg:
            arg = arg[0] 
        else:
            arg = None					
        if isinstance(arg, Vektor):
            if arg.dim != 2:
                raise AglaError('Punkt in der Ebene angeben')
                return			
            if not self.schnitt(arg):
                raise AglaError('der Punkt liegt nicht auf der Geraden')
                return						
            p = arg
        else:			
            if arg:			
                pw = sympify(arg)
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return	
                pw = nsimplify(pw)				 
                p = self.pkt(pw)
            else:
                p = self.pkt(self.par)		
        ri = self.richt
        n = Vektor(-ri.y, ri.x)
        t, s = symbols('t s')		
        t1 = t		
        if self.par == t:		
            t1 = s
        return Gerade(p, n, t1)		

    senkrechte = normale

	
    def parallele(self, *args, **kwargs):
        """Parallele zu einer Geraden"""	
		
        if self.dim != 2:
            print('agla: nur für Geraden in R^2 definiert')		
            return
			
        if kwargs.get('h'):
            print("\nParallele Gerade durch einen gegebenen Punkt oder")
            print("in einem gegebenem Abstand   (in der Ebene R^2)\n")		
            print("Aufruf   gerade . parallele( punkt | abstand )\n")		                     
            print("             gerade     Gerade")
            print("             punkt      Punkt")
            print("             abstand    Zahl; das Vorzeichen " + \
			       "bestimmt die Lage\n")
            return	
		
        try:		
            if len(args) != 1:
                raise AglaError("ein Argument angeben")
            args = sympify(args[0])
            if not ((isinstance(args, Vektor) and args.dim == 2) or \
			     is_zahl(args)):
                raise AglaError("einen Punkt in der Ebene oder eine Zahl " + \
				        "angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			
        if isinstance(args, Vektor):
            return Gerade(args, self.richt, self.par)
        stuetz = self.stuetz + self.norm.einh_vekt * args
        return Gerade(stuetz, self.richt, self.par)
		   	
			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        if self.dim == 3:		
            gerade_hilfe(3)
            return			
        gerade_hilfe(4)	
		
    h = hilfe				
	
  
# Benutzerhilfe für Gerade
# ------------------------

def gerade_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden im Raum R^3")
        print("h=4 - Eigenschaften und Methoden in der Ebene R^2")
        return
		   
    if h == 2:
        print("\nGerade - Objekt\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")		
        print("             Gerade( stütz, richt /[, par ] )\n")
        print("                 stütz    Stützvektor")
        print("                 richt    Richtungsvektor")
        print("                 par      Geradenparameter;") 
        print("                          t falls nicht angegeben\n")
        print("     oder    Gerade( schar /[, par ] )\n") 
        print("                 schar   Punkteschar, die eine Gerade bildet") 
        print("                 par     muss bei mehr als einem Parameter in")
        print("                         schar angegeben werden\n")                  
        print("Erzeugung nur in der Ebene R^2:\n")                           
        print("             Gerade( m, n )\n")
        print("                 m,n     Koeffizienten der Gleichung  y=mx+n\n")
        print("     oder    Gerade( a, b, c )\n")
        print("                 a,b,c   Koeffizienten der Gleichung  ax+by+c=0\n")                   
        print("Zuweisung     g = Gerade(...)   (g - freier Bezeichner)\n")
        print("Beispiele")
        print("A = v(2, -1, 4); B = v(0, 3, -2)")
        print("Gerade(A, v(A, B)) - Gerade durch 2 Punkte")
        print("Gerade(2, -3)) - Gerade in R^2 mittels m und n")
        print("Gerade(v(a+1, 3, 2*a+3)) - Gerade über eine Punkteschar\n") 		
        print("Vordefinierte Geraden")
        print("x_achse   ( = xAchse)    x-Achse im Raum R^3")
        print("y_achse   ( = yAchse)    y-Achse im Raum R^3")
        print("z_achse   ( = zAchse)    z-Achse im Raum R^3")
        print("x_achse2  ( = xAchse2)   x-Achse in der Ebene R^2")
        print("y_achse2  ( = yAchse2)   y-Achse in der Ebene R^2\n")		
        return

    if h == 3:
        print("\nEigenschaften und Methoden (M) für Gerade im Raum R^3\n")
        print("g.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("g.abstand(...)  M  Abstand zu anderen Objekten")
        print("g.auf_pkt          = stütz (Aufpunkt)") 
        print("g.bild(...)     M  Bild bei einer Abbildung")
        print("g.dim              Dimension")
        print("g.gleich           = g.prg")
        print("g.gleich_(...)  M  = g.prg_(...)")
        print("g.is_schar         Test auf Schar")
        print("g.par              Parameter der Gleichung")
        print("g.pkt(...)      M  Geradenpunkt")      
        print("g.prg              Gleichung (Parmeterform)")
        print("g.prg_(...)     M  ebenso, zugehörige Methode")
        print("g.proj(...)     M  Projektion auf eine Ebene")
        print("g.punkte           2 Geradenpunkte")
        print("g.punkte_(...)  M  ebenso, zugehörige Methode")
        print("g.richt            Richtungsvektor")
        print("g.sch_el(...)   M  Element einer Schar")
        print("g.sch_par          Scharparameter")
        print("g.schnitt(...)  M  Schnitt mit anderen Objekten")
        print("g.spur_xy          Spur in der xy-Ebene")
        print("g.spur_xz          Spur in der xz-Ebene")
        print("g.spur_yz          Spur in der yz-Ebene")
        print("g.stütz            Stützvektor")
        print("g.winkel(...)   M  Winkel mit anderen Objekten\n")
        print("Synonyme Bezeichner\n")
        print("hilfe    :  h")
        print("auf_pkt  :  aufPkt") 
        print("gleich_  :  Gleich")
        print("is_schar :  isSchar")
        print("prg_     :  Prg")
        print("punkte_  :  Punkte")
        print("sch_el   :  schEl")
        print("sch_par  :  schPar")
        print("spur_xy  :  spurXY")
        print("spur_xz  :  spurXZ")
        print("spur_yz  :  spurYZ\n")
        return	
  
    if h == 4:
        print("\nEigenschaften und Methoden (M) für Gerade in der Ebene R^2\n")
        print("g.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("g.aagl               Achsenabschnittsgleichung")
        print("g.abstand(...)    M  Abstand zu anderen Objekten")
        print("g.anstieg            Anstieg")
        print("g.auf_pkt          = stütz (Aufpunkt)") 
        print("g.bild(...)       M  Bild bei einer Abbildung")
        print("g.dim                Dimension")
        print("g.gleich             = g.prg")
        print("g.gleich_(...)    M  = g.prg_(...)")
        print("g.is_schar           Test auf Schar")
        print("g.fkt                Funktionsgleichung  y=mx+n")
        print("g.fkt_(...)       M  ebenso, zugehörige Methode")
        print("g.hnf                Hessesche Normalenform")
        print("g.koord              Koordinatengleichung  ax+by+c=0")
        print("g.koord_(...)     M  ebenso, zugehörige Methode") 
        print("g.m                  = anstieg")
        print("g.n                  = y_abschn")
        print("g.nf                 Normalenform der Gleichung")
        print("g.nf_(...)        M  ebenso, zugehörige Methode")
        print("g.norm               Normalenvektor")		
        print("g.normale(...)    M  Normale in einem Geradenpunkt")		
        print("g.par                Parameter der Gleichung")
        print("g.parallele(...)  M  Parallele Gerade")
        print("g.pkt(...)        M  Geradenpunkt")      
        print("g.prg                Parametergleichung")
        print("g.prg_(...)       M  ebenso, zugehörige Methode")
        print("g.punkte             2 Geradenpunkte")
        print("g.punkte_(...)    M  ebenso, zugehörige Methode")
        print("g.richt              Richtungsvektor")
        print("g.sch_el(...)     M  Element einer Schar")
        print("g.sch_par            Scharparameter")
        print("g.schnitt(...)    M  Schnitt mit anderen Objekten")
        print("g.senkrechte(...) M  = normale(...)")
        print("g.stütz              Stützvektor")
        print("g.winkel(...)     M  Winkel mit anderen Objekten")
        print("g.y_abschn           Abschnitt auf der y-Achse\n")
        print("Synonyme Bezeichner\n")
        print("hilfe    :  h")
        print("auf_pkt  :  aufPkt") 
        print("gleich_  :  Gleich")
        print("is_schar :  isSchar")
        print("fkt_     :  Fkt")
        print("koord_   :  Koord")
        print("nf_      :  Nf")
        print("prg_     :  Prg")
        print("punkte_  :  Punkte")
        print("sch_el   :  schEl")
        print("sch_par  :  schPar")		
        print("y_abschn :  yAbschn\n")
        return	
  
   
  
# Vordefinierte Geraden
 
Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
t = Symbol("t")
x_achse = xAchse = Gerade(Vektor(0, 0, 0), Vektor(1, 0, 0), t)
y_achse = yAchse = Gerade(Vektor(0, 0, 0), Vektor(0, 1, 0), t)
z_achse = zAchse = Gerade(Vektor(0, 0, 0), Vektor(0, 0, 1), t)
x_achse2 = xAchse2 = Gerade(Vektor(0, 0), Vektor(1, 0), t)
y_achse2 = yAchse2 = Gerade(Vektor(0, 0), Vektor(0, 1), t)
  
  

  