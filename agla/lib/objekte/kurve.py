#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Kurve - Klasse  von agla           
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



import math
import importlib

import numpy as np
from agla.lib.objekte.umgebung import UMG	

if UMG.grafik_3d == 'mayavi':						
    from mayavi import mlab	
else:
    from vispy import app, scene
    from vispy.scene import visuals
    from vispy.geometry import create_arrow
    from vispy.scene import STTransform, AffineTransform, ChainTransform
import matplotlib.pyplot as plt

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.simplify import nsimplify
from sympy.core.symbol import Symbol, symbols
from sympy.core.numbers import Integer, Float, Rational, pi
from sympy import N
from sympy.polys.polytools import Poly
from sympy.solvers.solvers import nsolve
from sympy.integrals.integrals import integrate
from sympy.core.function import diff, expand
from sympy.printing import latex
from sympy.functions.elementary.miscellaneous import sqrt
from sympy import (sin, cos, tan, exp, log, sinh, cosh, tanh, asin, 
     acos, atan, asinh, acosh, atanh, re, im)
	 	 
from agla.lib.funktionen.funktionen import (sing, cosg, tang, arcsin, arccos,
    arctan, arcsing, asing, arccosg, acosg, arctang, atang, ln, lg, arsinh, 
    arcosh, artanh, abs, determinante)	

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor, X
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene, xy_ebene, xz_ebene, yz_ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.matrix import Matrix
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, einfach, 
    parallel, identisch, Gleichung, ja, Ja, nein, Nein, mit, ohne) 
from agla.lib.funktionen.graf_funktionen import rgb2hex
import agla



# Kurve - Klasse   
# --------------

class Kurve(AglaObjekt):                                      
    """
	
Kurve im Raum und in der Ebene

**Erzeugung im Raum und in der Ebene** 

   Kurve ( *par_form, (par_name, par_unt, par_ob)* )
 
   *oder*
   
   Kurve ( *allg_punkt, (par_name, par_unt, par_ob)* )
		
**Erzeugung nur in der Ebene** 

   Kurve ( *gleichung /[, (par_name, par_unt, par_ob)]* )   
   
**Parameter**
  
   *par_form* :     Parameterform der Kurve
	  
   *allg_punkt* :   allgemeiner Kurvenpunkt
	  
   *par_name* :     Name des Kurvenparameters; freier Bezeichner; Standard *t*
	  
   *par_unt, par_ob* :      untere, obere Grenzen des Parameterbereiches
	  
   *gleichung* : gleichung kann sein (die Hochkomma sind mitzuschreiben)
	  
   * '*y = f(x)* '     Funktionsgleichung   (1)
      *x, y* - kartesische Koordinaten
			
   * '*r = f(phi)* '   Gleichung in Polarkoordinaten   (2)	
      *r, phi* - Polarkoordinaten  

   * '*F(x, y) = 0* '  Implizite Gleichung    *oder*

   * *F(x, y)*        ebenso, rechte Seite = 0 angenommen
	   
   Die Verwendung der Bezeichner *x* und *y* bzw. *r* und *phi* ist 
   zwingend
	  
   Bei (1) wird parametrisiert,wobei eventuell mitgeteilte Parameterangaben 
   benutzt werden; bei Fehlen derselben wird (*t, -10, 10*) verwendet	
	  
   Bei (2) wird automatisch in kartesische Koordinaten transformiert, *phi* 
   wird durch den angegebenen Parameter ersezt; bei Fehlen von 
   Parameterangaben wird wie bei (1) verfahren
		
   Für die Parameterangaben kann statt eines Tupels eine  Liste benutzt 
   werden

   Sollen weitere Gleichungen einer Kurve in der Ebene mit gespeichert werden, 
   sind sie über Schlüsselwortparameter mitzuteilen, wobei nur die rechte bzw. 
   linke Seite der jeweiligen Gleichung geschrieben wird
   
   - *prg = (...)* oder *v(...)*   Parameterform bzw. allgemeiner 
      Kurvenpunkt
	  
   - *fkt = f(x)*      - Funktionsgleichung (rechte Seite)
	  
   - *pol = f(phi)*    - Gleichung in Polarkoordinaten (rechte Seite)
	  
   - *imp = F(x, y)*   - Implizite Gleichung (linke Seite; rechte Seite = 0 
     angenommen)
	  
   Es wird nicht geprüft, ob diese Gleichungen zu der erzeugten Kurve gehören		
   
    """
	
	
    def __new__(cls, *args, **kwargs):  
						
        if kwargs.get("h") in range(1, 5):                         
            kurve_hilfe(kwargs["h"])		
            return	
		
        x, y = symbols('x y')		
        try:
		
            if not args:
                raise AglaError('ein oder zwei Argumente angeben')
            aa = args[0]	
            saa = str(aa).replace(' ', '')
            if len(args) > 1:		
                par_angabe = args[1]		
                if not isinstance(par_angabe, (tuple, Tuple)):
                    raise AglaError("das 2. Argument muss ein Tupel mit Parameterangaben sein")				
                if len(par_angabe) != 3:
                    raise AglaError("ein Parametertupel nuss drei Angaben enthalten")
                par_name, unt, ob = par_angabe
                unt, ob = sympify(unt), sympify(ob)
                if not isinstance(par_name, Symbol):
                    raise AglaError("der Parametername ist nicht frei")
                if not is_zahl(unt) or not is_zahl(ob):
                    txt = "für Bereichsgrenzen zwei Zahlenwerte angeben"
                    raise AglaError(txt)
                if not unt < ob:
                    raise AglaError('es muss untere < obere Grenze sein')	
                try:					
                    unt, ob = nsimplify(unt), nsimplify(ob)
                except RecursionError:	
                    pass	
            else:
                par_name, unt, ob = Symbol('t'), -10, 10   # defaults			
		
            # Erzeugen einer Raumkurve
			
            if (isinstance(aa, Vektor) and aa.dim == 3) or \
               (isinstance(aa, (tuple, Tuple)) and len(aa) == 3):
                if not len(args) == 2:    
                    raise AglaError("zwei Argumente angeben")
                allg_punkt = aa
                par_angabe = args[1]				
                if isinstance(allg_punkt, (tuple, Tuple)):
                    allg_punkt = Vektor(*allg_punkt)
                if not isinstance(par_angabe, (tuple, Tuple)):
                    raise AglaError("das 2. Argument muss ein Tupel mit Parameterangaben sein")
                if len(par_angabe) != 3:
                    raise AglaError("ein Parametertupel nuss drei Angaben enthalten")
                par_name, unt, ob = par_angabe
                unt, ob = sympify(unt), sympify(ob)
                if not allg_punkt.free_symbols:
                    txt = "im allgemeinen Punkt ist kein Parameter enthalten"
                    raise AglaError(txt)
                if not isinstance(par_name, Symbol):
                    raise AglaError("der Parametername ist nicht frei")
                if not par_name in allg_punkt.free_symbols:
                    txt = "der Parameter ist nicht in der Kurvengleichung enthalten"
                    raise AglaError(txt)
                if not is_zahl(unt) or not is_zahl(ob):
                    txt = "für Bereichsgrenzen zwei Zahlenwerte angeben"
                    raise AglaError(txt)
                if not unt < ob:
                    raise AglaError('es muss untere < obere Grenze sein')	
                try:					
                    unt, ob = nsimplify(unt), nsimplify(ob)
                except RecursionError:	
                    pass	
					
                if not allg_punkt.free_symbols.difference({par_name}):				
                    txt = 'der allgemeine Punkt ist nicht im gesamten Parameterbereich' + \
                         '\n      definiert'					
                    try:
                        pu = allg_punkt.subs(par_name, unt)				
                        po = allg_punkt.subs(par_name, ob)
                        if any([not k.is_real for k in pu.komp]) or \
                             any([not k.is_real for k in po.komp]):
                             raise AglaError(txt)	                    					   
                    except Exception:					
                        raise AglaError(txt)	
           				
                return AglaObjekt.__new__(cls, allg_punkt, 
			                                        (par_name, unt, ob))								
            else:
			
                # Erzeugen einer ebenen Kurve 
				
                # Auswerten der Schlüsselwortparameter 
				
                x, y, r, phi = Symbol('x'), Symbol('y'), Symbol('r'), \
                              Symbol('phi')					
                prg, fkt, pol, imp = [None] * 4
                if kwargs.get('prg'):
                    prg = kwargs.get('prg')
                    if not isinstance(prg, (Vektor, tuple, Tuple)):
                        raise AglaError('die Parametergleichung ist ' + \
                                   'falsch angegeben')	
                    if isinstance(prg, (tuple, Tuple)):
                        if len(prg) == 2 and is_zahl(prg[0]) and is_zahl(prg[1]):		
                            prg = Vektor(prg[0], prg[1])
                        else:
                            prg = Vektor(0, 0)						
                    if prg.dim != 2 or not mit_param(prg):
                        raise AglaError('die Parametergleichung ist ' + \
                              'falsch angegeben')	
                    prg = Gleichung(Vektor(x, y), prg)						
                if kwargs.get('fkt'):
                    fkt = kwargs.get('fkt')
                    if not isinstance(fkt, str):
                        fkt = str(fkt)					
                    if fkt.find('=') >= 0:						
                        raise AglaError('hier keine Gleichung, sondern ' + \
                              'einen Ausdruck angeben')	
                    if fkt.find('x') < 0 or fkt.find('y') >= 0: 
                        raise AglaError("einen Ausdruck in 'x' " + \
                             "angeben")
                    ende = False
                    while not ende:					
                        try:	
                            egl = sympify(fkt)
                            ende = True							
                        except NameError as e:
                            es = str(e)
                            par = es[es.find("'")+1:es.rfind("'")]					
                            locals()[par] = Symbol(par)						
                    fkt = Gleichung(y, egl)                    					
                if kwargs.get('pol'):
                    pol = kwargs.get('pol')
                    if not isinstance(pol, str):
                        pol = str(pol)
                    if pol.find('=') >= 0:						
                        raise AglaError('hier keine Gleichung, ' + \
                              'sondern einen Ausdruck angeben')	
                    if pol.find('phi') < 0: 
                        raise AglaError("einen Ausdruck in 'phi' " + \
                             "angeben")	
                    ende = False
                    while not ende:					
                        try:	
                            egl = sympify(pol)
                            ende = True							
                        except NameError as e:
                            es = str(e)
                            par = es[es.find("'")+1:es.rfind("'")]					
                            locals()[par] = Symbol(par)						
                    pol = Gleichung(r, egl)                    					
                if kwargs.get('imp'):
                    imp = kwargs.get('imp')
                    if not isinstance(imp, str):
                        imp = str(imp)					
                    if imp.find('=') >= 0:						
                        raise AglaError('hier keine Gleichung, sondern ' + \
                             'einen Ausdruck angeben')	
                    if imp.find('x') < 0 and imp.find('y') < 0: 
                        raise AglaError("einen Ausdruck in 'x' und 'y' " + \
                             "angeben")	
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
															  
            if (isinstance(aa, Vektor) and aa.dim == 2) or \
                (isinstance(aa, (tuple, Tuple)) and len(aa) == 2):
				
			      # Erzeugung mittels allgemeinem Kurvenpunkt 	
				
                typ = 'prg'			   
                if not len(args) == 2:    
                    raise AglaError("zwei Argumente angeben")
                allg_punkt = aa
                par_angabe = args[1]				
                if isinstance(allg_punkt, (tuple, Tuple)):
                    allg_punkt = Vektor(*allg_punkt)
                if not allg_punkt.free_symbols:
                    txt = "im allgemeinen Punkt ist kein Parameter enthalten"
                    raise AglaError(txt)
                if not par_name in allg_punkt.free_symbols:
                    txt = "der Parameter ist nicht in der Kurvengleichung enthalten"
                    raise AglaError(txt)
                prg = Gleichung(Vektor(x, y), allg_punkt)           				
                return AglaObjekt.__new__(cls, allg_punkt, 
			                                (par_name, unt, ob),
                                          (prg, fkt, pol, imp),
												  typ )													

            elif isinstance(aa, str) and saa[:2] == 'y=':

                # Erzeugung über Funktionsgleichung 'y = f(x)' 
				
                print('Erzeugung in Parameterform, x -> ' + str(par_name))
                typ = 'prg'				
                gl = aa
                srhs = gl[gl.find('=')+1:]					
                rhs = sympify(srhs)
                if srhs.find('y') >= 0:		
                    raise AglaError("die rechte Seite darf kein " + \
                         "y enthalten")						
                if gl.find('x') < 0:   # konstante Funktion 
                    allg_punkt = Vektor(par_name, rhs)
                else:				
                    yk = sympify(str(rhs).replace('x', str(par_name)))   				
                    allg_punkt = Vektor(par_name, yk)
                prg = Gleichung(Vektor(x, y), allg_punkt)	
                fkt = Gleichung(y, rhs)
                imp = Gleichung(y - rhs)
                return AglaObjekt.__new__(cls, allg_punkt, 
			                                (par_name, unt, ob),  
                                          (prg, fkt, pol, imp),
                                           typ )
				
            elif isinstance(aa, str) and 'r=' in saa:

                # Erzeugung über Polarkoordinaten 'r = r(phi)' 
				
                par_name = Symbol('t')				
                print('Erzeugung durch Umwandlung in kartesische Koordinaten und')
                print('Parametrisierung, phi -> ' + str(par_name))				
                typ = 'prg'				
                gl = aa
                srhs = gl[gl.find('=')+1:]					
                rhs = sympify(srhs)
                if gl[1:].find('r') >= 0:		
                    raise AglaError("die rechte Seite darf kein " + \
                         "r enthalten")						
                if gl.find('phi') < 0:   # konstante Funktion 
                    allg_punkt = Vektor(rhs*cos(par_name), rhs*sin(par_name))
                else:								
                    xx = rhs.subs(phi, par_name) * cos(par_name)
                    yy = rhs.subs(phi, par_name) * sin(par_name)                        
                    allg_punkt = Vektor(xx, yy)
                    prg = Gleichung(Vektor(x, y), allg_punkt)	                        
                    pol = Gleichung(r, rhs)
                return AglaObjekt.__new__(cls, allg_punkt, 
			                           (par_name, unt, ob), 
											(prg, fkt, pol, imp),
											 typ )
				
            elif isinstance(aa, str) and '=0' in saa or is_zahl(aa):

                # Erzeugung über implizite Gleichung 'F(x, y) = 0' 
                # bzw. F(x, y)                           				  
                typ = 'imp'
                t = Symbol('t')				
                gl = aa
                if 'x' in str(gl) and not 'y' in str(gl):
                    if len(args) > 1:	
                        return Kurve('y = ' + str(gl), args[1])						
                    return Kurve('y = ' + str(gl))				
                if len(args) > 1:	
                    raise AglaError('hier sind keine Parameterangaben möglich')
                if isinstance(gl, str):			
                    gl = gl[:gl.find('=')]
                sgl = str(gl)				
                if sgl.find('x') < 0 and sgl.find('y') < 0:
                    raise AglaError("die Gleichung muss x oder/und y enthalten")
                gl = Gleichung(sympify(gl), 0)					
                imp = gl
                if sgl.find('x') < 0: 
                    gl = sgl.replace('y', '0')				
                    print('Erzeugung mittels der Parametergleichung')
                    return Kurve((t, -sympify(gl.replace('x', 't'))), (t, -1000, 1000), \
                          imp=str(imp.lhs))					
                if sgl.find('y') < 0:
                    gl = sgl.replace('x', '0')				
                    print('Erzeugung mittels der Parametergleichung')
                    return Kurve((-sympify(gl.replace('y', 't')), t), (t, -1000, 1000), \
                          imp=str(imp.lhs))				
                return AglaObjekt.__new__(cls, gl,    # 3 Argumente
                                          (prg, fkt, pol, imp),
                                           typ )
            else:
                raise AglaError('Eingaben überprüfen')			
		  							
        except AglaError as e:	
            print('agla:', str(e))
            return			
  			
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            if self.dim == 3:
                return "Raumkurvenschar(" + ss + ")"
            else:
                if self._typ == 'prg':		
                    return "Kurvenschar(" + ss + "), Parameterform"
                return "Kurvenschar(" + ss + "), Implizite Gleichung"
        if self.dim == 3:
            return "Raumkurve"
        else:
            if self._typ == 'prg':		
                return "Kurve, Parameterform"			
            return "Kurve, Implizite Gleichung"			

    @property
    def _typ(self):              
        if self.dim == 3:
            return None		
        return str(self.args[-1])
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        if isinstance(self.args[0], Vektor) and self.args[0].dim == 3:
            return 3
        else:
            return 2
		
    @property
    def par(self):              
        """Kurvenparameter"""
        if self._typ != 'imp':
            return self.args[1][0]
        print('agla: nicht definiert (implizite Gleichung)')			
				
    @property
    def ber(self):              
        """Parameterbereich"""
        if self._typ != 'imp':
            return self.args[1][1], self.args[1][2]						
        print('agla: nicht definiert (implizite Gleichung)')			
				
    @property		
    def prg(self):              
        """Parametergleichung; nur zur Ausgabe"""
        x, y, z = symbols('x y z')
        xx = Vektor(x, y, z) if self.dim == 3 else Vektor(x, y)
        if self.dim == 3 or self._typ == 'prg':
            return Gleichung(xx, self.pkt(self.par))        
        else:
            gl = self.args[1][0]
            if gl:
                return gl
            print('agla: die Gleichung/Form ist nicht verfügbar')			
	
    @property		
    def pf(self):              
        """Parameterform; nur zur Ausgabe"""		
        if self._typ == 'imp':
            if self.prg:
                p = self.prg.rhs
            else:				
                return
        else:			
            t = self.args[1][0]			
            p = self.pkt(t)
        if self.dim == 3:		
            display(Math('\\left(' + latex(p.x) + ',\;' + latex(p.y) + ',\;' + \
                   latex(p.z) + '\\right)'))	
        else:			
            display(Math('\\left(' +latex(p.x) + ',\;' + latex(p.y) + '\\right)'))		

    @property		
    def gleich(self):              
        """Eingabegleichung; nach eventueller Parametrisierung"""
        if self.dim == 3:
            return self.prg 
        else:
            if self._typ == 'prg':
                return self.prg 
            else:
                gl = self.args[0]
                return gl				
	  
    @property		
    def fkt(self):              
        """Funktionsgleichung"""
        if self.dim == 3:
            print('agla: im Raum R^3 nicht definiert')		
            return
        if self._typ == 'prg':			
           gl = self.args[2][1]
        else:			
           gl = self.args[1][1]
        if gl:
            return gl
        print('agla: die Gleichung ist nicht verfügbar')
	  
    @property		
    def pol(self):              
        """Gleichung in Polarkoordinaten"""
        r, phi = Symbol('r'), Symbol('phi')
        if self.dim == 3:
            print('agla: im Raum R^3 nicht definiert')		
            return 
        if self._typ == 'prg':			
           gl = self.args[2][2]
        else:			
           gl = self.args[1][2]
        if gl:
            return gl
        print('agla: die Gleichung ist nicht verfügbar')
	  
    @property		
    def imp(self):              
        """Implizite Gleichung"""
        if self.dim == 3:
            print('agla: im Raum R^3 nicht definiert')		
            return 
        if self._typ == 'prg':
            gl = self.args[2][3]
        else:
            gl = self.args[1][3]
        if gl:
            return gl
        print('agla: die Gleichung ist nicht verfügbar')
		
    @property
    def sch_par(self):                             
        """Parameter einer Schar"""
        zahl = (int, Integer, float, Float, Rational)		
        if self.dim == 3 or (self.dim == 2 and self._typ != 'imp'):
            if self.dim == 3:
                pkt, par = self.args
            else:
                pkt, par = self.args[:2]			
            spar = pkt.free_symbols
            if not isinstance(par[1], zahl):
                spar |= par[1].free_symbols
            if not isinstance(par[2], zahl):
                spar |= par[2].free_symbols
            return spar - {self.par}
        else:
            x, y = Symbol('x'), Symbol('y')		
            return self.args[0].free_symbols - {x, y}		
		
    schPar = sch_par		

    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar	

    @property
    def is_eben(self):
        """Test auf ebene Kurve"""
        if self.dim == 3:		
            w = self.wind()
            if w == 0:
                return True
            if w.equals(0):
                return True
            return False
        return None			
		
    isEben = is_eben
				
    @property		
    def bog_laenge(self):
        """Bogenlänge"""	
        if self.dim == 2 and self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')			
            return		
        ber = self.ber
        if not mit_param(self):		
            # nummerische Integration mit scipy	
            from scipy.integrate import romberg
            def f(t):
                return float(self.geschw(t).betrag)			
            I = romberg(f, float(ber[0]), float(ber[1]), tol=1e-4) 
            return I
        else:
            print("agla: nicht implementiert (Parameter)")
            return
	
    bogLaenge = bog_laenge	
	
    @property	
    def evolute(self):
        """Evolute"""						
        if self.dim == 3 or self.dim == 2 and self._typ != 'imp':			
            par = self.par
            k = self.kr_kreis(par)
            m = k.mitte.einfach
            ber = self.ber
            return Kurve(m, (par, ber[0], ber[1]))			
        else:
            print('agla: nicht verfügbar (implizite Gleichung)')		
			
    @property	
    def in_raum(self):
        """Konvertierung in Raumkurve"""						
        if self.dim == 3:
            return self		
        if self._typ != 'imp':			
            p = self.pkt()
            p3 = Vektor(p.x, p.y, 0)
            par = self.par			
            ber = self.ber
            return Kurve(p3, (par, ber[0], ber[1]))			
        else:
            print('agla: nicht implementiert (implizite Gleichung)')		
	
    inRaum = in_raum	
	
    @property		
    def formeln(self):
        """Formeln"""
		
        if self.dim == 3:	
            print(' ')
            txt = 'Gleichung\: der\: Kurve\:\:\:\:\:\:\:\quad\:\:\:' + \
             '\\vec{x}(t)\:=\:' + \
		      '\\left(\\begin{matrix}x(t)\\\\y(t)\\\\z(t)\\end{matrix}\\right)'
            display(Math(txt))		
            txt = 'Geschwindigkeitsvektor\:\:\:\:\:\:\:' + "\\vec{x}\:'(t)\:=\:" + \
		      '\\left(\\begin{matrix}x'+"'"+'(t)\\\\y'+"'"+'(t)\\\\z'+"'" + \
			  '(t)\\end{matrix}\\right)'
            display(Math(txt))		
            txt = 'Beschleunigungsvektor\:\:\:\:\:\:\:' + "\\vec{x}\:''(t)\:=\:" + \
		      '\\left(\\begin{matrix}x'+"''"+'(t)\\\\y'+"''"+'(t)\\\\z' + \
			   "''" +'(t)\\end{matrix}\\right)' 
            display(Math(txt))		
            txt = 'Tangentialvektor,\: Tangente\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:'+ \
		       '\:\:\:\:\:\:\:\:' + '\\vec{\\tau}' + '(t)\:=\:' + \
			    "\\vec{x}\:'(t)" + \
             ',\:\:\:\\vec{X}(t)\:=\:' + '\\vec{x}(t)\:+\\lambda\:\\vec{\\tau}(t)'
            display(Math(txt))		
            txt = 'Binormalenvektor,\: Binormale\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\:\;'+\
		       '\:\:\:' + '\\vec{\\beta}' + '(t)\:=\:' + "\\vec{x}\:'(t)" + \
			   "\\times \\vec{x}\:''(t)" + \
             ',\:\:\:\\vec{X}(t)\:=\:' + '\\vec{x}(t)\:+\\lambda\:\\vec{\\beta}(t)'			   
            display(Math(txt))		
            txt = 'Hauptnormalenvektor,\: Hauptnormale\:\:\:\:\:\:\;' + \
		       '\\vec{\\eta}' + '(t)\:=\:' + "\\vec{\\tau}\:(t)" + \
			   "\\times \\vec{\\beta}\:(t)" + \
             ',\:\:\:\\vec{X}(t)\:=\:' + '\\vec{x}(t)\:+\\lambda\:\\vec{\\eta}(t)'			   
            display(Math(txt))		
            txt = 'Normalebene\qquad\qquad\qquad\qquad\qquad\;\,' + \
		       '(\\vec{X}(t)-\\vec{x}(t))\\circ\\vec{\\tau}(t)=0'			  
            display(Math(txt))		
            txt = 'Schmiegungsebene\qquad\qquad\qquad\qquad\:\:\:' + \
		       '(\\vec{X}(t)-\\vec{x}(t))\\circ\\vec{\\beta}(t)=0'			  
            display(Math(txt))		
            txt = 'Rektifizierende Ebene\qquad\qquad\qquad\quad\:\:\:\:' + \
		       '(\\vec{X}(t)-\\vec{x}(t))\\circ\\vec{\\eta}(t)=0'			  
            display(Math(txt))	
            txt = "Kruemmung\qquad\qquad\qquad\quad" + " K = K(t)=\\frac{" + \
		       "\\vec{x}'(t)\\circ\\vec{x}'(t)\\cdot\\vec{x}''(t)\\circ" + \
			    "\\vec{x}''(t)" + \
              "-(\\vec{x}'(t)\\circ\\vec{x}''(t))^2}{(\\vec{x}'(t)\\circ" + \
			    "\\vec{x}''(t))^3}"		
            display(Math(txt))	
            txt = "\qquad\qquad\qquad\qquad\qquad\qquad\:\, = " + \
		       "\\frac{(x'^2+y'^2+z'^2)\\cdot(x''^2+y''^2+z''^2)-(x'x''+" + \
			    "y'y''+z'z'')^2}{(x'^2+y'^2+z'^2)^3}(t)"
            display(Math(txt))	
            txt = "Kruemmungsradius\qquad\qquad\:\: R = R(t) = \\frac{1}{K(t)}"
            display(Math(txt))	
            txt = "Kruemmungsmittelpunkt\qquad\:\:\:\, \\vec{x}_M(t) = \\vec{x}(t)+" + \
              "R(t)\\cdot\\vec{\\eta}_0(t)"
            display(Math(txt))	
            txt = "Windung\quad\qquad\qquad\qquad\quad\: W = W(t) = R(t)^2\," + \
             "\\frac{(\\vec{x}'(t)\\times \\vec{x}''(t))\\circ\\vec{x}'''" + \
             "(t)}{(\\vec{x}'(t)\\circ\\vec{x}'(t))^3}"
            display(Math(txt))	
            txt = "\qquad\qquad\qquad\qquad\qquad\qquad\\,\,\, = " + \
              "R(t)^2\,\\frac{\\left|\\begin{matrix}x' & y' & " + \
             "z'\\\\x'' & y'' & z''" + \
             "\\\\x''' & y''' & z'''" + \
             "\\end{matrix}\\right|}{(x'^2+y'^2+z'^2)^3}(t)"
            display(Math(txt))	
            txt = "Windungsradius\qquad\qquad\quad\quad r = r(t) = \\frac{1}{W(t)}"
            display(Math(txt))	
            txt = "Bogenlaenge\qquad\qquad\qquad\quad\, b = \\int _{t_0} ^{t_1}" + \
              "\\sqrt{x'(t)^2+y'(t)^2+" + \
             "z'(t)^2}dt" 
            display(Math(txt))				 
            txt = "\qquad\qquad\qquad\qquad\qquad\qquad\quad\:" + \
             "(zwischen\: den\: Punkten\: mit\: den\: " + \
             "Parameterweren\: t_0\: und\: t_1)"
            display(Math(txt))	
            txt = "\\vec{X}\:-\:Ortsvektor\: des\: allgemeinen\: Punktes " + \
              "\:der\:\ Geraden\:bzw.\: Ebene"
            display(Math(txt))	
            txt = "\\vec{\\eta}_0\:-\: Hauptnormaleneinheitsvektor"
            display(Math(txt))	
            print(' ')
			
        elif self._typ == 'prg':
            print(' ')
            txt = "\mathrm{Berechnungsgrundlage} \quad \mathrm{Gleichung\:in\:Parameterform}" + \
                 "\quad \\vec{x}(t)\:=\:" + \
		          "\\left(\\begin{matrix}x(t)\\\\y(t)\\end{matrix}\\right)" + \
                 "\quad \mathrm{bzw.} \quad x=x(t), y=y(t)"			
            display(Math(txt))
            txt = "\mathrm{Tangentengleichung} \qquad\quad\quad \\frac{y-y_P}{y'} = \\frac{x-y_P}{x'}"
            display(Math(txt))
            txt = "\mathrm{Normalengleichung} \qquad\quad\quad\: x' \, (x-x_P)+y' \, (y-y_P)=0" 		
            display(Math(txt))
            txt = "\mathrm{Krümmung} \qquad\qquad\qquad\quad\:\, K=\\frac{\\left|\\begin{matrix}x' & y' " + \
             "\\\\x'' & y'' " + \
             "\\end{matrix}\\right|}{(x'^2+y'^2)^\\frac{3}{2}}"
            display(Math(txt))
            txt = "\mathrm{Krümmungskreis, Radius} \quad\quad\:\,\, R=1/K "
            display(Math(txt))
            txt = "\mathrm{ebenso, \,Mittelpunkt} \qquad\quad\quad\:\, x_M=x_P-\\frac{y'\,(x'^2+y'^2)}{\\left|\\begin{matrix}x' & y' " + \
             "\\\\x'' & y'' " + \
             "\\end{matrix}\\right|} \qquad\quad\: y_M=y_P+\\frac{x'\,(x'^2+y'^2)}{\\left|\\begin{matrix}x' & y' " + \
             "\\\\x'' & y'' " + \
             "\\end{matrix}\\right|} \qquad\quad "
            display(Math(txt))			 
            txt = "\mathrm{Bogenlänge}\qquad\qquad\qquad\quad\:\:\, b = \\int _{t_0} ^{t_1}" + \
              "\\sqrt{x'(t)^2+y'(t)^2}dt" + \
             "\qquad\qquad "
            display(Math(txt))			 
            txt = "\qquad\qquad\qquad\qquad\qquad\qquad\quad\:\:" + \
			       "\mathrm{zwischen\, den\, Punkten\, mit\ den\, Parameterwerten\:} t_0\: und\: t_1"
            display(Math(txt))	
            txt = "\mathrm{Geschwindigkeitsvektor}\qquad\:\:\:\: " + \
             "\\left(\\begin{matrix}x'(t)\\\\y'(t)\\end{matrix}\\right)"
            display(Math(txt))	
            txt = "\mathrm{Bechleunigungsvektor}\qquad\quad\:\:\: " + \
             "\\left(\\begin{matrix}x''(t)\\\\y''(t)\\end{matrix}\\right) "
            display(Math(txt))
            txt = "x_P,\: y_P \: - \mathrm{Koordinaten\, eines \,Kurvenpunktes}\: P"
            display(Math(txt))
            txt = "x,\: y \: \mathrm{laufende\: Koordinaten\,der\, Tangenten -\, bzw.\, Normalenpunkte}"
            display(Math(txt))
            txt = "\mathrm{Alle\, Ableitungen\, werden\, im\, Punkt} \:P\: \mathrm{berechnet}"		
            display(Math(txt))
            print(' ')
								
        elif self._typ == 'imp':
            print(' ')		
            txt = "\mathrm{Berechnungsgrundlage} \quad \mathrm{ Implizite\, Gleichung}" + \
                  "\quad F(x,y)=0"
            display(Math(txt))
            txt = "\mathrm{Tangentengleichung} \qquad\quad\quad F'_x \, (x-x_P) +" + \
               "F'_y\,(y-y_P) = 0"
            display(Math(txt))
            txt = "\mathrm{Normalengleichung} \qquad\quad\quad\:\\frac{y-y_P}{F'_x} = \\frac{x-x_P}{F'_y}"
            display(Math(txt))
            txt = "\mathrm{Krümmung} \qquad\qquad\qquad\quad \:\,\, K = \\frac{\\left|\\begin" + \
                 "{matrix}F_{xx}'' & F_{xy}'' & F_x'" + \
                 "\\\\F_{yx}'' & F_{yy}'' & F_y'\\\\F_x' & F_y' & 0" + \
                 "\\end{matrix}\\right|}{(F_x'^2+F_y'^2)^\\frac{3}{2}}"			 			 
            display(Math(txt))
            txt = "\mathrm{Krümmungskreis,\: Radius} \qquad\:\: R=1/K "
            display(Math(txt))
            txt = "\mathrm{ebenso, Mittelpunkt} \qquad\quad\quad\:\:\, " + \
             "x_M=x_P+\\frac{F_x'\,(F_x'^2+F_y'^2)}{\\left|\\begin{matrix}F_{xx}'' & F_{xy}'' & F_x'" + \
             "\\\\F_{yx}'' & F_{yy}'' & F_y'\\\\F_x' & F_y' & 0"+ \
             "\\end{matrix}\\right|} \qquad " + \
             "y_M=y_P+\\frac{F_y'\,(F_x'^2+F_y'^2)}{\\left|\\begin{matrix}F_{xx}'' & F_{xy}'' & F_x'" + \
             "\\\\F_{yx}'' & F_{yy}'' & F_y'\\\\F_x' & F_y' & 0"+ \
             "\\end{matrix}\\right|} \quad\qquad"
            display(Math(txt))
            txt = "x_P, y_P \: - \mathrm{Koordinaten\, eines \,Kurvenpunktes\,} P"
            display(Math(txt))
            txt = "x,\: y \: - " + \
                  "\mathrm{laufende\: Koordinaten \: der\: Tangenten- \: bzw. \: Normalenpunkte} "
            display(Math(txt))
            txt = "\mathrm{Alle\, Ableitungen\, werden\, im\, Punkt} \:P\: \mathrm{berechnet}"		
            display(Math(txt))
            print(' ')
			
			
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Kurvenschar\n")		
            print("Aufruf   kurve . sch_el( wert )\n")		                     
            print("             kurve   Kurve")
            print("             wert    Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben")
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien ' + \
                 'Parameter angeben')	
            return	
        try:			
            wert = nsimplify(wert)
        except	RecursionError:
            pass		
        if self.dim == 3 or self._typ != 'imp':		
            ap = self.args[0]
            unt, ob = self.args[1][1:]
            ap = ap.subs(p, wert)
            ber = unt.subs(p, wert), ob.subs(p, wert)
            return Kurve(ap, (self.par, ber[0], ber[1]))
        else:			
            gl = self.args[0]
            gl = gl.subs(p, wert)
            gl = repr(gl.lhs) + '= 0'
            return Kurve(gl)		
		
    schEl = sch_el	
		
		
    def pkt(self, *wert, **kwargs):
        """Kurvenpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt der Kurve\n")
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n") 			
            print("Aufruf    kurve . pkt( /[ wert ] )\n")		                     
            print("              kurve   Kurve")
            print("              wert    Wert des Kurvenparameters\n")
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           zugehöriger Kurvenpunkt")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           allgemeiner Punkt der Kurve\n") 			
            return
				
        pkt = self.args[0]
        par = self.par
        if not par:
            return		
        if not wert:
            return pkt
        if len(wert) == 1:
             pw = sympify(wert[0])
             if not is_zahl(pw):
                 print("agla: einen Zahlenwert angeben")
                 return
             try:				 
                 pw = nsimplify(pw)
             except RecursionError:
                 pass			 
             if self.dim == 3:			 
                 return Vektor(pkt.x.subs(par, pw), pkt.y.subs(par, pw), 
                                                     pkt.z.subs(par, pw))			 
             return Vektor(pkt.x.subs(par, pw), pkt.y.subs(par, pw)) 
        print("agla: nur einen Parameterwert angeben")
        return		
		
		 
    def geschw(self, *wert, **kwargs):
        """Geschwindigkeitsvektor"""
		 
        if kwargs.get('h'):
            print("\nGeschwindigkeits- / Tangentialvektor der Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . geschw( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Geschwindigkeitsvektor im zugehörigen Punkt")
            print("           der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Geschwindigkeitsvektor im allgemeinen Punkt der") 	
            print("           Kurve\n")			
            print("In der Ebene R^2 (für Kurven, die mittels impliziter Gleichung")
            print("erzeugt wurden):\n")
            print("Aufruf     kurve . geschw( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")	
            return 
						
        if self.dim == 3 or self.dim == 2 and self._typ != 'imp':
            pkt = self.pkt()
            par = self.par			
            if not wert:
                return pkt.diff(par)
            if len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return				 
                return  pkt.diff(par).subs(par, pw)			 
            print("agla: nur einen Parameterwert angeben")
            return	
        else:
            if len(wert) != 1:
                print("agla: einen Punkt in der Ebene  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt der Kurve angeben')
                return	
            x, y = Symbol('x'), Symbol('y')				
            if gl.subs({x:p.x, y:p.y}).lhs != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            Fx, Fy = gl.lhs.diff(x), gl.lhs.diff(y)
            zahl = (int, Integer, float, Float, Rational)			
            Fx = Fx if isinstance(Fx, zahl) else Fx.subs({x:p.x, y:p.y}) 
            Fy = Fy if isinstance(Fy, zahl) else Fy.subs({x:p.x, y:p.y}) 
            return Vektor(Fy, -Fx)			
		
    tang_vekt = geschw			
    tangVekt = tang_vekt		
	
		
    def beschl(self, *wert, **kwargs):
        """Beschleunigungssvektor"""
		 
        if kwargs.get('h'):
            print("\nBeschleunigungsvektor der Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . beschl( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Beschleunigungsvektor im zugehörigen Punkt der ")
            print("           Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Beschleunigungsvektor im allgemeinen Punkt der")
            print("           Kurve\n") 			
            return 
		
        if self._typ == 'imp':
            print("agla: nicht verfügbar (implizite Gleichung)")
            return			
			
        pkt = self.pkt()
        par = self.par			
        if not wert:
            return pkt.diff(par).diff(par)
        if len(wert) == 1:
            pw = sympify(wert[0])
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass			 
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return				 
            return  pkt.diff(par).diff(par).subs(par, pw)			 
        print("agla: nur einen Parameterwert angeben")
        return		
		
	
    def bi_normale(self, *wert, **kwargs):
        """Binormale"""
		 
        if self.dim != 3:
            print("agla: nur im Raum R^3 definiert")
            return
		  
        if kwargs.get('h'):
            print("\nBinormale der Kurve\n")		
            print("Im Raum R^3:\n")
            print("Aufruf     kurve . bi_normale( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Binormale im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Binormale im allgemeinen Punkt der Kurve\n") 			
            return 
			
        par = self.par		
        pkt = self.pkt(par)
        p1 = pkt.diff(par)
        p2 = p1.diff(par)	
        t, s = Symbol("t"), Symbol("s")
        if par == t:
            par1 = s
        else:
            par1 = t		
        if not wert:
            try:		
                return Gerade(pkt, p1.vp(p2).einfach, par1)
            except AglaError:
                print('agla: die Binormale ist nicht definiert')
                return None				
        if len(wert) == 1:
            pw = sympify(wert[0])
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass			 				 
            g = Gerade(pkt.subs(par, pw).einfach, 
		                           p1.vp(p2).subs(par, pw).einfach, par1)
            if g is not None:								   
                return g
            print('agla: die Binormale ist nicht definiert')
            return None				 
        print("agla: nur einen Parameterwert angeben")
        return		
		
    biNormale = bi_normale
	
	
    def h_normale(self, *wert, **kwargs):
        """Hauptnormale"""
		 
        if self.dim != 3:
            print("agla: nur im Raum R^3 definiert")
            return
			
        if kwargs.get('h'):
            print("\nHauptnormale der Kurve\n")		
            print("Im Raum R^3:\n")
            print("Aufruf     kurve . h_normale( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Hauptnormale im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Hauptnormale im allgemeinen Punkt der Kurve\n") 			
            return 
			
        par = self.par		
        pkt = self.pkt(par)
        p1 = pkt.diff(par)
        p2 = p1.diff(par)	
        t, s = Symbol("t"), Symbol("s")
        if par == t:
            par1 = s
        else:
            par1 = t		
        if not wert:
            try:		
                return Gerade(pkt, -p1.vp(p1.vp(p2)), par1)
            except AglaError:				
                print('agla: die Hauptnormale ist nicht definiert')
                return None				
        if len(wert) == 1:
            pw = sympify(wert[0])
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass
            try:
                return Gerade(pkt.subs(par, pw).einfach, 
			                     -p1.vp(p1.vp(p2)).subs(par, pw), par1)
            except AglaError:
                print('agla: die Hauptnormale ist nicht definiert')
                return			  
        print("agla: nur einen Parameterwert angeben")
        return		
		
    hNormale = h_normale
	
	
    def tangente(self, *wert, **kwargs):
        """Tangente"""
		 
        if kwargs.get('h'):
            print("\nTangente in einem Kurvenpunkt\n")
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . tangente( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Tangente im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Tangente im allgemeinen Punkt der Kurve\n") 
            print("In der Ebene R^2 (für Kurven, die mittels impliziter Gleichung")
            print("erzeugt wurden):\n")
            print("Aufruf     kurve . tangente( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")	
            return 
			
        if not (self.dim == 2 and self._typ == 'imp'):			
            par = self.par		
            pkt = self.pkt(par)
            gv = self.geschw(par)
            t, s = Symbol("t"), Symbol("s")
            if par == t:
                par1 = s
            else:
                par1 = t		
            if not wert:
                return Gerade(pkt, gv, par1)
            if len(wert) == 1:
                 pw = sympify(wert[0])
                 if not is_zahl(pw):
                     print("agla: einen Zahlenwert angeben")
                     return
                 try:				 
                     pw = nsimplify(pw)
                 except RecursionError:
                     pass			 					 
                 return  Gerade(pkt.subs(par, pw).einfach, 
                                            gv.subs(par, pw).einfach, par1)			 
            print("agla: nur einen Parameterwert angeben")
            return	
        else:	
            if len(wert) != 1:
                print("agla: einen Punkt in der Ebene  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt in der Ebene angeben')
                return	
            x, y = Symbol('x'), Symbol('y')				
            if gl.lhs.subs({x:p.x, y:p.y}) != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            Fx, Fy = gl.lhs.diff(x), gl.lhs.diff(y)
            zahl = (int, Integer, float, Float, Rational)			
            Fx = Fx if isinstance(Fx, zahl) else Fx.subs({x:p.x, y:p.y}) 
            Fy = Fy if isinstance(Fy, zahl) else Fy.subs({x:p.x, y:p.y}) 
            return Gerade(Fx, Fy, -Fx*p.x - Fy*p.y)			
         			
	
    def normale(self, *wert, **kwargs):
        """Normale"""
		 
        if self.dim == 3:
            print('agla: nur in der Ebene R^2 definiert')
            return
			
        if kwargs.get('h'):
            print("\nNormale in einem Kurvenpunkt\n")		
            print("In der Ebene R^2 (Parameterform, Funktionsgleichung")
            print("bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . normale( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Normale im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Normale im allgemeinen Punkt der Kurve\n") 			
            print("In der Ebene R^2 (für Kurven, die mittels impliziter Gleichung")
            print("erzeugt wurden):\n")
            print("Aufruf     kurve . normale( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")	
            return 
			
        if self._typ != 'imp':						
            par = self.par		
            p = self.pkt(par)
            ps = p.diff(par)
            t, s = Symbol("t"), Symbol("s")
            if par == t:
                par1 = s
            else:
                par1 = t		
            if not wert:
                ta = self.tangente(par)
                tv = ta.richt				
                nv = Vektor(1, 0) if tv.x == 0 else Vektor(-tv.y, tv.x)				
                return Gerade(ta.stuetz, nv, par1)
            if len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return	
                try:				 
                    pw = nsimplify(pw)
                except RecursionError:
                    pass			 
                ta = self.tangente(pw)
                tv = ta.richt				
                nv = Vektor(1, 0) if tv.x == 0 else Vektor(-tv.y, tv.x)				
                return Gerade(ta.stuetz, nv, par1)
            print("agla: nur einen Parameterwert angeben")
            return	
        else:
            if len(wert) != 1:
                print("agla: einen Punkt in der Ebene  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt der Kurve angeben')
                return	
            x, y = Symbol('x'), Symbol('y')				
            if gl.lhs.subs({x:p.x, y:p.y}) != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            ta = self.tangente(p)
            tv = ta.richt				
            nv = Vektor(1, 0) if tv.x == 0 else Vektor(-tv.y, tv.x)				
            return Gerade(ta.stuetz, nv)

			
    def drei_bein(self, *wert, **kwargs):
        """Begleitendes Dreibein"""

        if self.dim == 2:
            print('agla: nur im Raum R^3 definiert')		
            return	
			
        if kwargs.get('h'):
            print("\nBegleitendes Dreibein der Kurve\n")	
            print("Im Raum R^3:\n")		
            print("Aufruf     kurve . drei_bein( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   ( Tangenteneinheitsvektor,") 
            print("             Hauptnormaleneinheitsvektor,") 
            print("             Binormaleneinheitsvektor )\n")
            print("             bei Angabe eines Parameterwertes:") 
            print("             Dreibein im zugehörigen Punkt der Kurve")
            print("             bei leerer Argumentliste oder freiem Bezeichner:") 
            print("             Dreibein im allgemeinen Punkt der Kurve\n") 	
            return 
			
        par = self.par
        d1 = self.tang_vekt(par).einh_vekt.einfach
        hn = self.h_normale(par)
        bn = self.bi_normale(par)
        if hn is None or bn is None: 		
            print('agla: das Dreibein ist nicht definiert')
            return			
        d2 = hn.richt.einh_vekt.einfach 
        d3 = bn.richt.einh_vekt.einfach 
        if not wert:
            return d1, d2, d3
        if len(wert) == 1:
             pw = sympify(wert[0])
             if not is_zahl(pw):
                 print("agla: einen Zahlenwert angeben")
                 return
             try:				 
                 pw = nsimplify(pw)
             except RecursionError:
                 pass			 
             return d1.subs(par, pw), d2.subs(par, pw), d3.subs(par, pw)			 
        print("agla: nur einen Parameterwert angeben")
        return		
		
    dreiBein = drei_bein	
	

    def zwei_bein(self, *wert, **kwargs):
        """Begleitendes Zweibein"""

        if self.dim != 2:
           print('agla: nur der Ebene R^2 definiert')		
           return	
			
        if kwargs.get('h'):
            print("\nBegleitendes Zweibein der Kurve\n")	
            print("In der Ebene R^2\n")
            print("Parameterform, Funktionsgleichung bzw. Polarkoordinaten:\n")			
            print("Aufruf     kurve . zwei_bein( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   ( Tangenteneinheitsvektor,") 
            print("             Normaleneinheitsvektor)") 
            print("           bei Angabe eines Parameterwertes:") 
            print("           Zweibein im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Zweibein im allgemeinen Punkt der Kurve\n")
            print("Implizite Gleichung:\n")
            print("Aufruf     kurve . zwei_bein( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")				
            return 
			
        if self._typ != 'imp': 			
            par = self.par
            tv = self.tang_vekt(par)
            nv = self.normale(par)
            if tv is None or nv is None:
                print('agla: das Zweibein ist nicht definiert')
                return			
            d1 = tv.einh_vekt.einfach
            d2 = nv.richt.einh_vekt.einfach 
            if not wert:
                return d1, d2
            if len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return	
                try:				 
                    pw = nsimplify(pw)
                except RecursionError:
                    pass			 
                return d1.subs(par, pw), d2.subs(par, pw)		 
            print("agla: nur einen Parameterwert angeben")
            return	
        else:
            if len(wert) != 1:
                print("agla: einen Punkt in der Ebene  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt der Kurve angeben')
                return	
            x, y = Symbol('x'), Symbol('y')				
            if gl.lhs.subs({x:p.x, y:p.y}) != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            tv = self.tang_vekt(p)
            no = self.normale(p)
            if tv is None or no is None:
                return					
            return tv.einh_vekt.einfach, no.richt.einh_vekt.einfach			
		
    zweiBein = zwei_bein	

	
    def schm_ebene(self, *wert, **kwargs):
        """Schmiegebene"""
		 
        if self.dim != 3:
            print('agla: nur im Raum R^3 definiert')				
            return
			
        if kwargs.get('h'):
            print("\nSchmiegebene der Kurve\n")
            print("Im Raum R^3:\n")			
            print("Aufruf     kurve . schm_ebene( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Schmiegebene im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Schmiegebene im allgemeinen Punkt der Kurve\n") 			
            return 
			
        par = self.par		
        pkt = self.pkt(par)
        g = self.bi_normale(par)
        if not g:
            print('agla: die Schmiegebene ist nicht definiert')	
            return None			
        r, s, u, w = symbols('r s u w')
        par1, par2 = r, s		
        if par in (r, s):
           par1, par2 = u, w		
        if not wert:
            try:		
                return Ebene(pkt, g.richt, par1, par2)
            except AglaError:
                print('agla: die Schmiegebene ist nicht definiert')	
                return None			
        if len(wert) == 1:
            pw = sympify(wert[0])
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass			 				
            if not type(pw) in (int, Integer, float, Float, Rational):				 
                if pw.has(par1):
                    par1 = u if par1 in (r, s) else r
                if pw.has(par2):
                    par2 = w if par2 in (r, s) else s
            par1, par2 = sorted([par1, par2], key=str)	
            try:			
                return Ebene(pkt.subs(par, pw).einfach, 
			                 g.richt.subs(par, pw).einfach, par1, par2)		
            except AglaError:
                return None			
        print("agla: nur einen Parameterwert angeben")
        return		
		
    schmEbene = schm_ebene	
	

    def norm_ebene(self, *wert, **kwargs):
        """Normalebene"""

        if self.dim != 3:
            print('agla: nur im Raum R^3 definiert')		
            return
					
        if kwargs.get('h'):
            print("\nNormalebene der Kurve\n")		
            print("Im Raum R^3:\n")			
            print("Aufruf     kurve . norm_ebene( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Normalebene im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Normalebene im allgemeinen Punkt der Kurve\n") 			
            return 
			
        par = self.par		
        pkt = self.pkt(par)
        p1 = pkt.diff(par)
        g = self.bi_normale(par)
        if not g:
            print('agla: die Normalebene ist nicht definiert')	
            return None			
        r, s, u, w = symbols('r s u w')
        par1, par2 = r, s		
        if par in (r, s):
           par1, par2 = u, w		
        if not wert:
            try:		
                e = Ebene(pkt, p1, par1, par2)
                return e
            except AglaError:				
                print('agla: die Normalebene ist nicht definiert')	
                return None			
        if len(wert) == 1:
            pw = sympify(wert[0])
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return				  
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass			 
            if not type(pw) in (int, Integer, float, Float, Rational):				 
                if pw.has(par1):
                    par1 = u if par1 in (r, s) else r
                if pw.has(par2):
                    par2 = w if par2 in (r, s) else s
            par1, par2 = sorted([par1, par2], key=str)					
            try:		
                e = Ebene(pkt.subs(par, pw).einfach, 
                                        p1.subs(par, pw).einfach, par1, par2)
                return e
            except AglaError:				
                print('agla: die Normalebene ist nicht definiert')	
                return None			
        print("agla: nur einen Parameterwert angeben") 
        return		
		
    normEbene = norm_ebene		


    def rekt_ebene(self, *wert, **kwargs):
        """Rektifizierende Ebene"""
		 
        if self.dim != 3:
            print('agla: nur im Raum R^3 definiert')		
            return
							 
        if kwargs.get('h'):
            print("\nRektifizierende Ebene der Kurve\n")		
            print("Im Raum R^3:\n")			
            print("Aufruf     kurve . rekt_ebene( /[ wert ] )\n")		                     
            print("               kurve    Kurve")
            print("               wert     Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Rektifizierende Ebene im zugehörigen Punkt der")
            print("           Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Rektifizierende Ebene im allgemeinen Punkt der")
            print("           Kurve\n") 			
            return 
			
        par = self.par		
        pkt = self.pkt(par)
        g = self.h_normale(par)
        if not g:
            print('agla: die rektifizierende Ebene ist nicht definiert')	
            return None			
        r, s, u, w = symbols('r s u w')
        par1, par2 = r, s		
        if par in (r, s):
           par1, par2 = u, w		
        if not wert:
            return Ebene(pkt, g.richt, par1, par2)
        if len(wert) == 1:
            pw = sympify(wert[0])
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return				 
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass			 
            if not type(pw) in (int, Integer, float, Float, Rational):				 
                if pw.has(par1):
                    par1 = u if par1 in (r, s) else r
                if pw.has(par2):
                    par2 = w if par2 in (r, s) else s
            par1, par2 = sorted([par1, par2], key=str)					
            try:		
                e = Ebene(pkt.subs(par, pw).einfach, 
                                   g.richt.subs(par, pw).einfach, par1, par2)
                return e
            except AglaError:				
                print('agla: die rektifizierende ist nicht definiert')	
                return None											   
        print("agla: nur einen Parameterwert angeben")
        return		
		
    rektEbene = rekt_ebene		

		
    def kr_kreis(self, *wert, **kwargs):
        """Krümmungskreis"""
		 
        if kwargs.get('h'):
            print("\nKrümmungskreis der Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . kr_kreis( /[ wert ] )\n")		                     
            print("               kurve   Kurve")
            print("               wert    Wert des Kurvenparameters\n")	
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Krümmungskreis im zugehörigen Punkt der Kurve")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Krümmungskreis im allgemeinen Punkt der Kurve\n") 			
            print("In der Ebene R^2 (für Kurven, die mittels impliziter Gleichung")
            print("erzeugt wurden):\n")
            print("Aufruf     kurve . kr_kreis( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")	
            return 
			
        if self.dim == 3:			
            par = self.par		
            pkt = self.pkt(par)
            try:
                r = abs((1 / self.kruemm(par)))
                m = pkt + self.h_normale(par).richt.einh_vekt * r 		
            except ZeroDivisionError:
                print('agla: Division durch Null (Krümmung)')
                return                                       
            except AttributeError:
                print('agla: der Krümmungskreis ist nicht definiert')	
                return                                       
            if not wert:
                se = self.schm_ebene(par) 
                if se is None:
                    print('agla: der Krümmungskreis ist nicht definiert')	
                    return					
                return Kreis(se, m, r)
            if len(wert) == 1:
                pw = wert[0]
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return
                se = self.schm_ebene(pw)							
                if se is None:
                    print('agla: der Krümmungskreis ist nicht definiert')	
                    return					
                st = se.stuetz
                ri0 = se.richt[0]
                ri1 = se.richt[1]
                s, t, u = symbols('s t u')	
                ebpar = {s, t, u}.difference({par})	
                s, t = sorted(list(ebpar), key=str)				
                se = Ebene(st, ri0, ri1, s, t)				
                return Kreis(se, m.subs(par, pw), r.subs(par, pw))			 
            print("agla: nur einen Parameterwert angeben")
            return	

        elif self.dim == 2 and self._typ != 'imp':	
            par = self.par
            pkt = self.pkt(par)
            p1 = pkt.diff(par)
            p2 = p1.diff(par)
            try:
                r = abs(einfach(1 / self.kruemm(par)))
            except ZeroDivisionError:
                print('agla: Division durch Null (Krümmung)')
                return 
            d = determinante(Vektor(p1.x, p2.x), Vektor(p1.y, p2.y))
            if not d:
                print('agla: Division durch Null')
                return
            xm = einfach(pkt.x - p1.y * (p1.x**2 + p1.y**2) / d)			
            ym = einfach(pkt.y + p1.x * (p1.x**2 + p1.y**2) / d)
            m = Vektor(xm, ym)
            if not wert:
                return Kreis(m, r)
            if len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return				 
                try:				 
                    pw = nsimplify(pw)
                except RecursionError:
                    pass			 
                zahl = (int, Integer, float, Float, Rational)				
                r = r if isinstance(r, zahl) else r.subs(par, pw)
                return Kreis(m.subs(par, pw), r)			 
				
        else:		
            if len(wert) != 1:
                print("agla: einen Punkt in der Ebene  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt der Kurve angeben')
                return	
            x, y = Symbol('x'), Symbol('y')				
            if gl.subs({x:p.x, y:p.y}).lhs != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            Fx, Fy = gl.lhs.diff(x), gl.lhs.diff(y)
            try:
                r = abs(einfach(1 / self.kruemm(p)))
            except ZeroDivisionError:
                print('agla: Division durch Null (Krümmung)')
                return 
            zahl = (int, Integer, float, Float, Rational)		   
            Fx, Fy = gl.lhs.diff(x), gl.lhs.diff(y)
            Fxx = 0 if isinstance(Fx, zahl) else Fx.diff(x)	   
            Fyy = 0 if isinstance(Fy, zahl) else Fy.diff(y)		   
            Fxy = 0 if isinstance(Fx, zahl) else Fy.diff(y)		   
            Fyx = 0 if isinstance(Fy, zahl) else Fy.diff(x)		   
            d = determinante(Vektor(Fxx, Fyx, Fx), Vektor(Fxy, Fyy, Fy), \
                Vektor(Fx, Fy, 0))
            if not d:
                print('agla: Division durch Null')
                return				
            xm = einfach(p.x + Fx * (Fx**2 + Fy**2) / d)            		
            ym = einfach(p.y + Fy * (Fx**2 + Fy**2) / d)            		
            return Kreis(Vektor(xm, ym).subs({x:p.x, y:p.y}), r)
		
    krKreis = kr_kreis

	
    def kr_radius(self, *wert, **kwargs):
        """Krümmungsradius"""
		
        if kwargs.get('h'):
            print("\nKrümmungsradius der Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . kr_radius( /[ wert ] )\n")		                     
            print("               kurve   Kurve")
            print("               wert    Wert des Kurvenparameters\n")
            print("Rückgabe   bei Angabe eines Parameterwertes:") 
            print("           Krümmungsradius im zugehörigen Kurvenpunkt")
            print("           bei leerer Argumentliste oder freiem Bezeichner:") 
            print("           Krümmungsradius im allgemeinen Kurvenpunkt\n") 			
            print("In der Ebene R^2 (für Kurven, die mittels impliziter Gleichung")
            print("erzeugt wurden):\n")
            print("Aufruf     kurve . kr_radius( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")	
            print("Zusatz     d=1   Dezimaldarstellung\n")
            return
				
        if self.dim == 3 or self.dim == 2 and self._typ != 'imp':			
            par = self.par
            k = self.kruemm(par)
		
            if not wert:
                try:
                    res = abs(einfach(1 / k))		 
                    if mit_param(k):
                        return res
                    if kwargs.get('d'):
                        return float(res)
                    return res
                except ZeroDivisionError:
                    print("agla: Division durch Null (Krümmung)")
                    return				
            if len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return				
                try:				 
                    pw = nsimplify(pw)
                except RecursionError:
                    pass			 
                k = k.subs(par, pw)
                try:
                    res = abs(einfach(1 / k))		 
                    if mit_param(k):
                        return res
                    if kwargs.get('d'):
                        return float(res)
                    return res
                except ZeroDivisionError:
                    print("agla: Division durch Null (Krümmung)")
                    return
            print("agla: nur einen Parameterwert angeben")
            return		
		
        else:
            if len(wert) != 1:
                print("agla: einen Punkt in der Ebene  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt der Kurve angeben')
                return	
            x, y = Symbol('x'), Symbol('y')				
            if gl.subs({x:p.x, y:p.y}).lhs != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            try:
                r = abs(einfach(1 / self.kruemm(p)))
            except ZeroDivisionError:
                print('agla: Division durch Null (Krümmung)')
                return 
            if mit_param(r):
                return einfach(r)
            if kwargs.get('d'):
                return float(r)
            return einfach(r)			 
			
    krRadius = kr_radius
	
	
    def stueck(self, *bereich, **kwargs):
        """Kurvenstück / Änderung des Parameterbereiches"""
		 
        if kwargs.get('h'):
            print("\nStück einer Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf     kurve . stück( par_unt, par_ob )\n")		                     
            print("               kurve      Kurve")
            print("               par_unt    untere und obere Bereichsgrenzen")	
            print("               par_ob     des Kurvenparameters\n")
            return 

        if self.dim == 2 and self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')			
            return
			
        bereich = sympify(bereich)
        if not (isinstance(bereich, Tuple) and len(bereich) == 2):  
            print("agla: untere und obere Bereichsgrenzen angeben")
            return			
        if not (is_zahl(bereich[0]) and is_zahl(bereich[1])):			
            print("agla: zwei Zahlenwerte angeben")
            return			
        return Kurve(self.pkt(), (self.par, bereich[0], bereich[1]))
		
	
    def kruemm(self, *wert, **kwargs):
        """Krümmung"""
		
        if kwargs.get('h'):
            print("\nKrümmung der Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf    kurve . krümm( /[ wert ] )\n")		                     
            print("              kurve   Kurve")
            print("              wert    Wert des Kurvenparameters\n")
            print("Rückgabe  bei Angabe eines Parameterwertes:") 
            print("          Krümmung im zugehörigen Kurvenpunkt")
            print("          bei leerer Argumentliste oder freiem Bezeichner:") 
            print("          Krümmung im allgemeinen Kurvenpunkt\n") 			
            print("In der Ebene R^2 (für Kurven, die mittels impliziter Gleichung")
            print("erzeugt wurden):\n")
            print("Aufruf     kurve . krümm( punkt )\n")		                     
            print("               punkt    Punkt der Kurve\n")	
            print("Zusatz    d=1   Dezimaldarstellung\n")
            return				
		
        if self.dim == 3 or (self.dim == 2 and self._typ != 'imp'):				
            par = self.par
            pkt = self.pkt(par)
            p1 = pkt.diff(par)
            p2 = p1.diff(par)
			
        if self.dim == 3:
            try:		
                k = einfach( ( p1.sp(p1) * p2.sp(p2) - (p1.sp(p2))**2 ) 
		                                               / (p1.sp(p1))**3 )
                from sympy import sqrt   # zur Vermeidung eines Fehlers		
                k = sqrt(k)
            except ZeroDivisionError:
                return 
				
        elif self.dim == 2 and self._typ != 'imp':
            try:
                k = determinante(Vektor(p1.x, p2.x), Vektor(p1.y, p2.y)) / \
                    (p1.x**2 + p1.y**2)**Rational(3, 2)
            except ZeroDivisionError:
                return
				
        if self.dim == 3 or (self.dim == 2 and self._typ != 'imp'):				
            if not wert:
                if mit_param(k):
                    return einfach(k)
                if kwargs.get('d'):
                    return float(k)
                return einfach(k)
            if len(wert) == 1:
                pw = sympify(wert[0])
                if not is_zahl(pw):
                    print("agla: einen Zahlenwert angeben")
                    return		
                try:				 
                    pw = nsimplify(pw)
                except RecursionError:
                    pass			 
                res = k.subs(par, pw)
                if mit_param(res):
                    return einfach(res)
                if kwargs.get('d'):
                    return float(res)
                return einfach(res)		 
            print("agla: nur einen Parameterwert angeben")
            return		

        else:
            if len(wert) != 1:
                print("agla: einen Punkt der Kurve  angeben")
                return			
            gl = self.args[0]	
            p = wert[0]
            if not (isinstance(p, Vektor) and p.dim == 2):	
                print('agla: einen Punkt in der Ebene angeben')
                return	
            x, y = Symbol('x'), Symbol('y')
            if gl.subs({x:p.x, y:p.y}).lhs != 0:
                print('agla: einen Punkt der Kurve angeben')
                return
            Fx, Fy = gl.lhs.diff(x), gl.lhs.diff(y)
            zahl = (int, Integer, float, Float, Rational)		   
            Fxx = 0 if isinstance(Fx, zahl) else Fx.diff(x)	   
            Fyy = 0 if isinstance(Fy, zahl) else Fy.diff(y)		   
            Fxy = 0 if isinstance(Fx, zahl) else Fy.diff(y)		   
            Fyx = 0 if isinstance(Fy, zahl) else Fy.diff(x)		   
            d = determinante(Vektor(Fxx, Fyx, Fx), Vektor(Fxy, Fyy, Fy), \
                Vektor(Fx, Fy, 0))
            try:			   
                k = d / (Fx**2 + Fy**2)**Rational(3, 2)
                if not isinstance(k, zahl):			   
                    k = k.subs({x:p.x, y:p.y})
            except ZeroDivisionError:
                print('agla: Division durch Null')			
                return		   
            if mit_param(k):
                return einfach(k)
            if kwargs.get('d'):
                return float(k)
            return einfach(k)			 
		
		
    def wind(self, *wert, **kwargs):
        """Windung, Torsion"""
		
        if self.dim != 3:
            print('agla: nur im Raum R^3 definiert')
            return
			
        if kwargs.get('h'):
            print("\nWindung / Torsion der Kurve\n")	
            print("Im Raum R^3:\n")			
            print("Aufruf    kurve . wind( /[ wert ] )\n")		                     
            print("              kurve   Kurve")
            print("              wert    Wert des Kurvenparameters\n")
            print("Rückgabe  bei Angabe eines Parameterwertes:") 
            print("          Windung im zugehörigen Kurvenpunkt")
            print("          bei leerer Argumentliste oder freiem Bezeichner:") 
            print("          Windung im allgemeinen Kurvenpunkt\n") 			
            print("Zusatz    d=1   Dezimaldarstellung\n")
            return
				
        par = self.par
        pkt = self.pkt(par)
        p1 = pkt.diff(par)
        p2 = p1.diff(par)
        p3 = p2.diff(par)
        k = self.kruemm(par)
        if k != 0:
            w = einfach( 1/k**2 * ( p1.vp(p2).sp(p3) ) / (p1.sp(p1))**3 )
        else:
            print("agla: Division durch Null (Krümmung)")
            return			
		
        if not wert:
            if mit_param(w):
                return w
            if kwargs.get('d'):
                return float(w)
            return w
        if len(wert) == 1:
            pw = sympify(wert[0])
            if not is_zahl(pw):
                print("agla: einen Zahlenwert angeben")
                return	
            try:				 
                pw = nsimplify(pw)
            except RecursionError:
                pass			 
            res = w.subs(par, pw)
            if mit_param(res):
                return res
            if kwargs.get('d'):
                return float(res)
            return res			 
        print("agla: nur einen Parameterwert angeben")
        return		
		
    tors = wind
			

    def par_wert(self, *args, **kwargs):
        """Parameterwert eines Kurvenpunktes"""
		
        if mit_param(self):
            print('agla: nicht implementiert (Parameter)')
            return
            		
        if self.dim == 2 and self._typ == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')	
            return
        		
        if kwargs.get('h'):
            print("\nParameterwert eines Punktes der Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf    kurve . par_wert( punkt, start )\n")		                     
            print("              kurve   Kurve")
            print("              punkt   Punkt")	
            print("              start   Startwert des nummerischen") 
            print("                      Verfahrens\n")	
            print("Der Parameterwert wird über die Minimierung des Abstandes")
            print("des Punktes zu einem Kurvenpunkt gesucht; es wird 'nsolve'") 			
            print("verwendet (siehe SymPy-Dokumentation)\n")
            print("Zusatz   d=1 - Dezimaldarstellung")			
            print("         g=1 - Grafik der Abstandsfunktion")		
            print("              (Abstand des gegebenen Punktes zu den Kur-")
            print("               venpunkten)\n")			
			
            return 
		
        if len(args) != 2:
            print("agla: einen Punkt und einen Startwert angeben")
            return			
        punkt, start = args	
        start = sympify(start)			
        if not (isinstance(punkt, Vektor) and punkt.dim == self.dim and \
            is_zahl(start)):
            if self.dim == 3:
                print("agla: einen Punkt im Raum und einen Startwert angeben")
            else:
                print("agla: einen Punkt in der Ebene und einen " + \
                     "Startwert angeben")			
            return
			
        from numpy import abs		
        start = float(start)
        if kwargs.get('g'):
            import numpy as np
            from numpy import (pi, sqrt, sin, cos, tan, exp, log, sinh, cosh,
                 tanh, arcsin, arccos, arctan, arcsinh, arccosh, arctanh)
            ln = log			 
            import matplotlib.pyplot as plt	
            print("\nAbstandsfunktion")			
            fig = plt.figure(figsize=(4, 3))
            plt.axes().set_aspect('equal')	
            ax = fig.add_subplot(1, 1, 1)		
            t = Symbol('t')		
            aa = str(punkt.abstand(self.pkt(t))**2)
            t = np.arange(float(self.ber[0]), float(self.ber[1]), 1/200.0) 
            y = sqrt(abs(eval(aa)))
            for tick in ax.xaxis.get_major_ticks():
                tick.label1.set_fontsize(9)
                tick.label1.set_fontname('Times New Roman')
            for tick in ax.yaxis.get_major_ticks():
                tick.label1.set_fontsize(9)	
                tick.label1.set_fontname('Times New Roman')
            for pos in ('top', 'bottom', 'right', 'left'): 			
                ax.spines[pos].set_linewidth(0.5)
            plt.plot(t, y)
            plt.show()
            return		
        t = Symbol('t')		
        f = lambda t: punkt.abstand(self.pkt(t))**2
        f1 = lambda t: punkt.abstand(self.pkt(t)).evalf()
        d = kwargs.get('d')		
        try:
           res = nsolve(f(t).diff(t), start)
        except:
            print("agla: mit einem anderen Startwert versuchen\n" + \
                 "      der Punkt ist eventuell kein Kurvenpunkt")
            return	
        if abs(f1(res)) < 10**(-6):
            try:
                res = nsimplify(res)
                if d:
                    return float(res)		
                return res					
            except RecursionError:
                pass
            if d:				
                return float(res)		
            return res	
        else:
            print("agla: mit einem anderen Startwert versuchen\n" + \
                 "      der Punkt ist eventuell kein Kurvenpunkt")
			
    parWert = par_wert		

	
    def schnitt(self, *args, **kwargs):
        """Schnitt mit einer anderen Kurve"""
		
        if self.dim == 2 and self._typ == 'imp':
            print('agla: nicht implementiert (implizite Gleichung)')	
            return
			
        if mit_param(self):		
            print('agla: nicht implementiert (Parameter)')	
            return

        if kwargs.get('h'):
            print("\nParameterwerte eines Schnittpunktes mit einer anderen")
            print("parametrisierten Kurve\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten):\n")			
            print("Aufruf    kurve . schnitt( kurve1, start1, start2 )\n")		                     
            print("              kurve   Kurve")
            print("              start   Startwert des nummerischen Verfahrens\n")
            print("Rückgabe  ( Parameterwert für die gegebene Kurve,")
            print("            Parameterwert für die andere Kurve )\n")			
            print("Die beiden Startwerte für die Kurven sind so genau wie möglich")
            print("anzugeben; die Parameterwerte werden über die Minimierung des")
            print("Abstandes der Kurvenpunkte zueinander gesucht; es wird 'nsolve'")
            print("verwendet (siehe SymPy-Dokumentation)\n")	
            return 
		
        if len(args) != 3:
            print("agla: drei Argumente angeben")
            return
        kurve, start1, start2 = args		
        if isinstance(kurve, Kurve) and mit_param(kurve):
            print("agla: nicht implementiert(Parameter)")
            return			
        start1 = sympify(start1)			
        start2 = sympify(start2)			
        if not (isinstance(kurve, Kurve) and kurve.dim == self.dim 
		        and is_zahl(start1) and is_zahl(start2)):
            if self.dim == 3:
                print("agla: eine Raumkurve und zwei Startwerte angeben")
            else:
                print("agla: eine Kurve in der Ebene und zwei Startwerte " + \
                     "angeben")
            return
        if kurve.dim == 2 and str(kurve.args[-1]) == 'imp':
            print('agla: nicht verfügbar (implizite Gleichung)')	
            return
        try:
            start1, start2 = float(start1), float(start2)	
        except TypeError:
            print("zwei Zahlenwerte angebn")
            return			
        s, t = Symbol("s"), Symbol("t")
        p, q = self.pkt(s), kurve.pkt(t)
        f = lambda s, t: p.abstand(q)**2
        f1 = lambda s, t: p.abstand(q).evalf()
        try:
            gl = [f(s, t).diff(s) , f(s, t).diff(t)]
            res = nsolve(gl, [s, t], (start1, start2))
        except:
            print("agla: mit anderen Startwerten versuchen\n" + \
                 "       eventuell liegt kein Schnittpunkt vor")
            return			
        if abs(f1(s, t).subs(s, res[0, 0]).subs(t, res[1, 0])) < 10**(-6):
            return float(res[0,0]), float(res[1,0])
        else:
            print("agla: mit anderen Startwerten versuchen\n" + \
                 "      eventuell liegt kein Schnittpunkt vor")
            return			

				
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Kurve bei einer Abbildung\n")		
            print("Aufruf   kurve . bild( abb )\n")		                     
            print("             kurve   Kurve")
            print("             abb     Abbildung\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return			
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == self.dim):
            print("agla: eine Abbildung (mit gleicher Dimension) angeben")
            return
        if self.dim == 2 and self._typ == 'imp':
            m, v = abb.inverse.matrix, abb.inverse.versch
            x, y, X, Y = symbols('x y X Y')
            xx = m[0,0]*X + m[0,1]*Y + v.x
            yy = m[1,0]*X + m[1,1]*Y + v.y
            gl = self.args[1][3].subs({x:xx, y:yy})
            gl = expand(gl.lhs.subs({X:x, Y:y}))
            return Kurve(gl)
        p = self.pkt()
        q = p.bild(abb)
        return Kurve(q, (self.par, self.ber[0], self.ber[1]))
	
		
    def proj(self, *ebene, **kwargs):
        """Projektion auf eine Ebene"""
		
        if self.dim != 3:
            print('agla: nur im Raum R^3 definiert')
            return
			
        if kwargs.get('h'):
            print("\nProjektion der Kurve auf eine Ebene\n")
            print("Im Raum R^3:\n")			
            print("Aufruf    kurve . proj( ebene )\n")		                     
            print("              kurve   Kurve")
            print("              ebene   xy-, xz- oder yz-Ebene oder eine zu")
            print("                      einer von diesen parallele Ebene\n")			
            return
			
        par = self.par
        pkt = self.pkt(par)
        if not ebene:
            print("agla: eine Ebene angeben")
            return			
        ebene = ebene[0]
        gl = ebene.koord		
		
        if not isinstance(ebene, Ebene):
            print("agla: eine Ebene angeben")
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')			
        if parallel(ebene, xy_ebene):
            po = Poly(ebene.koord.lhs, z)
            cf = po.all_coeffs()	
            d = -cf[1] if cf[0] > 0 else cf[1]		
            return Kurve(Vektor(pkt.x, pkt.y, d), 
                       (par, self.ber[0], self.ber[1]))
        elif parallel(ebene, xz_ebene):
            po = Poly(ebene.koord.lhs, y)
            cf = po.all_coeffs()	
            d = -cf[1] if cf[0] > 0 else cf[1]		
            return Kurve(Vektor(pkt.x, d, pkt.z), 
                       (par, self.ber[0], self.ber[1]))
        elif parallel(ebene, yz_ebene):
            po = Poly(ebene.koord.lhs, x)
            cf = po.all_coeffs()	
            d = -cf[1] if cf[0] > 0 else cf[1]		
            return Kurve(Vektor(d, pkt.y, pkt.z), 
                       (par, self.ber[0], self.ber[1]))
        else:
            print("agla: nur für die Koordinatenebenen und dazu parallele implementiert")
            return			
	
		
    def winkel(self, *obj, **kwargs):
        """Winkel mit anderen Objekten"""
		
        if kwargs.get('h'):
            print("\nWinkel der Kurve mit einem anderen Objekt (in einem Schnittpunkt)\n")		
            print("Im Raum R^3 und in der Ebene R^2 (Parameterform,")
            print("Funktionsgleichung bzw. Polarkoordinaten), in Grad:\n")			
            print("Aufruf    kurve . winkel( objekt, par_wert_kurve /[, par_wert_objekt ] )\n")
            print("              kurve       Kurve")
            print("              objekt      Gerade, , Kurve, Ebene (im Raum R^3)")
            print("                          Gerade, Kurve (in der Ebene R^2)")			
            print("              par_wert    Parameterwert des Schnittpunktes")
            print("                          par_wert_objekt nur bei objekt=Kurve")
            print("                          diese nicht mit impliziter Gleichung")
            print("                          erzeugt\n")		
            print("In der Ebene R^2 (implizite Gleichung):\n")			
            print("Aufruf    kurve . winkel( objekt, punkt /[, par_wert_objekt ] )\n")			
            print("              punkt       Schnittpunkt der Kurve mit dem Objekt")
            print("              par_wert_objekt nicht bei objekt=Gerade oder Kurve,")	
            print("              erzeugt mit impliziter Gleichung\n")	
            print("Es wird nicht geprüft, ob die angegebenen Parameterwerte zu einem Schnitt-")
            print("punkt gehören bzw. ob der angegebene Punkt ein Schnittpunkt ist\n")		
            return							
			
        def tang_vekt_ok(vv):
            if vv.is_schar:
                vv = vv.sch_el(1)			
            ok = True
            for k in vv.komp:			
                if k + 1 == k:  # erfaßt NaN und oo
                    ok = False
                    break
            return ok					
		
        if len(obj) < 2 or len(obj) > 3:
            print("agla: zwei oder drei Argumente angeben")
            return			
        objekt = obj[0]
        x, y = Symbol('x'), Symbol('y')	
		
        try:		
            if self.dim == 3:
                if not isinstance(objekt, (Gerade, Ebene, Kurve)):
                    raise AglaError("Gerade, Ebene oder Kurve angeben")
                if isinstance(objekt, (Gerade, Kurve)) and objekt.dim != 3:
                    raise AglaError("das Objekt muss die Dimension 3 haben")			
            else:
                if not isinstance(objekt, (Gerade, Kurve)):
                    raise AglaError("Gerade oder Kurve angeben")
                if objekt.dim != 2:
                    raise AglaError("das Objekt muss die Dimension 2 haben")	

            if self.dim == 3:
                if isinstance(objekt, (Gerade, Ebene)):
                    if len(obj) != 2:
                        raise AglaError("ein Objekt und einen " + \
                             "Parameterwert angeben")
                    pw = sympify(obj[1])   
                    if not is_zahl(pw):
                        raise AglaError("für den Parameterwert eine " + \
                             "Zahl angeben")
                    tv = self.tang_vekt(pw)
                    if tang_vekt_ok(tv):					
                        return objekt.winkel(tv)
                    else:
                        raise AglaError("nicht definiert")	
					
                elif isinstance(objekt, Kurve):
                    if len(obj) != 3:
                        raise AglaError("eine Kurve und zwei " + \
                             "Parameterwerte angeben")
                    pw1, pw2 = sympify(obj[1]), sympify(obj[2])   
                    if not (is_zahl(pw1) and is_zahl(pw2)):
                        raise AglaError("für die Parameterwerte " + \
                             "Zahlen angeben")
                    tv1, tv2 = self.tang_vekt(pw1), objekt.tang_vekt(pw2)
                    if not tang_vekt_ok(tv1) or not tang_vekt_ok(tv2): 
                        raise AglaError("nicht definiert")						
                    wi = tv1.winkel(tv2)
                    if wi == 180.0:
                        wi = 0.0
                    return wi						
					
            elif self.dim == 2:
			
                if self._typ != 'imp':
                    if isinstance(objekt, Gerade):
                        if len(obj) != 2:
                            raise AglaError("ein Objekt und einen " + \
                                       "Parameterwert angeben")
                        pw = sympify(obj[1])   
                        if not is_zahl(pw):
                            raise AglaError("für den Parameterwert " + \
                                 "eine Zahl angeben")
                        tv = self.tang_vekt(pw)
                        if not tang_vekt_ok(tv): 
                            raise AglaError("nicht definiert")												
                        return objekt.winkel(tv)
                    else:
                        if str(objekt.args[-1]) != 'imp':                    
                            if len(obj) != 3:
                                raise AglaError("ein Objekt und zwei " + \
                                     "Parameterwerte angeben")
                            pw1, pw2 = sympify(obj[1]), sympify(obj[2])   
                            if not (is_zahl(pw1) and is_zahl(pw2)):
                                raise AglaError("für die Parameterwerte " + \
                                     "Zahlen angeben")
                            tv1, tv2 = self.tang_vekt(pw1), \
                                           objekt.tang_vekt(pw2)
                            if not tang_vekt_ok(tv1) or not tang_vekt_ok(tv2): 
                                raise AglaError("nicht definiert")						
                            wi = tv1.winkel(tv2)
                            if wi == 180.0:
                                wi = 0.0
                            return wi						
                        else:
                            if len(obj) != 2:
                                raise AglaError("ein Objekt und einen " + \
                                     "Punkt angeben")
                            punkt = obj[1]   
                            if not (isinstance(punkt, Vektor) and \
                                                         punkt.dim == 2):
                                raise AglaError("einen Punkt in der " + \
                                     "Ebene angeben")
                            tv1, tv2 = self.tang_vekt(punkt), \
                                               objekt.tang_vekt(punkt)
                            wi = tv1.winkel(tv2)
                            if wi == 180.0:
                                wi = 0.0
                            return wi						
							
                else:
                    if isinstance(objekt, Gerade):	
                        if len(obj) != 2:
                            raise AglaError("ein Objekt und einen Punkt " + \
                                 "angeben")
                        punkt = obj[1]   
                        if not (isinstance(punkt, Vektor) and punkt.dim == 2):
                            raise AglaError("einen Punkt in der Ebene angeben")
                        tv = self.tang_vekt(punkt)
                        return objekt.winkel(tv)	
                    elif str(objekt.args[-1]) != 'imp':				
                        if len(obj) != 3:
                            raise AglaError("ein Objekt, einen Punkt und " + \
                                 "einen Parameterwert angeben")
                        punkt, pw = obj[1], sympify(obj[2])   
                        if not (isinstance(punkt, Vektor) and punkt.dim == 2) \
                                                      and is_zahl(pw):
                            raise AglaError("einen Punkt und " + \
                                 "einen Zahlenwert angeben")
                        tv1, tv2 = self.tang_vekt(punkt), objekt.tang_vekt(pw)
                        wi = tv1.winkel(tv2)
                        if wi == 180.0:
                            wi = 0.0
                        return wi						
                    else:				
                        if len(obj) != 2:
                            raise AglaError("ein Objekt und einen Punkt " + \
                                 "angeben")
                        punkt = obj[1]   
                        if not (isinstance(punkt, Vektor) and punkt.dim == 2):
                            raise AglaError("einen Punkt in der Ebene " + \
                                 "angeben")
                        tv1, tv2 = self.tang_vekt(punkt), \
                                          objekt.tang_vekt(punkt)
                        wi = tv1.winkel(tv2)
                        if wi == 180.0:
                            wi = 0.0
                        return wi						
	
        except AglaError as e:
            print('agla:', str(e))
            return			

			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Kurve"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Kurve in R^3 mit mayavi"""
		
        # 'fein=ja / wert'   - verfeinerte Grafik; default - normale Grafik	
        # 'radius=ja / wert' - Darstellung als Röhre; default - normale Kurve
							
        fein = None	
        radius = None		
        if len(spez) > 4:
            for s in spez[4]:
                s.replace(' ', '').upper()			
                if 'fein' in s:                 			
                    if 'JA' in s or 'MIT' in s or '1' in s:
                        fein = 100
                    else:						
                        fein = eval(s[s.find('=')+1:])                    
                if 'radius' in s:
                    if 'JA' in s or 'MIT' in s or '1' in s:
                        radius = 0.02
                    else:						
                        radius = eval(s[s.find('=')+1:])                                   			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' \
                                                        else spez[2][1]
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
									
        unt, ob = float(self.ber[0]), float(self.ber[1])
        n = 200.0		
        if fein:
            if is_zahl(fein):
                n = float(fein)				
        d = np.abs(ob - unt) / n
        tt = np.arange(unt, ob + 0.5 * d, d)
        t = self.par
        pkt = self.pkt(t)
        if not anim:
            x = np.array([float(pkt.x.subs(t, p)) for p in tt])		
            y = np.array([float(pkt.y.subs(t, p)) for p in tt])		
            z = np.array([float(pkt.z.subs(t, p)) for p in tt])		
            return mlab.plot3d(x, y, z, line_width=lin_staerke, 
                        color=lin_farbe, tube_radius=radius) 
        else:
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20		
				
            _b, _t = Symbol('_b'), Symbol('_t')		
            kk = self.sch_el(_b)
            p = kk.pkt(_t)
            xx, yy, zz = [], [], []	
            xs, ys, zs = str(p.x), str(p.y), str(p.z) 			
            for s in tt:
                xx += [xs.replace('_t', str(s))] 
                yy += [ys.replace('_t', str(s))] 
                zz += [zs.replace('_t', str(s))]
					
            abs=np.abs; pi=np.pi; sqrt=np.sqrt; exp=np.exp; log=np.log
            ln=np.log; sin=np.sin; sinh=np.sinh; Abs=np.abs 
            arcsin=np.arcsin; arsinh=np.arcsinh; cos=np.cos; cosh=np.cosh 
            arccos=np.arccos; arcosh=np.arccosh; tan=np.tan; tanh=np.tanh 
            arctan=np.arctan; artanh=np.arctanh 
            asin=np.arcsin; acos=np.arccos; atan=np.arctan 
            asinh=np.arcsinh; acosh=np.arccosh; atanh=np.arctanh 			
										
            aa = np.linspace(float(aber[0]), float(aber[1]), N) 					
            xa, ya, za = [], [], []
            for bb in aa:   # Abs muss extra ersetzt werden
                bb = '(' + str(bb) + ')'
                xa += [[float(eval(str(x).replace('_b', bb).replace('Abs', 
                       'np.abs'))) for x in xx]]		
                ya += [[float(eval(str(y).replace('_b', bb).replace('Abs', 
                       'np.abs'))) for y in yy]]		
                za += [[float(eval(str(z).replace('_b', bb).replace('Abs', 
                       'np.abs'))) for z in zz]]		
            plt = mlab.plot3d(xa[0], ya[0], za[0], line_width=lin_staerke, 
                        color=lin_farbe, tube_radius=radius)
            return plt, (xa[1:], ya[1:], za[1:]), N-1		
		
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Kurve in R^3 mit vispy"""
		
        pass		
		
		
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Kurve in R^2"""	

        # 'punkte = (Nx,Ny)'  für Anzahl der Stützstellen in x-,y-Richtung
		
        from numpy import (pi, sqrt, sin, cos, tan, exp, log, sinh, cosh, tanh,
             arcsin, arccos, arctan, arcsinh, arccosh, arctanh, abs)
        ln = log
        asin, acos, atan = arcsin, arccos, arctan 
        asinh, acosh, atanh = arcsinh, arccosh, arctanh
        Abs = abs		
		
        import numpy as np		
			
        punkte = None			
        if len(spez) > 4:
            for s in spez[4]:
                s.replace(' ', '')			
                if 'punkte' in s:
                    punkte = eval(s[s.find('=')+1:])                    										
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' else spez[2][3]
        
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:
            if self._typ != 'imp':
                tmin, tmax = self.ber
                t = Symbol('t')				
                p = self.pkt(t).dez
                xs, ys = repr(N(p.x)), repr(N(p.y))   
                t = np.arange(float(tmin), float(tmax), 0.01)
                if not mit_param(p.x):
                    xe = np.empty(len(t)) 
                    xe.fill(p.x)
                else:	
                    xe = eval(xs)		
                if not mit_param(p.y):
                    ye = np.empty(len(t))
                    ye.fill(p.y)					
                else:					
                    ye = eval(ys)				
                return plt.plot(xe, ye, linewidth=lin_staerke, 
                            color=lin_farbe)
            else:
			
                if not punkte is None:
                    if not (isinstance(punkte, (tuple, Tuple, list)) and \
                        len(punkte) == 2):			
                        print('agla: für punkte Tupel/Liste mit zwei ' +
                             'Zahlen angeben')
                        return
                    Nx, Ny = punkte
                    if not (isinstance(Nx, (int, Integer)) and isinstance(Ny, \
                         (int, Integer))):
                        print('agla: zwei ganze Zahlen für Anzahl der ' +
                             'Punkte angeben')
                        return
                    if Nx < 3 or Ny < 3:
                        print("agla: Zahlen > 2 angeben")
                        return												
                else:
                    Nx, Ny = 300, 300
			
                xl, xr, yl, yr = UMG._sicht_box[:4]
                xl, xr, yl, yr = float(xl), float(xr), float(yl), float(yr)
                y, x = np.ogrid[xl:xr:Nx*1j, yl:yr:Ny*1j]  # Reihenfolge!	
                gl = str(self.imp.lhs)
                gl = eval(gl)
                if isinstance(lin_farbe, (tuple, Tuple)):
                    lin_farbe = rgb2hex(lin_farbe) 
                try:					
                    plt.gca().contour(x.ravel(), y.ravel(), gl, [0], \
                            linewidths=lin_staerke, colors=lin_farbe)	
                except:
                    return AglaError				
		
			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        if self.dim == 3:		
            kurve_hilfe(3)
            return			
        kurve_hilfe(4)	
		
    h = hilfe					
			
			
			
# Benutzerhilfe für Kurve
# -----------------------

def kurve_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden im Raum R^3")
        print("h=4 - Eigenschaften und Methoden in der Ebene R^2")
        return
		   
    if h == 2:
        print("\nKurve - Objekt\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")		
        print("             Kurve( par_form, ( par_name, par_unt, par_ob ) )\n")
        print("     oder    Kurve( allg_punkt, ( par_name, par_unt, par_ob ) )\n")
        print("                 par_form     Parameterform der Kurve")  
        print("                 allg_punkt   allgemeiner Kurvenpunkt")  
        print("                 par_name     Name des Kurvenparameters")
        print("                                  freier Bezeichner, standardmäßig t")
        print("                                  v ist nicht zulässig")
        print("                 par_unt      untere, obere Grenzen des Parameter-")
        print("                 par_ob       bereiches\n")  
        print("Erzeugung nur in der Ebene R^2:\n")
        print("             Kurve( gleichung  /[, ( par_name, par_unt, par_ob ) ] )\n")          
        print("                 gleichung kann sein (die Hochkomma sind mitzuschreiben)")
        print("                 'y = f(x)'     Funktionsgleichung   (1)")
        print("                                x, y - kartesische Koordinaten")		
        print("                 'r = f(phi)'   Gleichung in Polarkoordinaten   (2)")	
        print("                                r, phi - Polarkoordinaten   oder")		
        print("                 'F(x, y) = 0'  Implizite Gleichung    oder")
        print("                  F(x, y)       ebenso, rechte Seite = 0 angenommen\n")
        print("                 Die Verwendung der Bezeichner x und y bzw. r und phi ist")
        print("                 zwingend")
        print("                 Bei (1) wird parametrisiert,wobei eventuell mitgeteilte ")
        print("                 Parameterangaben benutzt werden; bei Fehlen derselben ")
        print("                 wird (t, -10, 10) verwendet")		
        print("                 Bei (2) wird automatisch in kartesische Koordinaten trans-")
        print("                 formiert, phi wird durch den angegebenen Parameter ersezt;")
        print("                 bei Fehlen von Parameterangaben wird wie bei (1) verfahren")
        print("                 Für die Parameterangaben kann statt eines Tupels eine")
        print("                 Liste benutzt werden\n")
        print("Sollen weitere Gleichungen einer Kurve in R^2 mit gespeichert werden, sind")
        print("sie über Schlüsselwortparameter mitzuteilen, wobei nur die rechte bzw. linke")
        print("Seite der jeweiligen Gleichung geschrieben wird")		
        print("   prg = (...) oder v(...)   Parameterform bzw. allgemeiner Kurvenpunkt")
        print("   fkt = f(x)     Funktionsgleichung (rechte Seite)")		
        print("   pol = f(phi)   Gleichung in Polarkoordinaten (rechte Seite)")		
        print("   imp = F(x, y)  Implizite Gleichung (li. Seite; re. Seite = 0 angenommen)")
        print("Es wird nicht geprüft, ob diese Gleichungen zu der erzeugten Kurve gehören\n")		
        print("Zuweisung     k = Kurve(...)   (k - freier Bezeichner)\n")
        print("Beispiele\n")
        print("Kurve( v(3*cos(t), 3*sin(t), 1/5*t), (t, 0, 6*pi) )\n")
        print("Kurve( (t, t^2, t^3), (t, -2, 2) )\n")
        print("Kurve( v(5*sin(t), 3*cos(t)), (t, 0, 2*pi), imp=x^2+y^2-9 )\n")
        print("Kurve( 'y = x^2/3' )\n")
        print("Kurve( 'r = phi^2/5', (t, -4*pi, 4*pi) )\n")
        return        
		
    if h == 3: 	
        print("\nEigenschaften und Methoden (M) für Kurve im Raum R^3\n")
        print("k.hilfe               Bezeichner der Eigenschaften und Methoden")
        print("k.ber                 Parameterbereich")
        print("k.beschl(...)      M  Beschleunigungsvektor")	
        print("k.bi_normale(...)  M  Binormale")	
        print("k.bild(...)        M  Bild bei einer Abbildung")
        print("k.bog_länge           Bogenlänge")	
        print("k.dim                 Dimension") 
        print("k.drei_bein(...)   M  Begleitendes Dreibein")	
        print("k.evolute             Evolute")	
        print("k.formeln             Berechnungsformeln")	
        print("k.geschw(...)      M  Geschwindigkeitsvektor")	
        print("k.gleich              Eingabegleichung")
        print("k.h_normale(...)   M  Hauptnormale")	
        print("k.is_eben             Test auf ebene Kurve")	
        print("k.is_schar            Test auf Schar")
        print("k.kr_kreis(...)    M  Krümmungskreis")	
        print("k.kr_radius(...)   M  Krümmungsradius")
        print("k.krümm(...)       M  Krümmung")   
        print("k.norm_ebene(...)  M  Normalebene")   
        print("k.par                 Kurvenparameter")  
        print("k.par_wert(...)    M  Parameterwert für einen Kurvenpunkt")  	
        print("k.pf                  Parameterform")    
        print("k.pkt(...)         M  Punkt der Kurve")    
        print("k.prg                 Parametergleichung ( = k.gleich) ") 
        print("k.proj(...)        M  Projektion auf eine Ebene")    
        print("k.rekt_ebene(...)  M  Rektifizierende Ebene")   
        print("k.sch_el(...)      M  Element einer Schar")
        print("k.sch_par             Parameter einer Schar")
        print("k.schm_ebene(...)  M  Schmiegebene")   
        print("k.schnitt(...)     M  Schnitt mit einer anderen Kurve")
        print("k.stück(...)       M  Kurvenstück")
        print("k.tang_vekt(...)   M  Tangentialvektor ( = k.geschw(...))")
        print("k.tangente(...)    M  Tangente in einem Kurvenpunkt")	
        print("k.tors(...)        M  Torsion ( = k.wind(...))")
        print("k.wind(...)        M  Windung")
        print("k.winkel(...)      M  Winkel mit einem anderen Objekt\n")
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("bi_normale :  biNormale")
        print("bog_länge  :  bogLänge")
        print("drei_bein  :  dreiBein")
        print("h_normale  :  hNormale")
        print("is_eben    :  isEben")
        print("is_schar   :  isSchar")
        print("kr_kreis   :  krKreis")
        print("kr_radius  :  krRadius")
        print("norm_ebene :  normEbene")
        print("par_wert   :  parWert")
        print("rekt_ebene :  rektEbene")
        print("sch_el     :  schEl")
        print("sch_par    :  schPar")
        print("schm_ebene :  schmEbene")
        print("tang_vekt  :  tangVekt\n")
        return
		
    if h == 4: 
        print("\nEigenschaften und Methoden (M) für Kurve in der Ebene R^2\n")
        print("Die mit einem (*) markierten sind für Kurven, die mittels ")		
        print("impliziter Gleichung erzeugt wurden,  nicht verfügbar\n")		
        print("k.hilfe               Bezeichner der Eigenschaften und Methoden")
        print("k.ber                 Parameterbereich  (*)")
        print("k.beschl(...)      M  Beschleunigungsvektor  (*)")
        print("k.bild(...)        M  Bild bei einer Abbildung")
        print("k.bog_länge           Bogenlänge  (*)")		
        print("k.dim                 Dimension") 
        print("k.evolute             Evolute  (*)")
        print("k.fkt                 Funktionsgleichung  (*)")
        print("k.formeln             Berechnungsformeln")
        print("k.geschw(...)      M  Geschwindigkeitsvektor")		
        print("k.gleich              Eingabegleichung")
        print("k.imp                 Implizite Gleichung")
        print("k.in_raum             Konvertierung in Raumkurve  (*)")   
        print("k.is_schar            Test auf Schar")
        print("k.krümm(...)       M  Krümmung")		
        print("k.kr_kreis(...)    M  Krümmungskreis")
        print("k.kr_radius(...)   M  Krümmungsradius")	
        print("k.normale(...)     M  Normale in einem Kurvenpunkt")		
        print("k.par                 Kurvenparameter  (*)")
        print("k.par_wert(...)    M  Parameterwert für einen Kurvenpunkt  (*)")
        print("k.pf                  Parameterform  (*)")    
        print("k.pkt(...)         M  Punkt der Kurve  (*)")		
        print("k.pol                 Gleichung in Polarkoordinaten  (*)")
        print("k.prg                 Parametergleichung  (*)")
        print("k.sch_el(...)      M  Element einer Kurvenschar")
        print("k.sch_par             Parameter einer Schar")
        print("k.schnitt(...)     M  Schnitt mit einem anderen Objekt  (*)")
        print("k.stück(...)       M  Kurvenstück  (*)")
        print("k.tangente(...)    M  Tangente	in einem Kurvenpunkt")
        print("k.tang_vekt(...)   M  Tangentialvektor ( = k.geschw(...))")
        print("k.winkel(...)      M  Winkel mit einem anderen Objekt")
        print("k.zwei_bein(...)   M  Begleitendes Zweibein\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("bog_länge :  bogLänge")
        print("in_raum   :  inRaum")		
        print("is_schar  :  isSchar")
        print("kr_kreis  :  krKreis")
        print("kr_radius :  krRadius")
        print("par_wert  :  parWert")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")
        print("zwei_bein :  zweibein")
        print("tang_vekt :  tangVekt\n")
        return
		