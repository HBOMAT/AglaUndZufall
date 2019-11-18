#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Viereck - Klasse  von agla           
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
from sympy.core.numbers import Integer
from sympy import Piecewise

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.ausnahmen import *
from agla.lib.funktionen.funktionen import (acosg, is_zahl, mit_param,
    wert_ausgabe, ja, Ja, nein, Nein, mit, ohne)
import agla



# Viereck - Klasse
# -----------------   
		
class Viereck(AglaObjekt):                                      
    """
	
Viereck im Raum und in der Ebene
	
**Erzeugung** 
	
   Viereck ( *punkt1, punkt2, punkt3, punkt4* )

   *oder*

   Viereck ( /[ stütz, ] spann1, spann2 )

      (Erzeugung wie Parallelogramm)
   
**Parameter**

   *punkt* : Eckpunkt  

   *stütz* : Stützvektor; bei Fehlen Nullvektor
   
   *spann* : Spannvektor   
   
Ist  bei der Erzeugung über vier Punkte als letztes Argument `kontrolle=nein` 
angegeben, wird nicht geprüft, ob die Reihenfolge der Punkte korrekt ist		
   
    """
		
    def __new__(cls, *args, **kwargs):  
			
        h = kwargs.get("h")		
        if h in (1, 2, 3):                         
            viereck_hilfe(h)		
            return	
        kontr = kwargs.get("kontrolle")
        if kontr is None:
            kontr = True		
		
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
		
        try:
		
            if len(args) in (2,  3):
                if len(args) == 2:
                    a, b = args
                    if not (isinstance(a, Vektor) and a.dim in [2, 3] and
                        isinstance(b, Vektor) and b.dim == a.dim):
                        raise AglaError("zwei Vektoren mit " + \
                              "gleicher Dimension angeben")
                    if a.kollinear(b):
                        raise AglaError("die Spannvektoren sind kollinear")
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
                        raise AglaError("die Spannvektoren sind kollinear")
                    if not (a.betrag or b.betrag):
                        raise AglaError("der Nullvektor kann nicht " + \
                             "Spannvektor sein")
					
                return AglaObjekt.__new__(cls, s, s + a, s + a + b, s + b)            
				
            elif len(args) == 4:
                a, b, c, d = args
                if not (isinstance(a, Vektor) and a.dim in (2, 3) and
                       isinstance(b, Vektor) and b.dim == a.dim and
                       isinstance(c, Vektor) and c.dim == a.dim and
                       isinstance(d, Vektor) and d.dim == a.dim):
                       raise AglaError("vier Punkte mit der selben " + \
                                                   "Dimension angeben")
                if a==b or a==c or a==d or b==c or b==d or c==d:
                    raise AglaError("vier verschiedene Punkte angeben")
                if a.dim == 3 and not a.komplanar(b, c, d):
                    raise AglaError("die Punkte liegen nicht in einer Ebene")
                if ( Vektor(a, b).kollinear(Vektor(a, c)) and 
			          Vektor(a, b).kollinear(Vektor(a, d)) ):
                    raise AglaError("alle Punkte liegen auf einer Geraden")
                s11, s12 = Strecke(a, b), Strecke(c, d)
                s21, s22 = Strecke(b, c), Strecke(d, a)	
                if mit_param(s11) or mit_param(s12) or mit_param(s21) or \
                                                        mit_param(s22):
                    raise AglaError("nicht implementiert (Parameter), " + \
                         "Erzeugung über\n      zwei Vektoren oder als " + \
                         "Parallelogramm versuchen")	
                if kontr:	
                    if s11.schnitt(s12) or s21.schnitt(s22):
                        txt = "die Reihenfolge der Punkte ist nicht korrekt"
                        raise AglaError(txt)
							
                return AglaObjekt.__new__(cls, a, b, c, d)                        
		
            else:
                raise AglaError("2, 3 oder 4 Argumente angeben")
		
        except AglaError as e:
            print('agla:', str(e))
            return
			
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Viereckschar(" + ss + ")"
        return "Viereck"					
   
		
# Für Vierecke in R^3 und R^2 gemeinsame Eigenschaften + Methoden
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
            print("\nAusgabe")
            print("bei Erzeugung über vier Punkte:   Eckpunkte (in der Reihenfolge ihrer Eingabe)")
            print("bei Erzeugung über drei Vektoren: vektor1, vektor1+vektor2, ")
            print("                                  vektor1+vektor2+vektor3, vektor1+vektor3")
            print("bei Erzeugung über zwei Vektoren: Ursprung, vektor1, vektor1+vektor2,")
            print("                                  vektor2\n")
            return
        return self.punkte			
		
    Punkte = punkte_		
		
    @property
    def schwer_pkt(self):              
        """Schwerpunkt"""
        a, b, c, d = self.punkte
        return (a + b + c + d) / 4		
		
    schwerPkt = schwer_pkt
			      
    @property	
    def ebene(self):              
        """Trägerebene; nur im Raum"""
        if self.dim != 3:
            print("nur für Vierecke im Raum R^3 verfügbar")		
            return
        a, b, c, d = self.punkte
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor
        Ebene = importlib.import_module('agla.lib.objekte.ebene').Ebene	
        return Ebene(a, Vektor(a, b), Vektor(a, c))

    @property			
    def laengen(self):              
        """Seitenlängen"""
        a, b, c, d = self.punkte		
        return b.abstand(a), c.abstand(b), d.abstand(c), a.abstand(d)
    def laengen_(self, **kwargs):              
        """Seitenlängen; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print("                         n - Anzahl der Nachkomma-/Stellen\n")			
            print('Ausgabe: Länge(1, 2), Länge(2, 3), Länge(3, 4), Länge(4, 1)')
            print('Länge(i, j) - Länge der Strecke zwischen dem i. und j.')
            print('Punkt in der Reihenfolge ihrer Eingabe\n')
            return
        l0, l1, l2, l3 = self.laengen			
        d = kwargs.get('d')
        return wert_ausgabe(l0, d), wert_ausgabe(l1, d), wert_ausgabe(l2, d), \
              wert_ausgabe(l3, d)
			
    Laengen = laengen_			
			
    @property
    def umfang(self):
        """Umfang"""
        ll = self.laengen
        return ll[0] + ll[1] + ll[2] + ll[3]
    def umfang_(self, **kwargs):
        """Umfang; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        u = self.umfang
        d = kwargs.get('d')
        return wert_ausgabe(u, d)
		
    Umfang = umfang_		
		
    @property
    def winkel(self):
        """Innenwinkel"""		
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        a, b, c, d = self.punkte
        return ( Vektor(a, b).winkel(Vektor(a, d)), 
                Vektor(b, a).winkel(Vektor(b, c)), 
		         Vektor(c, d).winkel(Vektor(c, b)), 
                Vektor(d, a).winkel(Vektor(d, c)) )
    def winkel_(self, **kwargs):              
        """Innenwinkel; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Argument oder d=n - Dezimaldarstellung')
            print("                         n - Anzahl der Nachkomma-/Stellen\n")			
            print('Ausgabe: Winkel bei den Eckpunkten in der Reihenfolge')
            print('ihrer Eingabe\n')
            return
        w0, w1, w2, w3 = self.winkel
        d = kwargs.get('d')
        return wert_ausgabe(w0, d), wert_ausgabe(w1, d), wert_ausgabe(w2, d), \
              wert_ausgabe(w3, d),
			
    Winkel = winkel_			
			
    @property			
    def sch_par(self):              
        """Scharparameter"""
        a, b, c, d = self.punkte		
        return ( a.free_symbols.union(b.free_symbols).union(c.free_symbols).
		         union(d.free_symbols) )
				 
    schPar = sch_par			 
	
    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar	

    @property
    def seiten(self):
        """Seiten"""
        a, b, c, d = self.punkte
        return Strecke(a, b), Strecke(b, c), Strecke(c, d), Strecke(d, a)
    def seiten_(self, **kwargs):              
        """Seiten; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nAusgabe: Seite(1, 2), Seite(2, 3), Seite(3, 4), Seite(4, 1)\n')
            print('Seite(i, j) - Strecke zwischen dem i. und j. Punkt in der ')
            print('              Reihenfolge ihrer Eingabe bzw. ihrer Ausgabe')
            print('              mit .punkte\n')
            return
        return self.seiten			
	
    Seiten = seiten_	
	
    @property
    def is_konvex(self):
        """Test auf Konvexität"""
        if mit_param(self):
            print('agla: nicht implementiert (Parameter)')
            return	
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        A, B, C, D = self.punkte
        g1, g2 = Gerade(C, Vektor(C,D)), Gerade(B, Vektor(B,C))
        s1, s2 = Strecke(A,B), Strecke(A,D)
        if g1.schnitt(s1) or g2.schnitt(s2):		
            return False
        return True			
					
    isKonvex = is_konvex	
		
    @property
    def dreiecke(self):
        """Zerlegungsdreiecke"""
        a, b, c, d = self.punkte
        if mit_param(self):
            return Dreieck(a, b, c), Dreieck(a, c, d)	
        if self.is_konvex:
            return Dreieck(a, b, c), Dreieck(a, c, d)
        else:
            g12 = Gerade(a, Vektor(a, b))
            s34 = Strecke(c, d)             
            if s34.schnitt(g12):
                s = s34.schnitt(g12)
            else:
                g34 = Gerade(c, Vektor(c, d))
                s12 = Strecke(a, b)             
                s = s12.schnitt(g34)
            return Dreieck(a, s, d), Dreieck(b, c, s)		
		
    @property		
    def flaeche(self):
        """Flächeninhalt"""
        dd = self.dreiecke
        return dd[0].flaeche + dd[1].flaeche		
    def flaeche_(self, **kwargs): 
        """Flächeninhalt; zugehörige Methode"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        f = self.flaeche
        d = kwargs.get('d')
        return wert_ausgabe(f, d)
		
    Flaeche = flaeche_		
		
    @property		
    def is_pargramm(self):
        """Test auf Parallelogramm"""
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        a, b, c, d = self.punkte
        return (Vektor(a, b).betrag == Vektor(c, d).betrag and 
		        Vektor(a, d).betrag == Vektor(b, c).betrag)  

    isPargramm = is_pargramm			
				
    @property
    def form(self):
        """Form"""
        if mit_param(self):
            print('agla: nicht implementiert (Parameter)')
            return			
        Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
        a, b, c, d = self.punkte
        wi = self.winkel
        ll = self.laengen
        if self.is_konvex:
            if wi[0]==90 and wi[1]==90 and wi[2]==90 and wi[3]==90: 		
                if ll[1]==ll[0] and ll[2]==ll[0] and ll[3]==ll[0]:
                    display(Math("Quadrat"))
                else:
                    display(Math("Rechteck"))
            elif ( (wi[0]==wi[2] or wi[1]==wi[3]) and ll[1]==ll[0] and 
			         ll[2]==ll[0] and ll[3]==ll[0] ):
                display(Math("Rhombus"))
            elif ( Vektor(a, c).sp(Vektor(b, d))==0 and not 
			       (Vektor(a, b).kollinear(Vektor(c, d)) or 
                   Vektor(b, c).kollinear(Vektor(d, a))) ):				
                display(Math("Drachenviereck"))
            elif ( Vektor(a, b).kollinear(Vektor(c, d)) and 
			        Vektor(b, c).kollinear(Vektor(d, a)) ):
                display(Math("Parallelogramm"))
            elif (Vektor(a, b).kollinear(Vektor(c, d)) or 
                   Vektor(b, c).kollinear(Vektor(d, a))):
                display(Math("Trapez"))
            else:
                if self.dim == 2:
                    a, b, c, d = Vektor(a.x, a.y, 0), Vektor(b.x, b.y, 0), \
                                Vektor(c.x, c.y, 0), Vektor(d.x, d.y, 0)	
                    self = Viereck(a, b, c, d, kontrolle=False)								
                g1, g2 = Gerade(a, Vektor(a, b)), Gerade(a, Vektor(a, c))
                m1 = Gerade((a+b)*1/2, g1.richt.vp(self.ebene.norm))
                m2 = Gerade((a+c)*1/2, g2.richt.vp(self.ebene.norm))
                try:				
                    m = m1.schnitt(m2)
                except NotImplementedError:
                    st, ri = m1.stuetz, m1.richt
                    st = Vektor(float(st.x), float(st.y), float(st.z)) 				
                    ri = Vektor(float(ri.x), float(ri.y), float(ri.z)) 
                    m1 = Gerade(st, ri)					
                    st, ri = m2.stuetz, m2.richt
                    st = Vektor(float(st.x), float(st.y), float(st.z)) 				
                    ri = Vektor(float(ri.x), float(ri.y), float(ri.z)) 
                    m2 = Gerade(st, ri)			
                    m = m1.schnitt(m2)	
                    am = a.abstand(m).evalf()
                    bm = b.abstand(m).evalf()					
                    cm = c.abstand(m).evalf()					
                    dm = d.abstand(m).evalf()		
                    grenz = 1e-5					
                    if abs(bm - am) < grenz and abs(cm - am) < grenz \
                        and abs(dm - am) < grenz:				
                        display(Math("Sehnenviereck"))
                    else:
                        display(Math("unregelmaessiges\:  konvexes\: Viereck"))					
                    print('(ermittelt mit float-Berechnung)')						  
                    return					
                if b.abstand(m) == a.abstand(m) and c.abstand(m) == \
                   a.abstand(m) and d.abstand(m) == a.abstand(m):
                    display(Math("Sehnenviereck"))
                else:
                    display(Math("unregelmaessiges\:  konvexes\: Viereck"))
					
        else:
            display(Math("nichtkonvexes\: Viereck"))	

    @property	
    def in_figur(self):
        """Konvertierung in Figur; nur in der Ebene"""
        if self.dim != 2:
            print("agla: nur in der Ebene R^2 verfügbar")		
            return		
        ecken = [p for p in self.punkte]
        ecken += [ecken[0]]		
        kanten = [[0, 1], [1, 2], [2, 3], [3, 4]]
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
        kanten = [[0, 1], [1, 2], [2, 3], [3, 0]]
        Koerper = importlib.import_module('agla.lib.objekte.koerper').Koerper	
        return Koerper(ecken, kanten)		
	
    inKoerper = in_koerper


    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Viereckschar\n")		
            print("Aufruf   viereck . sch_el( wert )\n")		                     
            print("             viereck    Viereck")
            print("             wert       Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if not wert or len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        if not is_zahl(wert):
            print('agla:  für Scharparameter Zahl oder freien Parameter ' + \
                 'angeben')	
            return
        try:			
            wert = nsimplify(wert)
        except RecursionError:
            pass		
        if not is_zahl(wert):
            print('agla: für den Scharparameter Zahlenwert oder freien ' + \
                 'Bezeichner angeben')
            return			
        a, b, c, d = self.punkte
        if a.has(p):
            a = a.sch_el(wert)
        if b.has(p):
            b = b.sch_el(wert)
        if c.has(p):
            c = c.sch_el(wert)
        if d.has(p):
            d = d.sch_el(wert)
        return Viereck(a, b, c, d)		

    schEl = sch_el
	
			
    def pkt(self, *wert, **kwargs):
        """Viereckpunkt"""
		
        if kwargs.get('h'):
            print("\nPunkt des Vierecks\n")		
            print("Aufruf   viereck . pkt( /[ wert ] )")		                     
            print("             viereck   Viereck")
            print("             wert      Wert des Viereckparameters\n")
            print("Rückgabe   bei Angabe eines Parameterwertes aus [0, 1]:")
            print("           Punkt des Vierecks, der zu diesem Wert gehört")		
            print("           (Parameter ist die Weglänge vom ersten Punkt aus,")
            print("           die gesamte Länge der Strecke ist 1 - es werden")
            print("           Werte aus dem Intervall [0, 1] angenommen)")
            print("           bei fehlendem Wert oder freiem Parameter:")
            print("           allgemeiner Punkt des Vierecks\n")
            return
				
        p0 = self.seiten[0].gerade.pkt(t)				
        p1 = self.seiten[1].gerade.pkt(t)				
        p2 = self.seiten[2].gerade.pkt(t)		
        p3 = self.seiten[3].gerade.pkt(t)		
        tt = simplify(self.umfang)
        t0 = simplify(self.laengen[0] / tt)
        t1 = simplify(t0 + self.laengen[1] / tt)	
        t2 = simplify(t1 + self.laengen[2] / tt)	
        p = Piecewise( (p0.subs(t, 0), t<=0), 
		               (p0, t<t0),  
					     (p1.subs(t, t-t0), t<t1), 
                      (p2.subs(t, t-t1), t<t2),
                      (p3.subs(t, t-t2), t<1),
                      (p3.subs(t, 1),  1<=t) )

        if not wert:
            return p
        if len(wert) == 1:
            if mit_param(wert[0]):
                return p.subs(t, wert[0])
            if not (0 <= wert[0] <= 1):
                print("agla: einen Wert aus dem Intrvall [0, 1] angeben")
                return				
            pw = simplify(sympify(wert[0]))
            return p.subs(t, pw)			 
        print("agla: Parameterwert angeben")
        return
		
			
    def schnitt(self, *objekt, **kwargs):
        """"Schnitt mit anderen Objekten"""
				
        if kwargs.get('h'):
            print("\nSchnitt des Vierecks mit einem anderen Objekt\n")		
            print("Aufruf   viereck . schnitt( objekt )")		                     
            print("             viereck   Viereck")
            print("             objekt    Punkt, Gerade  (im Raum R^3)")
            print("                       Punkt  (in der Ebene R^2)\n")
            print("Zusatz       l=1   Lageinformationen\n")			
            return
	
        dim = 3 if self.dim == 3 else 2
        try:	
            Vektor = importlib.import_module('agla.lib.objekte.vektor').Vektor	
            if len(objekt) != 1:
                raise AglaError("ein Objekt angeben")
            objekt = objekt[0]	
            if dim == 3:			
                if not isinstance(objekt, (Vektor, Gerade)):
                    raise AglaError("Punkt oder Gerade angeben")
            else:
                if not isinstance(objekt, Vektor):
                    raise AglaError("einen Punkt angeben")			
            if mit_param(self) or mit_param(objekt):
                raise AglaError("nicht implementiert (Parameter)")			
            if objekt.dim != self.dim or not objekt.dim in (2, 3):
                raise AglaError("Objekt mit passender Dimension angeben")				
            if dim == 2:
                a, b, c, d = self.punkte
                a, b, c, d = Vektor(a.x, a.y, 0), Vektor(b.x, b.y, 0), \
                            Vektor(c.x, c.y, 0), Vektor(d.x, d.y, 0)
                self = Viereck(a, b, c, d, kontrolle=False)
                objekt = Vektor(objekt.x, objekt.y, 0)
        except AglaError as e:
            print('agla:', str(e))
            return			
        dd = self.dreiecke
        s0, s1 = dd[0].schnitt(objekt), dd[1].schnitt(objekt)
        if s0 or s1:
            if kwargs.get('l'):
                if isinstance(objekt, Vektor):			
                    display(Math('\\text{der Punkt liegt im Viereck}'))
                else:
                    if isinstance(s0, Strecke) or isinstance(s1, Strecke):
                        display(Math('\\text{die Gerade schneidet das ' + \
                               'Viereck in einer Strecke}'))					
                    else:
                        if isinstance(s0, Vektor) or isinstance(s1, Vektor):
                            if isinstance(s0, Vektor) and \
                                       isinstance(s1, Vektor):						
                                if s0 != s1:
                                    display(Math('\\text{die Gerade ' + \
                                    'schneidet das Viereck in ' + \
                                    'einer Strecke}'))											  
                                else:
                                    display(Math('\\text{die Gerade schneidet ' + \
                                    'das Viereck im Punkt}' + s0.punkt_ausg_(s=1)))                                    
                            else:						
                                ss = s0 if s0 else s1			
                                display(Math('\\text{die Gerade schneidet ' + \
                                       'das Viereck im Punkt}' + ss.punkt_ausg_(s=1)))                                
                        else:
                            display(Math('\\text{die Gerade schneidet das' + \
                                   'Viereck  nicht}'))							
                return
            if s0:
                if dim == 2:
                    s0 = Vektor(s0.x, s0.y)				
                return s0
            else:
                if dim == 2:
                    s1 = Vektor(s1.x, s1.y)				
                return  s1
        else:
            if kwargs.get('l'):
                if isinstance(objekt, Vektor):			
                    display(Math('\\text{der Punkt liegt nicht im Viereck}'))
                else:					
                    display(Math('\\text{die Gerade schneidet das Viereck ' + \
                    'nicht}'))
                return				
            return set()
		

    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Vierecks bei einer Abbildung\n")		
            print("Aufruf   viereck . bild( abb )")		                     
            print("             viereck    Viereck")
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
            p, q, r, s = self.punkte
            if not mit_param(self) and not mit_param(abb):
                p1, q1, r1, s1 = (p.bild(abb), q.bild(abb), r.bild(abb), 
                                                             s.bild(abb))
                return Viereck(p1, q1, r1, s1)
            elif self.is_par_gramm:
                stuetz1 = self.punkte[0].bild(abb)
                spann1 = m * Vektor(self.punkte[0], self.punkte[1])
                spann2 = m * Vektor(self.punkte[0], self.punkte[3])
                return Viereck(stuetz1, spann1, spann2) 	
            else:
                print("agla: nicht implementiert ")
                return				
        else: 
            k = self.in_koerper
            return k.bild(abb)

		
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Viereck"""	
        if self.dim == 3:
            if UMG.grafik_3d == 'mayavi':
                return self.mayavi(spez, **kwargs)
            else:				
                return self.vispy(spez, **kwargs)
        else:
            return self.graf2(spez, **kwargs)
  			
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Viereck in R^3 mit mayavi"""
		
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
        flaech_farbe = lin_farbe

        anim = False			
        if spez[3]:
            anim = True            
            aber = spez[3][:2]
		
        a, b, c, d = self.punkte		
        if not anim:		
            x = [float(p.x) for p in (a, b, c, d, a)]
            y = [float(p.y) for p in (a, b, c, d, a)]
            z = [float(p.z) for p in (a, b, c, d, a)]
            if not fuell:				
                return mlab.plot3d(x, y, z, line_width=lin_staerke, 
		                      color=lin_farbe, tube_radius=None)
            else:
                dreiecke = [(0, 1, 2), (0, 2, 3)]
                return mlab.triangular_mesh(x, y, z, dreiecke, \
                                            color=flaech_farbe)
        else:
            return None   # in Grafik-Routinen auf Koerper -> Strecke zurückgeführt
		
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Viereck in R^3 mit vispy"""
		
        pass
		
		
    def graf2(self, spez, **kwargs):                       
        """Grafikelement für Viereck in R^2"""	

        # 'fuell=True' - gefüllte Darstellung; default - ungefülte Darstellung	
		
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
            points.append(points[0])		
            if not fuell:	
                polygon = patches.Polygon(points, fill=None, 
                         edgecolor=lin_farbe, linewidth=lin_staerke)
                plt.gca().add_patch(polygon)
                return plt.plot([0], [0], 'w', markersize=0.0001)  # dummy plot	 
            else:
                polygon = patches.Polygon(points, facecolor=lin_farbe, 
                         edgecolor=lin_farbe)
                plt.gca().add_patch(polygon)
                return plt.plot([0], [0], 'w', markersize=0.0001)		 	
	
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        viereck_hilfe(3)	
		
    h = hilfe					
	
	
	
# Benutzerhilfe für Viereck
# -------------------------

def viereck_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nViereck - Objekt\n")
        print("Erzeugung im Raum R^3 und in der Ebene R^2:\n")
        print("             Viereck( A, B, C, D )")
        print("                 A, B, C, D    Eckpunkte\n")
        print("     oder    Viereck( /[ stütz, ] spann1, spann2 )")
        print("                 stütz    Stützvektor; bei Fehlen Nullvektor")
        print("                 spann    Spannvektor\n")
        print("Ist bei der Erzeugung über 4 Punkte kontrolle=False angegeben,")
        print("wird nicht geprüft, ob die Reihenfolge der Punkte korrekt ist\n")		
        print("Zuweisung     ve = Viereck(...)   (ve - freier Bezeichner)\n")
        print("Beispiel")
        print("A = v(-1, 0, 0); B = v(-2, -2, 0); C = v(1, -2, -2); D = v(2, 0, -2)")
        print("Viereck(A, B, C, D)")
        print("Viereck(A, B)\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Viereck\n")   
        print("ve.hilfe            Bezeichner der Eigenschaften und Methoden")
        print("ve.bild(...)     M  Bild bei einer Abbildung")
        print("ve.dim              Dimension")
        print("ve.dreiecke         Zerlegungsdreiecke")
        print("ve.ebene            Trägerebene   (im Raum R^3)")
        print("ve.fläche           Flächeninhalt")
        print("ve.fläche_(...) M   ebenso, zugehörige Methode")
        print("ve.form             Form")
        print("ve.in_figur         Konvertierung in Figur  (in der Ebene R^2)")
        print("ve.in_körper        Konvertierung in Körper  (im Raum R^3)")
        print("ve.is_konvex        Test auf Konvexität")
        print("ve.is_pargramm      Test auf Parallelogramm")
        print("ve.is_schar         Test auf Schar")
        print("ve.längen           Seitenlängen")
        print("ve.längen_(...)  M  ebenso, zugehörige Methode")
        print("ve.pkt(...)      M  Viereckpunkt")
        print("ve.punkte           Eckpunkte")
        print("ve.punkte_(...)  M  ebenso, zugehörige Methode")
        print("ve.sch_el(...)   M  Element einer Schar")
        print("ve.sch_par          Parameter einer Schar")
        print("ve.schnitt(...)  M  Schnittmenge mit anderen Objekten")
        print("ve.schwer_pkt       Schwerpunkt")
        print("ve.seiten           Seiten")
        print("ve.seiten_(...)  M  ebenso, zugehörige Methode")
        print("ve.umfang           Umfang")
        print("ve.umfang_(...)  M  ebenso, zugehörige Methode")
        print("ve.winkel           Innenwinkel")
        print("ve.winkel_(...)  M  ebenso, zugehörige Methode\n")
        print("Synonyme Bezeichner\n")
        print("hilfe        :  h")
        print("fläche_      :  Fläche")
        print("in_figur     :  inFigur")
        print("in_körper    :  inKörper")
        print("is_konvex    :  isKonvex")
        print("is_pargramm  :  isPargramm")
        print("is_schar     :  isSchar")
        print("längen_      :  Längen")
        print("punkte_      :  Punkte")
        print("sch_el       :  schEl")
        print("sch_par      :  schPar")
        print("schwer_pkt   :  schwerPkt")
        print("umfang_      :  Umfang")
        print("winkel_      :  Winkel\n")
        return
 
 