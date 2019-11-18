#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Pyramide - Klasse  von agla           
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
from sympy.core.numbers import Rational, Integer

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.viereck import Viereck
from agla.lib.objekte.koerper import Koerper
from agla.lib.objekte.parallelogramm import Parallelogramm
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param, 
    wert_ausgabe, ja, Ja, nein, Nein, mit, ohne)				
import agla
	
	

	
# Pyramide - Klasse   
# -----------------
	
class Pyramide(AglaObjekt):                                      
    """Pyramide im Raum
	
**Erzeugung** 

   Pyramide ( *grund, höhe* )
 
      *grund* :   Grundfläche (Dreieck oder Viereck)
   
      *höhe* :    Höhe (Zahl); wird im Schwerpunkt von *grund* senkrecht zu diesem errichtet, das Vorzeichen bestimmt die Richtung 
	  
   *oder*   F
 
   Pyramide ( *grund, spitze* )
   
      *spitze* : Punkt; damit sind auch schiefe Pyramiden möglich
   
   *oder*   

   Pyramide ( */[ stütz, ] spann1, spann2, spann3 )* )
	  
      *stütz* :    Stützvektor; bei Fehlen Nullvektor
	  
      *spann* :   Spannvektor
	  
      (dreiseitige Pyramide, über Vektoren erzeugt)
	  
    """
		
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            pyramide_hilfe(kwargs["h"])		
            return	
			
        try:			    
            if len(args) == 2:
                a0, a1 = args
                a1 = sympify(a1)
                if not (isinstance(a0, Dreieck) or isinstance(a0, Viereck)):
                    raise AglaError("Dreieck oder Viereck angeben")
                if a0.dim != 3:					
                    raise AglaError("Dreieck oder Viereck im Raum angeben")
                if not (isinstance(a1, Vektor) and a1.dim == 3 or is_zahl(a1)):
                    raise AglaError("Höhe oder Spitze angeben")
                if a1 == 0:
                    raise AglaError("Höhe muss ungleich Null sein")
                if isinstance(a1, Vektor):
                    if not a1.abstand(a0.ebene):
                        raise AglaError("die Spitze liegt in der Grundebene")
                    return AglaObjekt.__new__(cls, a0, a1)				
                else:
                    try:				
                       a1 = nsimplify(a1)
                    except RecursionError:	
                        pass					
                    sp = a0.schwer_pkt
                    spitze = sp + a0.ebene.norm.einh_vekt * a1
                    return AglaObjekt.__new__(cls, a0, spitze)
               	
            elif len(args) in [3,  4]:
                if len(args) == 3:
                    a = Vektor(0, 0, 0)
                    b, c, s = args
                else:
                    a, b, c, s = args
                if not (isinstance(s, Vektor) and s.dim == 3 and
                       isinstance(a, Vektor) and a.dim == 3 and
                       isinstance(b, Vektor) and b.dim == 3 and
                       isinstance(c, Vektor) and c.dim == 3):
                        raise AglaError("Grundfläche und Höhe/Spitze oder 3-4 Vektoren angeben")
                grund = Dreieck(a, a + b, a + c)
                spitze = a + s
                return AglaObjekt.__new__(cls, grund, spitze)
							
            else:
                raise AglaError("2 bis 4 Argumente angeben")
				
        except AglaError as e:
            print('agla:', str(e))
            return
		
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Pyramidenschar(" + ss + ")"
        return "Pyramide"			
		
		
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
    def spitze(self):
        """Spitze"""
        return self.args[1]
					 
    @property			
    def hoehe(self):              
        """Höhe"""
        grund, spitze = self.args	
        return spitze.abstand(grund.ebene)
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
    gFlaeche_ = g_flaeche_
    G_flaeche = g_flaeche_	
		
    @property			
    def volumen(self):              
        """Volumen"""
        return self.g_flaeche * self.hoehe * Rational(1, 3)
    def volumen_(self, **kwargs):              
        """Volumen; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        if kwargs.get('f'):
            txt = 'V = \\frac{1}{3} G h \\quad\\quad G - Grundflaeche, \: h - Hoehe'
            display(Math(txt))
            return			
        vol = self.volumen
        d = kwargs.get('d')
        return wert_ausgabe(vol, d)
		
    Volumen = volumen_		
		
    @property
    def seiten(self):
        """Seitenflächen"""
        grund, s = self.args	
        p = grund.punkte
        if len(p) == 3:
            return (Dreieck(p[0], p[1], s), Dreieck(p[1], p[2], s), 
			         Dreieck(p[2], p[0], s)) 	
        else:
            return (Dreieck(p[0], p[1], s), Dreieck(p[1], p[2], s), 
		            Dreieck(p[2], p[3], s), Dreieck(p[3], p[0], s)) 	

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
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        m = self.m_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(m, d)
		
    mFlaeche  = m_flaeche		
    mFlaeche_ = m_flaeche_	
    M_flaeche = m_flaeche_	

    @property
    def o_flaeche(self):
        """Oberflächeninhalt"""
        return self.g_flaeche + self.m_flaeche
    def o_flaeche_(self, **kwargs):
        """Oberflächeninhalt; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print('                         n - Anzahl der Nachkomma-/Stellen')
            print('f=1   Formel\n')
            return
        if kwargs.get('f'):
            txt = 'O = G + M  \\quad\\quad ' + \
                 'G - Grundflaeche, \: M - Mantelflaeche'
            display(Math(txt))
            return			
        o = self.o_flaeche
        d = kwargs.get('d')
        return wert_ausgabe(o, d)
		
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
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar	

    @property
    def in_koerper(self):
        """Konvertierung in Körper"""
        if isinstance(self.grund, Dreieck):
            ecken = [self.grund.punkte[i] for i in range(3)] + [self.spitze]
            kanten = [[0, 1], [1, 2], [2, 0], [0, 3], [1, 3], [2, 3]]
        else:
            ecken = [self.grund.punkte[i] for i in range(4)] + [self.spitze]
            kanten = [[0, 1], [1, 2], [2, 3], [3, 0], [0, 4], [1, 4], 
                                                         [2, 4], [3, 4]]							 
        return Koerper(ecken, kanten)														 
       	
    inKoerper = in_koerper
	
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Pyramidenschar\n")		
            print("Aufruf   pyramide . sch_el( wert )\n")		                     
            print("             pyramide    Pyramide")
            print("             wert        Wert des Scharparameters")			
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
        g, s = self.args
        if g.has(p):
            g = g.sch_el(wert)
        if s.has(p):
            s = s.sch_el(wert)
        return Pyramide(g, s)		

    schEl = sch_el

	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Pyramide bei einer Abbildung\n")		
            print("Aufruf   pyramide . bild( abb )\n")		                     
            print("             pyramide    Pyramide")
            print("             abb         Abbildung\n")			
            return 				
			
        if len(abb) != 1:
            return print("agla: eine Abbildung angeben")
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == 3):
            return print("agla: Abbildung des Raumes angeben")
        m = abb.matrix
        if m.det != 0:
            grund1 = self.grund.bild(abb);
            spitze1 = self.spitze.bild(abb) 
            return Pyramide(grund1, spitze1) 		
        else:
            k = self.in_koerper
            return k.bild(abb)

    def graf(self, spez, **kwargs):                       
        """Grafikelement für Pyramide"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)
	
    def mayavi(self, spez, **kwargs):
        """Grafikelement für Pyramide mit mayavi"""
				
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
        """Grafikelement für Pyramide mit vispy"""
		
        pass		
						
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        pyramide_hilfe(3)	
		
    h = hilfe					

	
	
# Benutzerhilfe für Pyramide
# --------------------------

def pyramide_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nPyramide - Objekt\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Pyramide( grund, höhe )\n")
        print("                 grund    Grundfläche (Dreieck oder Viereck)")
        print("                 höhe     Höhe;  wird im Schwerpunkt von")
        print("                          grund errichtet, das Vorzeichen ")
        print("                          bestimmt die Richtung\n")
        print("     oder    Pyramide( grund, spitze )\n")		
        print("                 spitze   Punkt")
        print("                 auch schiefe Pyramiden möglich\n")
        print("     oder    Pyramide( /[ stütz, ] spann1, spann2, spann3 )\n")	
        print("                 stütz    Stützvektor; bei Fehlen Nullvektor")
        print("                 spann    Spannvektor")
        print("                 dreiseitige Pyramide, über Vektoren erzeugt\n")
        print("Zuweisung    p = Pyramide(...)   (p - freier Bezeichner)\n")
        print("Beispiele")
        print("A = v(2, -3, -1); B = v(2, 1, 2); C = v(0, 4, -1)")
        print("Pyramide(Dreieck(A, B, C), 5)")
        print("Pyramide(Viereck(A, B, C), O)\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Pyramide\n")   
        print("p.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("p.bild(...)       M  Bild bei einer Abbildung")
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
        print("p.spitze             Spitze")
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

 