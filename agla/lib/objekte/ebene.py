#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Ebene - Klasse  von agla           
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
if UMG.grafik_3d =='mayavi':
    from mayavi import mlab
else:
    from  vispy import scene
    from vispy.geometry.isosurface import isosurface
    from vispy.scene import STTransform
	
from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.abc import r, s, t
from sympy.simplify.simplify import nsimplify, simplify
from sympy.core.symbol import Symbol, symbols
from sympy.core.function import expand

from sympy.polys.polytools import gcd
from sympy import Abs
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.core.numbers import Integer, pi
from sympy.solvers.solvers import solve
from sympy.printing import latex
from sympy import acos

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, X, O
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kugel import Kugel		
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, Gleichung, 
     wert_ausgabe, kollinear, loese)
from agla.lib.funktionen.graf_funktionen import (_implicit_plot, hex2color,
    _funkt_sympy2numpy)
from agla.lib.objekte.ausnahmen import AglaError
import agla 


	
# Ebene - Klasse
# --------------	
	
class Ebene(AglaObjekt):    
    r"""
 
Ebene im Raum
	
**Erzeugung** 

   Ebene ( *stütz, richt1, richt2 /[, par1, par2 ]* )
   
      (über Parameterform) *oder*   
   
   Ebene ( *stütz, norm /[, par1, par2 ]* )
   
      (über Normalenform) *oder*         

   Ebene ( *a, b, c, d /[, par1, par2 ]* )
   
      (über Koordinatenform)
	
**Parameter**	
	
   *stütz* :    Stützvektor
	  
   *richt* :    Richtungsvektor
	  
   *norm* :    Normalenvektor
	  
   *a, b, c, d* : Koeffizienten der Gleichung *ax + by + cz + d = 0* 

   *par* :      Ebenenparameter; *r, s*  falls nicht angegeben	

|

**Vordefinierte Ebenen**
   
``xy_ebene`` : *xy* - Ebene 

``xz_ebene`` : *xz* - Ebene

``yz_ebene`` : *yz* - Ebene  
     
|
	 
    """
	
    #  Typ 1 Erzeugung der Ebene über die Normalengleichung
    #      2 	                       die Parametergleichung
    #      3	                       die Koordinatengleichung
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            ebene_hilfe(kwargs["h"])		
            return	
			
        try:
		
            if len(args) < 2 or len(args) > 6:
                raise AglaError("2-6 Argumente angeben")
			
            # Erzeugen einer Ebene aus Stütz- und Normalenvektor	   
            if len(args) in [2, 4]:		
                if len(args)==2 or len(args)==4 and isinstance(args[0], Vektor):   		
                    if (isinstance(args[0], Vektor) and args[0].dim == 3 and
                        isinstance(args[1], Vektor) and args[1].dim == 3): 	
                        if len(args) == 4:
                            if (isinstance(args[2], Symbol) and   
					             isinstance(args[3], Symbol)): 
                                r_parameter = args[2]
                                s_parameter = args[3]
                            else:
                                raise AglaError("Parameter nicht frei")					
                        else:
                            r_parameter, s_parameter = Symbol("r"), Symbol("s")
					
                        stuetz, norm = args[0], args[1]
                        if norm == Vektor(0, 0, 0):
                            raise AglaError("der Nullvektor kann nicht " + \
                                           "Normalenvektor sein")						
                        return AglaObjekt.__new__(cls, stuetz, norm, 
                                                r_parameter, s_parameter, 'nf')
		
            # Erzeugen einer Ebene aus Stütz- und 2 Richtungsvektoren
            if len(args) in [3, 5]:			
                if (isinstance(args[0], Vektor) and args[0].dim == 3 and
                    isinstance(args[1], Vektor) and args[1].dim == 3 and
                    isinstance(args[2], Vektor) and args[2].dim == 3): 	
                    if len(args) == 5:
                        if (isinstance(args[3], Symbol) and   
					         isinstance(args[4], Symbol)): 
                            r_parameter = args[3]
                            s_parameter = args[4]
                        else:
                            raise AglaError("der Parameter ist nicht frei")					
                    else:
                        r_parameter, s_parameter = Symbol("r"), Symbol("s") 
					
                    stuetz, richt1, richt2 = args[0], args[1], args[2]
                    O = Vektor(0, 0, 0)

                    if richt1 == richt2:					
                        raise AglaError("die Richtungsvektoren müssen verschieden sein")
                    if richt1 == O or richt2 == O:
                        raise AglaError("der Nullvektor kann nicht " + \
                                       "Richtungsvektor sein")					
                    return AglaObjekt.__new__(cls, stuetz, richt1, richt2, 
                                            r_parameter, s_parameter, 'prg')
		
            # Erzeugen einer Ebene aus den Koeffizienten der Koordinatengleichung
            if len(args) in [4, 6]:
                if not(len(args) == 4 and isinstance(args[0], Vektor)):	
                    try:				
                        a, b, c, d = [nsimplify(sympify(a)) for a in args[0:4]]	 
                    except RecursionError:
                        a, b, c, d = [a for a in args[0:4]]                        					
                    if a==0 and b==0 and c==0:
                        raise AglaError('die Koeffizienten bei x, y, z ' + \
						                  'dürfen nicht alle = 0 sein')					
                    for k in [a, b, c, d]:				
                        if not is_zahl(k):
                            raise AglaError("Zahlenwerte angeben")
                    if len(args) == 6:
                        if (isinstance(args[4], Symbol) and   
					           isinstance(args[5], Symbol)): 
                            r_parameter = args[4]
                            s_parameter = args[5]
                        else:
                            raise AglaError("der Parameter ist nicht frei")					
                    else:
                        r_parameter, s_parameter = Symbol("r"), Symbol("s") 
                    return AglaObjekt.__new__(cls, a, b, c, d, r_parameter, 
                                            s_parameter, 'koord')				
            else:
                raise AglaError("die Eingaben sind fehlerhaft")
			
        except AglaError as e:
            print('agla:', str(e))
            return
			
		
    @property
    def _typ(self):
        t = str(self.args[-1])
        if t == 'nf':
            return 1
        elif t == 'prg':
            return 2
        else:
            return 3
		    
    def __str__(self):  
        par = self.schPar
        if self._typ == 1:
            txt1 = ", Normalenform"
        elif self._typ == 2:
            txt1 = ", Parameterform"
        else:
            txt1 = ", Koordinatenform"		
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            ret = "Ebenenschar(" + ss + ")"
            return ret
        return 'Ebene' + txt1		
		

# Eigenschaften	
# -------------
		
    @property
    def __nf2koord__(self):
	# Konvertierung Normalen- -> Koordinatenform
        stuetz = self.args[0]
        norm = self.args[1]
        r, s = self.args[2:4]
        return Ebene(norm.x, norm.y, norm.z, -norm * stuetz, r, s)

    @property
    def __nf2prg__(self):
	# Konvertierung Normalen- -> Parameterform
        stuetz = self.args[0]
        norm = self.args[1]
        if norm.x == 0 and norm.y == 0:
            richt1 = Vektor(1, 0, 0)
        elif norm.x == 0 and norm.z == 0:
            richt1 = Vektor(1, 0, 0)
        elif norm.x == 0 and norm.z == 0:
            richt1 = Vektor(0, 1, 0)
        elif norm.x == 0:
            richt1 = Vektor(1, norm.z, -norm.y)
        elif norm.y == 0:
            richt1 = Vektor(norm.z, 1, -norm.x)
        elif norm.z == 0:
            richt1 = Vektor(norm.y, -norm.x, 1)
        else:
            richt1 = Vektor(norm.y, -norm.x, 0)		
        richt2 = norm.vp(richt1)			
        r, s = self.args[2:4]		
        return Ebene(stuetz, richt1, richt2, r, s)

    @property
    def __koord2prg__(self):
    # Konvertierung Koordinaten- -> Parameterform
        norm = Vektor(self.args[0:3])
        d = self.args[3]
        if norm.x != 0:
            x, y, z = Symbol("x"), 0, 0 
        elif norm.y != 0:
            x, y, z = 0, Symbol("y"), 0
        elif norm.z != 0:
            x, y, z = 0, 0, Symbol("z")
        gl = Vektor(x,y,z).sp(norm) + d
        if isinstance(x, Symbol):
            di = solve(gl, [x])
            stuetz = Vektor(di[0], 0, 0)
        elif isinstance(y, Symbol):
            di = solve(gl, [y])
            stuetz = Vektor(0, di[0], 0)
        else:
            di = solve(gl, [z])
            stuetz = Vektor(0, 0, di[0])				
        r, s = self.args[4:6]
        e = Ebene(stuetz, norm, r, s)
        return e.__nf2prg__
	
    @property
    def __prg2nf__(self):
    # Konvertierung Parameter- -> Normalenform
        norm = self.__norm__(*self.args[1:3])
        stuetz = self.args[0]
        r, s = self.args[3:5]
        return Ebene(stuetz, norm, r, s)
	
    @property
    def __prg2koord__(self):
    # Konvertierung Parameter- -> Koordinatenform
        e = self.__prg2nf__
        return e.__nf2koord__
						
    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def stuetz(self):              
        """Stützvektor"""
        if self._typ in [1, 2]:
            e = self
        else:
            e = self.__koord2prg__
        return e.args[0]
    
    auf_pkt = stuetz
    aufPkt = stuetz
	
    @property	
    def richt(self):              
        """Richtungsvektoren"""
        if self._typ == 1:
            e = self.__nf2prg__
        elif self._typ == 2:
            e = self
        else:
            e = self.__koord2prg__
        return e.args[1:3]

    spann = richt              

    @property	
    def norm(self):   
        """Normalenvektor"""
        if self._typ == 1:
            e = self
        elif self._typ == 2:
            e = self.__prg2nf__
        else:
            e = self.__koord2prg__
            e = e.__prg2nf__
        return e.args[1]

    @property			
    def par(self):              
        """Parameter der Gleichung"""
        return self.args[-3], self.args[-2]

    @property			
    def sch_par(self):              
        """Scharparameter"""
        ret = set()
        for i in range(0, len(self.args) - 3):
            ret |= self.args[i].free_symbols
        return ret
		
    schPar= sch_par		
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1		
			
    isSchar = is_schar		
		
    @property		
    def punkte(self):              
        """Drei Ebenenpunkte"""
        return ( self.stuetz, self.stuetz + self.richt[0], 
		         self.stuetz + self.richt[1] )
    def punkte_(self, **kwargs): 
        if kwargs.get('h'):
            print("\nAusgabe: Punkte mit den Parameterwerten (0, 0), " 
                                                + "(1, 0), (0, 1)\n")
            return												
        return self.punkte		
		
    Punkte = punkte_
	
    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        p1 = str(self.par[0])
        p2 = str(self.par[1])
        x, y, z = symbols('x y z')		
        lat = latex(X)+ latex('=') +latex(self.stuetz) + latex('+') + \
              latex(p1) + '\,' + latex(self.richt[0]) + latex('+') + latex(p2) + \
			    '\,' + latex(self.richt[1])
        return display(Math(lat))
    def prg_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""	
        if kwargs.get('h'):
            print('\nAngabe eines Punktes - Auswertung der Gleichung in ' + \
			        'diesem\n')
            return	
        try:	
            if len(punkt) != 1:
                raise AglaError("einen Punkt angeben")
            punkt = punkt[0]
            if isinstance(punkt, Vektor) and punkt.dim == 3:
                _r, _s = symbols('_r _s')			
                p = self.pkt(_r, _s)
                ll = loese(p - punkt, [_r, _s])
                if not ll:
                    lat = latex('\\text{die Gleichung ist nicht erfüllt}')				
                    return display(Math(lat))
                else:
                    lat = latex('\\text{die Gleichung ist erfüllt }' + \
					         '[%s = %s, %s = %s]' \
					        % (self.par[0], ll[_r], self.par[1], \
                                                   ll[_s]))
                return display(Math(lat))
            else:
                raise AglaError("Punkt im Raum angeben")	
        except AglaError as e:
            print('agla:', str(e))		
			
    Prg = prg_
	
    @property
    def koord(self):
        """Koordinatengleichung"""
        if self._typ == 1:
            e = self.__nf2koord__
        elif self._typ == 2:
            e = self.__prg2koord__
        else:
            e = self
        a, b, c, d = e.args[0:4]
        f = gcd(gcd(a, b), gcd(c, d))
        a, b, c, d = a/f, b/f, c/f, d/f        		  
        x, y, z = Symbol("x"), Symbol("y"), Symbol("z")
        gl = Gleichung(expand(simplify(a*x + b*y + c*z + d)))
        return gl			
		
    def koord_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""	
		
        if kwargs.get('h'):
            print('\nAngabe eines Punktes - Auswertung der Gleichung ' + \
			       'in diesem\n')
            return
			
        # kwarg 'ausgabe' zum internen Gebrauch			
        if kwargs.get('ausgabe') is None:         
            ausgabe = True
        else:
            ausgabe = kwargs.get('ausgabe')	
			
        if not ausgabe:			
            if self._typ == 1:
                e = self.__nf2koord__
            elif self._typ == 2:
                e = self.__prg2koord__
            else:
                e = self
            a, b, c, d = e.args[0:4]
            x, y, z = Symbol("x"), Symbol("y"), Symbol("z")
            gl = Gleichung(a*x + b*y + c*z + d)
            return gl
       
        try:			
            if len(punkt) != 1:
                raise AglaError("einen Punkt angeben")
            punkt = punkt[0]
            if isinstance(punkt, Vektor) and punkt.dim == 3:			
                if self._typ == 1:
                    e = self.__nf2koord__
                elif self._typ == 2:
                    e = self.__prg2koord__
                else:
                    e = self
                a, b, c, d = e.args[0:4]
                x, y, z = symbols('x y z')
                gl = Gleichung(a*x + b*y + c*z + d)			
                gl = gl.subs(x, punkt.x).subs(y, punkt.y).subs(z, punkt.z)
                if mit_param(simplify(gl.lhs)):
                    par = gl.lhs.free_symbols
                    txt = (str(list(par)[0]) if len(par) == 1 else \
                                      str(tuple([e for e in par])))					
                    display(Math(txt + '\\text{ ist Lösung der Gleichung}'))
                    lat = latex(gl.lhs) + '= 0'				
                    return display(Math(lat))
                if simplify(gl.lhs) == 0:
                    display(Math(latex('\\text{die Gleichung ist erfüllt}')))
                else:
                    display(Math(latex('\\text{die Gleichung ist nicht erfüllt}')))
                return
            else:
                raise AglaError("Punkt im Raum angeben")		
        except AglaError as e:
            print('agla:', str(e))		
		
    Koord = koord_
	
    @property
    def nf(self):
        """Normalenform der Gleichung; nur zur Ausgabe"""
        lat = latex('\\left[') + latex(X)+'-'+ latex(self.stuetz) + \
              latex('\\right]') + latex('\circ') + latex(self.norm) + \
              latex('=') + latex(0) 
        return display(Math(lat))
		
    def nf_(self, *punkt, **kwargs): 
        """zugehörige Methode; Auswertung in einem Punkt"""	
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
            if isinstance(punkt, Vektor) and punkt.dim == 3:
                x, y, z = symbols('x y z')
                gl = (X -self.stuetz) * self.norm      
                gl = gl.subs(x, punkt.x).subs(y, punkt.y).subs(z, punkt.z)
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
        lat = latex('\\left[') + latex(X)+'-'+ latex(self.stuetz) + \
              latex('\\right]') + latex('\circ') + \
              (latex(1/self.norm.betrag) if self.norm.betrag != 1 else '') \
			    + latex(self.norm) + latex('=') + latex(0) 
        return display(Math(lat))
		
    @property		
    def aagl(self):
        """Achsenabschnittsgleichung"""
        x, y, z = symbols('x y z')
        po = self.koord_(O, ausgabe=False).lhs.as_poly(x, y, z)		
        c = -po.coeff_monomial(1) 
        if c != 0:        
            gl = Gleichung((po + c) / c, 1)			
            return gl
        return display(Math(latex('\\text{die Achsenabschnittsgleichung ist nicht definiert}')))
		
    @property		
    def spur_xy(self):
        """Spur in der *xy* - Ebene"""
        if mit_param(self):
            ss = self.schnitt(xy_ebene)	
            if ss:
                return ss			
            return set()			
        p1, p2 = self.par
        zz = self.pkt().z		
        if zz.has(p1):
            ll = loese(zz, p1)
            gp = self.pkt().subs(p1, ll[p1])
            return Gerade(gp)			
        elif zz.has(p2):
            ll = loese(zz, p2)
            gp = self.pkt().subs(p2, ll[p2])
            return Gerade(gp)			
        else:
            if zz == 0:
                return self
            return set()	
			
    spurXY = spur_xy			
		
    @property		
    def spur_xz(self):
        """Spur in der *xz* - Ebene"""
        if mit_param(self):
            ss = self.schnitt(xz_ebene)	
            if ss:
                return ss			
            return set()			
        p1, p2 = self.par
        yy = self.pkt().y		
        if yy.has(p1):
            ll = loese(yy, p1)
            gp = self.pkt().subs(p1, ll[p1])
            return Gerade(gp)			
        elif yy.has(p2):
            ll = loese(yy, p2)
            gp = self.pkt().subs(p2, ll[p2])
            return Gerade(gp)			
        else:
            if yy == 0:
                return self
            return set()	

    spurXZ = spur_xz						
		
    @property		
    def spur_yz(self):
        """Spur in der *yz* - Ebene"""
        if mit_param(self):
            ss = self.schnitt(xy_ebene)	
            if ss:
                return ss			
            return set()			
        p1, p2 = self.par
        xx = self.pkt().x		
        if xx.has(p1):
            ll = loese(xx, p1)
            gp = self.pkt().subs(p1, ll[p1])
            return Gerade(gp)			
        elif xx.has(p2):
            ll = loese(xx, p2)
            gp = self.pkt().subs(p2, ll[p2])
            return Gerade(gp)			
        else:
            if xx == 0:
                return self
            return set()	

    spurYZ = spur_yz			
			
		
# Methoden
# --------
	 
    def __norm__(self, vekt1, vekt2):
        """Ermittlung eines Normalenvektors aus 2 Richtungsvektoren
             über Vektorprodukt"""
        nn = vekt1.vp(vekt2)
        try:		
            f = gcd(gcd(nn.x, nn.y), nn.z)
            if f > 1:
                nn = 1/f * nn
            if nn.x <= 0 and nn.y <= 0 and nn.z <= 0:
                nn = - nn	
        except TypeError:
            pass	   
        return nn			 
		
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        try:		
            if not self.is_schar or len(self.sch_par) > 1:
                raise AglaError("keine Schar mit einem Parameter")			
		
            if kwargs.get('h'):
                print("\nElement einer Schar von Ebenen\n")		
                print("Aufruf   ebene . sch_el( wert )\n")		                     
                print("             ebene    Ebene")
                print("             wert     Wert des Scharparameters\n")
                print("Es ist nur ein Scharparameter zugelassen\n")    
                return
			
            if not wert or len(wert) != 1:
                raise AglaError("einen Wert für den Scharparameter angeben") 
        except AglaError as e:
            print('agla:', str(e))
            return
			
        p = Tuple(*self.sch_par)[0]                                              
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter ' + \
			        'angeben')	
            return		
        try:
            wert = nsimplify(wert)		
        except RecursionError:
            pass		
        r, s = self.par
        if self._typ == 1:
            stuetz = Vektor([k.subs(p, wert) for k in self.stuetz.komp])
            norm = Vektor([k.subs(p, wert) for k in self.norm.komp])
            return Ebene(stuetz, norm, r, s)
        elif self._typ == 2:
            stuetz = Vektor([k.subs(p, wert) for k in self.stuetz.komp])
            richt1 = Vektor([k.subs(p, wert) for k in self.richt[0].komp]) 
            richt2 = Vektor([k.subs(p, wert) for k in self.richt[1].komp]) 
            return Ebene(stuetz, richt1, richt2, r, s)
        else:
            koeff = list(self.args[0:4])
            koeff = Tuple(*[k.subs(p, wert) for k in koeff])
            return Ebene(koeff[0], koeff[1], koeff[2], koeff[3], r, s)

    schEl = sch_el
	
			
    def pkt(self, *werte, **kwargs):
        """Ebenenpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt der Ebene\n")		
            print("Aufruf   ebene . pkt( /[ wert1, wert2 ] )\n")		                     
            print("             ebene    Ebene")
            print("             wert     Wert für einen Ebenenparameter\n")
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Ebenenpunkt, der zu diesen Werten gehört")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           allgemeiner Punkt der Ebene\n") 			
            return
				
        if not werte:
            return ( self.stuetz + self.richt[0] * self.par[0] + 
                    self.richt[1] * self.par[1] )
        if len(werte) == 2:
             try:		
                 pw0 = nsimplify(sympify(werte[0]))
                 pw1 = nsimplify(sympify(werte[1]))	
             except RecursionError:
                 pw0 = sympify(werte[0])
                 pw1 = sympify(werte[1])				 
             return self.stuetz + self.richt[0] *  pw0 + self.richt[1] * pw1 			 
        print("agla: zwei Parameterwerte angeben")
        return		

		
    def abstand(self, *objekt, **kwargs):
        """Abstand zu anderen Objekten"""
		
        if kwargs.get('h'):
            print("\nAbstand der Ebene zu einem anderen Objekt\n")		
            print("Aufruf   ebene . abstand( objekt )\n")		                     
            print("             ebene     Ebene")
            print("             objekt    Punkt, Gerade, Ebene, Kugel\n")
            print("Rückgabe 0, wenn ebene und objekt sich schneiden\n")
            print("Zusatz       d=n   Dezimaldarstellung")
            print("                   n - Anzahl der Nachkommastellen\n")
            return	
		
        try:	
            if not objekt:
                raise AglaError("Punkt, Gerade, Ebene oder Kugel angeben")			 
            if len(objekt) != 1:
                raise AglaError("nur ein Objekt angeben")	
            objekt = objekt[0]	
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
            if not isinstance(objekt, (Vektor, Gerade, Ebene, Kugel)):
                raise AglaError("Punkt, Gerade, Ebene oder Kugel angeben")
            if isinstance(objekt, Vektor) and objekt.dim != 3:
                raise AglaError('Vektor im Raum angeben')
        except AglaError as e:
            print('agla:', str(e))		
            return
			
        if isinstance(objekt, Vektor):
            wert = (objekt - self.stuetz).sp(self.norm.einh_vekt)
        elif isinstance(objekt, Gerade):
            if objekt.richt.sp(self.norm) == 0:
                wert = objekt.stuetz.abstand(self)
            else:
                wert = 0
        elif isinstance(objekt, Ebene):
            if objekt.norm.kollinear(self.norm):
                wert = objekt.stuetz.abstand(self)
            else:
                wert = 0
        else:
            wert = objekt.abstand(self)
        d = kwargs.get('d')
        if not isinstance(d, (Integer, int)) or d < 0:
            return wert
        return wert_ausgabe(wert, d)
	
			
    def schnitt(self, *objekt, **kwargs):
        """Schnitt mit anderen Objekten"""	
		
        if kwargs.get('h'):
            print("\nSchnitt der Ebene mit einem anderen Objekt\n")		
            print("Aufruf   ebene . schnitt( objekt )\n")		                     
            print("             ebene    Ebene")
            print("             objekt   Punkt, Gerade, Ebene, Kugel, Strecke\n")
            print("Zusatz       l=1   Lageinformationen\n")
            return	
		
        try:		
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")	
            objekt = objekt[0]
            Strecke = importlib.import_module('agla.lib.objekte.strecke').Strecke	
            Gerade = importlib.import_module('agla.lib.objekte.gerade').Gerade	
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel	
            if not isinstance(objekt, (Vektor, Gerade, Ebene, Strecke, Kugel)):
                raise AglaError("Punkt, Gerade, Ebene, Strecke oder Kugel angeben")   
        except AglaError as e:
            print('agla:', str(e))
            return			
        if isinstance(objekt, Vektor):
            if simplify(self.abstand(objekt)) == 0:
                if kwargs.get('l'):
                   lat = latex('\\text{der Punkt liegt in der Ebene}')				
                   return display(Math(lat))
                return objekt
            if kwargs.get('l'):
                lat = latex('\\text{der Punkt liegt nicht in der Ebene}')			
                return display(Math(lat))
            return set()
        elif isinstance(objekt, Gerade):
            if objekt.richt.sp(self.norm) == 0:
                if simplify(objekt.abstand(self)) == 0:
                    if kwargs.get('l'):
                        lat = latex('\\text{die Gerade liegt in der Ebene}')				
                        return display(Math(lat))
                    return objekt
                if kwargs.get('l'):
                    lat = latex('\\text{die Gerade ist parallel zur Ebene}')			
                    return display(Math(lat))
                return set()
            if not mit_param(self) and not mit_param(objekt):
                gl = self.koord_(O, ausgabe=False).lhs
                p = objekt.pkt(objekt.par)
                x, y, z = symbols('x y z')
                gl = gl.subs(x, p.x).subs(y, p.y).subs(z, p.z)				
                li = solve(gl, objekt.par)	
                q = p.subs(objekt.par, li[0])
            else:
                _r, _s, _t = symbols('_r _s _t')
                ee = Ebene(self.stuetz, self.norm, _r, _s)
                gg = Gerade(objekt.stuetz, objekt.richt, _t)
                pp = ee.pkt(_r, _s) - gg.pkt(_t)
                gl = [pp.x, pp.y, pp.z]
                li = solve(gl, [_r, _s, _t])
                try:				
                    q = gg.pkt(_t).subs(_t, li[_t])
                except KeyError:
                    return None
                li = [li[_t]]
            if kwargs.get('l'):
                lat = latex('\\text{die Gerade schneidet die Ebene im Punkt}') 
                lat1 = q.punkt_ausg_(s=1)
                lat2 = '\:\: [\:' + latex(objekt.par) + '=' +  \
                      latex(li[0]) + '\:]'	
                display(Math(lat + lat1 + lat2))
                return
            return q
        elif isinstance(objekt, Ebene):                                
            if objekt.norm.kollinear(self.norm):
                if simplify(objekt.stuetz.abstand(self)) == 0:
                    if kwargs.get('l'):
                        return display(Math(latex('\\text{die Ebenen sind identisch}')))
                    return self
                if kwargs.get('l'):
                    return display(Math(latex('\\text{die Ebenen sind parallel}')))
                return set()
            gl = self.koord_(O, ausgabe=False).lhs
            r, s = symbols('r s')
            p = objekt.pkt(r, s)
            x, y, z = symbols('x y z')
            gl = gl.subs(x, p.x).subs(y, p.y).subs(z, p.z)
            gl = simplify(gl)
            if not gl.has(r):
                li = solve(gl, s)
                q = p.subs(s, li[0]) 	
                par = 'r'				
            elif not gl.has(s):
                li = solve(gl, r)
                q = p.subs(r, li[0]) 	
                par = 's'
            else:				
                try:
                    li = solve(gl, r)
                    q = p.subs(r, li[0]) 	
                    par = 'r'				
                except IndexError:
                    li = solve(gl, s)
                    q = p.subs(s, li[0]) 
                    par = 's'				
                if len(q.free_symbols) > 1:
                     try:
                         vv = Vektor(simplify(q.x), simplify(q.y), simplify(q.z))
                     except KeyError:	
                         vv = q					 
                     if r in vv.free_symbols:
                         pa = r	
                     else:
                         pa = s					 
                     return Gerade(vv, pa)					 
            g = Gerade(q)
            if kwargs.get('l'):
                lat = latex('\\text{die Ebenen schneiden sich in ' + \
                      'der Geraden }')		
                display(Math(lat))
                g.prg				                
                return
            return g
			
        else:
            if kwargs.get('l'):
                return objekt.schnitt(self, l=1)
            return objekt.schnitt(self)
	
			
    def bild(self, *abb, **kwargs):	
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBildebene bei einer Abbildung\n")		
            print("Aufruf   ebene . bild( abb )\n")		                     
            print("             ebene    Ebene")
            print("             abb      Abbildung\n")
            return	
		
        try:		
            if len(abb) != 1:
                raise AglaError("eine Abbildung angeben")
            abb = abb[0]
            Abbildung = agla.lib.objekte.abbildung.Abbildung
            Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
            if not (isinstance(abb, Abbildung) and abb.dim == 3):
                raise AglaError("eine Abbildung des Raumes angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			
        p, q, r = self.punkte
        p1, q1, r1 = p.bild(abb), q.bild(abb), r.bild(abb)
        if not kollinear(p1, q1, r1):
            return Ebene(p1, Vektor(p1, q1), Vektor(p1, r1))
        else:
            if p1 == q1:
                return Gerade(p1, Vektor(p1, r1))
            else:
                return Gerade(p1, Vektor(p1, q1))
				
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Ebene"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Ebene mit mayavi"""
		
        x, y, z = symbols('x y z')		
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                     else spez[1]						
        if not isinstance(flaech_farbe, tuple):
            flaech_farbe = hex2color(flaech_farbe)		
													
        if spez[2] != 'default':
            print('agla: für eine Ebene ist nur die Farbe variierbar')
			
        anim = False			
        if spez[3]:
            anim = True        
            aber = spez[3][:2]
						
        from numpy import sin, cos, tan, abs, log, arcsin, arccos, arctan, \
            sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, exp, pi
        b_ = Symbol('b_')
        ee = self
        if self.is_schar:		
            ee = self.sch_el(b_)		
        gl = str(ee.koord.lhs)	
        tab = _funkt_sympy2numpy 		
        for tt in tab:
            if tt in gl:	
                gl = gl.replace(tt, tab[tt]) 
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
            xl, xr, yl, yr, zl, zr = UMG._sicht_box
            Nx, Ny, Nz = 20, 20, 20   
            xx, yy, zz = np.mgrid[xl:xr:eval('{}j'.format(Nx)), \
			     yl:yr:eval('{}j'.format(Ny)), zl:zr:eval('{}j'.format(Nz))]
            gl0 = gl.replace(str(b_), str(aber[0]))
            gl0 = gl0.replace('x', 'xx').replace('y', 'yy').replace('z', 'zz')
            scalars = eval(gl0)
            src0 = mlab.pipeline.scalar_field(xx, yy, zz, scalars) 
            plt = mlab.pipeline.iso_surface(src0, color=flaech_farbe, \
                        contours=[-1.e-5])             # Anfangsstellung
            aa = np.linspace(float(aber[0]), float(aber[1]), N)
            scalars = []
            try:			
                for cc in aa:	
                    cc = str(cc)			
                    gl0 = gl.replace('b_', cc)
                    gl0 = gl0.replace('x', 'xx').replace('y', 'yy').replace('z', 'zz')
                    scalars += [eval(gl0)]
                return plt, scalars, N-1
            except MemoryError:
                return AglaError('die Anzahl der Unterteilungen (' + str(N) + ') ist zu groß')				
			
    def vispy(self, spez, **kwargs):
        """Grafikelement für Ebene mit vispy"""
		
        pass		
				
			
    def parallele(self, *args, **kwargs):
        """Parallele zu einer Ebene"""	
		
        if kwargs.get('h'):
            print("\nParallele Ebene durch einen gegebenen Punkt oder")
            print("in einem gegebenen Abstand\n")		
            print("Aufruf   ebene . parallele( punkt | abstand )\n")		                     
            print("             ebene      Ebene")
            print("             punkt      Punkt")
            print("             abstand    Zahl; das Vorzeichen bestimmt " + \
			       "die Lage\n")
            return	
		
        try:		
            if len(args) != 1:
                raise AglaError("ein Argument angeben")
            args = sympify(args[0])
            if not ((isinstance(args, Vektor) and args.dim == 3) or \
			          is_zahl(args)):
                raise AglaError("einen Punkt im Raum oder eine Zahl angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			
        if isinstance(args, Vektor):
            return Ebene(args, self.norm, self.par[0], self.par[1])
        stuetz = self.stuetz + self.norm.einh_vekt * args
        return Ebene(stuetz, self.norm, self.par[0], self.par[1])
		   
				
    def winkel(self, *objekt, **kwargs):
        """Winkel mit einem anderen Objekt"""	
		
        if kwargs.get('h'):
            print("\nWinkel der Ebene mit einem anderen Objekt (in Grad)\n")		
            print("Aufruf   ebene . winkel( objekt )\n")		                     
            print("             ebene    Ebene")
            print("             objekt   Vektor, Gerade, Ebene\n")
            print("Zusatz       d=n   Dezimaldarstellung")
            print("                   n - Anzahl der Nachkommastellen\n")
	
        try:
            if not objekt:
                raise AglaError("Vektor, Gerade oder Ebene angeben")
            if len(objekt) != 1:
                raise AglaError("nur ein Objekt angeben")
            objekt = objekt[0]	
            if not isinstance(objekt, (Vektor, Gerade, Ebene)):		
                raise AglaError("Vektor, Gerade oder Ebene im Raum angeben")
            if objekt.dim != 3:
                raise AglaError("Vektor, Gerade oder Ebene im Raum angeben")
        except AglaError as e:
            print('agla:', str(e))
            return			
        if isinstance(objekt, Vektor):
            if objekt == Vektor(0, 0, 0):
                print('agla: der Winkel ist nicht definiert (Nullvektor)')
                return
            wi = 90 - self.norm.winkel(objekt) 
        if isinstance(objekt, Gerade):
            wi = -90.0 + self.norm.winkel(objekt.richt)
        if isinstance(objekt, Ebene):

            m1, m2 = self.norm, objekt.norm
            if mit_param(m1.sp(m2)):			
                 wi = acos(m1.sp(m2)/m1.betrag/m2.betrag) / pi * 180
            else:				 
                wi = (acos(Abs(m1.sp(m2))/m1.betrag/m2.betrag) / pi * 180).evalf()
			
        d = kwargs.get('d')
        if not isinstance(d, (Integer, int)) or d < 0:
            return wi
        return wert_ausgabe(wi, d)

		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        ebene_hilfe(3)	
		
    h = hilfe		
		
		
   
# Benutzerhilfe für Ebene
# -----------------------

def ebene_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nEbene - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Ebene( stütz, richt1, richt2 /[, par1, par2 ] )\n")
        print("                 stütz    Stützvektor")
        print("                 richt    Richtungsvektor")
        print("                 par      Ebenenparameter;")
        print("                          r,s  falls nicht angegeben")	
        print("                 (Erzeugung über Parameterform)\n")
        print("     oder    Ebene( stütz, norm /[, par1, par2 ] )\n")
        print("                 norm    Normalenvektor")
        print("                 (Erzeugung über Normalenform)\n")
        print("     oder    Ebene( a, b, c, d /[, par1, par2 ] )\n")
        print("                 (Erzeugung über Koordinatenform")
        print("                  ax+by+cz+d=0)\n")
        print("Zuweisung     e = Ebene(...)   (e - freier Bezeichner)\n")
        print("Beispiele")
        print("A = v(2, -1, 4); B = v(0, 3, -2); C = v(-1, -1, 1)")
        print("Ebene(A, v(A, B), v(A, C)) - Ebene durch 3 Punkte")
        print("Ebene(v(1, 2, 3), v(4, 5, 6), u, w)")
        print("Ebene(-1, 3, 2, 2)\n")
        print("Vordefinierte Ebenen")
        print("xy_ebene  ( = xyEbene)    xy-Ebene")
        print("xz_ebene  ( = xzEbene)    xz-Ebene")
        print("yz_ebene  ( = yzEbene)    yz-Ebene\n")
        return
		
    if h == 3:
        print("\nEigenschaften und Methoden (M) für Ebene\n")
        print("e.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("e.aagl              Achsenabschnittsgleichung")
        print("e.abstand(...)   M  Abstand zu anderen Objekten")
        print("e.auf_pkt           = e.stütz (Aufpunkt)") 
        print("e.bild(...)      M  Bild bei einer Abbildung")
        print("e.dim               Dimension")
        print("e.hnf               Hessesche Normalenform")							
        print("e.is_schar          Test auf Schar")							
        print("e.koord             Koordinatengleichung")							
        print("e.koord_(...)    M  ebenso, zugehörige Methode")							
        print("e.nf                Normalenform der Gleichung")							
        print("e.nf_(...)       M  ebenso, zugehörige Methode")							
        print("e.norm              Normalenvektor")							
        print("e.par               Parameter in der Parametergleichung")							
        print("e.parallele(...) M  parallele Ebene") 							
        print("e.pkt(...)       M  Ebenenpunkt")							
        print("e.prg               Parametergleichung")							
        print("e.prg_(...)      M  ebenso, zugehörige Methode")							
        print("e.punkte            Drei Punkte der Ebene")							
        print("e.punkte_(...)   M  ebenso, zugehörige Methode")							
        print("e.richt             Richtungs- (Spann-)vektoren")
        print("e.sch_el(...)    M  Element einer Schar")
        print("e.sch_par           Scharparameter")
        print("e.schnitt(...)   M  Schnittmenge mit anderen Objekten")
        print("e.spann             = e.richt")
        print("e.spur_xy           Spur in der xy-Ebene")							
        print("e.spur_xz           Spur in der xz-Ebene")							
        print("e.spur_yz           Spur in der yz-Ebene")							
        print("e.stütz             Stützvektor") 
        print("e.winkel(...)    M  Winkel mit anderen Objekten\n")	 
        print("Synonyme Bezeichner\n")
        print("hilfe    :  h")
        print("auf_pkt  :  aufPkt") 
        print("is_schar :  isSchar")	
        print("koord_   :  Koord")
        print("nf_      :  Nf")
        print("prg_     :  Prg")
        print("punkte_  :  Punkte")
        print("sch_el   :  schEl")
        print("sch_par  :  schPar")
        print("spur_xy  :  spurXY")
        print("spur_xz  :  spurXZ")
        print("spur_yz  :  spurYZ\n")
        return   

   
# Vordefinierte Ebenen
# --------------------
		
xy_ebene = xyEbene = Ebene(Vektor(0, 0, 0), Vektor(1, 0, 0), 
                                           Vektor(0, 1, 0), r, s)
xz_ebene = xzEbene = Ebene(Vektor(0, 0, 0), Vektor(1, 0, 0), 
                                           Vektor(0, 0, 1), r, s)
yz_ebene = yzEbene = Ebene(Vektor(0, 0, 0), Vektor(0, 1, 0), 
                                           Vektor(0, 0, 1), r, s)

										   
										   