#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
# Kegel - Klasse  von agla           
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
    from tvtk.tools import visual
    from mayavi import mlab	
else:
    from vispy import scene
    from vispy.geometry import create_cone
    from vispy.scene import STTransform, AffineTransform, ChainTransform
from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.simplify.simplify import simplify, nsimplify
from sympy import sin, cos, Abs
from sympy.core.numbers import Rational, Float, Integer, pi
from sympy.core.symbol import Symbol

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (is_zahl, mit_param,
     wert_ausgabe, kollinear, ja, Ja, nein, Nein, mit, ohne)
import agla
	
	

# Kegel - Klasse  
# --------------
	
class Kegel(AglaObjekt):                                      
    """
	
Kegel im Raum
	
**Erzeugung** 

   Kegel ( *grund, höhe* )
 
      *grund* :    Grundfläche (Kreis)
   
      *höhe* :    Höhe (Zahl); wird im Mittelpunkt von *grund* senkrecht zu
      diesem errichtet, das Vorzeichen bestimmt die Richtung 
	  
      *oder*   
 
   Kegel ( *grund, spitze* )
   
      *spitze* : Punkt; damit sind auch schiefe Kegel möglich
      
   Berechnungen sind nur für gerade Kreiskegel möglich, gezeichnet werden auch 
   andere
   
    """
	
	
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            kegel_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            a0, a1 = args
            a1 = sympify(a1)
            if not (isinstance(a0, Kreis) and a0.dim == 3):
                raise AglaError("Kreis im Raum angeben")
            if not (isinstance(a1, Vektor) and a1.dim == 3 or is_zahl(a1)):
                raise AglaError("Höhe oder Spitze angeben")
            if is_zahl(a1) and a1 == 0:
                raise AglaError("die Höhe muss ungleich Null sein")
				
            if isinstance(a1, Vektor):
                if not all([k.is_real for k in a1.komp]):
                    pass #raise AglaError("komplexe Zahlen sind nicht erlaubt")                    			
                if not a1.abstand(a0.ebene):
                    raise AglaError("die Spitze liegt in der Grundebene")
                return AglaObjekt.__new__(cls, a0, a1)
				
            else:      # Errichten der Höhe im Mittelpunkt des Kreises
                p0 = a0.mitte
                p1 = p0 + a0.ebene.norm.einh_vekt * a1
                return AglaObjekt.__new__(cls, a0, p1)
               			
        except AglaError as e:
            print('agla:', str(e))
            return

			
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Kegelschar(" + ss + ")"
        return "Kegel"			
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 3

    @property
    def is_gerade(self):              
        """Test auf geraden Kreiskegel"""
        grund, spitze = self.args
        if kollinear(grund.ebene.norm, Vektor(grund.mitte, spitze)):
            return True
        return False			
		
    isGerade = is_gerade
	
    @property
    def grund(self):
        """Grundfläche"""
        return self.args[0]
					      
    @property			
    def hoehe(self):              
        """Höhe"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        grund, spitze = self.args	
        h = spitze.abstand(grund.ebene)
        if mit_param(h):
            return h 		
        return Abs(h)
    def hoehe_(self, **kwargs):              
        """Höhe; zugehörige Methode"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        d = kwargs.get('d')
        w = self.hoehe
        wert_ausgabe(w, d)
		
    Hoehe = hoehe_		
		
    @property			
    def g_flaeche(self):              
        """Grundflächeninhalt"""
        return self.grund.flaeche
    def g_flaeche_(self, **kwargs):              
        """Grundflächeninhalt; zugehörige Mehode"""
        if kwargs.get('h')	:
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        if kwargs.get('f'):
            txt = 'G = \\pi r^2  \\quad\\quad r - Radius'
            display(Math(txt))
            return
        w = self.g_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(w, d)
		
    gFlaeche  = g_flaeche		
    gFlaeche_ = g_flaeche_		
    G_flaeche = g_flaeche_			
			
    @property			
    def volumen(self):              
        """Volumen"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return					
        return self.gFlaeche * self.hoehe * Rational(1, 3)
    def volumen_(self, **kwargs):              
        """Volumen; zugehörige Methode"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        if kwargs.get('f'):
            txt = 'V = \\frac{1}{3} G h = \\frac{1}{3} \\pi r^2 h  \\quad' + \
                  '\\quad G - Grundflaeche, \: r - Radius, \: h - Hoehe'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        w = self.volumen
        d = kwargs.get('d')
        return wert_ausgabe(w, d)
		
    Volumen = volumen_
	
    @property	
    def spitze(self):
        """Spitze"""
        return self.args[1]			

    @property
    def m_flaeche(self):
        """Mantelflächeninhalt"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        return ( pi * self.grund.radius * sqrt(self.grund.radius**2 + \
		         self.hoehe**2) )
    def m_flaeche_(self, **kwargs):
        """Mantelflächeninhalt; zugehörige Methode"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        if kwargs.get('f'):
            txt = 'M = \\pi r s  \\quad\\quad r - Radius, \: h - Hoehe, \:s = ' + \
                 '\\sqrt{r^2+h^2} - Seitenlinie'
            display(Math(txt))
            return	
        w = self.m_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(w, d)
				
    mFlaeche  = m_flaeche				
    mFlaeche_ = m_flaeche_				
    M_flaeche = m_flaeche_
	
    @property
    def o_flaeche(self):
        """Oberflächeninhalt"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        return self.gFlaeche + self.mFlaeche
    def o_flaeche_(self, **kwargs):
        """Oberflächeninhalt; zugehörige Methode"""
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
        if kwargs.get('f'):
            txt = 'O = G + M = \\pi \\left( r^2 + r s \\right) \\quad\\quad r - Radius, \: ' + \
                 'h - Hoehe, \:s = \\sqrt{r^2+h^2} - Seitenlinie'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        w = self.o_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(w, d)
		
    oFlaeche  = o_flaeche		
    oFlaeche_ = o_flaeche_		
    O_flaeche = o_flaeche_
	
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        g, s = self.args
        return g.sch_par.union(s.sch_par)
		
    schPar = sch_par		

    @property		
    def is_schar(self):              
        """Test auf Prismenschar"""
        return len(self.sch_par) == 1  

    isSchar = is_schar
	
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Kegelschar\n")		
            print("Aufruf   kegel . sch_el( wert )\n")		                     
            print("             kegel    Kegel")
            print("             wert     Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien ' +
                 'Parameter angeben')	
            return		
        try:			
            wert = nsimplify(wert)	
        except RecursionError:
            pass		
        g, s = self.args
        if g.is_schar:
            g = g.sch_el(wert)
        if s.is_schar:
            s = s.sch_el(wert)
        return Kegel(g, s)		

    schEl = sch_el

	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Kegels bei einer Abbildung\n")		
            print("Aufruf   kegel . bild( abb )\n")		                     
            print("             kegel   Kegel")
            print("             abb     Abbildung\n")			
            return 				
			
        if not self.is_gerade:
            print("agla: nicht implementiert (kein gerader Kreiskegel)")
            return			
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return			
        abb = abb[0]
        Matrix = importlib.import_module('agla.lib.objekte.matrix').Matrix	
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == 3):
            print("agla: eine Abbildung des Raumes angeben")
            return			
        m = abb.matrix
        dd = simplify(m.D)
        m1 = Matrix(Vektor(1, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 1))
        if not mit_param(dd) and abs(abs(dd)-1) < 1e-6 or m == m1 * m[0, 0]:
            grund1 = self.grund.bild(abb)
            spitze1 = self.spitze.bild(abb)
            return Kegel(grund1, spitze1)
        else:
            print("agla: nicht implementiert (der Grundkreis wird verzerrt)")
            return			
				
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Kegel"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
		
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Kegel mit mayavi"""
						
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                                           else spez[1]								
							
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			

        pi = np.pi
        cos = np.cos
        sin = np.sin				
		
        if not anim:
				
            r = float(self.grund.radius)
            m = self.grund.mitte
            s = self.spitze 		
            h = float(self.grund.ebene.abstand(s))	
            v1 = self.grund.ebene.richt[0]
            v2 = v1.vp(self.grund.ebene.norm)
            v1 = v1.einh_vekt
            v2 = v2.einh_vekt
            n = 100			
            t = np.linspace(0.0, 2*pi, n)
            x = r*cos(t)*float(v1.x) + r*sin(t)*float(v2.x) + float(m.x)
            y = r*cos(t)*float(v1.y) + r*sin(t)*float(v2.y) + float(m.y)
            z = r*cos(t)*float(v1.z) + r*sin(t)*float(v2.z) + float(m.z)
            x1 = np.r_[float(s.x), x]
            y1 = np.r_[float(s.y), y]
            z1 = np.r_[float(s.z), z]
            x2 = np.r_[float(m.x), x]
            y2 = np.r_[float(m.y), y]
            z2 = np.r_[float(m.z), z]
            triangles = [(0, i, i + 1) for i in range(1, n)]
            plt = [mlab.triangular_mesh(x1, y1, z1, triangles, color=flaech_farbe)]
            plt += [mlab.triangular_mesh(x2, y2, z2, triangles, color=flaech_farbe)]
		
            return tuple(plt)						
						
        else:
		
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20						
            b_, t = Symbol('b_'), Symbol('t')		
            keg = self.sch_el(b_)
            m = keg.grund.mitte			
            sp = keg.spitze
            kk = keg.grund
            p = kk.pkt(t * 180 / pi)
            n = 32			
            tt = 	np.linspace(0.0, 2*np.pi, n)
            xx, yy, zz = [], [], []			
            for s in tt:
                xx += [str(p.x).replace('t', str(s))] 
                yy += [str(p.y).replace('t', str(s))] 
                zz += [str(p.z).replace('t', str(s))] 
            aa = np.linspace(float(aber[0]), float(aber[1]), N)  
            xam, yam, zam = [], [], []
            xas, yas, zas = [], [], []
            for bb in aa:
                bb = '(' + str(bb) + ')'
                xam += [[float(eval(str(m.x).replace('b_', bb)))] + \
                      [float(eval(str(x).replace('b_', bb))) for x in xx]]
                yam += [[float(eval(str(m.y).replace('b_', bb)))] + \
                      [float(eval(str(y).replace('b_', bb))) for y in yy]]
                zam += [[float(eval(str(m.z).replace('b_', bb)))] + \
                      [float(eval(str(z).replace('b_', bb))) for z in zz]]						  
                xas += [[float(eval(str(sp.x).replace('b_', bb)))] + \
                      [float(eval(str(x).replace('b_', bb))) for x in xx]]
                yas += [[float(eval(str(sp.y).replace('b_', bb)))] + \
                      [float(eval(str(y).replace('b_', bb))) for y in yy]]
                zas += [[float(eval(str(sp.z).replace('b_', bb)))] + \
                      [float(eval(str(z).replace('b_', bb))) for z in zz]]
					  
            dreiecke = [(0, i, i + 1) for i in range(1, n)]
			
            pltm = mlab.triangular_mesh(xam[0], yam[0], zam[0], dreiecke, \
                      color=flaech_farbe)	
            plts = mlab.triangular_mesh(xas[0], yas[0], zas[0], dreiecke, \
                      color=flaech_farbe)	

            return (pltm, plts), ((xam[1:], yam[1:], zam[1:]), \
                                         (xas[1:], yas[1:], zas[1:])), N-1	
				
    def vispy(self, spez, **kwargs):
        """Grafikelement für Kegel mit vispy"""
		
        pass

			
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        kegel_hilfe(3)	
		
    h = hilfe				
			
	
# Benutzerhilfe für Kegel
# -----------------------

def kegel_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nKegel - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Kegel( grund, höhe )\n")
        print("                 grund    Grundfläche (Kreis)")
        print("                 höhe     Höhe;  wird im Mittelpunkt von grund")
        print("                          errichtet; Vorzeichen bestimmt die")
        print("                          Richtung\n")
        print("     oder    Kegel( grund, spitze )\n")		
        print("                 spitze   Punkt")                      
        print("                 auch schiefe Kegel möglich\n")		
        print("Berechnungen sind nur für gerade Kreiskegel möglich, gezeichnet")
        print("werden auch andere\n")		
        print("Zuweisung     k = Kegel(...)   (k - freier Bezeichner)\n")
        print("Beispiel")
        print("kreis = Kreis(xy_ebene, O, 4)")
        print("Kegel(kreis, 9)\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Kegel\n")   
        print("k.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("k.bild(...)       M  Bild bei einer Abbildung")
        print("k.dim                Dimension")	 
        print("k.g_fläche           Grundflächeninhalt") 
        print("k.g_fläche_(...) M   ebenso, zugehörige Methode") 
        print("k.grund              Grundfläche")
        print("k.höhe               Höhe")
        print("k.höhe_(...)      M  ebenso, zugehörige Methode")
        print("k.is_gerade          Test auf geraden Kreiskegel")
        print("k.is_schar           Test auf Schar")
        print("k.m_fläche           Mantelflächeninhalt")
        print("k.m_fläche_(...)  M  ebenso, zugehörige Methode")
        print("k.o_fläche           Oberflächeninhalt")
        print("k.o_fläche_(...) M   ebenso, zugehörige Methode")
        print("k.sch_el(...)     M  Element einer Schar")
        print("k.sch_par            Parameter einer Schar")
        print("k.spitze             Spitze")
        print("k.volumen            Volumen")
        print("k.volumen_(...)   M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("g_fläche  :  gFläche")
        print("höhe_     :  Höhe")
        print("is_gerade :  isGerade")
        print("is_schar  :  isSchar")
        print("m_fläche  :  mFläche")
        print("m_fläche_ :  M_fläche")
        print("o_fläche_ :  O_fläche")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")
        print("volumen_  :  Volumen\n")
        return		
        
		
		
		
		