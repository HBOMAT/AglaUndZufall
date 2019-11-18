#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Dreieck - Klasse  von agla           
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
import matplotlib.patches as patches

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.abc import t
from sympy.simplify.simplify import simplify, nsimplify
from sympy.core.symbol import Symbol
from  sympy.solvers.solvers import solve
from sympy import Piecewise
from sympy.core.numbers import Integer, Rational

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.kugel import Kugel
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (is_zahl, mit_param, det,
    wert_ausgabe, ja, Ja, nein, Nein, mit, ohne)
from agla.lib.funktionen.graf_funktionen import hex2color
import agla

	

# Dreieck - Klasse
# ----------------   
	
class Dreieck(AglaObjekt):                                      
    """Dreieck im Raum und in der Ebene
	
**Erzeugung** 
	
   Dreieck ( *punkt1, punkt2, punkt3* )

**Parameter**

   *punkt* : Eckpunkt   
   
    """
	
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            dreieck_hilfe(kwargs["h"])		
            return	
			
        try:			
            if len(args) != 3:
                raise AglaError("drei Punkte angeben")
            a, b, c = args
            Vektor = agla.lib.objekte.vektor.Vektor
            if not (isinstance(a, Vektor) and isinstance(b, Vektor) and \
                                                 isinstance(c, Vektor)):
                raise AglaError("drei Punkte angeben")                			
            if not (a.dim in (2, 3) and b.dim == a.dim and c.dim == a.dim):
                raise AglaError("drei Punkte in der Ebene oder im Raum angeben")
            if Vektor(a, b).kollinear(Vektor(a, c)):
                raise AglaError("die Punkte liegen auf einer Geraden")
        except AglaError as e:
            print('agla:', str(e))
            return			
			
        return AglaObjekt.__new__(cls, a, b, c)
        
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Dreieckschar(" + ss + ')'
        return "Dreieck"					
   		
		
# Für Dreiecke in R^3 und R^2 gemeinsame Eigenschaften + Methoden
# ---------------------------------------------------------------
		
    @property
    def dim(self):              
        """Dimension"""
        return self.args[0].dim
		
    @property
    def punkte(self):
        """Eckpunkte"""
        return self.args[:]
    def punkte_(self, **kwargs):
        """Eckpunkte; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nAusgabe: Eckpunkte (in der Reihenfolge ihrer Eingabe)\n")
            return
        return self.punkte
		
    @property
    def A(self):
        """Erster Eckpunkt"""
        return self.args[0]
		
    @property
    def B(self):
        """Zweiter Eckpunkt"""
        return self.args[1]
		
    @property
    def C(self):
        """Dritter Eckpunkt"""
        return self.args[2]
		
    @property
    def a(self):
        """Länge(B, C)"""
        return Vektor(self.B, self.C).betrag
		
    @property
    def b(self):
        """Länge(C, A)"""
        return Vektor(self.C, self.A).betrag
		
    @property
    def c(self):
        """Länge(A, B)"""
        return Vektor(self.A, self.B).betrag

    @property
    def alpha(self):
        """Winkel bei A"""
        return Vektor(self.A, self.B).winkel(Vektor(self.A, self.C))
		
    @property
    def beta(self):
        """Winkel bei B"""
        return Vektor(self.B, self.A).winkel(Vektor(self.B, self.C))

    @property
    def gamma(self):
        """Winkel bei C"""
        return Vektor(self.C, self.A).winkel(Vektor(self.C, self.B))
		
    @property
    def schwer_pkt(self):              
        """Schwerpunkt"""
        return (self.args[0] + self.args[1] + self.args[2]) * Rational(1, 3)
    
    schwerPkt = schwer_pkt
	
    @property	
    def ebene(self):              
        """Trägerebene; nur im Raum"""
        if self.dim != 3:
            print("nur für Dreiecke im Raum R^3 verfügbar")		
            return
        pfad = 'agla.lib.objekte.'
        Vektor = importlib.import_module(pfad + 'vektor').Vektor	
        Ebene = importlib.import_module(pfad +'ebene').Ebene	
        a = self.args		
        return Ebene(a[0], Vektor(a[0], a[1]), Vektor(a[0], a[2]))

    @property			
    def laengen(self):              
        """Seitenlängen"""
        return ( self.punkte[1].abstand(self.punkte[2]), 
		         self.punkte[2].abstand(self.punkte[0]), 
		         self.punkte[0].abstand(self.punkte[1]) )
    def laengen_(self, **kwargs):              
        """Seitenlängen; zugehörige Methode"""
        l0, l1, l2 = self.laengen
        h = kwargs.get('h')
        d = kwargs.get('d')			
        if h:
            print('\nAusgabe: Länge(2, 3), Länge(3, 1), Länge(1, 2)')
            print('Länge(i, j)  - Länge der Strecke zwischen dem i. und dem j.') 
            print('               Punkt in der Reihenfolge ihrer Eingabe\n')			
            print('kein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkommastellen\n')
            return
        l0 = l0 if mit_param(l0) else float(l0) 
        l1 = l1 if mit_param(l1) else float(l1) 
        l2 = l2 if mit_param(l2) else float(l2) 
        return wert_ausgabe(l0, d), wert_ausgabe(l1, d), wert_ausgabe(l2, d)		
				
    Laengen = laengen_
	
    @property
    def umfang(self):
        """Umfang"""
        return self.a + self.b + self.c
    def umfang_(self, **kwargs):
        """Umfang; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        w = self.umfang        
        d = kwargs.get('d')
        return wert_ausgabe(w, d)	
		
    Umfang = umfang_
	
    @property
    def winkel(self):
        """Innenwinkel"""
        a, b, c = self.punkte
        Vektor = agla.lib.objekte.vektor.Vektor		
        return ( Vektor(a, b).winkel(Vektor(a, c)), Vektor(b, a).
		         winkel(Vektor(b, c)), Vektor(c, a).winkel(Vektor(c, b)) )
    def winkel_(self, **kwargs):              
        """Innenwinkel; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nAusgabe:\n')
            print('Winkel(Vektor(1, 2), Vektor(1, 3)')
            print('Winkel(Vektor(2, 1), Vektor(2, 3)')
            print('Winkel(Vektor(3, 1), Vektor(3, 2)')			
            print('Vektor(i, j)  - Vektor zwischen dem i. und dem j.') 
            print('                Punkt in der Reihenfolge ihrer Eingabe\n')			
            print('kein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        w0, w1, w2 = self.winkel
        d = kwargs.get('d')			
        return wert_ausgabe(w0, d), wert_ausgabe(w1, d), wert_ausgabe(w2, d)		
	
    Winkel = winkel_
	
    @property
    def wink_summe(self):
        """Summe der Innenwinkel"""
        wa, wb, wc = self.winkel
        return wa + wb + wc
		
    winkSumme = wink_summe		
	
    @property			
    def sch_par(self):              
        """Scharparameter"""
        return ( self.args[0].free_symbols.union(self.args[1].free_symbols).
		         union(self.args[2].free_symbols) )
				 
    schPar = sch_par				 
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1

    isSchar	= is_schar	
		
    @property
    def seiten(self):
        """Seiten (Strecken)"""
        a, b, c = self.punkte
        return Strecke(b, c), Strecke(c, a), Strecke(a, b)
    def seiten_(self, **kwargs):
        """Seiten; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nAusgabe: Seite(2, 3), Seite(3, 1), Seite(1, 2)')
            print('Seite(i, j)  - Strecke zwischen dem i. und dem j. Punkt')
            print('               in der Reihenfolge ihrer Eingabe\n')
            return
        return self.seiten			
	
    Seiten = seiten_
	
    @property
    def is_recht_wink(self):
        """Test auf Rechtwinkligkeit"""
        a, b, c = self.punkte
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        ab_ac = Vektor(a, b).sp(Vektor(a, c))
        ba_bc = Vektor(b, a).sp(Vektor(b, c))
        ca_cb = Vektor(c, a).sp(Vektor(c, b))
        return ab_ac == 0 or ba_bc == 0 or ca_cb == 0
		
    isRechtWink = is_recht_wink	
		
    @property
    def flaeche(self):	
        """Flächeninhalt"""
        a, b, c = self.punkte
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        if self.dim == 2:		
            a, b, c = Vektor(a.x, a.y, 0), Vektor(b.x, b.y, 0), \
                     Vektor(c.x, c.y, 0)		
        d = Vektor(a, b).vp(Vektor(a, c))
        return Rational(1, 2) * d.betrag
    def flaeche_(self, **kwargs): 
        """Flächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = '(1) \qquad ' + 'A' + '=' + '\\frac{1}{2}' + '\,c\, h_c' + '\qquad ' + \
                  'A' + '=' + '\\frac{1}{2}' + '\,a\, h_a' + '\qquad ' + \
                  'A' + '=' + '\\frac{1}{2}' + '\,b\, h_b'				  
            display(Math(txt))
            txt = '(2) \qquad ' + 'A' + '=' + '\\frac{1}{2}' + '\,a\, b\,sin(\\gamma)' + '\qquad ' + \
                 'A' + '=' + '\\frac{1}{2}' + '\,a\, c\,sin(\\beta)' + '\qquad ' + \
				   'A' + '=' + '\\frac{1}{2}' + '\,b\, c\,sin(\\alpha)' + '\qquad '
            display(Math(txt))
            txt = '(3) \qquad ' + 'A' + '=' + '\\frac{1}{2}\,' + '\\sqrt{\\vec{a}^2\,\\vec{b}^2 - \
			        (\\vec{a} \\circ \\vec{b})^2}'
            display(Math(txt))
            if self.dim == 3:			
                txt = '(4) \qquad ' + 'A' + '=' + '\\frac{1}{2}\,' + '\\left| \, \\vec{a} \\times \\vec{b} \
			             \, \\right|'
                display(Math(txt))
            txt = 'a,\, b,\, c - Seiten,\:\: h_a,\,h_b,\,h_c - Hoehen,\:\: \\alpha,\, \\beta,\,\
                     \\gamma - Innenwinkel, \:\: \\vec{a},\, \\vec{b} - Spannvektoren'			
            display(Math(txt))
            print('\n')			
            return			
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('                        n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formeln\n')
            return
        w = self.flaeche
        d = kwargs.get('d')
        return wert_ausgabe(w, d)
		
    Flaeche = flaeche_
		
    @property
    def inkreis(self):
        """Inkreis"""
        a, b, c = self.laengen
        p = self.punkte
        m = 1/(a+b+c) * (a*p[0] + b*p[1] + c*p[2])   # m,r siehe Wikipedia
        m = m.einfach		
        r = simplify(2*self.flaeche / (a+b+c))
        if self.dim == 3:
            return Kreis(self.ebene, m, r) 	
        return Kreis(m, r) 	
		
    inKreis = inkreis	
		
    @property
    def umkreis(self):
        """Umkreis"""
		
        # vektorieller Ansatz für Mittelpunkt M(x,y,z) in R^3
        #    I   v(A,C) * v(M, mitte(A,C) = 0
        #   II   v(B,C) * v(M, mitte(B,C) = 0
        #  III        n * v(M, mitte(A,C) = 0	
        #   n - Normalenvektor der Dreiecksebene
        #   Lösung des LGS mit Cramerscher Regel		
  				
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix	
        A, B, C = self.punkte	
        if self.dim == 3:		
            n = self.ebene.norm
        else:			
            A, B, C = Vektor(A.x, A.y, 0), Vektor(B.x, B.y, 0), \
			           Vektor(C.x, C.y, 0)
            n = Vektor(0, 0, 1)
        M = Matrix(Vektor(C.x-A.x, C.x-B.x, n.x), Vektor(C.y-A.y, \
		        C.y-B.y, n.y), Vektor(C.z-A.z, C.z-B.z, n.z))
        mBC, mAC = 1/2*(B+C), 1/2*(A+C)
        b = Vektor((C-A).sp(mAC), (C-B).sp(mBC), n.sp(mAC))
        x = simplify(det(b, M.vekt[1], M.vekt[2]) / M.D) 			
        y = simplify(det(M.vekt[0], b, M.vekt[2]) / M.D) 			
        z = simplify(det(M.vekt[0], M.vekt[1], b) / M.D)
        m = Vektor(x, y, z)		
        r = m.abstand(A)
        if self.dim == 3:	
            return Kreis(self.ebene, m, r) 
        m = Vektor(x, y)			
        return Kreis(m, r) 	
		
    umKreis = umkreis
	
    @property
    def umkugel(self):
        """Umkugel; nur im Raum"""
        if self.dim == 2:
            print("agla: nur im Raum R^3 verfügbar")		
            return
        u = self.umkreis
        m, r = u.mitte, u.radius			
        return Kugel(m, r)
		
    @property
    def in_figur(self):
        """Konvertierung in Figur; nur in der Ebene"""
        if self.dim != 2:
            print("agla: nur in der Ebene R^2 verfügbar")		
            return		
        ecken = [p for p in self.punkte]
        ecken += [ecken[0]]		
        kanten = [[0, 1], [1, 2], [2, 3]]
        Figur = importlib.import_module('agla.lib.objekte.figur').Figur	
        return Figur(ecken, kanten)		
	
    inFigur = in_figur

    @property
    def in_koerper(self):
        """Konvertierung in Körper; nur im Raum"""
        if self.dim != 3:
            print("agla: nur im Raum R^3 verfügbar")		
            return		
        ecken = [p for p in self.punkte]
        kanten = [[0, 1], [1, 2], [2, 0]]
        Koerper = importlib.import_module('agla.lib.objekte.koerper').Koerper	
        return Koerper(ecken, kanten)		
	
    inKoerper = in_koerper

	
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Dreieckschar\n")		
            print("Aufruf   dreieck . sch_el( wert )\n")		                     
            print("             dreieck    Dreieck")
            print("             wert       Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if not wert or len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter ' +
                  'angeben')	
            return
        try:		
            wert = nsimplify(wert)	
        except RecursionError:
            pass		
        a, b, c = self.punkte
        if a.has(p):
            a = a.sch_el(wert)
        if b.has(p):
            b = b.sch_el(wert)
        if c.has(p):
            c = c.sch_el(wert)
        return Dreieck(a, b, c)		

    schEl = sch_el
	
		
    def pkt(self, *wert, **kwargs):
        """Dreieckpunkt"""   
		
        if kwargs.get('h'):
            print("\nPunkt des Dreiecks\n")		
            print("Aufruf   dreieck . pkt( /[ wert ] )\n")		                     
            print("             dreieck   Dreieck")
            print("             wert      Wert des Dreieckparameters\n")
            print("Rückgabe   bei Angabe eines Parameterwertes aus [0, 1]:")
            print("           Punkt des Dreiecks, der zu diesem Wert gehört")		
            print("           (Parameter ist die Weglänge vom ersten Punkt aus,")
            print("           die gesamte Länge der Strecke wird auf 1 gesetzt")
            print("           - es werden Werte aus dem Intervall [0, 1] angenommen)")
            print("           bei fehlendem Wert oder freiem Parameter:")
            print("           allgemeiner Punkt des Dreiecks\n")
            return
				
        t = Symbol('t')				
        p0 = self.seiten[2].gerade.pkt(t)				
        p1 = self.seiten[0].gerade.pkt(t)				
        p2 = self.seiten[1].gerade.pkt(t)		
        tt = simplify(self.umfang)
        t0 = simplify(self.laengen[2] / tt)
        t1 = simplify((self.laengen[2] + self.laengen[0]) / tt)		
        p = Piecewise( (p0.subs(t, 0), t<=0), 
		               (p0, t<t0),  
					     (p1.subs(t, t-t0), t<t1), 
                      (p2.subs(t, t-t1), t<1),
                      (p2.subs(t, 1),  1<=t) )

        if not wert:
            return p
        if len(wert) == 1:
            if mit_param(wert[0]):
                return p.subs(t, wert[0])
            if not (0 <= wert[0] <= 1):
                print("agla: Wert aus [0, 1] angeben")
                return				
            pw = simplify(sympify(wert[0]))
            try:
                pp = p.subs(t, pw).einfach
            except AttributeError:
                pp = p.subs(t, pw)			
            return pp	 
        print("agla: Parameterwert angeben")
        return 
		
		
    def schnitt(self, *objekt, **kwargs):
        """"Schnitt mit anderen Objekten"""
				
        if kwargs.get('h'):
            print("\nSchnitt des Dreiecks mit einem anderen Objekt\n")		
            print("Aufruf   dreieck . schnitt( objekt )\n")		                     
            print("             dreieck   Dreieck")
            print("             objekt    Punkt, Gerade  (im Raum R^3)")
            print("                       Punkt  (in der Ebene R^2)\n")
            print("Zusatz       l=1   Lageinformationen\n")			
            return
	
        dim = 3 if self.dim == 3 else 2
		
        try:
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")
            objekt = objekt[0]
            Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
            if self.dim == 3:			
                if not isinstance(objekt, (Vektor, Gerade)):
                    raise AglaError("Punkt oder Gerade angeben")
            else:
                if not isinstance(objekt, Vektor):
                    raise AglaError("einen Punkt angeben")			
            if mit_param(self) or mit_param(objekt):
                raise AglaError('nicht implementiert (Parameter)')			
            if objekt.dim != self.dim or not objekt.dim in (2, 3):
                raise AglaError("Objekt mit passender Dimension angeben")
            if self.dim == 2:
                a, b, c = self.punkte
                a, b, c = Vektor(a.x, a.y, 0), Vektor(b.x, b.y, 0), \
                         Vektor(c.x, c.y, 0)
                self = Dreieck(a, b, c)
                objekt = Vektor(objekt.x, objekt.y, 0)
        except AglaError as e:
            print('agla:', str(e))
            return			
        if isinstance(objekt, Gerade):
            S = objekt.schnitt(self.ebene)
            if not S:
                if kwargs.get('l'):
                    display(Math('{{text{die Gerade schneidet das ' + \
					          'Dreieck nicht}'))
                    return					
                return set()
            elif isinstance(S, Vektor):
                S1 = self.schnitt(S)
                if kwargs.get('l'):
                    if S1:				         
                        display(Math('\\text{die Gerade schneidet das' + \
                              ' Dreieck im Punkt}' + S1.punkt_ausg_(s=1)))                        	
                    else:						
                        display(Math('\\text{die Gerade schneidet das' + \
                               'Dreieck nicht}'))
                    return				
                return S1
				
            else:   # S ist Gerade in der Dreieckebene
                a, b, c = self.seiten
                S1 = [a.schnitt(S), b.schnitt(S), c.schnitt(S)]
                S2 = [el for el in S1 if el]
                SS = None					 
                for el in S2:
                    if isinstance(el, Strecke):
                        SS = el
                        break
                    if not el:
                        continue
                if not SS:
                    if len(S2) == 1:
                        SS = S2[0]
                    else:
                        if S2[0] != S2[1]:
                           SS = Strecke(S2[0], S2[1])
                        else:
                            SS = S2[0]						
                if kwargs.get('l'):
                    if isinstance(SS, Vektor):                						
                        display(Math('\\text{die Gerade schneidet das ' + \
                                    'Dreieck im Punkt }'))
                        SS.punkt_ausg						  
                        return	
                    else:
                        display(Math('\\text{die Gerade schneidet das ' + \
                              'Dreieck in einer Strecke}'))
                        return							  
                return SS					
           
        a, b, c = self.punkte
        v1, v2 = Vektor(a, b), Vektor(a, c)
        r, s = Symbol("r"), Symbol("s")
        gl = v1*r + v2*s
        obj = Vektor(a, objekt)
        di = solve([gl.x - obj.x, gl.y - obj.y, gl.z - obj.z])
        if not di:
            if kwargs.get('l'):
                display(Math('\\text{der Punkt liegt nicht im Dreieck}'))
                return				
            return set()
        di = di[0]
        if 0 <= di[r] <= 1 and 0 <= di[s] <= 1 and di[r] + di[s] <= 1:
            if kwargs.get('l'):
                display(Math('\\text{der Punkt liegt im Dreieck}'))
                return
            if dim == 2:
                objekt = Vektor(objekt.x, objekt.y)			
            return objekt
        else:
            if kwargs.get('l'):
                display(Math('\\text{der Punkt liegt nicht im Dreieck}'))
                return				
            return set()
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Dreiecks bei einer Abbildung\n")		
            print("Aufruf   dreieck . bild( abb )\n")		                     
            print("             dreieck    Dreieck")
            print("             abb        Abbildung\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return			
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == self.dim):
            print("agla: eine Abbildung (mit gleicher Dimension) angeben")
            return			
        m = abb.matrix
        if m.det != 0:
            p, q, r = self.punkte
            p1, q1, r1 = p.bild(abb), q.bild(abb), r.bild(abb)
            return Dreieck(p1, q1, r1)
        else:
            k = self.in_koerper
            return k.bild(abb)

			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Dreieck"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Dreieck in R^3 mit mayavi"""
		
        # 'füll=True' - gefüllte Darstellung
										
        fuell = None			
        if len(spez) > 4:
            for s in spez[4]:
                if 'fuell' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper() or '1' in s.upper():
                        fuell = True
			
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' \
                     else spez[2][1]
        if not isinstance(lin_farbe, tuple):
            lin_farbe = hex2color(lin_farbe)		
					 
        flaech_farbe = lin_farbe
		
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3][:2]

        a, b, c = self.punkte
        if not anim:		
            x = [float(p.x) for p in (a, b, c, a)]
            y = [float(p.y) for p in (a, b, c, a)]
            z = [float(p.z) for p in (a, b, c, a)]
            if not fuell:				
                return mlab.plot3d(x, y, z, line_width=lin_staerke, 
		                      color=lin_farbe, tube_radius=None)
            else:
                dreieck = [(0, 1, 2)]
                return mlab.triangular_mesh(x, y, z, dreieck, \
                           color=flaech_farbe)
        else:
            return None   # in Grafik-Routinen auf Koerper -> Strecke zurückgeführt
					
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Dreieck in R^3 mit vispy"""
		
        pass

		
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Dreieck in R^2"""	

        # 'füll=True' - gefüllte Darstellung; default - ungefülte Darstellung	
								
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else \
		                                                     spez[1]		
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
            points = [[el.x, el.y] for el in list(self.punkte)]	
            if not fuell:	
                polygon = patches.Polygon(points, fill=None, 
                         edgecolor=lin_farbe, linewidth=lin_staerke)
                plt.gca().add_patch(polygon)
            else:
                polygon = patches.Polygon(points, facecolor=lin_farbe, 
                         edgecolor=lin_farbe)
                plt.gca().add_patch(polygon)
		

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        dreieck_hilfe(3)	
		
    h = hilfe		
		
		
# Benutzerhilfe für Dreieck
# -------------------------

def dreieck_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nDreieck - Objekt\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")
        print("             Dreieck( A, B, C )\n")
        print("                 A, B, C   Eckpunkte\n")
        print("Zuweisung    d = Dreieck(...)   (d - freier Bezeichner)\n")
        print("Beispiel")
        print("A = v(1, -2, -1); B = v(-1, 0, 3); C = v(1, 5, -2)")
        print("Dreieck(A, B, C)\n")
        return
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Dreieck\n")
        print("d.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("d.A                1. Eckpunkt")
        print("d.B                2. Eckpunkt")
        print("d.C                3. Eckpunkt")
        print("d.a                Länge(B, C)")
        print("d.b                Länge(C, A)")
        print("d.c                Länge(A, B)")
        print("d.alpha            Winkel bei A")
        print("d.beta             Winkel bei B")
        print("d.gamma            Winkel bei C")
        print("d.bild(...)     M  Bild bei einer Abbildung")
        print("d.dim              Dimension")
        print("d.ebene            Trägerebene  (im Raum R^3)")
        print("d.fläche           Flächeninhalt")
        print("d.fläche_(...)  M  ebenso, zugehörige Methode")
        print("d.in_figur         Konvertierung in Figur  (in der Ebene R^2)")
        print("d.in_körper        Konvertierung in Körper  (im Raum R^3)")
        print("d.inkreis          Inkreis")
        print("d.is_recht_wink    Test auf Rechtwinkligkeit")
        print("d.is_schar         Test auf Schar")
        print("d.längen           Seitenlängen")
        print("d.längen_(...)  M  ebenso, zugehörige Methode")
        print("d.pkt(...)      M  Dreieckpunkt")
        print("d.punkte           Eckpunkte")
        print("d.sch_el (...)  M  Element einer Schar")
        print("d.sch_par          Parameter einer Schar")
        print("d.schnitt(...)  M  Schnittmenge mit anderen Objekten")
        print("d.schwer_pkt       Schwerpunkt")
        print("d.seiten           Seiten")
        print("d.seiten_(...)  M  ebenso, zugehörige Methode")
        print("d.umkreis          Umkreis")
        print("d.umfang           Umfang")
        print("d.umfang_(...)  M  ebenso, zugehörige Methode")
        print("d.umkugel          Umkugel")
        print("d.winkel           Innenwinkel")
        print("d.winkel_(...)  M  ebenso, zugehörige Methode")
        print("d.wink_summe       Summe der Innenwinkel\n")
        print("Synonyme Bezeichner\n")
        print("hilfe         :  h")
        print("fläche_       :  Fläche")
        print("in_figur      :  inFigur")
        print("in_körper     :  inKörper")
        print("is_recht_wink :  isRechtWink")
        print("is_schar      :  isSchar")		
        print("längen_       :  Längen")
        print("sch_el        :  schEl")
        print("sch_par       :  schPar")
        print("schwer_pkt    :  schwerPkt")
        print("seiten_       :  Seiten")
        print("umfang_       :  Umfang")
        print("winkel_       :  Winkel")
        print("wink_summe    :  winkSumme\n")
        return
   
		