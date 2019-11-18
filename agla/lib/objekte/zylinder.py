#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Zylinder - Klasse  von agla           
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
    from vispy.geometry import create_cylinder
    from vispy.scene import STTransform, AffineTransform, ChainTransform

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.core.numbers import Integer, pi
from sympy import cos, sin, Abs
from sympy.core.symbol import Symbol
from sympy.simplify.simplify import simplify, nsimplify

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.funktionen.funktionen import (is_zahl, mit_param,
     wert_ausgabe, ja, Ja, nein, Nein, mit, ohne)
import agla
	
	

# Zylinder - Klasse   
# -----------------
	
class Zylinder(AglaObjekt):                                      
    """
	
Zylinder im Raum
	
**Erzeugung** 

   Zylinder ( *grund, höhe* )
 
      *grund* :    Grundfläche (Kreis)
   
      *höhe* :    Höhe (Zahl); wird im Mittelpunkt von *grund* senkrecht zu 
      diesem errichtet, das Vorzeichen bestimmt die Richtung 
	  
   *oder*   
 
   Zylinder ( *grund, punkt* )
   
      *punkt* : Mittelpunkt der Deckfläche
   
   Es sind nur gerade Kreiszylinder möglich
	  
    """
	
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            zylinder_hilfe(kwargs["h"])		
            return	
						
        try:						
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            a0, a1 = args
            a1 = sympify(a1)
            if not (isinstance(a0, Kreis) and a0.dim == 3):
                raise AglaError("Kreis im Raum angeben")
            if not (isinstance(a1, Vektor) and a1.dim == 3 or is_zahl(a1)):
                raise AglaError("Höhe oder Mittelpunkt der Deckfläche angeben")
            if is_zahl(a1): 
                if a1.is_real not in (True, None) :
                    raise AglaError("reelle Zahl für Höhe angeben")				
                if a1 == 0:
                    raise AglaError("die Höhe muss ungleich Null sein")
                try:					
                    a1 = nsimplify(a1)
                except RecursionError:
                    pass				
            if isinstance(a1, Vektor):
                if not all([k.is_real for k in a1.komp]):
                    #raise AglaError("komplexe Zahlen sind nicht erlaubt")                    
                    pass 
                if not a1.abstand(a0.ebene):
                    raise AglaError("der Deckflächenmittelpunkt liegt in " + \
                         "der Grundebene")
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
            return "Zylinderschar(" + ss + ")"
        return "Zylinder"			
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property
    def grund(self):
        """Grundfläche"""
        return self.args[0]
					      
    @property			
    def hoehe(self):              
        """Höhe"""
        grund, deck_punkt = self.args		
        return deck_punkt.abstand(grund.ebene)
    def hoehe_(self, **kwargs):              
        """Höhe; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkommastellen\n')
            return
        h = self.hoehe
        d = kwargs.get('d')
        return wert_ausgabe(h, d)
		
    Hoehe = hoehe_		
		
    @property			
    def g_flaeche(self):              
        """Grundflächeninhalt"""
        return self.grund.flaeche
    def g_flaeche_(self, **kwargs):              
        """Grundflächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'G = \\pi r^2 \\quad\\quad r - Radius'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        d = kwargs.get('d')			
        g = self.g_flaeche
        return wert_ausgabe(g, d)
		
    gFlaeche  = g_flaeche		
    GFlaeche = g_flaeche_			
			
    @property			
    def volumen(self):              
        """Volumen"""
        return Abs(self.gFlaeche * self.hoehe)
    def volumen_(self, **kwargs):          
        """Volumen; zugehörige Methode"""    
        if kwargs.get('f'):
            txt = 'V = G h = \\pi r^2 h  \\quad\\quad G - Grundflaeche,\: r - Radius, \:h - Hoehe'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1  Formel\n')
            return
        vol = self.volumen
        d = kwargs.get('d')
        return wert_ausgabe(vol, d)
		
    Volumen = volumen_		
		
    @property	
    def deck(self):
        """Deckfläche"""
        grund, punkt = self.args
        deck_ebene = Ebene(punkt, grund.ebene.norm)
        return Kreis(deck_ebene, punkt, grund.radius)			

    @property
    def m_flaeche(self):
        """Mantelflächeninhalt"""
        return Abs(2 * pi * self.grund.radius * self.hoehe)
    def m_flaeche_(self, **kwargs):
        """Mantelflächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'M = 2 \\pi r h  \\quad\\quad r - Radius, \: h - Hoehe'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        d = kwargs.get('d')
        m = self.m_flaeche
        return wert_ausgabe(m, d)
		
    mFlaeche  = m_flaeche		
    MFlaeche = m_flaeche_			
				
    @property
    def o_flaeche(self):
        """Oberflächeninhalt"""
        return 2 * self.g_flaeche + self.m_flaeche
    def o_flaeche_(self, **kwargs):
        """Oberflächeninhalt; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'O = 2 G + M = 2 \\pi r^2 + 2 \\pi r h  \\quad\\quad\\quad ' + \
                 'G - Grundflaeche, \: M - Mantelflaeche, \: r - Radius, \: h - Hoehe'
            display(Math(txt))
            return
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkommastellen')
            print('f=1   Formel\n')
            return
        o = self.o_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(o, d)
		
    oFlaeche  = o_flaeche		
    OFlaeche = o_flaeche_			
	
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        g, p = self.args
        return g.sch_par.union(p.sch_par)
		
    schPar = sch_par		

    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1  
		
    isSchar = is_schar		

		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Zylinderschar\n")		
            print("Aufruf   zylinder . sch_el( wert )\n")		                     
            print("             zylinder   Zylinder")
            print("             wert       Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        g, q = self.args
        if g.has(p) and g.is_schar:
            g = g.sch_el(wert)
        if q.has(p) and q.is_schar:
            q = q.sch_el(wert)
        return Zylinder(g, q)		

    schEl = sch_el

	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Zylinders bei einer Abbildung\n")		
            print("Aufruf   zylinder . bild( abb )")		                     
            print("             zylinder   Zylinder")
            print("             abb        Abbildung\n")			
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
            mitte1 = self.deck.mitte.bild(abb)
            return Zylinder(grund1, mitte1)
        else:
            print("agla: nicht implementiert (der Grundkreis wird verzerrt)")
            return			
				
			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Zylinder"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
				
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Zylinder mit mayavi"""
				
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                      else spez[1]								
       			
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3]			
		
        if not anim:
			
            sin, cos, pi = np.sin, np.cos, np.pi			
            r = float(self.grund.radius)
            mg = self.grund.mitte
            md = self.deck.mitte
            h = float(self.hoehe)	
            v1 = self.grund.ebene.richt[0]
            v2 = v1.vp(self.grund.ebene.norm)
            v1 = v1.einh_vekt
            v2 = v2.einh_vekt
            m = self.grund.mitte
            n = 100			
            t = np.linspace(0.0, 2*pi, n)
            x1 = r*cos(t)*float(v1.x) + r*sin(t)*float(v2.x) + float(mg.x)
            y1 = r*cos(t)*float(v1.y) + r*sin(t)*float(v2.y) + float(mg.y)
            z1 = r*cos(t)*float(v1.z) + r*sin(t)*float(v2.z) + float(mg.z)
            xx1 = np.r_[float(mg.x), x1]
            yy1 = np.r_[float(mg.y), y1]
            zz1 = np.r_[float(mg.z), z1]
            triangles = [(0, i, i + 1) for i in range(1, n)]
            mlab.triangular_mesh(xx1, yy1, zz1, triangles, color=flaech_farbe)
            x2 = r*cos(t)*float(v1.x) + r*sin(t)*float(v2.x) + float(md.x)
            y2 = r*cos(t)*float(v1.y) + r*sin(t)*float(v2.y) + float(md.y)
            z2 = r*cos(t)*float(v1.z) + r*sin(t)*float(v2.z) + float(md.z)
            xx2 = np.r_[float(md.x), x2]
            yy2 = np.r_[float(md.y), y2]
            zz2 = np.r_[float(md.z), z2]		
            mlab.triangular_mesh(xx2, yy2, zz2, triangles, color=flaech_farbe)
            x = np.hstack((x1, x2))
            y = np.hstack((y1, y2))
            z = np.hstack((z1, z2))
            triangles = [(i, i+1, n+i) for i in range(n-1)] + \
                       [(n+i, n+i+1, i+1) for i in range(n-1)]
            plt = [mlab.triangular_mesh(x, y, z, triangles, \
                                       color=flaech_farbe)]
	
            return tuple(plt)
		
        else:
            
            print('agla:  lange Rechenzeiten')			
            if len(aber) == 3:
                N = aber[2]
            else:
                N = 20		
            from numpy import sin, cos, tan, abs, log, arcsin, arccos, arctan, \
               sinh, cosh, tanh, arcsinh, arccosh, arctanh, sqrt, exp, pi				
            b_, t_ = Symbol('b_'), Symbol('t_')		
            zyl = self.sch_el(b_)
            mg = zyl.grund.mitte			
            md = zyl.deck.mitte
            kg = zyl.grund
            kd = zyl.deck
            p, q = kg.pkt(t_ * 180 / pi), kd.pkt(t_ * 180 / pi)
            n = 32			
            tt = np.linspace(0.0, 2*pi, n)
            px, py, pz = [], [], []			
            qx, qy, qz = [], [], []			
            for s in tt:
                px += [str(p.x).replace('t_', str(s))] 
                py += [str(p.y).replace('t_', str(s))] 
                pz += [str(p.z).replace('t_', str(s))] 
                qx += [str(q.x).replace('t_', str(s))] 
                qy += [str(q.y).replace('t_', str(s))] 
                qz += [str(q.z).replace('t_', str(s))] 
            aa = np.linspace(float(aber[0]), float(aber[1]), N)  
            xag, yag, zag = [], [], []
            xad, yad, zad = [], [], []
            for bb in aa:
                bb = '(' + str(bb) + ')'
                xag += [[float(eval(str(mg.x).replace('b_', bb)))] + \
                      [float(eval(str(x).replace('b_', bb))) for x in px]]
                yag += [[float(eval(str(mg.y).replace('b_', bb)))] + \
                      [float(eval(str(y).replace('b_', bb))) for y in py]]
                zag += [[float(eval(str(mg.z).replace('b_', bb)))] + \
                      [float(eval(str(z).replace('b_', bb))) for z in pz]]						  
                xad += [[float(eval(str(md.x).replace('b_', bb)))] + \
                      [float(eval(str(x).replace('b_', bb))) for x in qx]]
                yad += [[float(eval(str(md.y).replace('b_', bb)))] + \
                      [float(eval(str(y).replace('b_', bb))) for y in qy]]
                zad += [[float(eval(str(md.z).replace('b_', bb)))] + \
                      [float(eval(str(z).replace('b_', bb))) for z in qz]]						  
            dreiecke = [(0, i, i + 1) for i in range(1, n)]
            pltg = mlab.triangular_mesh(xag[0], yag[0], zag[0], dreiecke, \
                      color=flaech_farbe)	
            pltd = mlab.triangular_mesh(xad[0], yad[0], zad[0], dreiecke, \
                      color=flaech_farbe)
					  
            px = [[float(eval(x.replace('b_', str(bb)))) for x in px] for bb in aa]
            py = [[float(eval(x.replace('b_', str(bb)))) for x in py] for bb in aa]
            pz = [[float(eval(x.replace('b_', str(bb)))) for x in pz] for bb in aa]
            qx = [[float(eval(x.replace('b_', str(bb)))) for x in qx] for bb in aa]
            qy = [[float(eval(x.replace('b_', str(bb)))) for x in qy] for bb in aa]
            qz = [[float(eval(x.replace('b_', str(bb)))) for x in qz] for bb in aa]			
			
            xam = np.hstack((px, qx)) 
            yam = np.hstack((py, qy)) 
            zam = np.hstack((pz, qz)) 
						
            dreiecke = [(i, i+1, n+i) for i in range(n-1)] + \
                       [(n+i, n+i+1, i+1) for i in range(n-1)]
            					   
            pltm = mlab.triangular_mesh(xam[0], yam[0], zam[0], dreiecke, \
                                       color=flaech_farbe)
	  					  
            return (pltg, pltd, pltm), ((xag[1:], yag[1:], zag[1:]), \
                   (xad[1:], yad[1:], zad[1:]), (xam[1:], yam[1:], zam[1:])), \
                   N-1					  

					  
    def vispy(self, spez, **kwargs):
        """Grafikelement für Zylinder mit vispy"""
		
        pass		
		
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        zylinder_hilfe(3)	
		
    h = hilfe					


	
# Benutzerhilfe für Zylinder
# --------------------------

def zylinder_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nZylinder - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Zylinder( grund, höhe )")
        print("                 grund    Grundfläche (Kreis)")
        print("                 höhe 	  Höhe;  wird im Mittelpunkt von grund")
        print("                          errichtet, Vorzeichen bestimmt die")
        print("                          Richtung\n")
        print("     oder    Zylinder( grund, punkt )")		
        print("                 punkt    Mittelpunkt der Deckfläche\n")
        print("Es sind nur gerade Kreiszylinder möglich\n")
        print("Zuweisung     zyl = Zylinder(...)   (zyl - freier Bezeichner)\n")
        print("Beispiel")
        print("k = Kreis(xy_ebene, O, 4)")
        print("Zylinder(k, 9)\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Zylinder\n")   
        print("zyl.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("zyl.bild(...)       M  Bild bei einer Abbildung")
        print("zyl.deck               Deckfläche")
        print("zyl.dim                Dimension")	 
        print("zyl.g_fläche           Grundflächeninhalt") 
        print("zyl.g_fläche_(...)  M  ebenso, zugehörige Methode")
        print("zyl.grund              Grundfläche")
        print("zyl.höhe               Höhe")
        print("zyl.höhe_(...)      M  ebenso, zugehörige Methode")
        print("zyl.is_schar           Test auf Schar")
        print("zyl.m_fläche           Mantelflächeninhalt")
        print("zyl.m_fläche_(...)  M  ebenso, zugehörige Methode")
        print("zyl.o_fläche           Oberflächeninhalt")
        print("zyl.o_fläche_(...)  M  ebenso, zugehörige Methode")
        print("zyl.sch_el(...)     M  Element einer Schar")
        print("zyl.sch_par            Parameter einer Schar")
        print("zyl.volumen            Volumen")
        print("zyl.volumen_(...)   M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("g_fläche  :  gFläche")
        print("g_fläche_ :  GFläche")
        print("höhe_     :  Höhe")
        print("is_schar  :  isSchar")
        print("m_fläche  :  mFläche")
        print("m_fläche_ :  MFläche")
        print("o_fläche  :  oFläche")
        print("o_fläche_ :  OFläche")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")
        print("volumen_  :  Volumen\n")
        return


		