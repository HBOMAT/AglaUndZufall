#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Klassen der sphärischen Geometrie von agla           
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



# Inhalt (Klassen):
#
#   sPunkt			Sphärischer Punkt
#   sGerade			Sphärische Gerade
#   sStrecke		Sphärische Strecke
#   sKreis			Sphärischer Kreis
#   sDreieck		Sphärisches Dreieck
#   sZweieck		Sphärisches Zweieck



import importlib

import numpy as np
from numpy import inf
from scipy.optimize import root

from IPython.display import display, Math

from sympy.abc import *
from sympy.core.symbol import Symbol
from sympy.core.sympify import sympify
from sympy.core.numbers import pi
from sympy.solvers.solvers import solve
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.evalf import N
from sympy import sin, cos, acos, sinh, cosh, acosh, atan

from agla.lib.objekte.basis import AglaObjekt
from sympy.core.containers import Tuple
from sympy.polys.polytools import Poly
from sympy.simplify.simplify import simplify, nsimplify

from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.abbildung import Abbildung
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, kollinear,
   sing, cosg, tang, arccosg, arctang, loese, kug_koord, wert_ausgabe, determinante)
from agla.lib.funktionen.abb_funktionen import drehung, spiegelung
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.objekte.umgebung import UMG  
import agla	
	

	
# sPunkt - Klasse   
# ---------------

class sPunkt(AglaObjekt):                                      
    """
	
sPunkt  - sphärischer Punkt

**Erzeugung** 
	
   sPunkt ( *länge, breite* ) *oder*
   
   sPunkt ( *punkt* ) *oder*
   
   sPunkt ( *x, y, '+' | '-'* ) 
   
**Parameter**

   *länge* : sphärische Koordinate eines Punktes der Einheitssphäre; 
   *länge* :math:`\in [0, 2 \pi]`
		
   *breite* : ebenso; *breite* :math:`\in [-\pi/2, \pi/2]`
   
   *punkt* : Punkt der Einheitssphäre
   
   *x, y* : Koordinaten eines Punktes der Einheitskreisscheibe; '+', '-' - 
   zugehöriger Punkt der Einheitssphäre ober- oder unterhalb der *xy* - Ebene
   				
"""


    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            sPunkt_hilfe(kwargs["h"])		
            return	
				
        try:
            if len(args) not in (1, 2, 3):		
                raise AglaError("1-3 Argumente angeben")
				
            if len(args) == 1:
                p = args[0]
                if not (isinstance(p, Vektor) and p.dim == 3):
                    raise AglaError("Punkt des Raumes angeben")
                try:
                    px = float(p.x)
                except TypeError:
                    px = p.x
                try:
                    py = float(p.y)
                except TypeError:
                    py = p.y
                try:
                    pz = float(p.z)
                except TypeError:
                    pz = p.z						
                p = [ px, py, pz ] 					
					
            elif len(args) == 2:
                l, b = args
                if not (is_zahl(l) and is_zahl(b)):
                    raise AglaError("zwei Zahlenwerte für Länge und Breite angeben")
                if not mit_param(l):
                    if not 0 <= l <= 2*pi:				
                        raise AglaError("Länge aus [0, 2*pi] angeben")
                if not mit_param(b):
                    if not -pi/2 <= b <= pi/2:				
                        raise AglaError("Breite aus [-pi/2, pi/2] angeben")
                if b == pi/2 or b == pi/2 or l == 2*pi:
                    l = 0
                try:
                    l = float(l)
                except TypeError:
                    pass
                try:
                    b = float(b)
                except TypeError:
                    pass					
                p = [ cos(l)*cos(b), sin(l)*cos(b), sin(b) ]                				
				
            elif len(args) == 3:
                x, y, ri = args
                if not (is_zahl(x) and is_zahl(y)):
                    raise AglaError("zwei Zahlenwerte angeben und +/- angeben")
                if not mit_param(x) and not mit_param(y):
                    if x**2 + y**2 > 1:				
                        raise AglaError("Der Punkt liegt außerhalb des Einheitskreises")
                try:
                    x = float(x)
                except TypeError:
                    pass
                try:
                    y = float(y)
                except TypeError:
                    pass						
                if not ri in ('+', '-'):
                    raise AglaError("+ oder - für Lage angeben")
                if ri == '+':
                    p = [ x, y, sqrt(1 - x**2 - y**2) ]
                else:
                    p = [ x, y, -sqrt(1 - x**2 - y**2) ]
				
            return AglaObjekt.__new__(cls, p)
        except AglaError as e:	
            print('agla:', str(e))
            return			
  			
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "sPunktSchar(" + ss + ")"
        return "sPunkt"			

		
# Eigenschaften und Methoden für sPunkt
# -------------------------------------
				
    @property
    def dim(self):              
        """Euklidische Dimension"""
        return 3
			
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        a = self.args[0]
        return a[0].free_symbols.union(a[1].free_symbols). \
                                 union(a[2].free_symbols)
    schPar = sch_par		
	
    @property
    def e(self):
        """Euklidischer Punkt"""
        a = self.args[0]
        return Vektor(*a)
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar	
	
    @property		
    def breite(self):              
        """Breite; sphärische Koordinate"""
        l, b = kug_koord(self)		
        return b

    b = breite		
    phi = breite
		
    @property		
    def laenge(self):              
        """Länge; sphärische Koordinate"""
        l, b = kug_koord(self)		
        return l 

    l = laenge		
    lamda = laenge    # Schreibweise!

    @property		
    def geo_koord(self):              
        """Geografische Koordinaten Breite, Länge"""
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")		
            return		
        l, b = kug_koord(self)		
        if l in (0, pi):
            ll = format(float(l*180/pi), '.2f') + '^\circ'	
        elif l < pi:
            ll = format(float(l*180/pi), '.2f') + '^\circ \:O'	
        elif l > pi:
            ll = format(float((2*pi-l)*180/pi), '.2f') + '^\circ \:W'		
        if b == 0:
            bb = format(float(-b*180/pi), '.2f') + '^\circ'		
        if b < 0:
            bb = format(-float(b*180/pi), '.2f') + '^\circ \:S'
        elif b > 0:
            bb = format(float(b*180/pi), '.2f') + '^\circ \:N'
        return display(Math(bb + ', \:\:\: ' + ll))	
		
    geoKoord = geo_koord				
	
    @property		
    def diam(self):              
        """diametral gegenüber liegender Punkt"""
        p = self.e        		
        return sPunkt(-p) 
		
    gegen = diam		

    @property		
    def polare(self):              
        """Polare"""
        O = Vektor(0, 0, 0)		
        e = Ebene(O, self.e)
        k = Kreis(e, O, 1)
        t = Symbol('t')
        p = k.pkt(t)
        pp = Vektor(N(p.x), N(p.y), N(p.z))
        p0, p1 = pp.subs(t, 0), pp.subs(t, 90)
        return sGerade(sPunkt(p0), sPunkt(p1))
								
    def abstand(self, *punkt, **kwargs):	
        """sphärischer Abstand zu einem anderen Punkt"""
		
        if kwargs.get('h'):
            print("\nSphärischer Abstand des Punktes zu einem anderen Punkt\n")		
            print("Aufruf   spunkt . abstand( spunkt1 )\n")		                     
            print("             spunkt    sphärischer Punkt\n")
            return
        if len(punkt) != 1:
            print('agla: einen anderen Punkt angeben')
            return
        p = punkt[0]			
        if not isinstance(p, sPunkt):
            print("agla: einen sphärischen Punkt angeben")	
        a = abs(acos(self.e.sp(p.e)))
        return wert_ausgabe(a, 12)
		
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        try:
		
            if not self.is_schar or len(self.sch_par) > 1:
                raise AglaError("keine Schar mit einem Parameter")			
		
            if kwargs.get('h'):
                print("\nElement einer Schar von sphärischen Punkten\n")		
                print("Aufruf   spunkt . sch_el( wert )\n")		                     
                print("             spunkt   sphärischer Punkt")
                print("             wert     Wert des Scharparameters")			
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
        try:			
            wert = nsimplify(wert)
        except RecursionError:	
            pass								
        px = self.args[0][0].subs(p, wert)
        py = self.args[0][1].subs(p, wert)
        pz = self.args[0][2].subs(p, wert)
        return sPunkt(Vektor(px, py, pz))			
		
    schEl = sch_el		
		
    def schnitt(self, *obj, **kwargs):  
        """Schnitt mit einer sphärischen Geraden"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nSchnitt des sphärischen Punktes mit einer sphärischen Geraden\n")
            print("Aufruf    spunkt . schnitt( sgerade )\n")		                     
            print("              spunkt    sphärischer Punkt")
            print("              sgerade   sphärische Gerade\n")
            return
				
        try:				
            if len(obj) != 1:
                raise AglaError('ein sphärisches Objekt angeben')
            obj = obj[0]			 
            if not isinstance(obj, sGerade):			 
                raise AglaError("sphärische Gerade angeben")
            if mit_param(obj):
                raise AglaError("nicht implementiert (Parameter)")
        except AglaError as e:
            print('agla:', str(e))
            return	

        S = obj.schnitt(self)			
        return S			
					
					
    def bild(self, *args, **kwargs):  
        """Bild bei einer Isometrie"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nBild des sphärischen Punktes bei einer Isometrie der Sphäre\n")
            print("Aufruf    spunkt . bild( abb )\n")		                     
            print("              spunkt   sphärischer Punkt")
            print("              abb      euklidische Drehung/Spiegelung\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('eine Abbilung des Raumes angeben')
            abb = args[0]			 
            if not isinstance(abb, Abbildung):			 
                raise AglaError('eine Abbilung des Raumes angeben')
            if mit_param(abb):
                raise AglaError("nicht implementiert (Parameter)")
            if not (abs(abb.matrix.D) == 1 and abb.versch == Vektor(0, 0, 0)):
                raise AglaError("Isometrie der Sphäre angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        P = self.e.bild(abb)
        return sPunkt(P)		
					
		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für sPunkt"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für sPunkt mit mayavi"""
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]			
        vv = self.e	# Zurückführen auf Vektor.graf		
        vv.graf((None, spez[1], spez[2], None))
		
    def vispy(self, spez, **kwargs):
        """Grafikelement für sPunkt mit vispy"""
		
        pass		
		
	
    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        sPunkt_hilfe(3)	
		
    h = hilfe		
	
	
# Benutzerhilfe für sPunkt
# ------------------------

def sPunkt_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften")
        return
		   
    if h == 2:
        print("\nsPunkt - Objekt     Sphärischer Punkt\n")
        print("Erzeugung     sPunkt( länge, breite )\n")
        print("                  länge,   sphärische Koord. eines Punktes der Einheitssphäre")
        print("                  breite   (länge aus [0, 2*pi], breite aus [-pi/2, pi/2])\n")		
        print("oder          sPunkt( punkt )\n")
        print("                  punkt    Punkt der Einheitssphäre\n")
        print("oder          sPunkt( x, y, '+' | '-' )\n")
        print("                  x, y       Koord. eines Punktes der Einheitskreisscheibe")
        print("                  '+', '-'   ober-/unterhalb der xy-Ebene\n")
        print("Zuweisung     sp = sPunkt(...)   (sp - freier Bezeichner)\n")
        print("Beispiele")
        print("sPunkt( pi/4, pi/3 )") 
        print("sPunkt( 1/2, 1/3, '+' )\n") 		
        print("Parameter sind aktuell nur bei sphärischen Punkten möglich, für die anderen")
        print("sphärischen Objekte ist das nicht implemntiert\n")		
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für sPunkt\n")
        print("sp.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("sp.abstand(...)   M  Sphärischer Abstand")	
        print("sp.b                 = sp.breite")
        print("sp.breite            Sphärische Koordinate")
        print("sp.bild(...)      M  Bild bei einer Isometrie")
        print("sp.e                 Euklidischer Punkt")
        print("sp.diam              Gegenpunkt")
        print("sp.dim               Euklidische Dimension")
        print("sp.gegen             = sp.diam")
        print("sp.geo_koord         Geografische Koordinaten")
        print("sp.is_schar          Test auf Schar")
        print("sp.l                 = sp.länge")
        print("sp.länge             Sphärische Koordinate")
        print("sp.lamda             = sp.länge / Schreibweise beachten")
        print("sp.phi               = sp.breite")
        print("sp.polare            Polare")
        print("sp.schnitt(...)   M  Schnitt mit einer Geraden")	
        print("ss.sch_el(...)    M  Element einer Schar")
        print("sp.sch_par           Scharparameter\n")	
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")		
        print("geo_koord :  geoKoord")		
        print("is_schar  :  isSchar")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar\n")
        return
		
	
			
# sGerade - Klasse   
# ---------------
	
class sGerade(AglaObjekt):                                      
    """
	
sGerade  - sphärische Gerade

**Erzeugung** 
	
   sGerade ( *spunkt1, spunkt2* ) 
   
**Parameter**

   *spunkt* : sphärischer Punkt 

   """

   
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            sGerade_hilfe(kwargs["h"])		
            return	
						
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            A, B = args
            if not (isinstance(A, sPunkt) and isinstance(B, sPunkt)): 			
                raise AglaError("zwei sphärische Punkte angeben")
            if mit_param(A) or mit_param(B):
                raise AglaError("nicht implementiert (Parameter)")
            if A == B:
                raise AglaError("die Punkte müssen verschieden sein")
            return AglaObjekt.__new__(cls, A, B)		
        except AglaError as e:	
            print('agla:', str(e))
            return			
  			
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "sGeradeSchar(" + ss + ")"
        return "sGerade"		

		
# Eigenschaften und Methoden für sGerade
# --------------------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return 3
				
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        a = self.args
        return a[0].sch_par.union(a[1].sch_par)
		
    schPar = sch_par		
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar	
				
    @property
    def traeger(self):	
        """Euklidischer Kreis"""
        A, B = self.args
        O = Vektor(0, 0, 0) 
        e = Ebene(O, A.e, B.e)
        return Kreis(e, O, 1)		
				
    e = traeger

    @property
    def pol(self):	
        """Zwei Pole"""
        n = self.traeger.ebene.norm.einh_vekt
        return sPunkt(n), sPunkt(-n)		
	
    @property
    def punkte(self):	
        """Erzeugende Punkte"""
        return self.args 			
			
    def pkt(self, *wert, **kwargs):
        """Punkt der sphärischen Geraden"""
		
        if kwargs.get('h'):
            print("\nPunkt der sphärischen Geraden\n")		
            print("Aufruf    sgerade . pkt( /[ wert ] )\n")		                     
            print("              sgerade   sphärische Gerade")
            print("              wert      Wert des Geradenparameters aus [0,2*pi]\n")
            print("Rückgabe      bei Angabe eines Parameterwertes:") 
            print("              Geradenpunkt, der zu diesem Wert gehört")
            print("              bei leerer Argumentliste oder freiem " + \
			       "Bezeichner:") 
            print("              allgemeiner Punkt der Geraden\n") 			
            return
				
        k = self.traeger	
        t = Symbol('t')		
        if not wert:
            p = k.pkt(t*180/pi)
            return sPunkt(p)
        elif len(wert) == 1:
            pw = wert[0]
            if not is_zahl(pw):
                print('agla: Zahlenwert oder freien Bezeichner angeben')
                return	
            if not mit_param(pw) and not 0 <= pw <= 2*pi:
                print('agla: Zahlenwert aus dem Parameterbereich [0, 2*pi] angeben')
                return				
            p = k.pkt(pw * 180 / pi)
            return sPunkt(p)
        else:
            print("agla: einen Parameterwert angeben")
            return		

		
    def schnitt(self, *obj, **kwargs):  
        """Schnitt mit anderem sphärischen Objekt"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nSchnitt der sphärischen Geraden mit einem anderen sphärischen")
            print("Objekt\n")		
            print("Aufruf    sgerade . schnitt( sobjekt )\n")		                     
            print("              sgerade   sphärische Gerade")
            print("              sobjekt   sphärische(r) Punkt, Gerade, Kreis\n")
            return
				
        try:				
            if len(obj) != 1:
                raise AglaError('ein sphärisches Objekt angeben')
            obj = obj[0]			 
            if not isinstance(obj, (sPunkt, sGerade, sKreis)):			 
                raise AglaError("sphärische(n) Punkt, Gerade oder Kreis angeben")
            if mit_param(obj):
                raise AglaError("nicht implementiert (Parameter)")
        except AglaError as e:
            print('agla:', str(e))
            return	

        if obj == self:		
            print("agla: die Geraden sind identisch")
            return	
			
        if isinstance(obj, sPunkt):   # sPunkt
            g = self.e		
            q = obj.e		
            pw = par_wert(g, q)						  
            if pw is not None:
                return obj
            else:
                return set()			
			
        elif isinstance(obj, (sGerade, sKreis)):   
            Kugel = importlib.import_module('agla.lib.objekte.kugel').Kugel
            ek = Kugel(Vektor(0, 0, 0), 1)				
            if isinstance(obj, sGerade):			
                e1, e2 = self.traeger.ebene, obj.traeger.ebene
                r11, r12 = e1.richt
                r21, r22 = e2.richt
                r11 = Vektor(float(r11.x), float(r11.y), float(r11.z), simpl=False)			
                r12 = Vektor(float(r12.x), float(r12.y), float(r12.z), simpl=False)	
                r21 = Vektor(float(r21.x), float(r21.y), float(r21.z), simpl=False)			
                r22 = Vektor(float(r22.x), float(r22.y), float(r22.z), simpl=False)	
                ee1 = Ebene(e1.stuetz, r11, r12)
                ee2 = Ebene(e2.stuetz, r21, r22)
                g = ee1.schnitt(ee2)
                ri = g.richt
                ri = Vektor(float(ri.x), float(ri.y), float(ri.z), simpl=False)
                gg = Gerade(g.stuetz, ri)
                t = Symbol('t')
                p = gg.pkt(t)				
                L = solve((ek.gleich.lhs - 1).subs({x:p.x, y:p.y, z:p.z}))
                S1, S2 = p.subs(t, float(L[0])), p.subs(t, float(L[1]))
                return sPunkt(S1), sPunkt(S2)
            M, r = obj.e.mitte.dez, obj.e.radius
            k1 = Kugel(M, r)
            e, e1 = self.traeger.ebene, obj.traeger.ebene
            g = e.schnitt(e1)       
            S = g.schnitt(ek) 
            gr = 1e-8			
            if len(S) == 0:
                return set()			
            elif len(S) == 1:
                if N(S.abstand(M) - r) < gr:
                    return sPunkt(S)
                else:
                    return set()				
            else:
                if N(S[0].abstand(S[1])) < gr:
                    S = 0.5*(S[0] + S[1])				
                    if N(S.abstand(M) - r) < gr:
                        return sPunkt(S)
                    else:
                        return set()	
                else:
                    SS = []
                    if N(S[0].abstand(M) - r) < gr:
                        SS += [S[0]]					
                    if N(S[1].abstand(M) - r) < gr:
                        SS += [S[1]]	
                    if len(SS) == 0:
                        return set()
                    elif len(SS) == 1:
                        return sPunkt(SS[0])					
                    else:
                        return sPunkt(SS[0]), sPunkt(SS[1])					
					
			
    def normale(self, *punkt, **kwargs):
        """Normale in einem Geradenpunkt"""
		
        if kwargs.get('h'):
            print("\nNormale in einem Punkt der sphärischen Geraden\n")		
            print("Aufruf    sgerade . normale( spunkt )\n")		                     
            print("              sgerade    sphärische Gerade")
            print("              spunkt     sphärischer Punkt\n")
            print("Es wird nicht geprüft, ob der Punkt auf der Geraden liegt\n")
            return
				
        try:				
            if not len(punkt) == 1:
                raise AglaError('einen sphärischen Punkt angeben')
            p = punkt[0]
            if not isinstance(p, sPunkt):
                raise AglaError('einen sphärischen Punkt angeben')
            if mit_param(p):
                raise AglaError('nicht implementiert (Parameter)')
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        po = self.pol[0]
        return sGerade(p, po)
				
		
    def winkel(self, *args, **kwargs):  
        """Winkel mit anderer hyperbolischer Geraden"""
		
        if kwargs.get('h'):
            print("\nWinkel der sphärischen Geraden mit einer anderen sphärischen")
            print("Geraden im gemeinsamen Schnittpunkt\n")		
            print("Aufruf    sgerade . winkel( sgerade1 )\n")		                     
            print("              sgerade   sphärische Gerade\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('sphärische Gerade angeben')
            gg = args[0]		 
            if not isinstance(gg, sGerade):			 
                raise AglaError("sphärische Gerade angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
		
        if gg == self:		
            return 0			
        P1 = self.pol			
        P2 = gg.pol
        wi1 = P1[0].e.winkel(P2[0].e)
        wi2 = P1[0].e.winkel(P2[1].e)
        return wi1, wi2			
		        			

    def bild(self, *args, **kwargs):  
        """Bild der Geraden bei einer Isometrie"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nBild der sphärischen Gerade bei einer Isometrie der Sphäre\n")
            print("Aufruf    sgerade . bild( abb )\n")		                     
            print("              sgerade   sphärische Gerade")
            print("              abb       euklidische Drehung/Spiegelung\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('eine Abbilung des Raumes angeben')
            abb = args[0]			 
            if not isinstance(abb, Abbildung):			 
                raise AglaError('eine Abbilung des Raumes angeben')
            if mit_param(abb):
                raise AglaError("nicht implementiert (Parameter)")
            if not (abs(abb.matrix.D) == 1 and abb.versch == Vektor(0, 0, 0)):
                raise AglaError("Isometrie der Sphäre angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        p1, p2 = self.punkte		
        p1, p2 = p1.e.bild(abb), p2.e.bild(abb)
        return sGerade(sPunkt(p1), sPunkt(p2))		
							
        	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für sGerade"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für sGerade mit mayavi"""

        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        if lin_staerke == UMG._staerke[1][1]:
            tr = '0.0035'
        elif lin_staerke == UMG._staerke[2][1]:	
            tr = '0.0055'		
        elif lin_staerke == UMG._staerke[3][1]:			
            tr = '0.0075'	
			
        k0 = self.traeger	# Zurückführen auf Kreis.graf	
        k0.graf((None, spez[1], spez[2], None, ('radius=' + tr,)))
		
		
    def vispy(self, spez, **kwargs):
        """Grafikelement für sGerade mit vispy"""
		
        pass		
		
		
    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        sGerade_hilfe(3)	
		
    h = hilfe		
		
	
# Benutzerhilfe für sGerade
# -------------------------

def sGerade_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften")
        return
		   
    if h == 2:
        print("\nsGerade - Objekt     Sphärische Gerade\n")
        print("Erzeugung     sGerade( spunkt1, spunkt2 )\n")
        print("                  spunkt   sphärischer Punkt\n")
        print("Zuweisung     sg = sGerade(...)   (sg - freier Bezeichner)\n")
        print("Beispiele")
        print("A = sPunkt(pi/3, -pi/4); B = sPunkt(pi/3, pi/4)")		
        print("sGerade( A, B)\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für sGerade\n")
        print("sg.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("sg.bild(...)       M  Bild bei einer Isometrie")
        print("sg.dim                Euklidische Dimension")		
        print("sg.e                  = sg.träger")		
        print("sg.pol                Pole")
        print("sg.normale(...)    M  Normale in einem Geradenpunkt")
        print("sg.pkt(...)        M  Geradenpunkt")
        print("sg.punkte             Erzeugende Punkte")
        print("sg.schnitt(...)    M  Schnitt mit anderem Objekt")	
        print("sg.träger             Euklidischer Trägerkreis")
        print("sg.winkel(...)     M  Winkel mit anderer Geraden\n")	
        print("Synonymer Bezeichner\n")
        print("hilfe   : h\n")   		
        return
		
		
		
# sStrecke - Klasse   
# -----------------
	
class sStrecke(AglaObjekt):                                      
    """
	
sStrecke  - sphärische Strecke

**Erzeugung** 
	
   sStrecke ( *spunkt1, spunkt2* ) 
   
**Parameter**

   *spunkt* : sphärischer Punkt 

   """
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            sStrecke_hilfe(kwargs["h"])		
            return	
			
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            A, B = args
            if not (isinstance(A, sPunkt) and isinstance(B, sPunkt)): 			
                raise AglaError("zwei sphärische Punkte angeben")
            if mit_param(A) or mit_param(B):
                raise AglaError("nicht implementiert (Parameter)")
            if A == B:
                raise AglaError("die Punkte müssen verschieden sein")
            if B == A.diam:
                raise AglaError("die Punkte dürfen keine Gegenpunkte sein")
            O = Vektor(0, 0, 0)
            ee = Ebene(O, A.e.dez, B.e.dez)
            k = Kreis(ee, O, 1)
            p0, p1 = 0, par_wert(k, ee, B.e.dez)
            if p1 > 180:
                p1 = 360 - p1			
            return AglaObjekt.__new__(cls, k, A, B, [p0, p1])		
        except AglaError as e:	
            print('agla:', str(e))
            return			
		        		
				
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "sStreckeSchar(" + ss + ")"
        return "sStrecke"		

		
# Eigenschaften und Methoden für sStrecke
# ---------------------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        a = self.args
        return a[1].sch_par.union(a[2].sch_par)
		
    schPar = sch_par		
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar			
		
    @property
    def gerade(self):	
        """Sphärische Trägergerade"""
        A, B = self.args[1:3]
        return sGerade(A, B)		
		
    @property
    def traeger(self):	
        """Euklidischer Trägerkreis"""
        return self.args[0]
		
    e = traeger

    @property
    def par(self):	
        """Parameter"""
        return self.args[0].pkt().sch_par.pop()
	
    @property
    def ber(self):	
        """Parameterbereich"""		
        return self.args[3] 		

    @property
    def punkte(self):	
        """Erzeugende Punkte"""
        return self.args[1:3]		
		
    @property
    def laenge(self):	
        """Länge"""
        p1, p2 = self.args[1:3]		
        return p1.abstand(p2) 		

    @property
    def mitte(self):	
        """Mittelpunkt"""
        return self.pkt(0.5) 		
				
    @property		
    def mitt_senkr(self, **kwargs):
        """Mittelsenkrechte der Strecke"""	
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
        m = self.mitte			
        return self.normale(m)

    mittSenkr = mitt_senkr
				
    def pkt(self, *wert, **kwargs):
        """Punkt der sphärischen Strecke"""
		
        if kwargs.get('h'):
            print("\nPunkt der sphärischen Strecke\n")		
            print("Aufruf    sstrecke . pkt( /[ wert ] )\n")		                     
            print("              sstrecke   sphärische Strecke")
            print("              wert       Wert des Streckenparameters aus [0,1]\n")
            print("Rückgabe      bei Angabe eines Parameterwertes:") 
            print("              Streckenpunkt, der zu diesem Wert gehört")
            print("              bei leerer Argumentliste oder freiem " + \
			       "Bezeichner:") 
            print("              allgemeiner Punkt der Strecke\n") 			
            return
								
        g = self.gerade
        u, o = self.ber	
        if mit_param(u) or mit_param(o):
            print("agla: nicht implementiert, Parameter")
            return			
        if not mit_param(u):		
            u = float(u)
        if not mit_param(o):		
            o = float(o)			
        if not wert:
            t = Symbol('t')		
            p = g.e.pkt(u + t * (o - u))
        elif len(wert) == 1:
            pw = wert[0]
            if not is_zahl(pw):
                print('agla: Zahlenwert oder freien Bezeichner angeben')
                return	
            if not mit_param(pw):
                if not u <= u + pw*(o-u) <= o:	
                    print('agla: Wert aus [0,1] angeben')
                    return	
            p = g.e.pkt(u + pw*(o-u))
            p = Vektor(N(p.x), N(p.y), N(p.z), simpl=False)			
        else:
            print("agla: einen Parameterwert angeben")
            return		
        return sPunkt(p)


    def normale(self, *punkt, **kwargs):
        """Normale in einem Streckenpunkt"""
		
        if mit_param(self):
            print('agla; nicht implementiert (Parameter)')
            return			
		
        if kwargs.get('h'):
            print("\nNormale in einem Punkt der sphärischen Strecke\n")		
            print("Aufruf    sstrecke . normale( spunkt )\n")		                     
            print("              sstrecke   sphärische Strecke")
            print("              spunkt     sphärischer Punkt\n")
            print("Es wird nicht geprüft, ob der Punkt auf der Strecke liegt\n")
            return
				
        try:				
            if not len(punkt) == 1:
                raise AglaError('einen sphärischen Punkt angeben')
            p = punkt[0]
            if not isinstance(p, sPunkt):
                raise AglaError('einen sphärischen Punkt angeben')
            if mit_param(p):
                raise AglaError('nicht implementiert (Parameter)')
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        g = self.gerade
        return g.normale(p)
				
		
    def winkel(self, *args, **kwargs):  
        """Winkel mit anderer sphärischer Strecke"""
		
        if kwargs.get('h'):
            print("\nWinkel der sphärischen Strecke mit einer anderen sphäri-")
            print("schen Strecke in einem gemeinsamen Endunkt\n")		
            print("Aufruf    sstrecke . winkel( sstrecke1 )\n")		                     
            print("              sstrecke   sphärische Strecke\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('sphärische Strecke angeben')
            ss = args[0]		 
            if not isinstance(ss, sStrecke):			 
                raise AglaError("sphärische Strecke angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
		
        if ss == self:		
            print("agla: die Strecken sind identisch")
            return	
        A, B = self.punkte
        C, D = ss.punkte
        if A == C:
            G, P, Q = A, B, D   # gemeinsamer P. / Endpunkt self / Endpunkt ss
        elif A == D:
            G, P, Q = A, B, C
        elif  B == C:
            G, P, Q = B, A, D
        elif B == D:
            G, P, Q = B, A, C
        else:
            print("agla: die Strecken haben keinen gemeinsamen Endpunkt")
            return	
        dd = sDreieck(G, P, Q)			
        return dd.winkel[0]		
        
		
    def wink_halb(self, *args, **kwargs):  
        """Winkelhalbierende mit anderer sphärischer Strecke"""
		
        if mit_param(self):
            print('agla; nicht implementiert (Parameter)')
            return			
				
        if kwargs.get('h'):
            print("\nWinkelhalbierende der sphärischen Strecke mit einer anderen")
            print("sphärischen Strecke in einem gemeinsamen Endpunkt\n")		
            print("Aufruf    sstrecke . wink_halb( sstrecke1 )\n")		                     
            print("              sstrecke   sphärische Strecke\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('sphärische Strecke angeben')
            ss = args[0]		 
            if not isinstance(ss, sStrecke):			 
                raise AglaError("sphärische Strecke angeben")
            if mit_param(ss):
                raise AglaError("nicht implementiert (Parameter)")		
        except AglaError as e:
            print('agla:', str(e))
            return	
		
        if ss == self:		
            return self 
			
        A, B = self.punkte
        C, D = ss.punkte
        if A == C:
            G, P, Q = A, B, D   # gemeinsamer P. / Endpunkt self / Endpunkt ss
        elif A == D:
            G, P, Q = A, B, C
        elif  B == C:
            G, P, Q = B, A, D
        elif B == D:
            G, P, Q = B, A, C
        else:
            print("agla: die Strecken haben keinen gemeinsamen Endpunkt")
            return			
        O = Vektor(0, 0, 0)
        e1 = self.traeger.ebene
        e2 = ss.traeger.ebene
        e1n, e2n = e1.norm, e2.norm
        n1 = np.array([float(e1n.x), float(e1n.y), float(e1n.z)])
        n2 = np.array([float(e2n.x), float(e2n.y), float(e2n.z)])
        b1, b2 = np.sqrt(np.dot(n1, n1)), np.sqrt(np.dot(n2, n2))   # Beträge
        nn = list(1/b1*n1 - 1/b2*n2)   
        ewh = Ebene(O, Vektor(nn))
        k = Kreis(ewh, O, 1)
        if ewh.abstand(P.e) * ewh.abstand(Q.e) > 0:   # P, Q auf verschiedenen Seiten von ewh
            nn = 1/b1*n1 + 1/b2*n2   
            ewh = Ebene(O, Vektor(nn))
            k = Kreis(ewh, O, 1)
        P1, Q1 = k.pkt(0), k.pkt(45)
        return sGerade(sPunkt(P1), sPunkt(Q1))				
					
    winkHalb = wink_halb					

	
    def bild(self, *args, **kwargs):  
        """Bild der Strecke bei einer Isometrie"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nBild der sphärischen Strecke bei einer Isometrie der Sphäre\n")
            print("Aufruf    strecke . bild( abb )\n")		                     
            print("              sstrecke   sphärische Strecke")
            print("              abb        euklidische Drehung/Spiegelung\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('eine Abbilung des Raumes angeben')
            abb = args[0]			 
            if not isinstance(abb, Abbildung):			 
                raise AglaError('eine Abbilung des Raumes angeben')
            if mit_param(abb):
                raise AglaError("nicht implementiert (Parameter)")
            if not (abs(abb.matrix.D) == 1 and abb.versch == Vektor(0, 0, 0)):
                raise AglaError("Isometrie der Sphäre angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        p1, p2 = self.punkte		
        p1, p2 = p1.e.bild(abb), p2.e.bild(abb)
        return sStrecke(sPunkt(p1), sPunkt(p2))		
							        	
	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für sStrecke"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für sStrecke mit mayavi"""
        		
        from mayavi import mlab	
					
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]			
        if lin_staerke == UMG._staerke[1][1]:
            tr = '0.0035'
        elif lin_staerke == UMG._staerke[2][1]:	
            tr = '0.0055'		
        elif lin_staerke == UMG._staerke[3][1]:			
            tr = '0.0075'	
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        # Modifizieren des  Codes von Kreis.graf			
        n = 70
        kk = self.traeger
        ber = self.ber
        ee = kk.ebene		
        v1 = ee.richt[0]
        v2 = -v1.vp(ee.norm)
        v1 = v1.einh_vekt
        v2 = v2.einh_vekt
        sin, cos = np.sin, np.cos	
        v1x, v1y, v1z = float(v1.x), float(v1.y), float(v1.z)		
        v2x, v2y, v2z = float(v2.x), float(v2.y), float(v2.z)		
        t = np.linspace(float(ber[0]/180*np.pi), float(ber[1]/180*np.pi), n)
        x = np.cos(t)*v1x + np.sin(t)*v2x
        y = np.cos(t)*v1y + np.sin(t)*v2y
        z = np.cos(t)*v1z + np.sin(t)*v2z
        mlab.plot3d(x, y, z, line_width=lin_staerke, color=lin_farbe, tube_radius=tr)  

		
    def vispy(self, spez, **kwargs):
        """Grafikelement für sStrecke mit vispy"""
		        
        pass
				

    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        sStrecke_hilfe(3)	
		
    h = hilfe		
		
		
# Benutzerhilfe für sStrecke
# --------------------------		
							
def sStrecke_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nsStrecke - Objekt     Sphärische Strecke\n")
        print("Erzeugung     sStrecke( spunkt1, spunkt2 )\n")
        print("                  spunkt   sphärischer Punkt\n")
        print("Zuweisung     ss = sStrecke(...)   (ss - freier Bezeichner)\n")
        print("Beispiele")
        print("A = sPunkt(0, -pi/4); B = sPunkt(0, pi/4)")		
        print("sStrecke( A, B)\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für sStrecke\n")
        print("ss.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("ss.ber               Parameterbereich")
        print("ss.bild(...)      M  Bild bei einer Isometrie")
        print("ss.dim               Euklidische Dimension")
        print("ss.e                 = ss.träger")
        print("ss.gerade            sphärische Trägergerade")
        print("ss.länge             Länge")
        print("ss.mitte             Mittelpunkt")
        print("ss.mitt_senkr        Mittelsenkrechte")
        print("ss.normale(...)   M  Normale in einem Streckenpunkt")
        print("ss.pkt(...)       M  Streckenpunkt")
        print("ss.punkte            Erzeugende Punkte")
        print("ss.träger            Euklidischer Kreis")
        print("ss.winkel(...)    M  Winkel mit anderer Strecke")	
        print("ss.wink_halb(...) M  Winkelhalbierende mit anderer Strecke\n") 
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")		
        print("mitt_senkr :  mittSenkr")		
        print("wink_halb  :  winkHalb\n")
        return

				
	
# sKreis - Klasse   
# -----------------
	
class sKreis(AglaObjekt):                                      
    """
	
sKreis  - sphärischer Kreis

**Erzeugung** 
	
   sKreis ( *mitte, radius* ) 
   
**Parameter**

   *mitte* : sphärischer Punkt - Mittelpunkt
   
   *radius* : Radius

   """
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            sKreis_hilfe(kwargs["h"])		
            return	
			
        try:
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            M, r = args
            if not (isinstance(M, sPunkt) and is_zahl(r)): 			
                raise AglaError("einen sphärischen Punkt und einen Radius angeben")
            if mit_param(M) or mit_param(r):
                raise AglaError("nicht implementiert (Parameter)")
            if not mit_param(r):				
                if not 0 <= r <= pi: 			
                    raise AglaError("Radius aus [0,pi] angeben")		
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        return AglaObjekt.__new__(cls, M, r)				
		        		
				
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "sKreisSchar(" + ss + ")"
        return "sKreis"		

		
# Eigenschaften und Methoden für sKreis
# -------------------------------------
			
    @property
    def dim(self):              
        """Dimension"""
        return 3
					
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        a = self.args
        return a[0].sch_par.union(a[1].free_symbols)

    schPar = sch_par		
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar	
									
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
		
    r = radius
	
    @property		
    def traeger(self):              
        """Euklidischer Träger-Kreis"""
        m, r = self.args		
        R = sin(r)
        M = cos(r) * m.e
        e = Ebene(M, m.e)
        return Kreis(e, M, R)
          
    e = traeger		
	
    @property		
    def umfang(self):              
        """Umfang"""   
        return 2 * pi * sin(self.radius)		
    def umfang_(self, **kwargs):              
        """Umfang; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'L' + '=' + '2 \\pi \\sin r \quad\quad r - Radius'
            display(Math(txt))
            return
        h = kwargs.get('h')
        l = self.laenge
        if mit_param(l):
            if h:
                print("\nf=1  - Formel\n")
                return			
            return l	
        if h:			
            print("\nkein Argument - Länge (dezimal)")
            print("f=1  - Formel\n")
            return						
        return N(l)	
		
    Umfang = umfang_
	
    @property		
    def flaeche(self):                   
        """Flächeninhalt"""
        return 2 * pi * (1 - cos(self.radius))	
    def flaeche_(self, **kwargs):              
        """Fläche; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'A' + '=' + '2 \\pi \; (1-\\cos r) \\quad\\quad r - Radius'
            display(Math(txt))
            return	
        h = kwargs.get('h')
        f = self.flaeche
        if mit_param(f):
            if h:
                print("\nf=1  - Formel\n")
                return	
            return f				
        if h:			
            print("\nkein Argument - Fläche (dezimal)")
            print("f=1  - Formel\n")
            return			
        return N(f)			
		
    Flaeche = flaeche_		
				
				
    def bild(self, *args, **kwargs):  
        """Bild des Kreises bei einer Isometrie"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nBild des sphärischen Kreises bei einer Isometrie der Sphäre\n")
            print("Aufruf    skreis . bild( abb )\n")		                     
            print("              skreis   sphärischer Kreis")
            print("              abb      euklidische Drehung/Spiegelung\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('eine Abbilung des Raumes angeben')
            abb = args[0]			 
            if not isinstance(abb, Abbildung):			 
                raise AglaError('eine Abbilung des Raumes angeben')
            if mit_param(abb):
                raise AglaError("nicht implementiert (Parameter)")
            if not (abs(abb.matrix.D) == 1 and abb.versch == Vektor(0, 0, 0)):
                raise AglaError("Isometrie der Sphäre angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        m = self.mitte		
        m1 = m.e.bild(abb)
        return sKreis(sPunkt(m1), self.radius)		
					

    def schnitt(self, *obj, **kwargs):  
        """Schnitt mit sphärischer Geraden"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nSchnitt des sphärischen Keises mit einer sphärischen Geraden\n")
            print("Aufruf    skreis . schnitt( sgerade )\n")		                     
            print("              skreis    sphärischer Kreis")
            print("              sgerade   sphärische Gerade\n")
            return
				
        try:				
            if len(obj) != 1:
                raise AglaError('eine sphärische Gerade angeben')
            obj = obj[0]			 
            if not isinstance(obj, sGerade):			 
                raise AglaError("sphärische Gerade angeben")
            if mit_param(obj):
                raise AglaError("nicht implementiert (Parameter)")
        except AglaError as e:
            print('agla:', str(e))
            return	
        return obj.schnitt(self)			
		        	
					
    def graf(self, spez, **kwargs):                       
        """Grafikelement für sKreis"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für sKreis mit mayavi"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]	
        if lin_staerke == UMG._staerke[1][1]:
            tr = '0.0035'
        elif lin_staerke == UMG._staerke[2][1]:	
            tr = '0.0055'		
        elif lin_staerke == UMG._staerke[3][1]:			
            tr = '0.0075'	
			
        kk = self.traeger		
        kk.graf((None, spez[1], spez[2], None, ('radius=' + tr,)))

    def vispy(self, spez, **kwargs):
        """Grafikelement für sKreis mit vispy"""	
		
        pass		
						
						
    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        sKreis_hilfe(3)	
		
    h = hilfe		

	
# Benutzerhilfe für sKreis
# ------------------------
	
def sKreis_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nsKreis - Objekt     Sphärischer Kreis\n")
        print("Erzeugung     sKreis( mitte, radius )\n")
        print("                  mitte    sphärischer Punkt")
        print("                  radius   Radius\n")
        print("Zuweisung     sk = sKreis(...)   (sk - freier Bezeichner)\n")
        print("Beispiel")
        print("sKreis( sPunkt(pi/4, pi/3), 3/2 )\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für sKreis\n")

        print("sk.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("sk.bild(...)     M  Bild bei einer Isometrie")
        print("sk.dim              Euklidische Dimension")
        print("sk.e                = sk.träger")
        print("sk.fläche           Flächeninhalt")
        print("sk.fläche_(...)  M  ebenso, zugehörige Methode")
        print("sk.M                = sk.mitte")
        print("sk.m                = sk.mitte")
        print("sk.mitte            Mittelpunkt")
        print("sk.r                = sk.radius")
        print("sk.radius           Radius")
        print("sk.schnitt(...)  M  Schnitt mit sphärischer Geraden")
        print("sk.träger           Euklidischer Träger-Kreis")
        print("sk.umfang           Umfang")
        print("sk.umfang_(...)  M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe   :  h")		
        print("fläche_ :  Fläche")	
        print("umfang_ :  Umfang\n")
        return


		
# sDreieck - Klasse   
# -----------------
	
class sDreieck(AglaObjekt):                                      
    """
	
sDreieck  - sphärisches Dreieck

**Erzeugung** 
	
   sDreieck ( *spunkt1, spunkt2, spunkt3* ) 
   
**Parameter**

   *spunkt* : sphärischer Punkt 

   """
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            sDreieck_hilfe(kwargs["h"])		
            return	
			
        try:
            if len(args) != 3:
                raise AglaError("drei Argumente angeben")
            A, B, C = args
            if not (isinstance(A, sPunkt) and isinstance(B, sPunkt) and \
               isinstance(C, sPunkt)): 			
                raise AglaError("drei sphärische Punkte angeben")	
            if mit_param(A) or mit_param(B) or mit_param(C):
                raise AglaError("nicht implementiert (Parameter)")
            if A == B or A == C or B == C:
                raise AglaError("die Punkte müssen verschieden sein")
        except AglaError as e:	
            print('agla:', str(e))
            return	
        return AglaObjekt.__new__(cls, A, B, C)				
			
			
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "sDreieckSchar(" + ss + ")"
        return "sDreieck"		

		
# Eigenschaften und Methoden für sDreieck
# ---------------------------------------
			
    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        a = self.args
        return a[0].sch_par.union(a[1].sch_par).union(a[2].sch_par)
		
    schPar = sch_par		
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar	
						
    @property
    def punkte(self):
        """Eckpunkte"""
        return self.args

    @property
    def laengen(self):
        """Seitenlängen"""
        A, B, C = self.args       		
        return B.abstand(C), A.abstand(C), A.abstand(B)	
	
    @property
    def umfang(self):
        """Umfang"""
        A, B, C = self.args        		
        return B.abstand(C) + A.abstand(C) + A.abstand(B)	
	
    @property
    def seiten(self):
        """Seiten"""
        A, B, C = self.args        		
        return sStrecke(B, C), sStrecke(C, A), sStrecke(A, B)	
	
    @property
    def winkel(self):
        """Innenwinkel"""
        a, b, c = self.laengen
        # Berechnung nach dem 	Seitenkosinussatz
        wia = arccosg((cos(a)-cos(b)*cos(c))/(sin(b)*sin(c)))
        wib = arccosg((cos(b)-cos(a)*cos(c))/(sin(a)*sin(c)))
        wic = arccosg((cos(c)-cos(a)*cos(b))/(sin(a)*sin(b)))
        return N(wia), N(wib), N(wic)	

    @property
    def wink_summe(self):
        """Innenwinkelsumme"""
        wia, wib, wic = self.winkel
        return wia + wib + wic
		
    winkSumme = wink_summe		
				
    @property
    def flaeche(self):
        """Flächeninhalt"""
        wi = self.winkel 		
        return N(((wi[0]+wi[1]+wi[2]) - 180) * pi / 180)		
		
    @property
    def inkreis(self):
        """Inkreis"""
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
        ss = self.seiten
        wh1 = ss[1].wink_halb(ss[2])		
        wh2 = ss[0].wink_halb(ss[2])	
        M, M1 = wh1.schnitt(wh2)
        A, B, C = self.args        				
        if A.abstand(M1) + B.abstand(M1) + C.abstand(M1) < A.abstand(M) + \
                                              B.abstand(M) + C.abstand(M):
            M = M1											  
        a, b, c = self.laengen
        wic = arccosg((cos(c)-cos(a)*cos(b))/(sin(a)*sin(b)))		
        tr = tang(wic/2)*sin(1/2*(a+b+c)-c) 
        R = N(abs(atan(tr)))
        return sKreis(M, R)		
						
    @property
    def umkreis(self):
        """Umkreis"""
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return			
        A, B, C = self.args	
        ss = self.seiten;
        s1, s2 = ss[0], ss[1]
        ms1 = s1.normale(s1.mitte)
        ms2 = s2.normale(s2.mitte) 
        M, M1 = ms1.schnitt(ms2)
        if M.abstand(A) > pi/2:
            M = M1
        return sKreis(M, N(M.abstand(A)))			
		  			
					
    def bild(self, *args, **kwargs):  
        """Bild des Dreiecks bei einer Isometrie"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nBild des sphärischen Dreiecks bei einer Isometrie der Sphäre\n")
            print("Aufruf    sdreieck . bild( abb )\n")		                     
            print("              sdreieck   sphärisches Dreieck")
            print("              abb        euklidische Drehung/Spiegelung\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('eine Abbilung des Raumes angeben')
            abb = args[0]			 
            if not isinstance(abb, Abbildung):			 
                raise AglaError('eine Abbilung des Raumes angeben')
            if mit_param(abb):
                raise AglaError("nicht implementiert (Parameter)")
            if not (abs(abb.matrix.D) == 1 and abb.versch == Vektor(0, 0, 0)):
                raise AglaError("Isometrie der Sphäre angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        p1, p2, p3 = [self.punkte[i].e.bild(abb) for i in (0, 1, 2)]		
        return sDreieck(sPunkt(p1), sPunkt(p2), sPunkt(p3))		
							        	
					
    def graf(self, spez, **kwargs):                       
        """Grafikelement für sDreieck"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für sDreieck mit mayavi"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
        if lin_staerke == UMG._staerke[1][1]:
            tr = '0.0035'
        elif lin_staerke == UMG._staerke[2][1]:	
            tr = '0.0055'		
        elif lin_staerke == UMG._staerke[3][1]:			
            tr = '0.0075'	
				
        p1, p2, p3 = self.punkte			
        s1, s2, s3 = sStrecke(p1, p2), sStrecke(p1, p3), sStrecke(p2, p3)
        ( s1.graf((None, spez[1], spez[2], None, ('radius=' + tr,))),
          s2.graf((None, spez[1], spez[2], None, ('radius=' + tr,))),
          s3.graf((None, spez[1], spez[2], None, ('radius=' + tr,))) )
		
    def vispy(self, spez, **kwargs):
        """Grafikelement für sDreieck mit vispy"""

        pass		
	

    @property
    def exzess(self):
        """Exzess"""
        w = self.wink_summe	- 180 
        return w
		
    defekt = exzess		

				
    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        sDreieck_hilfe(3)	
		
    h = hilfe		
				
				
# Benutzerhilfe für sDreieck
# --------------------------
				
def sDreieck_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nsDreieck - Objekt     Sphärisches Dreieck\n")
        print("Erzeugung     sDreieck( spunkt1, spunkt2, spunkt3 )\n")
        print("                  spunkt   sphärischer Punkt\n")
        print("Zuweisung     sd = sDreieck(...)   (sd - freier Bezeichner)\n")
        print("Beispiele")
        print("A = sPunkt(pi/3, pi/4); B = sPunkt(0, pi/4); C = sPunkt(pi/3, 0)")		
        print("sDreieck( A, B, C)") 
        print("sDreieck( sPunkt(0.3, 0.4, '+'), sPunkt(0.1, -0.5, '+'), sPunkt(-0.2, 0.1, '-') )\n")		
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für sDreieck\n")
        print("sd.hilfe           Bezeichner der Eigenschaften und Methoden")
        print("sd.bild(...)    M  Bild bei einer Isometrie")
        print("sd.defekt          = sd.exzeß")
        print("sd.dim             Euklidische Dimension")
        print("sd.exzeß           Exzeß (in Grad)")
        print("sd.fläche          Flächeninhalt")
        print("sd.inkreis         Inkreis")
        print("sd.längen          Seitenlängen")
        print("sd.punkte          Eckunkte")
        print("sd.seiten          Seiten")	
        print("sd.umfang          Umfang")
        print("sd.umkreis         Umkreis")
        print("sd.winkel          Innenwinkel")	
        print("sd.wink_summe      Innenwinkelsumme \n")	
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")		
        print("wink_summe :  winkSumme\n")		
        return
	
	
	
# sZweieck - Klasse   
# -----------------
	
class sZweieck(AglaObjekt):                                      
    """
	
sZweieck  - sphärisches Zweieck

**Erzeugung** 
	
   sZweieck ( *ecke, spunkt1, spunkt2* ) 
   
**Parameter**

   *ecke* : sphärischer Punkt - eine Ecke
   
   *spunkt* : sphärischer Punkt - ein Punkt je Seite

   """
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            sZweieck_hilfe(kwargs["h"])		
            return	
			
        try:
            if len(args) != 3:
                raise AglaError("drei Argumente angeben")
            A, B, C = args
            if not (isinstance(A, sPunkt) and isinstance(B, sPunkt) and \
               isinstance(C, sPunkt)): 			
                raise AglaError("drei sphärische Punkte angeben")					
            if mit_param(A) or mit_param(B) or mit_param(C):
                raise AglaError("nicht implementiert (Parameter)")
            if A == B or A == C or B == C:
                raise AglaError("die Punkte müssen verschieden sein")
        except AglaError as e:	
            print('agla:', str(e))
            return
			
        return AglaObjekt.__new__(cls, A, B, C)				
	
	
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "sZweieckSchar(" + ss + ")"
        return "sZweieck"		

		
# Eigenschaften und Methoden für sZweieck
# ---------------------------------------	
	
    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        a = self.args
        return a[0].sch_par.union(a[1].sch_par).union(a[1].sch_par). \
              union(a[2].sch_par)		
    schPar = sch_par		
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    @property
    def punkte(self):
        """Ecke und ein Punkt je Seite"""
        return self.args	
	
    @property
    def seiten(self):
        """Seiten"""
        A, B, C = self.args        		
        return sGerade(A, B), sGerade(A, C)	
	
    @property
    def umfang(self):
        """Umfang"""
        return 2 * pi		
	
    @property
    def winkel(self):
        """Innenwinkel"""
        A, B, C = self.args
        s1, s2 = sStrecke(A, B), sStrecke(A, C)
        wi = s1.winkel(s2)
        if wi > 90:
            wi = 180 - wi
        return wi
		
    @property
    def flaeche(self):
        """Flächeninhalt"""
        return N(2 * self.winkel /180 * pi)

    def bild(self, *args, **kwargs):  
        """Bild des Zweiecks bei einer Isometrie"""
		
        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        if kwargs.get('h'):
            print("\nBild des sphärischen Zweiecks bei einer Isometrie der Sphäre\n")
            print("Aufruf    szweieck . bild( abb )\n")		                     
            print("              szweieck   sphärisches Zweieck")
            print("              abb        euklidische Drehung/Spiegelung\n")
            return
				
        try:				
            if len(args) != 1:
                raise AglaError('eine Abbilung des Raumes angeben')
            abb = args[0]			 
            if not isinstance(abb, Abbildung):			 
                raise AglaError('eine Abbilung des Raumes angeben')
            if mit_param(abb):
                raise AglaError("nicht implementiert (Parameter)")
            if not (abs(abb.matrix.D) == 1 and abb.versch == Vektor(0, 0, 0)):
                raise AglaError("Isometrie der Sphäre angeben")
        except AglaError as e:
            print('agla:', str(e))
            return	
			
        p1, p2, p3 = [self.punkte[i].e.bild(abb) for i in (0, 1, 2)]		
        return sZweieck(sPunkt(p1), sPunkt(p2), sPunkt(p3))		
							        			
		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für sZweieck"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für sZweieck mit mayavi"""	
							
        if len(spez) > 4:
            for s in spez[4]:
                exec(s)			
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]			
        if lin_staerke == UMG._staerke[1][1]:
            tr = '0.0035'
        elif lin_staerke == UMG._staerke[2][1]:	
            tr = '0.0055'		
        elif lin_staerke == UMG._staerke[3][1]:			
            tr = '0.0075'	
			
        ss = self.seiten
        k1, k2 = ss[0].traeger, ss[1].traeger		
        t = Symbol('t')
        Kurve = importlib.import_module('agla.lib.objekte.kurve').Kurve	
        P1 = k1.pkt(t)
        Q1 = Vektor(N(P1.x), N(P1.y), N(P1.z), simpl=False)		
        ku1 = Kurve(Q1, (t, 0, 180))
        P2 = k2.pkt(t)
        Q2 = Vektor(N(P2.x), N(P2.y), N(P2.z), simpl=False)
        ku2 = Kurve(Q2, (t, 0, 180))
        ( ku1.graf((None, spez[1], spez[2], None, ('radius=' + tr,))),
          ku2.graf((None, spez[1], spez[2], None, ('radius=' + tr,))) )
	
    def vispy(self, spez, **kwargs):
        """Grafikelement für sZweieck mit vispy"""	
		
        pass		
	
	
    @property					
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        sZweieck_hilfe(3)	
		
    h = hilfe		

	
# Benutzerhilfe für sZweieck
# --------------------------
	
def sZweieck_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nsZweieck - Objekt     Sphärisches Zweieck\n")
        print("Erzeugung     sZweieck( ecke, spunkt1, spunkt2 )\n")
        print("                  ecke     sphärischer Punkt - eine Ecke")		
        print("                  spunkt   sphärischer Punkt - ein Punkt je Seite\n")
        print("Zuweisung     sz = sZweieck(...)   (sz - freier Bezeichner)\n")
        print("Beispiel")
        print("A = sPunkt(pi/5, -pi/4); B = sPunkt(pi/3, pi/4); C = sPunkt(0, pi/4)")		
        print("sZweieck( A, B, C)\n") 
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden für sZweieck\n")
        print("sz.hilfe         Bezeichner der Eigenschaften und Methoden")
        print("sz.bild(...)  M  Bild bei einer Isometrie")
        print("sz.dim           Euklidische Dimension")
        print("sz.fläche        Flächeninhalt")
        print("sz.punkte        Eckpunkte")
        print("sz.seiten        Seiten")	
        print("sz.umfang        Umfang")
        print("sz.winkel        Innenwinkel\n")	
        print("Synonymer Bezeichner\n")
        print("hilfe :  h\n")		
        return
	
	
	
# Parameterwert für einen Kreispunkt - Hilfsfunktion
# --------------------------------------------------
	
def par_wert(kreis, ebene, punkt):
    v1 = ebene.richt[0].dez
    v2 = -v1.vp(ebene.norm).dez
    v1 = v1.einh_vekt.dez
    v2 = v2.einh_vekt.dez
    r = float(kreis.radius)
    gl = kreis.mitte.dez + r*cos(t)*v1 + r*sin(t)*v2
    p0 = sPunkt(gl.subs(t, 0))
    if not mit_param(punkt) and not mit_param(p0):	
        pp = sPunkt(punkt)
        d = float(pp.abstand(p0))   # sphärischer Abstand	
        p1 = gl.subs(t, d)	
        if N(abs(p1.abstand(punkt))) < 1e-6:
            return float(d*180/pi)
        return -float(d*180/pi)		
    dt = p0.sp(punkt)
    return acos(dt)*180/pi	 
	
		
	
