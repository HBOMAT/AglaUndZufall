 #!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Flaeche - Klasse von agla           
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



import time
import importlib

import numpy as np
from agla.lib.objekte.umgebung import UMG	
if UMG.grafik_3d == 'mayavi':
    from mayavi import mlab
else:
    pass
from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.numbers import Integer, Float, Rational, pi, NaN, nan, oo
from sympy.core.containers import Tuple
from sympy.simplify import simplify, nsimplify
from sympy.solvers.solvers import solve, nsolve
from sympy import (sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, asinh, 
     acosh, atanh, exp, log, Abs, cot, coth, sqrt, Max)
from sympy.core.evalf import N	 
from sympy.core.symbol import Symbol, symbols
from sympy.core.function import diff
from sympy.polys.polytools import Poly
from sympy.printing import latex

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, X
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.kurve import Kurve
from agla.lib.objekte.matrix import Matrix
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, Gleichung, 
     einfach, ja, Ja, nein, Nein, mit, ohne)
from agla.lib.funktionen.graf_funktionen import (_implicit_plot, 
            hex2color)
import agla



# Flaeche - Klasse   
# ----------------
	
class Flaeche(AglaObjekt):                                      
    """
	
Fläche im Raum

**Erzeugung** 
 
   Fläche ( *par_form, (u_par_name, u_unt, u_ob), (w_par_name, w_unt, w_ob)* )
 
   *oder*
   
   Fläche ( *allg_punkt, (u_par_name, u_unt, u_ob), (w_par_name, w_unt, w_ob)* )
   
   *oder*
   
   Fläche ( *fkt_gleich /[, (u_par_name, u_unt, u_ob), (w_par_name, w_unt, w_ob) ]* )
   
   *oder*
   
   Fläche ( *imp_gleich* )
   
**Parameter**

   *par_form* :     Parameterform  

   *allg_punkt* :   Vektor (allgemeiner Flächenpunkt)
     	
   *fkt_gleich* :   '*z = f(x, y )* '  Funktionsgleichung		
		
   *imp_gleich*:   
      '*F(x, y, z ) = 0* ' *oder* *F(x, y, z)*, 
      rechte Seite = 0 angenommen; Implizite Gleichung 
		  
   *u_par_name*: 
      Name des *u*-Flächenparameters; freier Bezeichner; 
      Standard *u*
   
   *w_par_name*: 
      ebenso, *w*-Flächenparameter; Standard *w*
	  
   *u_unt, u_ob*: 
      untere, obere Grenzen des Parameterbereiches für 
      den *u*-Parameter
   
   *w_unt, w_ob*: ebenso, *w*-Parameter
	  
   Die Verwendung der Bezeichner *x*, *y* und *z* ist zwingend
	  
   Bei einer Funktionsgleichung wird parametrisiert, wobei
   eventuell mitgeteilte Parameterangaben benutzt werden; dabei werden
   *x* und *y* durch die angegebenen Parameter ersetzt; wurden keine
   Parameterangaben gemacht, wird *(u, -10, 10),  (w, -10, 10)* verwendet

   Für die Parameterangaben kann statt eines Tupels eine Liste benutzt
   werden

Sollen weitere Gleichungen einer Fläche mit gespeichert werden, sind sie 
über Schlüsselwortparameter mitzuteilen, wobei nur die rechte bzw. linke 
Seite der jeweiligen Gleichung geschrieben wird
   
   - *prg = (...)* oder *v(...)*   Parameterform bzw. allgemeiner Flächenpunkt
	  
   - *fkt = f(x, y )*      - Funktionsgleichung (rechte Seite)
	  	  
   - *imp = F(x, y, z )*   - Implizite Gleichung (linke Seite; rechte Seite = 0 angenommen)
	  
Es wird nicht geprüft, ob diese Gleichungen zu der erzeugten Fläche gehören		

|
   
**Vordefinierte Flächen**
   
   ``EinhSphäre`` : Einheitssphäre
	  
   ``HypSchale``  : Obere Hälfte des Zweischaligen Hyperboloids
	  
   ``Sphäre`` (*mitte, radius* ) : Sphäre 
	  
      *mitte* : Mittelpunkt
		
      *radius* : Radius
		 
   ``KugelOberFläche = Sphäre``	
	  
|
   
    """
		
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3, 4):                         
            flaeche_hilfe(kwargs["h"])		
            return
			
        try:
		
            if len(args) > 0:
                aa = args[0]
                saa = str(aa).replace(' ', '')
				
                # Erzeugung über Parameterform bzw. allgemeinen Punkt' 
                if (isinstance(aa, Vektor) and aa.dim == 3) or \
                    (isinstance(aa, (tuple, Tuple)) and len(aa) == 3):
                    typ = 'prg'
                    if isinstance(aa, (tuple, Tuple)):
                        aa = Vektor(*aa)				
					
                # Erzeugung über Funktionsgleichung 'z = f(x, y)' 
                elif isinstance(aa, str) and saa[:2] == 'z=':
                    typ = 'fkt'
			
                # Erzeugung über implizite Gleichung 'F(x, y, z) = 0' 
                # bzw. F(x, y,z)                           				  
                elif isinstance(aa, str):
                    if not '=0' in saa:
                        raise AglaError("rechte Seite muss = 0 sein")
                    typ = 'imp'
                    gl = aa				   
                elif is_zahl(aa):
                    typ = 'imp'
                    gl = aa				   
			
                else:
                    raise AglaError("Eingabe überprüfen")
					
            else:
                raise AglaError("mindestens ein Argument angeben")
            						
            # Auswerten der Schlüsselwortparameter					
            x, y, z = Symbol('x'), Symbol('y'), Symbol('z')					
            prg, fkt, imp = [None] * 3
            if kwargs.get('prg'):
                prg = kwargs.get('prg')
                if isinstance(prg, (tuple, Tuple)):
                    try:
                        prg = Vektor(*prg)
                    except:
                        raise AglaError('Parameterform oder allgemeinen ' +
                             'Punkt angeben')						
                if not isinstance(prg, Vektor):
                    raise AglaError('die Parametergleichung ist falsch ' +
                         'angegeben')	
                if prg.dim != 3 or not mit_param(prg):
                    raise AglaError('die Parametergleichung ist falsch ' +
                         'angegeben')	
                prg = Gleichung(Vektor(x, y, z), prg)						
            if kwargs.get('fkt'):
                fkt = kwargs.get('fkt')
                if not isinstance(fkt, str):
                    fkt = str(fkt)					
                if fkt.find('=') >= 0:						
                   raise AglaError('hier keine Gleichung, sondern ' +
                        'einen Ausdruck angeben')	
                if fkt.find('x') < 0 and fkt.find('y') < 0 or fkt.find('z') \
                                                                >= 0: 
                    raise AglaError("einen Ausdruck in x und y " +
                         "angeben (als Zeichenkette)")
                ende = False
                while not ende:					
                    try:	
                        egl = fkt
                        ende = True							
                    except NameError as e:
                        es = str(e)
                        par = es[es.find("'")+1:es.rfind("'")]					
                        locals()[par] = Symbol(par)
                try:
                    egl = nsimplify(egl)
                except RcursionError:
                    pass				
                fkt = Gleichung(y, egl)                    					
            if kwargs.get('imp'):
                imp = kwargs.get('imp')
                if not isinstance(imp, str):
                    imp = str(imp)					
                if imp.find('=') >= 0:						
                    raise AglaError('hier keine Gleichung, sondern ' +
                         'einen Ausdruck angeben')	
                if imp.find('x') < 0 and imp.find('y') < 0 and imp.find('z') \
                                                                  < 0: 
                    raise AglaError("einen Ausdruck in x, y und z " +
                         "angeben (als Zeichenkette)")	
                ende = False
                while not ende:					
                    try:	
                        egl = sympify(imp)
                        ende = True							
                    except NameError as e:
                        es = str(e)
                        par = es[es.find("'")+1:es.rfind("'")]					
                        locals()[par] = Symbol(par)		
                imp = Gleichung(egl, 0)                    					
						
            # Erzeugen einer parametrisierten Fläche
		
            if typ in ['prg', 'fkt']:

                eingabeGleichung = []
				
                # über den allgemeinen Punkt
                if typ == 'prg':
                    if isinstance(args[0], Vektor):
                        allg_punkt = args[0]
                    else:					
                        allg_punkt = Vektor(*args[0]) 
                    if not (isinstance(allg_punkt, Vektor) and 
                                              allg_punkt.dim==3):
                        txt = "als erstes Argument den allgemeinen " + \
                                                  "Flächenpunkt angeben"
                        raise AglaError(txt)
                    if len(allg_punkt.free_symbols) < 2:
                        txt = "im allgemeinen Punkt müssen zwei " + \
                                         "Flächenparameter enthalten sein"
                        raise AglaError(txt)
						
                    if not len(args) in (3, 7):
                        txt = "es müssen Angaben für zwei Parameter " + \
                                                      "gemacht werden"
                        raise AglaError(txt)
                    if not prg:
                        prg = Gleichung(Vektor(x, y, z), allg_punkt)					
														
                # über die Funktionsgleichung  z = f(x, y)
                if typ == 'fkt':
                    allg_punkt = None				
                    if isinstance(args[0], Gleichung):
                        eingabeGleichung = args[0]
                    else:						
                        fkt = args[0]
                        if (fkt.find('x') < 0 and fkt.find('y') < 0 
                                                  and fkt.find('z') < 0):
                            txt = "eine Gleichung in den Variablen x," + \
                                  "y und z angeben" 
                            raise AglaError(txt)
                        if fkt.find('=') < 0:
                            lhs, rhs = fkt, 0
                        elif fkt.find('=') > 0:
                            lhs, rhs = fkt[:fkt.find('=')], \
                                               fkt[fkt.find('=')+1:]
                        else:
                            raise AglaError("Eingabegleichung überprüfen")
                        if lhs.find('z') < 0 or lhs.find('x') > 0 or \
                                                   lhs.find('y') > 0:
                            raise AglaError("auf der linken Seite der " + \
                                 "Gleichung darf nur z stehen")					
                        if rhs.find('z') > 0:
                            raise AglaError("auf der rechten Seite der " \
                                 "Gleichung dürfen nur x und y stehen")	
                        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
                        try:
                            lhs, rhs = nsimplify((lhs)), nsimplify((rhs))  
                        except (RecursionError, TokenError, SympifyError):
                           pass						
                        eingabeGleichung = Gleichung(lhs, rhs)
                        fkt = eingabeGleichung

                par_angaben = False				
                if len(args) in [3, 7]: 
                    par_angaben = True				
                    if len(args) == 3:
                        u_angaben = args[1]
                        if ( (not type(u_angaben) in (tuple, Tuple, list)) 
                             or len(u_angaben) != 3 ):
                            txt = ("drei Argumente für u-Parameter " +
                                     "(als Tupel oder Liste) angeben")
                            raise AglaError(txt)
                        u_par, u1, u2 = u_angaben[0], u_angaben[1], u_angaben[2]
                        w_angaben = args[2]
                        if ( not type(w_angaben) in (tuple, Tuple, list) 
                             or len(w_angaben) != 3 ):
                            txt = ("drei Argumente für w-Parameter " +
                                      "(als Tupel oder Liste) angeben")
                            raise AglaError(txt)
                        w_par, w1, w2 = w_angaben[0], w_angaben[1], w_angaben[2]
                    else:
                        u_par, u1, u2 = args[1:4]
                        w_par, w1, w2 = args[4:]
			
                else:
                    u, w = symbols('u w')                 
                    return Flaeche(	aa, (u, -10, 10), (w, -10, 10))			 
				 
                if not isinstance(u_par, Symbol):
                    raise AglaError("der u-Parameter ist nicht frei")
                if allg_punkt and not u_par in allg_punkt.free_symbols:    
                    txt = "der u-Parameter ist nicht im allgemeinen " + \
                          "Punkt enthalten"
                    raise AglaError(txt)
                if not (is_zahl(u1) and is_zahl(u2)):
                    raise AglaError("für den u-Bereich zwei Zahlenwerte " +
                         "angeben")
                try:						 
                    u1, u2 = nsimplify(u1), nsimplify(u2)
                except RecursionError:
                    pass				
                if not isinstance(w_par, Symbol):
                    raise AglaError("der w-Parameter ist nicht frei")
                if allg_punkt and not w_par in allg_punkt.free_symbols:
                    txt = "der w-Parameter ist nicht im allgemeinen " + \
                          "Punkt enthalten"
                    raise AglaError(txt)
                if not (is_zahl(w1) and is_zahl(w2)):
                    raise AglaError("für den w-Bereich zwei Zahlenwerte " + 
                                                            "angeben")
                try:															
                    w1, w2 = nsimplify(w1), nsimplify(w2)
                except RecursionError:
                    pass				
                u_angaben = (u_par, u1, u2)
                w_angaben = (w_par, w1, w2)
									
                if typ == 'fkt':
                    x, y = Symbol('x'), Symbol('y')
                    z_koord = eingabeGleichung.rhs.subs(x, u_par).subs \
                            (y, w_par)
                    z_koord = einfach(z_koord)
                    allg_punkt = Vektor(u_par, w_par, z_koord)
                    if not prg:						
                        prg = Gleichung(Vektor(x, y, z), allg_punkt)	
                    if not imp:		
                        gl = eingabeGleichung	
                        lhs = gl.lhs - gl.rhs
                        try:
                            nsimplify(lhs)
                        except RecursionError:
                            pass						
                        imp = Gleichung(lhs, 0)											
                										
                if allg_punkt:
                    if typ == 'fkt':
                        print("Erzeugung in Parameterform, " + " x -> " + \
                        str(u_angaben[0]) + ", y -> " + str(w_angaben[0]))
                        typ = 'prg'					
                    return AglaObjekt.__new__(cls, allg_punkt, 
                                               u_angaben, 
											          w_angaben, 
													   (prg, fkt, imp),
													   typ)	
                else:	
                    gl = 'z -' + str(eingabeGleichung.rhs)				
                    return Flaeche(gl)
						
            # Erzeugen einer Fläche mit der impliziten Gleichung
            elif typ == 'imp':
                if isinstance(gl, Gleichung):
                    gleich = gl
                else:
                    if not isinstance(gl, str):                        					
                        gl = str(gl) + '=0'
                    if gl.find('x') < 0 and gl.find('y') < 0 and \
                                                gl.find('z') < 0:
                        raise AglaError("eine Gleichung in x, y " + 
                                                   "und z angeben")	
                    if gl.find('=') < 0:
                        raise AglaError('die Zeichenkette muss ' + \
                             'eine Gleichung mit rechter Seite = 0 enthalten')
                    elif gl.find('=') > 0:
                        lhs, rhs = gl[:gl.find('=')], gl[gl.find('=')+1:]
                    else:
                        raise AglaError("Eingabe überprüfen")
                    lhs, rhs = sympify(lhs), sympify(rhs)	
                    if rhs != 0:
                        pass  #raise AglaError("rechte Seite = 0 angeben")				
                    if not (is_zahl(lhs) and is_zahl(rhs)):
                        raise AglaError("Funktionsausdrücke für beide " +
                                          "Seiten der Gleichung angeben")
                    lhs = lhs - rhs 					
                    try:
                        lhs = nsimplify(lhs)
                    except RecursionError:						
                        pass					
                    gleich = Gleichung(lhs, 0)
                    if not imp:
                        imp = gleich					
			
                return AglaObjekt.__new__(cls, gleich, (prg, fkt, imp),	typ)	
            else:
                raise AglaError("mindestens ein Argument angeben")
  			
        except AglaError as e:
            print('agla:', str(e))
            return
			
		
    def __str__(self):  
        par = self.sch_par
        if par:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Flächenschar(" + ss + ")"
        return "Fläche"	
	
    @property
    def _typ(self):
        return str(self.args[-1])	
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def par(self):              
        """Flächenparameter"""
        if self._typ == 'prg':
            return self.args[1][0], self.args[2][0]		
        else:
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
				
    @property
    def ber(self):              
        """Parameterbereiche"""
        if self._typ == 'prg':
            return ((self.args[1][1], self.args[1][2]), 
			                  (self.args[2][1], self.args[2][2]))
        else:
            print('agla: nicht verfügbar (implizite Gleichung)')					
				
    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        if self._typ == 'prg':
            gl = Gleichung(Vektor(x, y, z), self.pkt())
            return gl  
        gl = self.args[1][0]
        if gl:
            return gl		
        print('agla: die Gleichung/Form ist nicht verfügbar')					

    @property		
    def imp(self):              
        """Implizite Gleichung"""                               
        if self._typ == 'imp':		
            return self.args[0]
        gl = self.args[3][2]						
        if gl:
            return gl		
        print('agla: die Gleichung ist nicht verfügbar')					
			
    @property		
    def fkt(self):              
        """Funktionsgleichung""" 
        if self._typ == 'prg':
            gl = self.args[3][1]
        elif self._typ == 'imp':
            gl = self.args[1][1]
        if gl:
            return gl		
        print('agla: die Gleichung ist nicht verfügbar')					
			
    @property		
    def pf(self):              
        """Parameterform; nur zur Ausgabe"""
        if self._typ == 'imp':
            prg = self.prg	
            if prg:
                p = prg.rhs
            else:				
                print('agla: die Parameterform ist nicht verfügbar')					
                return
        else:			
            u, w = self.par			
            p = self.pkt(u, w)		
        display(Math('\\left(' + latex(p.x) + ',\;' + latex(p.y) + ',\;' + \
                   latex(p.z) + '\\right)'))	
        						
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        if self._typ == 'imp':
            gl = self.args[0]
            par = gl.lhs.free_symbols.union(gl.rhs.free_symbols)
            x, y, z = Symbol("x"), Symbol("y"), Symbol("z")
            par -= {x, y, z}
            return par
        else:
            pkt, u_par, w_par, gl, typ = self.args
            spar = pkt.free_symbols
            spar |= u_par[1].free_symbols
            spar |= u_par[2].free_symbols
            spar |= w_par[1].free_symbols
            spar |= w_par[2].free_symbols
            return spar - {self.par[0], self.par[1]}
			
    schPar = sch_par			

    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar	
		
    @property		
    def formeln(self):              
        print(' ')
        if self._typ == 'prg':		
            txt = '\mathrm{Berechnungsgrundage}\quad \mathrm{Gleichung\:in\:Parameterform}'
            display(Math(txt))		
            txt = '\\vec{x}(u,w)\:=\:' + \
		           '\\left(\\begin{matrix}x(u,w)\\\\y(u,w)\\\\z(u,w)\\end{matrix}' + \
                  '\\right)' + '\quad  \mathrm{bzw.}\quad' + \
        		    ' x=x(u,w),\: y=y(u,w),\: z=z(u,w)'
            display(Math(txt))		
            txt = "\mathrm{Tangentialebene} \quad\quad\quad\quad " + "\\left|\\begin{matrix}x-x_P &" + \
       		    "y-y_P & z-z_P\\\\x_u & y_u & z_u \\\\x_w & y_w & z_w" + \
                 "\\end{matrix}\\right| = 0"		 
            display(Math(txt))		
            txt = "\mathrm{Tangentenvektoren} \quad\quad\quad\:\, " + "\\vec{x}_u" + ", \:"+ \
		          "\\vec{x}_w"
            display(Math(txt))		
            txt = "\mathrm{Normaleneinheitsvektor} \quad\:\: " + "\\frac{ \\vec{x}_u " + \
		           "\\times \\vec{x}_w} {\\left| \\vec{x}_u \\times \\vec{x}_w \\right| }"
            display(Math(txt))		
            txt = "\mathrm{Erste\: quadratische\: Fundamentalform}"
            display(Math(txt))				
            txt = "\qquad\qquad\: E\, du^2+2\, F\, du\, dw+G\, dw^2"
            display(Math(txt))		
            txt = "\qquad\qquad\: E = x_u^2+y_u^2+z_u^2, \:\:\: F = x_u\, x_w+y_u \, y_w+z_u\, " + \
                  "z_w \:\:\: G = x_w^2+y_w^2+z_w^2"
            display(Math(txt))		
            txt = "\mathrm{Zweite\: quadratische\: Fundamentalform}"
            display(Math(txt))				
            txt = "\qquad\qquad\: L\, du^2+2\, M\, du\, dw+N\, dw^2"
            display(Math(txt))		
            txt = "\qquad\qquad\: L = \\frac{l}{\\sqrt{E\,G-F^2}}, \: M = \\frac{m}{\\" + \
		           "sqrt{E\,G-F^2}}, \: N = \\frac{n}{\\sqrt{E\,G-F^2}}"
            display(Math(txt))		
            txt = "\qquad\qquad\:l = \\left|\\begin{matrix}x_{uu} &" + \
       	    	"y_{uu} & z_{uu}\\\\x_u & y_u & z_u \\\\x_w & y_w & z_w" + \
                 "\\end{matrix}\\right|" + \
                 ", \:\:\:m = \\left|\\begin{matrix}x_{uw} &" + \
       		    "y_{uw} & z_{uw}\\\\x_u & y_u & z_u \\\\x_w & y_w & z_w" + \
                  "\\end{matrix}\\right|, \:\:\:" + \
                 " n = \\left|\\begin{matrix}x_{ww} &" + \
       		    "y_{ww} & z_{ww}\\\\x_u & y_u & z_u \\\\x_w & y_w & z_w" + \
             "\\end{matrix}\\right|"
            display(Math(txt))		
            txt = "\mathrm{Hauptkrümmungen} \:\:\: k_1,\: k_2, \:\:\:\:" + \
                 "\mathrm{Hauptkrümmungsradien} \:\:\: R_1 = \\frac{1}{k_1}, \:" + \
		           "R_2 = \\frac{1}{k_2} "
            display(Math(txt))		
            txt = "\qquad\qquad\: k_1\: \mathrm{und} \:k_2 \: \mathrm{sind\: Eigenwerte\: der}\:"
            display(Math(txt))		
            txt = "\qquad\qquad\: \mathrm{Weingartenmatrix} \:\:\;\;\;\;\ \\left(\\begin{matrix}E &" + \
       		    "F\\\\F & G " + \
                 "\\end{matrix}\\right)^{-1} \\left(\\begin{matrix}L &" + \
       		    "M\\\\M & N \\end{matrix}\\right)"
            display(Math(txt))		
            txt = "\qquad\qquad\: \mathrm{bzw.\: Lösungen\: der\: Gleichung}	"
            display(Math(txt))		
            txt = "\qquad\qquad\: k^2 - 2\, H\, k + K = 0 "
            display(Math(txt))					
            txt = "\mathrm{Gauß-Krümmung} \:\:\:\:\:\:\: K = \\frac{L\,N-M^2}{E\, G-F^2}" + \
                 "= k_1\,k_2"
            display(Math(txt))		
            txt = "\mathrm{Mittlere\: Krümmung} \:\:\:\:\:\:\: H = \\frac{L\,G-2\,F\,M+E\,N}" + \
                 "{2\,(E\, G-F^2)} = \\frac{1}{2}\,(k_1+,k_2)"
            display(Math(txt))		
            txt = "\mathrm{Bogenlänge\: einer\: Kurve}\:\: \\vec{x} = \\vec{x}(u(t), w(t))" + \
                  "\:\:\mathrm{auf\: der\: Fläche}\:"
            display(Math(txt))		
            txt = "\qquad\qquad\:b = \\int _{t_0} ^{t_1}" + \
                  "\\sqrt{E \, \dot{u}^2+2\,F\,\dot{u}\,\dot{w}+" + \
                 "G\,\dot{w}^2}dt" 
            display(Math(txt))				 
            txt = "\quad\quad\quad\quad\quad\quad ( \mathrm{zwischen\: den\: Punkten\: mit\:" + \
                  "den\: Parameterwerten}\: t_0\: und\: t_1)" 
            display(Math(txt))					  
            txt = "\mathrm{Winkel\: zwischen\: zwei\: Kurven}\:\: \\vec{x}_1 = \\vec{x}(u_1(t), w_1(t))" + \
                  ",\:\:\\vec{x}_2 = \\vec{x}(u_2(t), w_2(t))\:\:"
            display(Math(txt))					  
            txt = "\mathrm{auf\: der\: Fläche,\:die\: sich\: in\:einem\: Punkt\: schneiden}"
            display(Math(txt))		
            txt = "\qquad\qquad\:cos(\\alpha) = \\frac{E\,\dot{u_1}\, \dot{u_2} + F\,(\dot{u_1}\," + \
                 "\dot{w_2}+\dot{u_2}\,\dot{w_1}) + G\,\dot{w_1}\,\dot{w_2}}" + \
                 "{\\sqrt{E\,\dot{u_1}^2+2\,F\,\dot{u_1}\,\dot{w_1}+G\,\dot{w_1}^2}" + \
                 "\: \\sqrt{E\,\dot{u_2}^2+2\,F\,\dot{u_2}\,\dot{w_2}+G\,\dot{w_2}^2}}"
            display(Math(txt))	
            txt = "x_u,\:x_w,\,...\: -\:\mathrm{Ableitungen\: von}\:\: x(u,w)\:\mathrm{nach}\:\:u,\:w,\:..."
            display(Math(txt))	
            txt = "\dot{u},\:\dot{u_1},\,...\: -\:\mathrm{Ableitungen\: von}\: \:u(t),\:u_1(t),\:" + \
                 "...\:\:\mathrm{nach}\:t"
            display(Math(txt))	
            txt = "F_x, ...\: -\:\mathrm{Ableitung\: von} \:F(x,y,z),\:\mathrm{nach}\:\:x,\:..."
            display(Math(txt))	
            txt = "\\vec{x}_P -\:\mathrm{Ortsvektor\: des  \:Punktes\:P\:der\: Fläche;\: " + \
		           "alle\:Ableitungen\: werden\: für\: diesen\: berechnet}"
            display(Math(txt))	
            txt = "k_1,\: k_2\:\: -\:\mathrm{Hauptkrümmungen},\quad R_1,\: R_2\:\:-\:" + \
                  "\mathrm{Hauptkrümmungsradien}"	
            display(Math(txt))

        elif self._typ == 'imp':		
            txt = '\mathrm{Berechnungsgrundlage}\quad \mathrm{Implizite\:Gleichung}\:\: F(x,y,z)=0' 
            display(Math(txt))		
            txt = "\mathrm{Tangentialebene} \quad\quad\quad\quad\:\: " + \
			       "(\\vec{x}-\\vec{x}_P) \\circ " + \
                 '\\left(\\begin{matrix}F_x\\\\F_y\\\\F_z\\end{matrix} \\right) =0'
            display(Math(txt))
            txt = "\mathrm{Normaleneinheitsvektor}\quad\:\:\:"	+ \
                  "\\frac{1}{\\sqrt{F_x^2+F_y^2+F_z^2}}" + \
			        '\\left(\\begin{matrix}F_x\\\\F_y\\\\F_z\\end{matrix} \\right)'			
            display(Math(txt))	
            txt = "F_x, ...\: -\:\mathrm{Ableitungen\: von} \:F(x,y,z),\:nach\:\:x,\:..."
            display(Math(txt))	
            txt = "\\vec{x}_P -\:\mathrm{Ortsvektor\: des  \:Punktes\:P\:der\: Fläche;\: " + \
		           "die\:Ableitungen\: werden\: für\: diesen\: berechnet}"
            display(Math(txt))	
			
        print(' ')
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Flächenschar\n")		
            print("Aufruf   fläche . sch_el( wert )\n")		                     
            print("             fläche    Fläche")
            print("             wert      Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print("agla: für Scharparameter Zahl oder freien Parameter angeben")
            return
        if self._typ == 'imp':
            gl = self.imp
            gl = (gl.lhs - gl.rhs).subs(p, wert)
            gl = str(gl) + "= 0"
            return Flaeche(gl)
        else:
            ap = self.args[0]
            ap = ap.subs(p, wert)
            ber1, ber2 = self.ber[0], self.ber[1]
            ber11 = ber1[0].subs(p, wert)
            ber12 = ber1[1].subs(p, wert)
            ber21 = ber2[0].subs(p, wert)
            ber22 = ber2[1].subs(p, wert)
            return Flaeche(ap, (self.par[0], ber11, ber12), (self.par[1], 
                                                              ber21, ber22))
    schEl = sch_el														  
		
		
    def pkt(self, *wert, **kwargs):
        """Flächenpunkt"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
		 
        if kwargs.get('h'):
            print("\nPunkt der (parametrisierten) Fläche\n")		
            print("Aufruf     fläche . pkt( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           zugehöriger Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:")
            print("           allgemeiner Punkt der Fläche\n") 			
            return 
			
        pkt = self.args[0]
        if len(wert) == 0:
            return pkt
        par1, par2 = self.par
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")
                return	
            try:				 
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:		
                pass			 
            return  pkt.subs(par1, u_wert).subs(par2, w_wert)			 
        print("agla: zwei Parameterwerte angeben")
        return		
		
		
    def tang_vekt(self, *wert, **kwargs):
        """Tangentenvektoren"""
		 
        if kwargs.get('h'):
            print("\nTangentenvektoren der (parametrisierten) Fläche\n")		
            print("Aufruf     fläche . tang_vekt( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Tangentenvektoren in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Tangentenvektoren im allgemeinen Punkt der Fläche\n") 			
            print("Bei Erzeugung der Fläche mittels impliziter Gleichung:\n")			
            print("Aufruf     fläche . tang_vekt( punkt )\n")		                     
            print("               punkt     Punkt der Fläche\n")	
            print("Rückgabe   Tangentenvektoren im angegebenen Punkt\n") 
            return 
			
        if self._typ == 'imp':
            if len(wert) == 0:
                print("agla: Punkt der Fläche angeben")
                return				            			
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 3):
                print("agla: Punkt der Fläche angeben")
                return				
            f = self.imp.lhs - self.imp.rhs
            x, y, z = Symbol('x'), Symbol('y'), Symbol('z')			
            if f.subs({x:p.x, y:p.y, z:p.z}) != 0:
                print("agla: Punkt der Fläche angeben")		
                return				
            te = self.tang_ebene(p)
        else:
            if len(wert) == 0:
                te = self.tang_ebene()
            elif len(wert) == 2:
                u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
                if not is_zahl(u_wert) and is_zahl(w_wert):
                    print("agla: zwei Zahlenwerte angeben")
                    return
                try:				 
                    u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
                except RecursionError:
                    pass	
                te = self.tang_ebene(u_wert, w_wert)
            else:			
                print("agla: zwei Parameterwerte angeben")
                return		
        		
        return te.richt			
		
    tangVekt = tang_vekt		
		
	
    def norm(self, *wert, **kwargs):
        """Normalenvektor"""
		 
        if kwargs.get('h'):
            print("\nNormalenvektor der Fläche\n")
            print("Bei parametrisierten Flächen:\n")			
            print("Aufruf     fläche . norm( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Normalenvektor in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Normalenvektor im allgemeinen Punkt der Fläche\n") 
            print("Bei Erzeugung der Fläche mittels impliziter Gleichung:\n")			
            print("Aufruf     fläche . norm( punkt )")		                     
            print("               punkt     Punkt der Fläche\n")	
            print("Rückgabe   Normalenvektor im angegebenen Punkt\n") 
            return 	
			
        if self._typ == 'imp':
            if len(wert) == 0:
                print("agla: Punkt der Fläche angeben")
                return				            			
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 3):
                print("agla: Punkt der Fläche angeben")
                return				
            f = self.imp.lhs - self.imp.rhs
            x, y, z = Symbol('x'), Symbol('y'), Symbol('z')			
            if f.subs({x:p.x, y:p.y, z:p.z}) != 0:
                print("agla: Punkt der Fläche angeben")		
                return				
            try:		
                fsx = f.diff(x).subs(x, p.x).subs(y, p.y).subs(z, p.z)
                fsy = f.diff(y).subs(x, p.x).subs(y, p.y).subs(z, p.z)
                fsz = f.diff(z).subs(x, p.x).subs(y, p.y).subs(z, p.z)
                fs = Vektor(fsx, fsy, fsz)				
            except ValueError:
                return None
            if fs != Vektor(0, 0, 0):
                return einfach(fs)
            else:
                ig = self.imp		
                if not ig is None:
                    ff = Flaeche(str(ig.lhs) + '=' + str(ig.rhs))
                    p = self.pkt(u_wert, w_wert)
                    return einfach(ff.norm(p))				
                return None			
						
        par1, par2 = self.par			
        t1, t2 = self.tang_vekt(par1, par2)
        if t1 is None or t2 is None:
            return None		

        if len(wert) == 0:
            return einfach(t1.vp(t2))
        if len(wert) == 2:
             u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
             if not is_zahl(u_wert) and is_zahl(w_wert):
                 print("agla: zwei Zahlenwerte angeben")
                 return		
             try:				 
                 u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
             except RecursionError:
                 pass			 
             t1 = t1.subs(par1, u_wert).subs(par2, w_wert)
             t2 = t2.subs(par1, u_wert).subs(par2, w_wert)             
             nn = t1.vp(t2)
             if nn != Vektor(0, 0, 0):
                 return einfach(nn)
             else:				
                 ig = self.imp			
                 if not ig is None:
                     ff = Flaeche(str(ig.lhs) + '=' + str(ig.rhs))
                     p = self.pkt(u_wert, w_wert)
                     return einfach(ff.norm(p))				
                 return None		
        print("agla: zwei Parameterwerte angeben")
        return		
		
		
    def drei_bein(self, *wert, **kwargs):
        """Begleitendes Dreibein"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
					 
        if kwargs.get('h'):
            print("\nBegleitendes Dreibein der (parametrisierten) Fläche\n")
            print("Aufruf       fläche . drei_bein( /[ u_wert, w_wert ] )\n")		                     
            print("                 fläche    Fläche")
            print("                 wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   ( zwei Tangenteneinheitsvektoren,") 
            print("             Normaleneinheitsvektor )\n")  
            print("             bei Angabe von zwei Parameterwerten:") 
            print("             Dreibein in einem bestimmten Punkt der Fläche")
            print("             bei leerer Argumentliste oder freien Bezeichnern:") 
            print("             Dreibein im allgemeinen Punkt der Fläche\n") 
            return 
			
        par1, par2 = self.par			
        tt = self.tang_vekt(par1, par2)
        t1, t2, n = tt[0], tt[1], self.norm(par1, par2)
        if t1 is None or t2 is None or n is None:
            return None
        t1, t2, n = t1.einh_vekt.einfach, t2.einh_vekt.einfach, \
                   n.einh_vekt.einfach
        if len(wert) == 0:
            return t1, t2, n
        if len(wert) == 2:
             u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
             if not is_zahl(u_wert) and is_zahl(w_wert):
                 print("agla: zwei Zahlenwerte angeben")
                 return
             try:				 
                 u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
             except RecursionError:
                 pass			 
             t1 = t1.subs(par1, u_wert).subs(par2, w_wert).einfach
             t2 = t2.subs(par1, u_wert).subs(par2, w_wert).einfach             
             n = n.subs(par1, u_wert).subs(par2, w_wert).einfach             
             return t1, t2, n			 
        print("agla: zwei Parameterwerte angeben")
        return		
		
    dreiBein = drei_bein	
				
			
    def tang_ebene(self, *wert, **kwargs):
        """Tangentialebene"""
		 
        if kwargs.get('h'):
            print("\nTangentialebene der Fläche\n")
            print("Bei parametrisierten Flächen:\n")			
            print("Aufruf     fläche . tang_ebene( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Tangentialebene in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Tangentialebene im allgemeinen Punkt der Fläche\n") 
            print("Bei Erzeugung der Fläche mittels impliziter Gleichung:\n")			
            print("Aufruf     fläche . tang_ebene( punkt )\n")		                     
            print("               punkt     Punkt der Fläche\n")	
            print("Rückgabe   Tangentialebene im angegebenen Punkt\n") 
            return 
			
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')						
        if self._typ == 'imp':
            txt = "agla: einen Punkt der Fläche angeben"		
            if len(wert) != 1:
                print(txt)
                return				
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 3):			
                print(txt)
                return
            gl = self.imp.lhs - self.imp.rhs
            if gl.subs({x:p.x, y:p.y, z:p.z}) != 0:			
                print(txt)		
                return				
            n = self.norm(p)
            if n is None:
                return None
            else:
                return Ebene(p, n)

        u, w = self.par
        p = self.pkt(u, w)
        try:		
            pu, pw = p.diff(u), p.diff(w)
        except:
            return None
		
        v1 = Vektor(x - p.x, pu.x, pw.x)
        v2 = Vektor(y - p.y, pu.y, pw.y)
        v3 = Vektor(z - p.z, pu.z, pw.z)
        m = Matrix(v1, v2, v3)
        gl = m.D
        po = gl.as_poly(x, y ,z)
        di = po.as_dict()
        try:		
            k0 = di[0,0,0]
        except KeyError:
            k0 = 0		 
        try:		
            kx = di[1,0,0]
        except KeyError:
            kx = 0		 
        try:		
            ky = di[0,1,0]
        except KeyError:
            ky = 0		 
        try:		
            kz = di[0,0,1]
        except KeyError:
            kz = 0	
			
        r, s = Symbol('r'), Symbol('s')        
        if len(wert) == 0:
            return Ebene(kx, ky, kz, k0, r, s)
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")
                return			
            try:				
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:
                pass
            typ = (int, Integer, float, Float, Rational)
            koeff = [kx, ky, kz, k0]
            koeff1 = []			
            for el in koeff:
                if not isinstance(el, typ):
                    el1 = el.subs(u, u_wert).subs(w, w_wert)
                else:
                    el1 = el								
                koeff1 += [el1]				   
            if all([el == 0 for el in (kx, ky, kz, k0)]):
                ig = self.imp			
                if not ig is None:
                    ff = Flaeche(str(ig.lhs) + '=' + str(ig.rhs))
                    p = self.pkt(u_wert, w_wert)
                    return ff.tang_ebene(p)				
                return None			
            return Ebene(*koeff1, r, s)
        print("agla: zwei Parameterwerte angeben")
        return		
		
    tangEbene = tang_ebene
	
		
    def fund_form1(self, *wert, **kwargs):
        """1. Fundamentalform"""

        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite  Gleichung)')					
            return
					
        if kwargs.get('h'):
            print("\n1. Fundamentalform der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . fund_form1( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Koeffizienten der 1. Fundamentalform im zugehörigen Punkt") 
            print("           der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Koeffizienten der 1. Fundamentalform im allgemeinen Punkt")
            print("           der Fläche\n")
            print("Zusatz     d=1   Dezimaldarstellung") 
            print("           df=1  Darstellung in Differentialen") 
            print("           m=1   Matrix-Darstellung\n") 
            return 
			
        u, w = self.par			
        du, dw = symbols('du dw')
        p = self.pkt(u, w)
        txt = 'agla: die 1. Fundamentalform ist nicht definiert'		
        try:
            pu, pw = p.diff(u), p.diff(w)
        except:
            print('agla: die 1. Fundamentalform ist nicht definiert')		
            return None
		
        ee, ff, gg = pu.sp(pu), pu.sp(pw), pw.sp(pw)
	
        if len(wert) == 0:
            if all([x not in (nan, NaN) for x in (ee, ff, gg)]):	
                ee, ff, gg = einfach(ee), einfach(ff), einfach(gg)
                if kwargs.get('d'):
                    return N(ee), N(ff), N(gg)
                if kwargs.get('df'):
                    display(Math(latex(ee*du**2 + 2*ff*du*dw + gg*dw**2)))	
                    return
                if kwargs.get('m'):
                    m = Vektor(ee, ff).kette(Vektor(ff, gg))	
                    return m	
                return ee, ff, gg
            print(txt)            
            return None						
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")
                return	
            try:				 
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:
                pass			 
            ee = ee.subs(u, u_wert).subs(w, w_wert)
            ff = ff.subs(u, u_wert).subs(w, w_wert)             
            gg = gg.subs(u, u_wert).subs(w, w_wert)             
            if all([x not in (nan, NaN) for x in (ee, ff, gg)]):			
                ee, ff, gg = einfach(ee), einfach(ff), einfach(gg)
                if kwargs.get('d'):
                    return N(ee), N(ff), N(gg)
                if kwargs.get('df'):
                    display(Math(latex(ee*du**2 + 2*ff*du*dw + gg*dw**2)))	
                    return
                if kwargs.get('m'):
                    m = Vektor(ee, ff).kette(Vektor(ff, gg))	
                    return m	
                return ee, ff, gg
            print(txt)            
            return None				
        print("agla: zwei Parameterwerte angeben")
        return		
		
    fundForm1 = fund_form1
    ff1 = fund_form1
    I = fund_form1	
	

    def fund_form2(self, *wert, **kwargs):
        """2. Fundamentalform"""

        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
					
        if kwargs.get('h'):
            print("\n2. Fundamentalform der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . fund_form2( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Koeffizienten der 2. Fundamentalform im zugehörigen Punkt") 
            print("           der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Koeffizienten der 2. Fundamentalform im allgemeinen Punkt")
            print("           der Fläche\n")
            print("Zusatz     d=1   Dezimaldarstellung") 
            print("           df=1  Darstellung in Differentialen") 
            print("           m=1   Matrix-Darstellung\n") 
            return 
        		
        u, w = self.par			
        du, dw = symbols('du dw')
        p = self.pkt(u, w)
        txt = 'agla: die 2. Fundamentalform ist nicht definiert'		
        try:
            pu, pw = p.diff(u), p.diff(w)
        except:
            print(txt)		
            return None
			
        r = simplify(p.betrag)
        if not mit_param(r) and 	r > 0:     # explizite Rückgabe für Sphäre
            ll, mm, nn = r, 0, r*cos(u)**2   # wegen unzureichender Vereinfachung
            if kwargs.get('d'):
                return N(ll), N(mm), N(nn)
            if kwargs.get('df'):
                display(Math(latex(ll*du**2 + 2*mm*du*dw + nn*dw**2)))	
                return
            if kwargs.get('m'):
                m = Vektor(ll, mm).kette(Vektor(mm, nn))	
                return m	
            return ll, mm, nn
			
        ee, ff, gg = pu.sp(pu), pu.sp(pw), pw.sp(pw)
        n = sqrt(ee * gg - ff**2)		
        try:
            1/n
        except ZeroDivisionError:			
            print(txt)
            return None		
        try:
            puu = pu.diff(u)			
            puw = pu.diff(w)			
            pww = pw.diff(w)			
            mat_l = Matrix( Vektor(puu.x, pu.x, pw.x), Vektor(puu.y, pu.y, pw.y),
                   Vektor(puu.z, pu.z, pw.z) ) 
            ll = mat_l.D / n
            mat_m = Matrix( Vektor(puw.x, pu.x, pw.x), Vektor(puw.y, pu.y, pw.y),
                   Vektor(puw.z, pu.z, pw.z) )
            mm = mat_m.D / n
            mat_n = Matrix( Vektor(pww.x, pu.x, pw.x), Vektor(pww.y, pu.y, pw.y),
                   Vektor(pww.z, pu.z, pw.z) )
            nn = mat_n.D / n			
        except:
            print(txt)		
            return None
        if len(wert) == 0:
            if all([x not in (nan, NaN) for x in (ll, mm, nn)]):
                ll, mm, nn = simplify(ll), simplify(mm), simplify(nn)
                if kwargs.get('d'):
                    return N(ll), N(mm), N(nn)
                if kwargs.get('df'):
                    display(Math(latex(ll*du**2 + 2*mm*du*dw + nn*dw**2)))	
                    return
                if kwargs.get('m'):
                    m = Vektor(ll, mm).kette(Vektor(mm, nn))	
                    return m	
                return ll, mm, nn
            print(txt)            
            return None				
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")
                return	
            try:				
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:
                pass			
            ll = ll.subs(u, u_wert).subs(w, w_wert)
            mm = mm.subs(u, u_wert).subs(w, w_wert)             
            nn = nn.subs(u, u_wert).subs(w, w_wert)
            if all([x not in (nan, NaN) for x in (ll, mm, nn)]):
                ll, mm, nn = simplify(ll), simplify(mm), simplify(nn)
                if kwargs.get('d'):
                    return N(ll), N(mm), N(nn)
                if kwargs.get('df'):
                    display(Math(latex(ll*du**2 + 2*mm*du*dw + nn*dw**2)))	
                    return
                if kwargs.get('m'):
                    m = Vektor(ll, mm).kette(Vektor(mm, nn))	
                    return m	
                return ll, mm, nn
            print(txt)            
            return None				
        print("agla: zwei Parameterwerte angeben")
        return		
	
    fundForm2 = fund_form2		
    ff2 = fund_form2		
    II = fund_form2	
	
    def gauss_kruemm(self, *wert, **kwargs):
        """Gauß'sche Krümmung"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if kwargs.get('h'):
            print("\nGauß'sche Krümmung der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . gauss_krümm( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Gauß-Krümmung in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Gauß-Krümmung im allgemeinen Punkt der Fläche\n") 
            print("Synonymer Bezeichner:  K\n")
            print("Zusatz     d=1   Dezimaldarstellung\n")
            return 

        u, w = self.par
        ff1 = self.fund_form1(u, w)
        ff2 = self.fund_form2(u, w)
        if ff1 is None or ff2 is None:
            return None
        ee, ff, gg = ff1
        ll, mm, nn = ff2
        n = ee * gg - ff**2
        if n == 0:
            return None
			
        K = (ll * nn - mm**2) / n
		        
        if len(wert) == 0:
            if mit_param(K):
                return K
            if kwargs.get('d'):
                return float(K)
            return K
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")	
                return
            try:				
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:
                pass			
            try:
                K = K.subs(u, u_wert).subs(w, w_wert)
            except:
                return None
            if mit_param(K):
                return K
            if kwargs.get('d'):
                return float(K)
            return K
        print("agla: zwei Parameterwerte angeben")
        return		
	
    K = k = gauss_kruemm
    gaussKruemm = gauss_kruemm
	
	
    def mitt_kruemm(self, *wert, **kwargs):
        """Mittlere Krümmung"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if kwargs.get('h'):
            print("\nMittlere Krümmung der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . mitt_krümm( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Mittlere Krümmung in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Mittlere Krümmung im allgemeinen Punkt der Fläche\n") 
            print("Synonymer Bezeichner:  H\n")
            print("Zusatz     d=1   Dezimaldarstellung\n")
            return 
			
        u, w = self.par
        ff1 = self.fund_form1(u, w)
        ff2 = self.fund_form2(u, w)
        if ff1 is None or ff2 is None:
            return None
        ee, ff, gg = ff1
        ll, mm, nn = ff2
        n = ee * gg - ff**2
        if n == 0:
            return None
			
        H = (ll * gg - 2 * ff * mm + ee * nn) / (2 * n)

        if len(wert) == 0:
            H = einfach(H)		
            if mit_param(H):
                return H
            if kwargs.get('d'):
                return float(H)
            return H
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")	
                return	
            try:				
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:
                pass			
            try:
                H = H.subs(u, u_wert).subs(w, w_wert)
            except:
                return None
            res = einfach(H)
            if mit_param(res):
                return res
            if kwargs.get('d'):
                return float(res)
            return res
        print("agla: zwei Parameterwerte angeben")
        return		
	
    H = hh = mitt_kruemm
    mittKruemm = mitt_kruemm	


    def haupt_kruemm(self, *wert, **kwargs):
        """Hauptkrümmungen"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if kwargs.get('h'):
            print("\nHauptkrümmungen der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . haupt_krümm( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Hauptkrümmungen in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Hauptkrümmungen im allgemeinen Punkt der Fläche\n") 
            print("Synonymer Bezeichner  HK\n")
            print("Zusatz     d=1   Dezimaldarstellung\n")
            return 


        #K = k = self.gauss_kruemm(*wert)
        #H = h = self.mitt_kruemm(*wert)   

		 # Gleichung für die Hauptkrümmungen:  k^2 - 2*H*k + K = 0
		 # schneller als Eigenwerte der Weingarten-Matrix
		 
        #k1, k2 = H + sqrt(H**2 - K), H - sqrt(H**2 - K)  
              
        W = self.weing_matrix()
        k = W.eig_wert
        if isinstance(k, list):
            k1, k2 = k
        else:
            k1 = k2 = k		
        if k1 in (NaN, nan) or k2 in (NaN, nan):
            print('agla: die Hauptkrümmungen sind nicht definiert')
            return None
        k1, k2 = simplify(k1), simplify(k2)			
        if kwargs.get('d'):
            return N(k1), N(k2)
        return k1, k2
			
    HK = hk = haupt_kruemm
    hauptKruemm = haupt_kruemm
	
	
    def haupt_kr_richt(self, *wert, **kwargs):
        """Hauptkrümmungsrichtungen"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if kwargs.get('h'):
            print("\nHauptkrümmungsrichtungen der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . haupt_kr_richt( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Hauptkrümmungsrichtungen in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Hauptkrümmungsrichtungen im allgemeinen Punkt der Fläche\n") 
            print("Synonymer Bezeichner  HKRicht\n")
            print("Zusatz     d=1   Dezimaldarstellung\n")
            return 

        u, w = Symbol('u', real=True), Symbol('w', real=True)
		
        W = self.weing_matrix(u, w)
        txt = 'agla: die Hauptkrümmungsrichtungen sind nicht definiert'
        if not W:
            print(txt)
            return None
			
        ev1, ev2 = W.eig_vekt
        ta = self.tang_vekt(u, w)
        hkr1 = ev1.x*ta[0] + ev1.y*ta[1] 
        hkr2 = ev2.x*ta[0] + ev2.y*ta[1] 
        if len(wert) == 0:
            if mit_param(hkr1) or mit_param(hkr2):
                return hkr1, hkr2
            if kwargs.get('d'):
                return hkr1.dez, hkr2.dez
            return hkr1, hkr2
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")		
                return	
            try:				
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:
                pass			
            hkr1 = hkr1.subs(u, u_wert).subs(w, w_wert).einfach
            hkr2 = hkr2.subs(u, u_wert).subs(w, w_wert).einfach
            if hkr1.betrag * hkr2.betrag == 0:
                p = self.pkt()
                aa = einfach(p.x**2 + p.y**2 + p.z**2)
                if not aa.free_symbols and aa > 0:	  # Bedingung für Kugel	
                    print('jede beliebige Tangentialrichtung, z.B.')				
                    return self.tang_vekt(u_wert, w_wert)
                print(txt)
                return				
            if kwargs.get('d'):
                return hkr1.dez, hkr2.dez
            return hkr1, hkr2
        print("agla: zwei Parameterwerte angeben")
        return		
	
    hauptKrRicht = haupt_kr_richt	
    HKRicht = hkRicht = haupt_kr_richt	
	
	
    def haupt_kr_radius(self, *wert, **kwargs):
        """Hauptkrümmungsradien"""
		 
        if self._typ == 'imp':		 
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
										
        if kwargs.get('h'):
            print("\nHauptkrümmungsradien der Fläche\n")
            print("Bei parametrisierten Flächen:\n")			
            print("Aufruf     fläche . haupt_kr_radius( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Hauptkrümmungsradien in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Hauptkrümmungsradien im allgemeinen Punkt der Fläche\n") 
            print("Synonymer Bezeichner:  HKR\n")
            print("Zusatz     d=1   Dezimaldarstellung\n")
            return 
		            
        if len(wert) not in (0, 2):
            print('agla: zwei Parameterwerte angeben')		
            return
        k = self.haupt_kruemm(*wert)
		
        if k[0] is None or k[1] is None:		
            print('agla: die Hauptkrümmungsradien sind nicht definiert')		
            return
        if k[0] != 0:			
            r1 = 1 / k[0]
        else:
            r1 = oo		
        if k[1] != 0:			
            r2 = 1 / k[1]
        else:
            r2 = oo		
        if kwargs.get('d'):
            return float(r1), float(r2)
        return abs(r1), abs(r2)			
	
    HKR = hkr = haupt_kr_radius	
    hauptKrRadius = haupt_kr_radius
	
	
    def kurve(self, *args, **kwargs):
        """Kurve auf der Fläche"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if kwargs.get('h'):
            print("\nKurve auf der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . kurve( u_fkt, w_fkt, ( par_name, par_unt, par_ob ) )\n")		                     
            print("               fläche     Fläche")
            print("               fkt        Funktion in einem Argument (Parameter)")	
            print("               par_name   Name des Parameters")
            print("               par_unt,   untere und obere Bereichsgrenzen")
            print("               par_ob     des Parameters\n")
            return 
			
        try:			
            if len(args) != 3:
                raise AglaError("drei  Argumente angeben")
            u_fkt = sympify(args[0])
            w_fkt = sympify(args[1])
				
            if not (is_zahl(u_fkt) and is_zahl(w_fkt)):  
                txt = "zwei Funktionensausdrücke (in einem Parameter) angeben"		
                raise AglaError(txt)		
            par = sympify(args[2])
            if not (isinstance(par, (tuple, Tuple, list)) and len(par) == 3):
                raise AglaError("ein Tupel/eine Liste mit drei Parameterangaben eingeben")
            par_name = par[0]
            unt, ob = par[1], par[2]
            if not (isinstance(par_name, Symbol) and is_zahl(unt) and is_zahl(ob)):
                raise AglaError("einen Parameternamen und zwei Zahlenwerte angeben")
            puw = u_fkt.free_symbols.union(w_fkt.free_symbols)
            if not puw:
                raise AglaError("in den Funktionen ist kein Parameter enthalten")
            if not par_name in puw:
                txt = "der Parameter ist nicht in den Funktionen enthalten"
                raise AglaError(txt)
        except AglaError as e:
            print('agla:', str(e))
            return
			
        u, w = self.par
        p = self.pkt(u, w).subs(u, u_fkt).subs(w, w_fkt).einfach
        return Kurve(p, (par_name, unt, ob))
			   

    def weing_matrix(self, *wert, **kwargs):
        """Weingarten-Matrix"""
		 
        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if kwargs.get('h'):
            print("\nWeingarten-Matrix der (parametrisierten) Fläche\n")
            print("Aufruf     fläche . weing_matrix( /[ u_wert, w_wert ] )\n")		                     
            print("               fläche    Fläche")
            print("               wert      Wert eines Flächenparameters\n")	
            print("Rückgabe   bei Angabe von zwei Parameterwerten:") 
            print("           Weingarten-Matrix in einem bestimmten Punkt der Fläche")
            print("           bei leerer Argumentliste oder freien Bezeichnern:") 
            print("           Weingarten-Matrix im allgemeinen Punkt der Fläche\n") 
            return 
         			
        u, w = Symbol('u', real=True), Symbol('w', real=True)
        u_wert, w_wert = u, w
		
        if len(wert) == 2:
            u_wert, w_wert = sympify(wert[0]), sympify(wert[1])
            if not is_zahl(u_wert) and is_zahl(w_wert):
                print("agla: zwei Zahlenwerte angeben")
                return	
            try:				
                u_wert, w_wert = nsimplify(u_wert), nsimplify(w_wert)
            except RecursionError:	
                pass			
		
        ff1 = self.fund_form1(u_wert, w_wert)
        ff2 = self.fund_form2(u_wert, w_wert)
        txt = 'agla: die Weingarten-Matrix ist nicht definiert'		
        if ff1 is None or ff2 is None:
            print(txt)		
            return None
        
        ee, ff, gg = ff1
        ll, mm, nn = ff2
        m1 = Vektor(ee, ff).kette(Vektor(ff, gg))
        m2 = Vektor(ll, mm).kette(Vektor(mm, nn))
        if len(wert) == 0:
            try:
                return m1**(-1) * m2
            except:
                print(txt)		
                return None				
        m11 = m1.vekt[0].subs(u, u_wert).subs(w, w_wert)
        m12 = m1.vekt[1].subs(u, u_wert).subs(w, w_wert)
        m21 = m2.vekt[0].subs(u, u_wert).subs(w, w_wert)
        m22 = m2.vekt[1].subs(u, u_wert).subs(w, w_wert)
        m1 = Matrix(m11, m12)
        m2 = Matrix(m21, m22)

        try:
            m = m1**(-1) * m2
        except:
            print(txt)		
            return None
        return m
        print("agla: zwei Parameterwerte angeben")
		
    weingMatrix = weing_matrix
	
	
    def par_wert(self, *args, **kwargs):
        """Parameterwerte eines Flächenpunktes"""

        if self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')					
            return
			
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
			
        grenze = 10**(-8)
		 
        if kwargs.get('h'):		 
            print("\nParameterwerte eines Punktes der (parametrisierten) Fläche\n")		
            print("Aufruf   fläche . par_wert( punkt, start1, start2 )\n")		                     
            print("             fläche   Fläche")
            print("             punkt    Punkt der Fläche")			
            print("             start    Startwert des nummerischen Verfahrens") 
            print("                      zur Berechnung der Flächenparameter\n")
            print("Die Startwerte für die beiden Flächenparameter sind so genau wie ")
            print("möglich anzugeben; die Parameterwerte werden über die Minimierung")
            print(" des Abstandes, des gegebenen Punktes zu den Flächenpunkten ")
            print("gesucht; es wird 'nsolve' verwendet (siehe SymPy-Dokumentation)\n")	
            return 
		
        if len(args) != 3:
            print("agla: drei Argumente angeben")
            return			
        punkt, start1, start2 = args	
        start1 = sympify(start1)			
        start2 = sympify(start2)	
        if not (isinstance(punkt, Vektor) and punkt.dim == 3 
		   and is_zahl(start1) and is_zahl(start2)):
            print("agla: einen Punkt und zwei Zahlenwerte angeben")
            return			
        if mit_param(punkt):
            print("agla: nicht implementiert (Parameter)")
            return
        start1 = float(start1)		
        start2 = float(start2)			
        u, w = self.par
        def f(u, w):
            q = self.pkt(u, w)
            return punkt.abstand(q)**2
        try:
            gl = [diff(f(u, w), u), diff(f(u, w), w)]
            res = nsolve(gl, [u, w], [start1, start2])	
        except ZeroDivisionError:
            print("agla: mit anderen Startwerten versuchen\n" + \
                 "       die Werte sind eventuell mit nsolve nicht ermittelbar")
            return			
        if f(u, w).subs(u, res[0, 0]).subs(w, res[1, 0]) < grenze:
            try:		
                return nsimplify(res[0,0]), nsimplify(res[1,0])
            except RecursionError:
                return res[0,0], res[1,0]			
        else:
            txt = "mit anderen Startwert versuchen\n" + \
                 "       der Punkt ist eventuell kein Flächenpunkt"
            print("agla: " + txt)
            return			
			
    parWert = par_wert			
	
	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Fläche bei einer Abbildung\n")		
            print("Aufruf   kurve . bild( abb )\n")		                     
            print("             fläche     Fläche")
            print("             abb        Abbildung\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == 3):
            print("agla: Abbildung des Raumes angeben")
            return
        if self._typ == 'prg':			
            p = self.pkt()
            q = p.bild(abb)
            if not self.args[3][2] is None:
                x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
                X, Y, Z = Symbol('X'), Symbol('Y'), Symbol('Z')
                gl = self.imp.subs([(x, X), (y, Y), (z, Z)])
                vv = abb.inverse.matrix * (Vektor(x, y, z) - abb.versch)
                gl1 = gl.subs([(X, vv.x), (Y, vv.y), (Z, vv.z)])				
            else:
                gl1 = None
            if gl1 is None:
                return Flaeche(q, 
                          (self.par[0], self.ber[0][0], self.ber[0][1]), 
			               (self.par[1], self.ber[1][0], self.ber[1][1]))
            return Flaeche(q,  
                          (self.par[0], self.ber[0][0], self.ber[0][1]), 
			               (self.par[1], self.ber[1][0], self.ber[1][1]), 
                         imp = str(gl1.lhs))		
        else:
            x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
            U, V, W = Symbol('U'), Symbol('V'), Symbol('W')			
            gl = self.imp.lhs		
            uvw = abb.matrix.inverse * (Vektor(U, V, W) - abb.versch)
            gl = gl.subs({x:uvw.x, y:uvw.y, z:uvw.z})		
            gl = einfach(gl.subs({U:x, V:y, W:z}))		
            return Flaeche(gl)			
            			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Flaeche"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
					
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Flaeche mit mayavi"""
		
        # 'gitter = ja / (Nu,Nw)' für Flächengitter; N - Anzahl Linien, Standard 12
        # 'punkte = (Nx,Ny,Nz)'  für Anzahl der Stützstellen in x-,y-,z-Richtung
        # 'draht= ja / (Nu,Nw)' für Drahtgitter; N - Anzahl Linien, Standard 12		
				        						
        gitter, punkte, draht = None, None, None			
        if len(spez) > 4:
            for s in spez[4]:
                s.replace(' ', '')
                if 'gitter' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper():				
                        gitter = (18, 18)	
                    else:
                        gitter = eval(s[s.find('=')+1:])                    					
                if 'draht' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper(): # or '1' in s.upper():				
                        draht = (18, 18)
                    else:
                        draht = eval(s[s.find('=')+1:])                    					
                if 'punkte' in s:
                    punkte = eval(s[7:])

        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                      else spez[1]
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' \
                      else spez[1]								
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                        spez[2][1]
        if not isinstance(flaech_farbe, tuple):
            flaech_farbe = hex2color(flaech_farbe)		
        if not isinstance(lin_farbe, tuple):
            lin_farbe = hex2color(lin_farbe)		

        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3][:2]
			     
        abs=np.abs; pi=np.pi; sqrt=np.sqrt; exp=np.exp; log=np.log
        ln=np.log; sin=np.sin; sinh=np.sinh; Abs=np.abs
        arcsin=np.arcsin; arsinh=np.arcsinh; cos=np.cos; cosh=np.cosh
        arccos=np.arccos; arcosh=np.arccosh; tan=np.tan; tanh=np.tanh 
        arctan=np.arctan; artanh=np.arctanh 
        asin=np.arcsin; acos=np.arccos; atan=np.arctan 
        asinh=np.arcsinh; acosh=np.arccosh; atanh=np.arctanh 			
						
        # Anpassung hyperbolische Geometrie						
        if self == HypSchale:
            zo = UMG._sicht_box[-1]  
            if zo <= 1:
                print('agla: die obere Grenze des z-Bereiches muss > 1 sein')	
                return
            ww = sqrt(zo**2-1)
			  
        if not anim:   # ohne Animation
		
            if self._typ == 'prg':	
                u, w = Symbol('u'), Symbol('w')					  
                p = self.pkt(u, w)					  		
                u_ber = self.ber[0]
                if self != HypSchale:				
                    w_ber = self.ber[1]	
                else:
                    w_ber = [-ww, ww]				
                uu, uo =  float(u_ber[0]), float(u_ber[1])		
                wu, wo =  float(w_ber[0]), float(w_ber[1])		
                uo = uo + 0.5 * np.abs(uo - uu) / 101				
                wo = wo + 0.5 * np.abs(wo - wu) / 101				
                plt = []		
                if not draht:	
                    d = 101				
                    u, w = np.mgrid[uu:uo:101j, wu:wo:101j]
                    xs, ys, zs = repr(p.x), repr(p.y), repr(p.z)
                    if xs.find('u') >= 0 or xs.find('w') >= 0:
                        x = eval(xs.replace('Abs', 'np.abs')) 
                    else:
                        x = np.full((101, d), p.x)
                    if ys.find('u') >= 0 or ys.find('w') >= 0:
                        y = eval(ys.replace('Abs', 'np.abs')) 
                    else:
                        y = np.full((101, d), p.y)	
                    if zs.find('u') >= 0 or zs.find('w') >= 0:
                        z = eval(zs.replace('Abs', 'np.abs')) 
                    else:
                        z = np.full(((101, d)), p.z)
                    plt += [mlab.mesh(x, y, z, color=flaech_farbe)]

                Nu, Nw = 12, 12
				
                if gitter or draht:
                    if gitter:
                        linien = gitter
                    else:
                        linien = draht	
                    if not (linien == True or \
                        isinstance(linien, (tuple, Tuple, list))):			
                        print("agla: '' oder Tupel/Liste mit zwei Zahlen angeben")
                        return
                    if isinstance(linien, (tuple, Tuple, list)):
                        if len(linien) != 2 or not \
                           isinstance(linien[0], (Integer, int)) or not \
                           isinstance(linien[1], (Integer, int)):
                            print('agla: zwei ganze Zahlen für die Anzahl der ' +
                                 'Gitterlinien angeben')	
                            return
                        Nu, Nw = linien[0], linien[1]
						
                    from agla.lib.funktionen.graf_funktionen import _many_lines_mayavi
					
                    if gitter:					
                        plt += [ _many_lines_mayavi(self, Symbol('u'), 100, Nu, 
						                color=(0.7, 0.7, 0.7), line_width=1, opacity=0.5),
                                _many_lines_mayavi(self, Symbol('w'), 100, Nw, 
								         color=(0.7, 0.7, 0.7), line_width=1, opacity=0.5) ]											   
                    else:											   
                        plt += [ _many_lines_mayavi(self, Symbol('u'), 100, Nu, 
						                color=lin_farbe, line_width=lin_staerke, opacity=0.8),
                                _many_lines_mayavi(self, Symbol('w'), 100, Nw, 
								         color=lin_farbe, line_width=lin_staerke, opacity=0.8) ]
                return plt
				
            else:   # typ 'imp'
			
                if gitter:
                    print('agla: ein Gitter ist hier nicht implementiert')
                    return
                if not punkte is None:
                    if not (isinstance(punkte, (tuple, Tuple, list)) and \
                        len(punkte)== 3):			
                        print('agla: für punkte Tupel/Liste mit drei ' +
                             'Zahlen angeben')
                        return
                    Nx, Ny, Nz = punkte
                    if not (isinstance(Nx, (int, Integer)) and isinstance(Ny, \
                         (int, Integer)) and isinstance(Nz, (int, Integer))):
                        print('agla: drei ganze Zahlen für Anzahl der ' +
                             'Punkte angeben')
                        return
                    if Nx < 3 or Ny < 3 or Nz < 3:
                        print("agla: Zahlen > 2 angeben")
                        return												
                else:
                    Nx, Ny, Nz = 100, 100, 100
                gl = repr(self.imp.lhs - self.imp.rhs)
                fig = kwargs.get('figure')			
                plt = _implicit_plot(gl, UMG._sicht_box, fig_handle=fig, 
                       Nx=Nx, Ny=Ny, Nz=Nz, col_isurf=flaech_farbe, 
                       col_osurf=flaech_farbe)	
                return plt			
		
        else:   # mit Animation
             
            if anim and (gitter or draht or punkte):  
                return None
				
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20							
            if self._typ == 'prg':	
                b_, u, w = Symbol('b_'), Symbol('u'), Symbol('w')		
                ff = self.sch_el(b_)
                p = ff.pkt(u, w)	
                u_ber = self.ber[0]
                w_ber = self.ber[1]		
                uu, uo =  float(u_ber[0]), float(u_ber[1])		
                vu, vo =  float(w_ber[0]), float(w_ber[1])		
                aa = np.linspace(float(aber[0]), float(aber[1]), N)  		
                u, w = np.mgrid[uu:uo:101j, vu:vo:101j]
                xs, ys, zs = repr(p.x), repr(p.y), repr(p.z)
                xa, ya, za = [], [], []
                for bb in aa:
                    bb = '(' + str(bb) + ')'
                    xa += [eval(xs.replace('b_', bb))]
                    ya += [eval(ys.replace('b_', bb))]
                    za += [eval(zs.replace('b_', bb))]
                plt = mlab.mesh(xa[0], ya[0], za[0], color=flaech_farbe)
                return plt, (xa[1:], ya[1:], za[1:]), N-1				
            else:	   	
                gl = str(self.imp.lhs)
                par = self.sch_par.pop()	
                xl, xr, yl, yr, zl, zr = UMG._sicht_box
                Nx, Ny, Nz = 100, 100, 100   
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
                try:			
                    for cc in aa:	
                        cc = str(cc)			
                        gl0 = gl.replace(par, cc)
                        gl0 = gl0.replace('x', 'xx').replace('y', 'yy').replace('z', 'zz')
                        scalars += [eval(gl0)]
                    return plt, scalars, N-1
                except MemoryError:
                    return AglaError('die Anzahl der Unterteilungen (' + str(N) + ') ist zu groß')				
				
    def vispy(self, spez, **kwargs):
        """Grafikelement für Flaeche mit vispy"""
        pass   		
				

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        if self._typ != 'imp':		
            flaeche_hilfe(3)
            return			
        flaeche_hilfe(4)
		
    h = hilfe		

	
				
# Benutzerhilfe für Flaeche
# -------------------------

def flaeche_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden (parametrisierte Flächen)")
        print("h=4 - Eigenschaften und Methoden (Flächen mit impliziter Gleichung)")
        return
		   
    if h == 2:
        print("\nFläche - Objekt\n")    
        print("Erzeugung im Raum R^3:\n")
        print("             Fläche( par_form, (u_par_name, u_unt, u_ob),")
        print("                               (w_par_name, w_unt, w_ob) )\n")
        print("       oder  Fläche( allg_punkt, (u_par_name, u_unt, u_ob),")
        print("                                 (w_par_name, w_unt, w_ob) )\n")
        print("       oder  Fläche( fkt_gleich /[, (u_par_name, u_unt, u_ob), ")
        print("                                   (w_par_name, w_unt, w_ob) ] )\n")
        print("       oder  Fläche( imp_gleich )\n")
        print("                 par_form     Parameterform der Fläche")  
        print("                 allg_punkt   Vektor (allgemeiner Flächenpunkt)")  
        print("                 fkt_gleich   'z = f(x, y)'      Funktionsgleichung")
        print("                 imp_gleich   'F(x, y, z) = 0'   Implizite Gleichung")
        print("                       oder    F(x, y, z)        ebenso, rechte Seite ") 
        print("                                                 = 0 angenommen")
        print("                               (die Hochkomma sind mitzuschreiben)\n")       
        print("                 par_name      Name eines Flächenparameters")
        print("                                    freier Bezeichner, standardmäßig u ")
        print("                                    und w; v ist nicht zulässig")
        print("                 u_unt, u_ob,  untere und obere Grenzen")  
        print("                 w_unt, w_ob   der Parameterbereiche\n")
        print("                 Die Verwendung der Bezeichner x, y und z ist zwingend\n")		
        print("                 Bei einer Funktionsgleichung wird parametrisiert, wobei ")
        print("                 eventuell mitgeteilte Parameterangaben benutzt werden;") 
        print("                 dabei werden x und y durch die angegebenen Parameter") 
        print("                 ersetzt; wurden keine Parameterangaben gemacht, wird") 
        print("                 (u, -10, 10),  (w, -10, 10) verwendet\n")
        print("                 Für die Parameterangaben kann statt eines Tupels eine")
        print("                 Liste benutzt werden\n")
        print("Sollen weitere Gleichungen einer Fläche mit gespeichert werden, sind sie ")
        print("über Schlüsselwortparameter mitzuteilen, wobei nur die rechte bzw. linke ")
        print("Seite der jeweiligen Gleichung geschrieben wird")		
        print("   prg = (...) oder v(...)   Parameterform bzw. allgemeiner Flächenpunkt")
        print("   fkt = f(x, y)     Funktionsgleichung (rechte Seite)")		
        print("   imp = F(x, y, z)  Implizite Gleichung (linke Seite)")   
        print("Es wird nicht geprüft, ob diese Gleichungen zu der erzeugten Fläche gehören\n")		
        print("Zuweisung     f = Fläche(...)   (f - freier Bezeichner)\n")
        print("Beispiele\n")
        print("Fläche(v(5*sin(u)*cos(w), 5*sin(u)*sin(w), 5*cos(u)), (u, 0, pi), (w, 0, 2*pi))\n")  
        print("Fläche( (5*sin(u)*cos(w), 5*sin(u)*sin(w), 5*cos(u)), (u, 0, pi), (w, 0, 2*pi),")
        print("        imp='x^2 + y^2 + z^2 - 25' )\n")  
        print("Fläche(v(u, w, u^2 - w^2), (u, -3, 3), (w, -3, 3))\n")  
        print("Fläche('z = 1/2 * (x^2 - y^2)')\n")
        print("Vordefinierte Flächen")
        print("EinhSphäre    Einheitssphäre")
        print("HypSchale     Obere Hälfte des Zweischaligen Hyperboloids")
        print("Sphäre(mitte, radius)        Sphäre / Kugeloberfläche")		
        print("     mitte    Mittelpunkt")
        print("     radius   Radius")	
        print("KugelOberFläche = Sphäre\n")		
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für parametrisierte Flächen\n")
        print("f.hilfe                   Bezeichner der Eigenschaften und Methoden")
        print("f.ber                     Parameterbereiche")
        print("f.bild(...)            M  Bild bei einer Abbildung")
        print("f.dim                     Dimension") 
        print("f.drei_bein(...)       M  Begleitendes Dreibein")
        print("f.fkt                     Funktionsgleichung (falls angegeben)")
        print("f.fund_form1(...)      M  1. Fundamentalform")
        print("f.fund_form2(...)      M  2. Fundamentalform")
        print("f.gauß_krümm(...)      M  Gaußsche Krümmung")
        print("f.H(...)               M  = f.mitt_krümm(...)")
        print("f.haupt_kr_radius(...) M  Hauptkrümmungsradius")
        print("f.haupt_kr_richt(...)  M  Hauptkrümmungsrichtung")
        print("f.haupt_krümm(...)     M  Hauptkrümmungen")
        print("f.HK(...)              M  = f.haupt_krümm(...)")
        print("f.HKR(...)             M  = f.haupt_kr_radius(...)")
        print("f.HKRicht(...)         M  = f.haupt_kr_richt(...)")
        print("f.imp                     Implizite Gleichung (falls angegeben)")
        print("f.is_schar                Test auf Schar")
        print("f.K(...)               M  = f.gauß_krümm(...)")
        print("f.kurve(...)           M  Kurve auf der Fläche")
        print("f.mitt_krümm(...)      M  Mittlere Krümmung")
        print("f.norm(...)            M  Normalenvektor")
        print("f.par                     Parameter der Fläche")
        print("f.par_wert(...)        M  Param.werte eines Flächenpunktes")
        print("f.pf                      Parameterform")    
        print("f.pkt(...)             M  Flächenpunkt")
        print("f.prg                     Parametergleichung")
        print("f.sch_el(...)          M  Element einer Schar")
        print("f.sch_par                 Parameter einer Schar")
        print("f.tang_ebene(...)      M  Tangentialebene")
        print("f.tang_vekt(...)       M  Tangentenvektoren")
        print("f.weing_matrix(...)    M  Weingarten-Matrix\n")
        print("Synonyme Bezeichner\n")
        print("hilfe           :  h")
        print("drei_bein       :  dreiBein")
        print("fund_form1      :  fundForm1")
        print("fund_form1      :  ff1")
        print("fund_form1      :  I")
        print("fund_form2      :  fundForm2")		
        print("fund_form2      :  ff2")		
        print("fund_form2      :  II")		
        print("gauß_krümm      :  gaußKrümm")
        print("H               :  hh")  # h ist besetzt
        print("haupt_kr_radius :  hauptKrRadius")
        print("haupt_kr_richt  :  hauptKrRicht")
        print("haupt_krümm     :  hauptKrümm")
        print("HK              :  hk")
        print("HKR             :  hkr")
        print("HKRicht         :  hkRicht")
        print("is_schar        :  isSchar")
        print("K               :  k")
        print("mitt_krümm      :  mittKrümm")
        print("par_wert        :  parWert")
        print("sch_el          :  schEl")
        print("sch_par         :  schPar")
        print("tang_ebene      :  tangEbene")
        print("tang_vekt       :  tangVekt")
        print("weing_matrix    :  weingMatrix\n")
        return
   
    if h == 4:   
        print("\nEigenschaften und Methoden (M) für Flächen, die mittels impliziter")		
        print("Gleichung erzeugt wurden\n")		
        print("f.hilfe                   Bezeichner der Eigenschaften und Methoden")
        print("f.bild(...)            M  Bild bei einer Abbildung")
        print("f.dim                     Dimension") 
        print("f.fkt                     Funktionsgleichung")
        print("f.imp                     Implizite Gleichung")
        print("f.is_schar                Test auf Schar")
        print("f.norm(...)            M  Normalenvektor")
        print("f.pf                      Parameterform")    
        print("f.prg                     Parametergleichung")
        print("f.sch_el(...)          M  Element einer Schar")
        print("f.sch_par                 Parameter einer Schar")
        print("f.tang_ebene(...)      M  Tangentialebene")
        print("f.tang_vekt(...)       M  Tangentenvektoren\n")
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("is_schar   :  isSchar")
        print("sch_el     :  schEl")
        print("sch_par    :  schPar")
        print("tang_ebene :  tangEbene")
        print("tang_vekt  :  tangVekt\n")
        return           


# Vordefinierte Flächen
u, w, x, y, z = symbols('u w x y z')
def Sphaere(*args, **kwargs):
    if kwargs.get('h'):
        print("\nSphäre   (Fläche - Objekt)\n")    
        print("Erzeugung im Raum R^3:\n")
        print("             Sphäre( mitte, radius )\n")
        print("                 mitte    Mittelpunkt")
        print("                 radius   Radius\n")
        return 
    if len(args) != 2:
        print('agla : zwei Argumente angeben')
        return		
    M, r = args		
    if not (isinstance(M, Vektor) and M.dim == 3):
        print('agla : für den Mittelpunkt einen Punkt im R^3 angeben')
        return		
    if not mit_param(r):
        if not (is_zahl(r) and r > 0):
            print('agla : für den Radius eine positive Zahl angeben')
            return	
    u, w = symbols('u w')		
    P = M + r * Vektor(cos(w)*cos(u), cos(w)*sin(u), sin(w))
    imp = (x - M.x)**2 + (y - M.y)**2 + (z - M.z)**2 - r**2	
    return Flaeche(P, (u, 0, 2*pi), (w, -pi/2, pi/2), 
             imp=str(imp))	
					 
KugelOberFlaeche = Sphaere					 
					 
EinhSphaere = Sphaere(Vektor(0, 0, 0), 1)
					 
HypSchale = Flaeche(Vektor(w*cos(u), w*sin(u), sqrt(1+w**2)), 
                  (u, 0, 2*pi), 
                  (w, 0, 10),
                   imp='x**2 + y**2 - z**2 + 1')		
				
   
	