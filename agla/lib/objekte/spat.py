#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Spat - Klasse  von agla           
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

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.core.symbol import Symbol
from sympy.abc import t
from sympy.simplify import nsimplify

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.objekte.prisma import Prisma
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    wert_ausgabe) 
from agla.lib.funktionen.graf_funktionen import _arrow 			
import agla



# Spat - Klasse 
# -------------  
	
class Spat(AglaObjekt):                                      
    """Spat im Raum
	
**Erzeugung** 
	
   Spat ( */[ stütz, ] spann1, spann2, spann3* )

**Parameter**

   *stütz* : Stützvektor
   
   *spann* : Spannvekor   
   
    """
	
			
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            spat_hilfe(kwargs["h"])		
            return	
			
        try:			
            if len(args) in [3,  4]:
                if len(args) == 3:
                    a, b, c = args
                    if not (isinstance(a, Vektor) and a.dim == 3 and
                           isinstance(b, Vektor) and b.dim == 3 and
                           isinstance(c, Vektor) and c.dim == 3):
                        raise AglaError("drei Vektoren im Raum angeben")
                    if a.kollinear(b) or a.kollinear(c) or b.kollinear(c):
                        raise AglaError("die Spannvektoren dürfen nicht " + \
                             "kollinear sein")
                    if not (a.betrag or b.betrag or c.betrag):
                        raise AglaError("der Nullvektor kann nicht " + \
                             "Spannvektor sein")
                    s = a.O
                else:
                    s, a, b, c = args
                    if not (isinstance(a, Vektor) and a.dim == 3 and
                           isinstance(b, Vektor) and b.dim == 3 and
                           isinstance(c, Vektor) and c.dim == 3 and
					          isinstance(s, Vektor) and s.dim == 3):
                        raise AglaError("vier Vektoren im Raum angeben")
                    if a.kollinear(b) or a.kollinear(c) or b.kollinear(c):
                        raise AglaError("die Spannvektoren dürfen " + \
                             "nicht kollinear sein")
                    if not (a.betrag or b.betrag or c.betrag):
                        raise AglaError("der Nullvektor kann nicht " + \
                             "Spannvektor sein")
					
                return AglaObjekt.__new__(cls, s, a, b, c)            
						
            else:
                raise AglaError("drei oder vier Argumente angeben")
		
        except AglaError as e:
            print('agla:', str(e))
            return			
		
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Spatschar(" + ss + ")"
        return "Spat"			

		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def punkte(self):
        """Eckpunkte"""
        s, a, b, c = self.args
        return (s, s + a, s + a + b, s + b, s + c, s + a + c, s + a + b + c,
               s + b + c)
    def punkte_(self, **kwargs): 
        """Eckpunkte; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nAusgabe:") 
            print("Punkt / Ortsvektor")
            print(" 0 Stützvektor")
            print(" 1 Stützvektor + Spannvektor0")
            print(" 2 Stützvektor + Spannvektor0 + Spannvektor1")
            print(" 3 Stützvektor + Spannvektor1")
            print(" 4 Stützvektor + Spannvektor2")
            print(" 5 Stützvektor + Spannvektor0 + Spannvektor2")
            print(" 6 Stützvektor + Spannvektor0 + Spannvektor1 + " + \
                 "Spannvektor2")
            print(" 7 Stützvektor + Spannvektor1 + Spannvektor2\n")
            return
        return self.punkte		

    Punkte = punkte_		
		
    @property			
    def laengen(self):              
        """Seitenlängen"""
        s, a, b, c = self.args		
        return a.betrag, b.betrag, c.betrag
    def laengen_(self, **kwargs):              
        """Seitenlängen; zugehörige Methode"""
        l0, l1, l2 = self.laengen
        d = kwargs.get('d')
        return wert_ausgabe(l0, d), wert_ausgabe(l1, d), wert_ausgabe(l2, d)
		
    Laengen = laengen_		
		
    @property			
    def volumen(self):              
        """Volumen"""
        a, b, c = self.args[1:]		
        return abs(a.vp(b).sp(c))
    def volumen_(self, **kwargs):              
        """Volumen; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'V' + '=' + ' \\left| \, ( \\vec{a} \\times \\vec{b} ) \\circ \\vec{c}' + \
                  '\, \\right| \;\;\;\;\;\;\;\;\; \\vec{a},\, \\vec{b} , \, \\vec{c} - Spannvektoren '			
            display(Math(txt))
            return			
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('                        n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        vol = self.volumen
        d = kwargs.get('d')
        return wert_ausgabe(vol, d)
	
    Volumen = volumen_	
	
    @property
    def stuetz(self):
        """Stützvektor"""
        return self.args[0]
		
    @property
    def spann(self):
        """Spannvektoren"""
        return self.args[1:]		
		
    @property
    def winkel(self):
        """Winkel zwischen den Spannvektoren"""
        a, b, c = self.args[1:]
        return a.winkel(b), a.winkel(c), b.winkel(c)
    def winkel_(self, **kwargs):              
        """Winkel zwischen den Spannvektoren; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nkein Argument oder d=n - Dezimaldarstellung")
            print("                         n - Anzahl der Nachkommastellen")			
            print("Ausgabe:") 
            print("Winkel(0, 1)       Winkel(i, j) - Winkel zwischen")
            print("Winkel(0, 2)                      dem i. und dem j. ")
            print("Winkel(1, 2)                      Spannvektor\n")
            return
        w0, w1, w2 = self.winkel
        d = kwargs.get('d')
        return wert_ausgabe(w0, d), wert_ausgabe(w1, d), wert_ausgabe(w2, d)
	
    Winkel = winkel_	
	
    @property			
    def sch_par(self):              
        """Scharparameter"""
        s, a, b, c = self.args		
        return ( a.free_symbols.union(b.free_symbols).union(c.free_symbols).
                union(s.free_symbols) )
    schPar = sch_par	
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		
	
    @property		
    def in_koerper(self):              
        """Konvertierung in Körper"""
        return self.in_prisma.in_koerper

    inKoerper = in_koerper
	
    @property		
    def in_prisma(self):              
        """Konvertierung in Prisma"""
        s, a, b, c = self.args
        Viereck(s, a, b)	
        return Prisma(Viereck(s, a, b), s + c)
		
    inPrisma = in_prisma
	
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Spatschar\n")		
            print("Aufruf   spat . sch_el( wert )\n")		                     
            print("             spat    Spat")
            print("             wert    Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if not wert or len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter angeben')	
            return		
        wert = nsimplify(wert)				
        s, a, b, c = self.args
        if s.has(p):
            s = s.sch_el(wert)
        if a.has(p):
            a = a.sch_el(wert)
        if b.has(p):
            b = b.sch_el(wert)
        if c.has(p):
            c = c.sch_el(wert)
        return Spat(s, a, b, c)		

    schEl = sch_el
	
	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Spates bei einer Abbildung\n")		
            print("Aufruf   spat . bild( abb )\n")		                     
            print("             spat    Spat")
            print("             abb     Abbildung\n")			
            return 				
			
        try:			
            if len(abb) != 1:
                raise AglaError("eine Abbildung angeben")
            abb = abb[0]
            Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
            if not (type(abb) is Abbildung and abb.dim == 3):
                raise AglaError("Abbildung des Raumes angeben")
            m = abb.matrix
            if m.det != 0:
                stuetz1 = self.stuetz.bild(abb)
                spann1 = m * self.spann[0]
                spann2 = m * self.spann[1]
                spann3 = m * self.spann[2]
                return Spat(stuetz1, spann1, spann2, spann3)
            else:
                raise AglaError("nicht implementiert (Determinante der Abbildungsmatrix = 0)")
        except AglaError as e:
            print('agla:', str(e))
            return
			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Spat"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Spat mit mayavi"""	
		
        _mass = UMG._mass()
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                             spez[2][1]
		
        if spez[3]:      # Animation nicht implementiert
            return None
		
        st = self.stuetz
        sp0, sp1, sp2 = self.spann	
        
        plt = []
        plt += [_arrow(st.x, st.y, st.z, sp0.x+st.x, sp0.y+st.y, sp0.z+st.z,  
		                color=lin_farbe, size=lin_staerke),
               _arrow(st.x, st.y, st.z, sp1.x+st.x, sp1.y+st.y, sp1.z+st.z,  
		                color=lin_farbe, size=lin_staerke),
               _arrow(st.x, st.y, st.z, sp2.x+st.x, sp2.y+st.y, sp2.z+st.z,  
		                color=lin_farbe, size=lin_staerke)]	
				
        def linie(p, q):
            x, y, z = [float(p.x), float(q.x)], [float(p.y), float(q.y)], \
                     [float(p.z), float(q.z)]  
            return mlab.plot3d(x, y, z, line_width=lin_staerke, color=lin_farbe, 
                  tube_radius=tr)
				  
        tr = lin_staerke / 50. * _mass
        s, a, b, c, d, e, f, g = self.punkte
        plt += [linie(a, b), linie(b, c), linie(a, e), linie(b, f), 
               linie(g, c), linie(d, e), linie(e, f), linie(f, g), linie(g, d)]
				
        return tuple(plt)	   
	   
    def vispy(self, spez, **kwargs):
        """Grafikelement für Spat mit vispy"""	
		
        pass

	   
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        spat_hilfe(3)	
		
    h = hilfe					

	
	   
# Benutzerhilfe für Spat
# ----------------------

def spat_hilfe(h):
  
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		  
    if h == 2:
        print("\nSpat - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Spat( /[ stütz, ] spann1, spann2, spann3 )\n")
        print("                 stütz    Stützvektor; bei Fehlen Nullvektor")
        print("                 spann    Spannvektor\n")
        print("Zuweisung    s = Spat(...)   (s - freier Bezeichner)\n")
        print("Beispiele")
        print("A = v(0, 2, -3); B = v(2, 1, 3); C = v(-3,4,2)")
        print("Spat(A, B, C)")
        print("Spat(A, A, B, C)\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Spat\n")   
        print("p.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("s.bild(...)     M  Bild bei einer Abbildung")
        print("s.dim              Dimension")
        print("s.in_körper        Konvertierung in Körper")
        print("s.in_prisma        Konvertierung in Prisma")
        print("s.is_schar         Test auf Schar")
        print("s.längen           Seitenlängen")
        print("s.längen_(...)  M  ebenso, zugehörige Methode")
        print("s.punkte           Eckpunkte")
        print("s.punkte_(...)  M  ebenso, zugehörige Methode")
        print("s.sch_el(...)   M  Element einer Schar") 
        print("s.sch_par          Parameter einer Schar")
        print("s.spann            Spannvektoren")
        print("s.stütz            Stützvektor")
        print("s.volumen          Volumen")
        print("s.volumen_(...) M  ebenso, zugehörige Methode")
        print("s.winkel           Winkel zwischen den Spannvektoren")
        print("s.winkel_(...)  M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("in_körper :  inKörper")
        print("in_prisma  :  inPrisma")
        print("is_schar  :  isSchar")
        print("längen_  :  Längen")
        print("punkte_  :  Punkte")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")
        print("volumen_  :  Volumen\n")
        return
 
 