#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Prisma - Klasse  von agla           
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

from agla.lib.objekte.umgebung import UMG
if UMG.grafik_3d == 'mayavi':
    from mayavi import mlab
else:
    from vispy import scene

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy.core.containers import Tuple
from sympy.simplify.simplify import nsimplify
from sympy.core.numbers import Integer
from sympy import  Abs

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.objekte.koerper import Koerper
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    wert_ausgabe, ja, Ja, nein, Nein, mit, ohne)
from agla.lib.funktionen.abb_funktionen import verschiebung 
import agla



# Prisma - Klasse   
	
class Prisma(AglaObjekt):                                      
    """Prisma im Raum
	
**Erzeugung** 

   Prisma ( *grund, höhe* )
 
      *grund* :    Grundfläche (Dreieck oder Viereck)
   
      *höhe* :    Höhe (Zahl); wird im Schwerpunkt von *grund* senkrecht zu 
      diesem errichtet, das Vorzeichen bestimmt die Richtung 
	  
   *oder*   
 
   Prisma ( *grund, punkt* )
   
      *punkt* : Punkt; erster Punkt der Deckfläche (entspricht dem ersten 
      Punkt der Grundfläche); damit sind auch schiefe Prismen möglich
      
    """
				
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            prisma_hilfe(kwargs["h"])		
            return	
			
        try:			
            if len(args) != 2:
                raise AglaError("zwei Argumente angeben")
            a0, a1 = args
            a1 = sympify(a1)
            if mit_param(a0) or mit_param(a1):
                pass #raise AglaError("nicht implementiert (Parameter)")			
            if not (isinstance(a0, Dreieck) or isinstance(a0, Viereck)):
                raise AglaError("Dreieck oder Viereck angeben")
            if not (isinstance(a1, Vektor) and a1.dim == 3 or is_zahl(a1)):
                raise AglaError("Höhe oder Spitze angeben")
            if is_zahl(a1) and a1 == 0:
                raise AglaError("die Höhe muss ungleich Null sein")
            if isinstance(a1, Vektor):
                if not a1.abstand(a0.ebene):
                    raise AglaError("die Deckfläche liegt in der Grundebene")
                return AglaObjekt.__new__(cls, a0, a1)
            else:
                try:				
                    a1 = nsimplify(a1)
                except RecursionError:
                    pass				
                p0 = a0.punkte[0]
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
            return "Prismenschar(" + ss + ")"
        return "Prisma"			

		
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
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        h = self.hoehe
        d = kwargs.get('d')
        return wert_ausgabe(h, d)
		
    Hoehe = hoehe_		
		
    @property			
    def g_flaeche(self):              
        """Grundflächeninhalt"""
        return self.args[0].flaeche
    def g_flaeche_(self, **kwargs):              
        """Grundflächeninhalt; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        g = self.g_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(g, d)
		
    gFlaeche  = g_flaeche		
    GFlaeche = g_flaeche_			
			
    @property			
    def volumen(self):              
        """Volumen"""
        return Abs(self.g_flaeche * self.hoehe)
    def volumen_(self, **kwargs):              
        """Volumen; zugehörige Methode"""
        if kwargs.get('f'):
            txt = 'V = G \, h  \\quad\\quad \;\;\; G - Grundflaeche,\: \:h - Hoehe'
            display(Math(txt))
            return			
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        vol = Abs(self.volumen)
        d = kwargs.get('d')
        return wert_ausgabe(vol, d)
		
    Volumen = volumen_		
		
    @property	
    def deck(self):
        """Deckfläche"""
        g, q0 = self.args
        p = g.punkte		
        vv = Vektor(p[0], q0)
        return self.grund.bild(verschiebung(vv))			
        
    @property
    def seiten(self):
        """Seitenflächen"""
        p = self.grund.punkte	
        q = self.deck.punkte	
        if len(p) == 3:
            return (Viereck(p[0], Vektor(p[0], p[1]), Vektor(p[0], q[0])), \
                   Viereck(p[1], Vektor(p[1], p[2]), Vektor(p[1], q[1])), \
                   Viereck(p[2], Vektor(p[2], p[0]), Vektor(p[2], q[2])))
        return (Viereck(p[0], Vektor(p[0], p[1]), Vektor(p[0], q[0])), \
               Viereck(p[1], Vektor(p[1], p[2]), Vektor(p[1], q[1])), \
               Viereck(p[2], Vektor(p[2], p[3]), Vektor(p[2], q[2])), \
               Viereck(p[3], Vektor(p[3], p[0]), Vektor(p[3], q[3])))

    @property
    def m_flaeche(self):
        """Mantelflächeninhalt"""
        s = self.seiten
        f = s[0].flaeche + s[1].flaeche + s[2].flaeche
        if len(s) == 4:
            f = f + s[3].flaeche
        return f
    def m_flaeche_(self, **kwargs):
        """Mantelflächeninhalt; zugehörige Methode"""
        if kwargs.get('h'):
            if not mit_param(self):		
                print('\nkein Argument oder d=n - Dezimaldarstellung')
                print('n - Anzahl der Nachkomma-/Stellen\n')
                return
        m = self.m_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(m, d)
		
    mFlaeche = m_flaeche		
    MFlaeche = m_flaeche_			

    @property
    def o_flaeche(self):
        """Oberflächeninhalt"""
        return 2 * self.g_flaeche + self.m_flaeche
    def o_flaeche_(self, **kwargs):
        """Oberflächeninhalt; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        if kwargs.get('f'):
            txt = 'O = 2G + M  \quad\quad G - Grundflaeche,\: M - Mantelflaeche'
            display(Math(txt))
            return			
        o = self.o_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(o, d)
		
    oFlaeche  = o_flaeche		
    OFlaeche = o_flaeche_			

    @property
    def sch_par(self):
        """Parameter einer Schar"""
        g, q = self.args
        return g.sch_par.union(q.sch_par)
		
    schPar = sch_par		

    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		

    @property
    def in_koerper(self):
        """Konvertierung in Körper"""
        if isinstance(self.grund, Dreieck):
            ecken = ([self.grund.punkte[i] for i in range(3)] +
                    [self.deck.punkte[i] for i in range(3)])            
            kanten = [[0, 1], [1, 2], [2, 0], [0, 3], [1, 4], [2, 5], [3, 4], 
                     [4, 5], [5, 3]]
        else:
            ecken = ([self.grund.punkte[i] for i in range(4)] + 
                    [self.deck.punkte[i] for i in range(4)])
            kanten = [[0, 1], [1, 2], [2, 3], [3, 0], [0, 4], [1, 5], [2, 6],         
                    [3, 7], [4, 5], [5, 6], [6, 7], [7, 4]]
        return Koerper(ecken, kanten)														 
	
    inKoerper = in_koerper
	
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")			
            return		
		
        if kwargs.get('h'):
            print("\nElement einer Prismenenschar\n")		
            print("Aufruf   prisma . sch_el( wert )\n")		                     
            print("             prisma    Prisma")
            print("             wert      Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben")
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahl oder freien Parameter angeben')	
            return	
        try:			
            wert = nsimplify(wert)	
        except RecursionError:
            pass		
        g, q = self.args
        if g.has(p):
            g = g.sch_el(wert)
        if q.has(p):
            q = q.sch_el(wert)
        return Prisma(g, q)		

    schEl = sch_el

	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Prismas bei einer Abbildung\n")		
            print("Aufruf   prisma . bild( abb )\n")		                     
            print("             prisma    Prisma")
            print("             abb       Abbildung\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == 3):
            print("agla: eine Abbildung des Raumes angeben")
            return
        m = abb.matrix
        if m.D != 0:
            grund1 = self.grund.bild(abb)
            if grund1 is not None:
                deck1 = self.deck.punkte[0].bild(abb) 
                return Prisma(grund1, deck1) 
            else:
                return			
        else:
            k = self.in_koerper
            return k.bild(abb)
			
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Prisma"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)	
	
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Prisma mit mayavi"""	
		
        # 'füll=ja'    - gefüllte Darstellung; default - ungefülte Darstellung	
        # 'kanten=nein' - kein Zeichnen der Kanten; default - Zeichnen als 
        #                  schwarze Linien
							
        _mass = UMG._mass()
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' else \
                                                             spez[2][1]
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                                                        else spez[1]
        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3][:2]
														
        fuell = None	
        kanten = True		
        if len(spez) > 4:
            for s in spez[4]:
                if 'fuell' in s:
                    if 'JA' in s.upper() or 'MIT' in s.upper() or '1' in s.upper():
                        fuell = True
                if 'kanten' in s:
                    if 'NEIN' in s.upper() or 'OHNE' in s.upper() or '0' in s.upper():				
                        kanten = False	
		
        if not anim:			
            kk = self.in_koerper	# Zurückführen auf Koerper.graf
            if not fuell:
                kk.graf((None, spez[1], spez[2], None))
            else:
                kw = ('fuell=ja', )
                if not kanten:
                    kw = ('fuell=ja', 'kanten=nein') 
                kk.graf((None, spez[1], spez[2], None, kw))
        else:
            return None   # in Grafik-Routinen auf Koerper -> Strecke zurückgeführt

			
    def vispy(self, spez, **kwargs):
        """Grafikelement für Prisma mit vispy"""	
		
        pass		
					
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        prisma_hilfe(3)	
		
    h = hilfe					

	
	
# Benutzerhilfe für Prisma
# ------------------------

def prisma_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nPrisma - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Prisma( grund, höhe )\n")
        print("                 grund   Grundfläche (Dreieck oder Viereck)")
        print("                 höhe    Höhe;  wird im Schwerpunkt von grund")
        print("                         errichtet, Vorzeichen bestimmt die")
        print("                         Richtung\n")
        print("oder         Prisma( grund, punkt )\n")		
        print("                 punkt   erster Punkt der Deckfläche (entspricht")
        print("                         dem ersten Punkt der Grundfläche)")
        print("                         auch schiefe Prismen möglich\n")
        print("Zuweisung    p = Prisma(...)   (p - freier Bezeichner)\n")
        print("Beispiele")
        print("A = v(2, -3, -1); B = v(2, 1, 2); C = v(0, 4, -1)")
        print("Prisma(Dreieck(A, B, C), 5)")
        print("Prisma(Viereck(A, B, C), v(5, 4, 3))\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Prisma\n")   
        print("p.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("p.bild(...)       M  Bild bei einer Abbildung")
        print("p.deck               Deckfläche") 
        print("p.dim                Dimension")
        print("p.g_fläche           Grundflächeninhalt")
        print("p.g_fläche_(...)  M  ebenso, zugehörige Methode")
        print("p.grund              Grundfläche")
        print("p.höhe               Höhe")
        print("p.höhe_(...)      M  ebenso, zugehörige Methode")
        print("p.in_körper          Konvertierung in Körper")
        print("p.is_schar           Test auf Schar")
        print("p.m_fläche           Mantelflächeninhalt")
        print("p.m_fläche_(...)  M  ebenso, zugehörige Methode")
        print("p.o_fläche           Oberflächeninhalt")
        print("p.o_fläche_(...)  M  ebenso, zugehörige Methode")
        print("p.sch_el(...)     M  Element einer Schar")	
        print("p.sch_par            Parameter einer Schar")
        print("p.seiten             Seitenflächen")
        print("p.volumen            Volumen")
        print("p.volumen_(...)   M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("g_fläche  :  gFläche")
        print("g_fläche_ :  GFläche")
        print("höhe_     :  Höhe")
        print("in_körper :  inKörper")
        print("is_schar  :  isSchar")
        print("m_fläche  :  mFläche")
        print("m_fläche_ :  MFläche")
        print("o_fläche  :  oFläche")
        print("o_fläche_ :  OFläche")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")
        print("volumen_  :  Volumen\n")
        return

