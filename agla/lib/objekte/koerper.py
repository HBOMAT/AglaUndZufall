#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Koerper - Klasse  von agla           
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



import copy
import importlib

from agla.lib.objekte.umgebung import UMG	
if UMG.grafik_3d == 'mayavi':
    from tvtk.tools import visual
    from mayavi import mlab	
else:
    from vispy import app, scene
		
from sympy import Symbol
from sympy.core.sympify import sympify, SympifyError
from sympy.core.containers import Tuple
from sympy.core.numbers import Zero, One, Integer

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.ebene import Ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.figur import Figur
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.matrix import Matrix
from agla.lib.funktionen.funktionen import is_zahl, mit_param
from agla.lib.funktionen.abb_funktionen import drehung, verschiebung, kabinett
from agla.lib.funktionen.funktionen import ja, Ja, nein, Nein, mit, ohne
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.objekte.umgebung import UMG	
import agla



# Koerper - Klasse   
	
class Koerper(AglaObjekt):                                      
    """
	
Konvexe Körper im Raum
	
**Erzeugung** konvexer Körper

   Körper ( *ecke1, ecke2*, ... )
 
      *ecke* :    Eckpunkt
   
            Zur Ermittlung der Eckenfolge wird bei einer Ecke begonnen und 
            die gesamte Kantenmenge des Körpers in einem Zug durchlaufen, 
            wobei alle auf dem Weg liegenden Ecken eingetragen werden; wird 
            eine Ecke erneut durchlaufen, ist sie erneut zu notieren 	  
		
   *oder*   
 
   Körper ( *ecken, kanten* )
   
      *ecken* : Liste mit den Eckpunkten; jeder Eckpunkt  ist ein Mal 
      enthalten
      
      *kanten* : (2-elementige Listen/Tupel mit den Indizes von Anfangs- 
      und Endpunkt in der Eckenliste

   *oder*   

   Körper ( *körper1, körper2, ...* )
   
      *körper* : beliebiger Körper 
	  
            Wird der Zusatz `seiten=ja` angegeben, wird der Körper als 
            über seine Seitenflächen erzeugt angesehen; diese müssen 
            geschlossene ebene Körper (Polygone) darstellen
   
    """	
	
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            koerper_hilfe(kwargs["h"])		
            return	
						
        try:
		
            if not args:
                raise AglaError("mindestens ein Argument angeben")
            a = args[0]
            #matrix_eingabe = False
						
            if isinstance(a, Vektor):
                txt = "in der Eckenliste Punkte im Raum angeben"			
                if a.dim != 3:
                    raise AglaError(txt)
                ecken_liste = list(args)
                if not ( all([isinstance(x, Vektor) for x in ecken_liste])
			          and all([x.dim == 3 for x in ecken_liste]) ):
                    raise AglaError(txt)
                ecken = [];
                for p in ecken_liste: 
                    if not p in ecken:
                        ecken += [p]
                if len (ecken) < 2:						
                    raise AglaError("mindestens 2 Ecken angeben")
                kanten = []
                q = ecken_liste[0]
                for p in ecken_liste[1:]:
                    if p != q:
                         kanten += [[ecken.index(q), ecken.index(p)]]
                    q = p
                ecken_liste = ecken
                kanten_liste = kanten
				
            elif isinstance(a, list):
                if not (len(args) == 2 and isinstance(args[1], list)):
                    raise AglaError("es müssen zwei Listen angegeben werden")
				
                ecken_liste, kanten_liste = args
			
                if len(ecken_liste) < 2 or len(kanten_liste) < 1:
                    txt = "mindestens zwei Ecken und eine Kante "+\
                          "angeben"
                    raise AglaError(txt)
			
                if not ( all([type(x) == Vektor for x in ecken_liste])
			         and   all([x.dim == 3 for x in ecken_liste]) ):
                    raise AglaError("in der Punkteliste Punkte im Raum " + \
                         "angeben")
				
                if not ( all([isinstance(x, (list, tuple, Tuple)) for x in kanten_liste])
                    and   all([len(x) == 2 for x in kanten_liste]) ):
                    txt = "in der Kantenliste Listen/Tupel der Länge 2 angeben"
                    raise AglaError(txt)
										            			
            elif isinstance(a, Koerper):
                koerper_liste = list(args)
                if not all([isinstance(x, Koerper) for x in koerper_liste]):
                    raise AglaError("mehrere Koerper angeben")
                summen_koerper = koerper_liste[0]
                for k in koerper_liste[1:]:
                    summen_koerper = summen_koerper.vereinigen(k)
            				
                # zusätzliche Abspeicherung der Seiten
                if kwargs.get("seiten"):   
                    ecken = summen_koerper.ecken         
                    kanten = summen_koerper.kanten     
                    return AglaObjekt.__new__(cls, ecken, kanten, 
				                                         koerper_liste)
                else:				
                    return summen_koerper
					
            elem = set()
            for li in kanten_liste:
                if li[0] == li[1]:
                    txt = "zu einer Kante sind verschiedene Punktenummern " + \
                          "anzugeben"
                    raise AglaError(txt)
                elem |= {li[0]}.union({li[1]})
            elem = [sympify(x) for x in elem]
            if not ( all([type(x) in (Integer, Zero, One) for x in elem])  
                and all([(0 <= x <= len(ecken_liste) - 1) for x in elem]) ):
                raise AglaError("ein Index ist falsch")
            def f(x):
                if x[0] < x[1]: 
                    return x 
                else: 
                    return [x[1], x[0]]
            kanten_liste = [f(x) for x in kanten_liste]
		     # Sortierung nach zweiter Kantennummer, dann nach erster
            kanten_liste = sorted(kanten_liste, key=lambda x: x[1])			
            kanten_liste = sorted(kanten_liste, key=lambda x: x[0])	
            # Beseitigung von doppelten Kanten
            kante = kanten_liste[0]
            kl = [kante]
            for ka in kanten_liste[1:]:
                if not ka == kante:
                    kl += [ka]
                    kante = ka
            kanten_liste = kl

            return AglaObjekt.__new__(cls, ecken_liste, kanten_liste)
		           
        except AglaError as e:
            print('agla:', str(e))
            return			
		
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Körperschar(" + ss + ")"
        else:
            return "Körper"	
			
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 3
		
    @property			
    def ecken(self):              
        """Eckenliste"""
        return self.args[0]
		
    @property			
    def kanten(self):              
        """Kantenliste"""		
        return self.args[1]
	
    @property			
    def anz_ecken(self):              
        """Anzahl Ecken"""
        return len(self.ecken)
		
    anzEcken = anz_ecken		
		
    @property			
    def anz_kanten(self):              
        """Anzahl Kanten"""
        return len(self.kanten)
		
    anzKanten = anz_kanten	
		
    @property			
    def anz_seiten(self):              
        """Anzahl Seiten"""
        s = self.seiten
        return len(s)
		
    anzSeiten = anz_seiten		
		
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        pl = self.args[0]
        par = set()
        for p in pl:
            par |= p.sch_par
        return par
		
    schPar = sch_par		

    @property		
    def is_schar(self):              
        """Test auf Schar"""
        return len(self.sch_par) == 1
		
    isSchar = is_schar		

    @property
    def is_eben(self):
        """Test auf ebenen Koerper"""
        grenze = 10**(-4)
        e = self.ecken
        if len(e) < 4:
            return True
        eb = Ebene(e[0], Vektor(e[0], e[1]), Vektor(e[0], e[2]))
        for i in range(3, len(e)):
            if abs(e[i].abstand(eb)) > grenze:
                return False
        return True
		
    isEben = is_eben		
		
    @property
    def seiten(self):
        """Seitenflächen"""
					
        if len(self.args) >= 3:
            if type(self.args[2]) == list:
                return self.args[2]
        if self.is_eben:
            return [self]			
        if mit_param(self):
            print('agla: nicht implementiert (Parameter)')	
            return
			
        import numpy as np			
        from scipy.spatial import ConvexHull
			
        ecken = self.ecken
        xx = np.array([p.x for p in ecken])
        yy = np.array([p.y for p in ecken])
        zz = np.array([p.z for p in ecken])
        pts = np.array([xx, yy, zz], 'f').T
        hull = ConvexHull(pts)
        grenze = 0.0001
        # Sammeln der komplanaren Punkte
        behandelt = [False] * len(hull.simplices)
        komplanare_punkte = []
        for i, d in enumerate(hull.simplices):   # eventuell nicht effizient
            if behandelt[i]:
                continue
            punkte = set(d)
            gl = hull.equations[i]
            for j, d1 in enumerate(hull.simplices):
                if not behandelt[j]:
                    gl1 = hull.equations[j]
                    if abs(gl[0]*gl1[0] + gl[1]*gl1[1] + gl[2]*gl1[2] - 1) \
                                                        < grenze:
                        punkte = punkte.union(set(d1))
                        behandelt[j] = True
            behandelt[i] = True
            komplanare_punkte += [[punkte, gl]]
        # konvexe Hülle (2D) der komplanaren Punkte ermitteln
        seiten_liste = []		
        for kp in komplanare_punkte:
            punkte, gl = kp[0], kp[1]
            if abs(abs(gl[1]) - 1) < grenze:  # Projekton auf xz-Ebene
                pts_2d = pts[:, ::2] 
            elif abs(gl[2]) < grenze and abs(gl[1]) < 1:  # auf yz-Ebene
                pts_2d = pts[:, 1:]
            else:                         # auf xy-Ebene
                pts_2d = pts[:, :2]
            punkte_2d = np.array([pts_2d[hull.vertices[i]] for i in punkte])
            punkte_3d = [ecken[hull.vertices[i]] for i in punkte]
            hull_2d = ConvexHull(punkte_2d)
            # Punkteliste der Seite			
            sl = [punkte_3d[i] for i in hull_2d.vertices]
            # Kantenzug schliessen			
            sl = sl + [sl[0]]
            seite = Koerper(*sl)
            seiten_liste += [seite]     
        return seiten_liste			                                   			   				
			
    @property			
    def pfad(self):
        """Pfad; Durchlaufen aller Kanten des Körpers in einem Zug; siehe Erzeugung eines Körpers über seine Ecken"""
        al = adjazenz_liste(self.ecken, self.kanten)			
        pfad = durchlauf(al, 0)
        pfad = [self.ecken[pfad[i]] for i in range(len(pfad))]        		
        return pfad
		    			
    @property			
    def matrix(self):
        """Matrix aus den Punkten des Pfades"""
        pf = self.pfad        		
        return Matrix(*pf)	
						
    @property
    def mark_ecken(self):
        """Markieren der Ecken in der Grafik"""

        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
			
        _mass = UMG._mass()		
        mlab.close(all=True)
		
        fig = mlab.figure(bgcolor=(1, 1, 1))    
        visual.set_viewer(fig)		
        dist = 3 * _mass
        mlab.view(azimuth=15, elevation=70, distance=dist)
        self.graf((None, 'default', 'default', None))
        for i, e in enumerate(self.ecken):
            mlab.text3d(e.x, e.y, e.z , '%s'%i, scale=0.4*_mass, 
                      color=(0, 0, 0))
        mlab.show()

    markEcken = mark_ecken
	
    @property
    def mark_kanten(self):
        """Markieren der Kanten in der Grafik"""

        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        _mass = UMG._mass()		
        mlab.close(all=True)
		
        fig = mlab.figure(bgcolor=(1, 1, 1))    
        visual.set_viewer(fig)		
        dist = 3 * _mass
        mlab.view(azimuth=15, elevation=70, distance=dist)
        self.graf((None, 'default', 'default', None))
        ecken = self.ecken
        for i, k in enumerate(self.kanten):
            m = 1/2 * (ecken[k[0]] + ecken[k[1]])
            mlab.text3d(m.x, m.y, m.z + 0.1*_mass, '%s'%i, \
                           scale=0.4*_mass, color=(0, 0, 0))
        mlab.show()
		
    markKanten = mark_kanten
		
    @property
    def mark_seiten(self):
        """Markieren der Seiten in der Grafik"""

        if mit_param(self):
            print("agla: nicht implementiert (Parameter)")
            return
					
        _mass = UMG._mass()		
        mlab.close(all=True)
		
        fig = mlab.figure(bgcolor=(1, 1, 1))    
        visual.set_viewer(fig)		
        dist = 3 * _mass
        mlab.view(azimuth=15, elevation=70, distance=dist)
        self.graf((None, 'default', 'default', None))
        for i, s in enumerate(self.seiten):
            m = Vektor(0, 0, 0)		
            for e in s.ecken:
                m += e
            m = m * 1/s.anz_ecken
            mlab.text3d(m.x, m.y, m.z + 0.1*_mass, '%s'%i, \
                           scale=0.4*_mass, color=(0, 0, 0))
        mlab.show()

    markSeiten = mark_seiten		
		
    def vereinigen(self, *args, **kwargs):
        """Vereinigen mit einem anderen Koerper"""
		
        if kwargs.get('h'):
            print("\nVereinigen mit einem anderen Körper\n")		
            print("Aufruf   körper . vereinigen( körper1 )\n")		                     
            print("             körper   Körper\n")
            return 		
				
        if len(args) == 0:				
            print("agla: einen anderen Körper angeben")
            return			 
        grenze = 10**(-4)
        koerper = args[0]	
        if not isinstance(koerper, Koerper):
            print("agla: einen anderen Körper angeben")
            return			 
        ecken_1, ecken_2 = self.ecken, koerper.ecken
        ecken_neu = ecken_1[:]		
        ind = dict()
        for i in range(len(ecken_2)):
            ende = False
            try:
                ind[i] = ecken_1.index(ecken_2[i])
                ende = True
            except:
                for j in range(len(ecken_1)):
                    if _abstand(ecken_1[j], ecken_2[i]) < grenze:
                        ind[i] = j
                        ende = True
            if not ende:
                ecken_neu.append(ecken_2[i])
                ind[i] = len(ecken_neu) - 1				
        li = [[ind[int(x[0])], ind[int(x[1])]] for x in koerper.kanten]
        kanten_neu = self.kanten[:]
        kanten_neu += li
        return Koerper(ecken_neu, kanten_neu)

		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Körperschar\n")		
            print("Aufruf   körper . sch_el( wert )\n")		                     
            print("             körper   Körper")
            print("             wert     Wert des Scharparameters")			
            print("\nEs ist nur ein Scharparameter zugelassen\n")    
            return 
			
        if len(wert) != 1:
            print("agla: einen Wert für den Scharparameter angeben") 
            return			
        p = Tuple(*self.sch_par)[0]
        wert = sympify(*wert)
        ecken_neu = []
        for e in self.ecken:
            if e.has(p):
                e = e.sch_el(wert)
            ecken_neu += [e]
        return Koerper(ecken_neu, self.kanten)
		
    schEl = sch_el

	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild des Körpers bei einer Abbildung\n")		
            print("Aufruf   körper . bild( abb )\n")		                     
            print("             körper    Körper")
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
        ecken1 = [e.bild(abb) for e in self.ecken]
        return Koerper(ecken1, self.kanten)
	
    @property	
    def in_2d(self):
        """Konvertierung in Figur-Objekt; nur für ebene Körper"""		
        bild = self.bild(kabinett)		
        e, k = bild.ecken, bild.kanten
        e = [ Vektor(p.y, p.z) for p in e ]
        return Figur(e, k)		

    in2d = in_2d
	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Koerper"""
        if UMG.grafik_3d == 'mayavi':
            return self.mayavi(spez, **kwargs)
        else:				
            return self.vispy(spez, **kwargs)	
	
    def mayavi(self, spez, **kwargs):                       
        """Grafikelement für Koerper mit mayavi"""
		
        # 'füll=ja'   - gefüllte Darstellung; default - ungefülte Darstellung	
        # 'kanten=nein' - kein Zeichnen der Kanten; default - Zeichnen
		
        import numpy as np
        from mayavi import mlab
			
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
				
        if fuell and self.is_eben:
            if self.anz_kanten > self.anz_ecken:
                print('agla: das Füllen des Körpers ist nicht implementiert')
                fuell = False				
			
        flaech_farbe = UMG._default_flaech_farbe if spez[1] == 'default' \
                                                        else spez[1]		
        lin_farbe = UMG._default_lin_farbe if spez[1] == 'default' else spez[1]		
        lin_staerke = UMG._default_lin_staerke if spez[2] == 'default' \
                                                       else spez[2][1]
        if fuell and kanten:
            lin_farbe =(0, 0, 0)		
            lin_staerke = UMG._default_lin_staerke
													   
        anim = False			
        if self.is_schar:
            anim = True            
            aber = spez[3][:2]
				
        if not anim:
            if not fuell or kanten:	
                ecken, kant = self.ecken, self.kanten
                plt = []
                for k in kant:		
                    x = [float(ecken[k[0]].x), float(ecken[k[1]].x)]		
                    y = [float(ecken[k[0]].y), float(ecken[k[1]].y)]		
                    z = [float(ecken[k[0]].z), float(ecken[k[1]].z)]
                    plt += [mlab.plot3d(x, y, z, line_width=lin_staerke, 
		                      color=lin_farbe, tube_radius=None)]
            if fuell:
                plt = []			
                for s in self.seiten:
                    ecken = s.ecken
                    x = [float(e.x) for e in ecken]		
                    y = [float(e.y) for e in ecken]		
                    z = [float(e.z) for e in ecken]		
                    dreiecke = [(0, i, i+1) for i in range(len(ecken) - 1)]
                    plt += [mlab.triangular_mesh(x, y, z, dreiecke, 
                           color=flaech_farbe)]
            return tuple(plt)	
        else:	
            return self   # in Grafik-Routinen auf Strecke zurükgeführt
			
                     	
    def vispy(self, spez, **kwargs):                       
        """Grafikelement für Koerper mit vispy"""
		
        pass		
		

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        koerper_hilfe(3)	
		
    h = hilfe					
				

	
# Algorithmen für Graphen
# -----------------------

# Adjazenz-Liste, gewonnen aus Ecken- und Kantenliste eines Graphen

def adjazenz_liste(ecken, kanten):
    adj = []
    for e in ecken:
        el = []
        for k in kanten:
            ei = ecken.index(e)
            if ei in k:
                if ei == k[0]:
                    if k[1] not in el:
                        el += [k[1]]
                else:
                    if k[0] not in el:
                        el += [k[0]]
        adj += [el]
    return adj	

# Ermitteln eines Weges durch den Graphen, der jede Kante
# mindestens einmal enthält	
# zunächst wird per Tiefensuche ein Weg mit allen Knoten ermittelt
# danach werden die fehlenden Kanten ergänzt
# es wird nicht auf Effizienz geachtet
#
# Der Graph ist mittels Adjazenz-Liste gegeben	

def durchlauf(graph, start_knoten):

    def besuch(knoten, weg): 
        if not besucht[knoten]: 
            besucht[knoten] = True		
            weg += [knoten]
            for nachbar in graph[knoten]: 
                besuch(nachbar, weg)
				
    besucht = [False] * len(graph)
    weg = []	
    besuch(start_knoten, weg)
	
    kanten = []
    zug = []
    for knoten in weg:
        zug += [knoten]
        for nachbar in graph[knoten]:
            k = sorted([knoten, nachbar])		
            if not k in kanten:
                kanten += [k]
                zug += [nachbar, knoten]	
				
    return zug
	
	
# Schnelle Abstandsberechnung
# ---------------------------
def _abstand(p1, p2):
    import numpy as np
    return np.abs(np.sqrt((float(p1.x)-float(p2.x))**2 + 
	      (float(p1.y)-float(p2.y))**2 + (float(p1.z)-float(p2.z))**2))
		
		
	
# Benutzerhilfe für Koerper
# -------------------------

def koerper_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nKörper - Objekt       zur Erzeugung konvexer Körper\n")
        print("Erzeugung im Raum R^3:\n")
        print("             Körper( ecke1, ecke2, ... )\n")
        print("                 ecke    Eckpunkt\n")
        print("                 Zur Ermittlung der Eckenfolge wird bei einer")
        print("                 Ecke begonnen und die gesamte Kantenmenge des ") 
        print("                 Körpers in einem Zug durchlaufen, wobei alle auf")  
        print("                 dem Weg liegenden Ecken eingetragen werden; ") 
        print("                 wird eine Ecke erneut durchlaufen, ist sie erneut")
        print("                 zu notieren\n")        
        print("     oder    Körper( ecken, kanten )\n")
        print("                 ecken    Liste mit den Eckpunkten; jeder Eckpunkt")  		
        print("                          ist ein Mal enthalten")		
        print("                 kanten   Liste mit den Kanten (2-elementige")
        print("                          Listen/Tupel mit den Indizes von Anfangs-")
        print("                          und Endpunkt in der Eckenliste)\n")
        print("     oder    Körper( körper1, körper2, ... )\n")
        print("                 körper    beliebiger Körper\n")
        print("                 Wird mit einem Schlüsselwortparameter seiten=ja") 
        print("                 angegeben, wird der Körper als über seine Seiten-")
        print("                 flächen erzeugt angesehen; diese müssen geschlos-")
        print("                 sene ebene Körper (Polygone) darstellen\n")
        print("Zuweisung     k = Körper(...)   (k - freier Bezeichner)\n")
        print("Beispiele\n")
        print("Körper(v(-2, 0, 3), v(2, -2, 0), v(5, 2, -1), v(2, -1, 1), v(-2, 0, 3))\n")
        print("ecken = [ v(-2, 0, 3), v(2, -2, 0), v(5, 2, -1) ]");
        print("kanten = [ [0, 1], [1, 2], [0, 2] ]")
        print("Körper(ecken, kanten) - ein ebener Körper (Dreieck)\n")
        print("A = O; B = v(4, 0, 0); C = v(0, 4, 0); S = v(0, 0, 5)")
        print("seiten = [ Körper(A, B, C, A), Körper(A, B, S, A), Körper(B, C, S, B),")
        print("           Körper(C, A, S, C) ]")
        print("k = Körper(*seiten, seiten=ja) - über Seiten definiert\n")		
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Körper\n")
        print("k.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("k.anz_ecken          Anzahl Ecken") 
        print("k.anz_kanten         Anzahl Kanten") 
        print("k.anz_seiten         Anzahl Seitenflächen") 
        print("k.bild(...)       M  Bild bei einer Abbildung") 
        print("k.dim                Dimension") 
        print("k.ecken              Eckpunkte") 
        print("k.in_2d              Konvertierung in Figur")
        print("k.is_eben            Test auf ebenen Körper")
        print("k.is_schar           Test auf Schar")
        print("k.kanten             Kanten") 
        print("k.mark_ecken         Markieren der Ecken in der Grafik")
        print("k.mark_kanten        Markieren der Kanten in der Grafik")
        print("k.mark_seiten        Markieren der Seitenflächen in der Grafik")
        print("k.matrix             Matrix aus den Punkten des Pfades k.pfad")
        print("k.pfad               Durchlaufen aller Kanten; eventuell mehrfach")
        print("k.sch_par            Parameter einer Schar")
        print("k.sch_el(...)     M  Element einer Körperschar")
        print("k.seiten             Seitenflächen")
        print("k.vereinigen(...) M  Vereinigen mehrerer Körper\n")
        print("Synonyme Bezeichner\n")
        print("hilfe       :  h")
        print("anz_ecken   :  anzEcken")
        print("anz_kanten  :  anzKanten")
        print("anz_seiten  :  anzSeiten")
        print("in_2d       :  in2d")
        print("is_eben     :  isEben")
        print("is_schar    :  isSchar")
        print("mark_ecken  :  markEcken")
        print("mark_kanten :  markKanten")
        print("mark_seiten :  markSeiten")
        print("sch_par     :  schPar")
        print("sch_el      :  schEl\n")
        return
   		
	
	