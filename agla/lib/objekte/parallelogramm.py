#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Parallelogramm - Klasse  von agla           
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
from sympy.abc import t
from sympy.core.symbol import Symbol
from sympy.core.numbers import Float, Integer
from sympy.simplify import nsimplify

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    wert_ausgabe) 
from agla.lib.funktionen.graf_funktionen import _arrow, _arrow2
from agla.lib.objekte.ausnahmen import AglaError
import agla

	

# Parallelogramm - Klasse  
# ----------------------- 
	
class Parallelogramm(AglaObjekt):                                      
    """Parallelogramm im Raum und in der Ebene
	
**Kurzform**

   **ParGramm** *oder* **Pargramm**

**Erzeugung** 
	
   Parallelogramm ( */[ stütz, ] spann1, spann2* )

   *oder*
   
   Pargramm ( */[ stütz, ] spann1, spann2* )
   
**Parameter**

   *stütz* : Stützvektor; Nullvektor, wenn weggelassen
   
   *spann* : Spannvekor   
   
    """
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            parallelogramm_hilfe(kwargs["h"])		
            return	
			
        try:
		
            if len(args) in [2,  3]:
                if len(args) == 2:
                    a, b = args
                    if not (isinstance(a, Vektor) and a.dim in (2, 3) and
                           isinstance(b, Vektor) and b.dim == a.dim):
                        raise AglaError("zwei Vektoren gleicher Dimension " + \
                             "angeben")
                    if a.kollinear(b):
                        raise AglaError("die Spannvektoren dürfen nicht " + \
                             "kollinear sein")
                    if not (a.betrag or b.betrag):
                        raise AglaError("der Nullvektor kann nicht " + \
                             "Spannvektor sein")
                    s = a.O
                else:
                    s, a, b = args
                    if not (isinstance(a, Vektor) and a.dim in (2, 3) and
                           isinstance(b, Vektor) and b.dim == a.dim and
					          isinstance(s, Vektor) and s.dim == a.dim):
                        raise AglaError("drei Vektoren mit der selben " + \
                             "Dimension angeben")
                    if a.kollinear(b):
                        raise AglaError("die Spannvektoren dürfen nicht " + \
                             "kollinear sein")
                    if not (a.betrag or b.betrag):
                        raise AglaError("der Nullvektor kann nicht " + \
                             "Spannvektor sein")
					
                return AglaObjekt.__new__(cls, s, a, b)            
						
            else:
                raise AglaError("zwei oder drei Argumente angeben")

        except AglaError as e:
            print('agla:', str(e))
            return			
		
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Parallelogrammschar(" + ss + ")"
        return "Parallelogramm"			

		
# Für Parallelogramme in R^3 und R^2 gemeinsame Eigenschaften + Methoden
# ----------------------------------------------------------------------

    @property
    def dim(self):              
        """Dimension"""
        return self.args[0].dim
		
    @property
    def punkte(self):
        """Eckpunkte"""
        a, b, c = self.args
        return a, a + b, a + b + c, a + c
    def punkte_(self, **kwargs): 
        """Eckpunkte; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nAusgabe:") 
            print("Punkt / Ortsvektor")
            print(" 0 Stützvektor")
            print(" 1 Stützvektor + Spannvektor0")
            print(" 2 Stützvektor + Spannvektor0 + Spannvektor1")
            print(" 3 Stützvektor + Spannvektor1\n")
            return
        return	 self.punkte		
			
    Punkte = punkte_
			
    @property			
    def laengen(self):              
        """Seitenlängen"""
        a, b, c = self.args		
        return b.betrag, c.betrag
    def laengen_(self, **kwargs):              
        """Seitenlängen; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        l0, l1 = self.laengen
        d = kwargs.get('d')
        return wert_ausgabe(l0, d), wert_ausgabe(l1, d)
			
    Laengen = laengen_
	
    @property			
    def flaeche(self):              
        """Flächeninhalt"""
        b, c = self.args[1:]	
        if self.dim == 2:		
            b, c = Vektor(b.x, b.y, 0), Vektor(c.x, c.y, 0)		
        return b.vp(c).betrag
    def flaeche_(self, **kwargs): 
        """Flächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            print("\nIm Raum R^3:")		
            lat = 'A' + '=' + '\\left| \, \\vec{a} \\times \\vec{b} \,' + \
                      '\\right|'
            display(Math(lat))
            print("Im Raum R^3 und in der Ebene R^2:")		
            lat = 'A = a b \\sin(\\alpha)'
            display(Math(lat))				
            lat = '\\vec{a},\, \\vec{b}' + '- Spannvektoren\; mit\; den\; Laengen\; a,\; b'			
            display(Math(lat))				
            lat = '\\alpha' + '- Winkel\; zwischen\; ihnen'			
            display(Math(lat))				
            return			
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('                        n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formeln\n')
            return
        f = self.flaeche
        d = kwargs.get('d')
        return wert_ausgabe(f, d)
		
    Flaeche = flaeche_		
		
    @property
    def stuetz(self):
        """Stützvektor"""
        return self.args[0]
		
    @property
    def spann(self):
        """Spannvektoren"""
        b, c = self.args[1:]		
        return b, c
		
    @property
    def winkel(self):
        """Winkel zwischen den Spannvektoren"""
        b, c = self.args[1:]
        return b.winkel(c)
    def winkel_(self, **kwargs):
        """Winkel zwischen den Spannvektoren; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        b, c = self.args[1:]
        wi = b.winkel(c)
        d = kwargs.get('d')
        return wert_ausgabe(wi, d)
		
    Winkel = winkel_		
	
    @property			
    def sch_par(self):              
        """Scharparameter"""
        a, b, c = self.args		
        return a.free_symbols.union(b.free_symbols).union(c.free_symbols)
	
    schPar = sch_par
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		

    @property		
    def in_viereck(self):              
        """Konvertierung in Viereck"""
        a, b, c = self.args
        return Viereck(a, b, c)
		
    inViereck = in_viereck		
		
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Parallelogrammschar\n")		
            print("Aufruf   pargramm . sch_el( wert )\n")		                     
            print("             pargramm    Parallelogramm")
            print("             wert        Wert des Scharparameters")			
            print("\nes ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if not wert or len(wert) != 1:
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
        except RecursionError:
            pass		
        a, b, c = self.args
        if a.has(p):
            a = a.sch_el(wert)
        if b.has(p):
            b = b.sch_el(wert)
        if c.has(p):
            c = c.sch_el(wert)
        return Parallelogramm(a, b, c)		

    schEl = sch_el
		
		
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Parallelogramms bei einer Abbildung\n")		
            print("Aufruf   parallelogramm . bild( abb )\n")		                     
            print("             parallelogramm   Parallelogramm")
            print("             abb              Abbildung\n")			
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
            stuetz1 = self.stuetz.bild(abb)
            spann1 = m * self.spann[0]
            spann2 = m * self.spann[1]
            return Parallelogramm(stuetz1, spann1, spann2)
        else:
            print("agla: nicht implementiert (die Determinante der " + \
                 "Abbildungsmatrix ist = 0)")
            return			

		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Parallelogramm"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Parallelogramm in R^3 mit mayavi"""	
		
        _mass = UMG._mass()
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                            spez[2][1]
		
        if spez[3]:      # Animation nicht implementiert
            return None

        st = self.stuetz
        sp0, sp1 = self.spann	
        
        plt = []
        plt += [_arrow(st.x, st.y, st.z, sp0.x+st.x, sp0.y+st.y, st.z+sp0.z,  
		                color=lin_farbe, size=lin_staerke),
               _arrow(st.x, st.y, st.z, sp1.x+st.x, sp1.y+st.y, st.z+sp1.z,  
		                color=lin_farbe, size=lin_staerke)]	
        tr = lin_staerke / 50. * _mass
        b, c, d = self.in_viereck.punkte[1:]
        x, y, z = [float(b.x), float(c.x)], [float(b.y), float(c.y)], \
                 [float(b.z), float(c.z)]  
        plt += [mlab.plot3d(x, y, z, line_width=lin_staerke, color=lin_farbe, \
               tube_radius=tr)]
        x, y, z =  [float(d.x), float(c.x)], [float(d.y), float(c.y)], \
                  [float(d.z), float(c.z)] 
        plt += [mlab.plot3d(x, y, z, line_width=lin_staerke, color=lin_farbe, \
               tube_radius=tr)]
        return tuple(plt)	   	   
	   
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Parallelogramm in R^3 mit vispy"""	
		
        pass		
	   		
	   
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Parallelogramm in R^2"""	
			
        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke2 if spez[2] == 'default' else \
                                                             spez[2][3]
		
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:
            st = self.stuetz 
            sp1, sp2 = self.spann		
            arr1 = _arrow2(st.x, st.y, st.x+sp1.x, st.y+sp1.y,  
		                    color=lin_farbe, linewidth=lin_staerke)			
            arr2 = _arrow2(st.x, st.y, st.x+sp2.x, st.y+sp2.y,  
		                    color=lin_farbe, linewidth=lin_staerke)	
            a, b, c, d = self.punkte
            line1 = plt.plot([b.x, c.x], [b.y, c.y], color=lin_farbe, 
			         linewidth=lin_staerke)
            line2 = plt.plot([d.x, c.x], [d.y, c.y], color=lin_farbe, 
                   linewidth=lin_staerke) 						
            plt.gca().add_line(arr1[0])
            plt.gca().add_patch(arr1[1])			
            plt.gca().add_line(arr2[0])
            plt.gca().add_patch(arr2[1])	
            return line1, line2
		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        parallelogramm_hilfe(3)	
		
    h = hilfe					
		
		
# Benutzerhilfe für Parallelogramm
# --------------------------------

def parallelogramm_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nParallelogramm - Objekt\n")
        print("Synonymer Bezeichner   ParGramm\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")
        print("             ParGramm( /[ stütz, ] spann1, spann2 )\n")
        print("                 stütz    Stützvektor; bei Fehlen Nullvektor")
        print("                 spann    Spannvektor\n")
        print("Zuweisung      p = ParGramm(...)   (p - freier Bezeichner)\n")
        print("Beispiele")
        print("A = v(2, 0, -1); B = v(4, -2, 0); C = v(0, 3, 2)")
        print("Parallelogramm(C, A, B)")
        print("ParGramm(A, B)\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Parallelogramm\n")   
        print("p.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("p.bild(...)     M  Bild bei einer Abbildung")
        print("p.dim              Dimension")
        print("p.fläche           Flächeninhalt")
        print("p.fläche_(...)  M  ebenso, zugehörige Methode")
        print("p.in_viereck       Konvertierung in Viereck")
        print("p.is_schar         Test auf Schar")
        print("p.längen           Seitenlängen")
        print("p.längen_(...)  M  ebenso, zugehörige Methode")
        print("p.punkte           Eckpunkte")
        print("p.punkte_(...)  M  ebenso, zugehörige Methode")
        print("p.sch_el(...)   M  Element einer Schar")
        print("p.sch_par          Parameter einer Schar")
        print("p.spann            Spannvektoren")
        print("p.stütz            Stützvektor")
        print("p.winkel           Winkel zwischen den Spannvektoren")
        print("p.winkel_(...)  M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("fläche_    :  Fläche")
        print("in_viereck :  inViereck")
        print("is_schar   :  isSchar")
        print("längen_    :  Längen")
        print("punkte_    :  Punkte")
        print("sch_el     :  schEl")		
        print("sch_par    :  schPar")		
        print("winkel_    :  Winkel\n")
        return
		
 
ParGramm = Parallelogramm
Pargramm = Parallelogramm
 
 
 
 