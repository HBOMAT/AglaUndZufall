#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
# Figur - Klasse  von agla           
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

import numpy as np
from agla.lib.objekte.umgebung import UMG	
if UMG.grafik_3d == 'mayavi':
    from tvtk.tools import visual
    from mayavi import mlab	
else:
    from vispy import app, scene
import matplotlib.pyplot as plt
import matplotlib.patches as patches		
		
from sympy.core.symbol import Symbol
from sympy.core.sympify import sympify, SympifyError
from sympy.core.containers import Tuple
from sympy.core.numbers import Zero, One, Integer

from agla.lib.objekte.basis import AglaObjekt
from agla.lib.objekte.vektor import Vektor
from agla.lib.objekte.gerade import Gerade
from agla.lib.objekte.ebene import Ebene, xy_ebene
from agla.lib.objekte.strecke import Strecke
from agla.lib.objekte.kreis import Kreis
from agla.lib.objekte.dreieck import Dreieck
from agla.lib.objekte.matrix import Matrix
from agla.lib.funktionen.funktionen import is_zahl, mit_param
from agla.lib.funktionen.abb_funktionen import drehung, verschiebung
from agla.lib.objekte.ausnahmen import AglaError
from agla.lib.objekte.umgebung import UMG	
import agla



# Figur - Klasse   
# --------------
	
class Figur(AglaObjekt):                                      
    """
			
Figur in der Ebene
	
**Erzeugung** 

   Figur ( *ecke1, ecke2*, ... )
 
      *ecke* : Eckpunkt
   
            Zur Ermittlung der Eckenfolge wird bei einer Ecke begonnen und 
            die gesamte Kantenmenge der Figur in einem Zug durchlaufen, 
            wobei alle auf dem Weg liegenden Ecken eingetragen werden; wird 
            eine Ecke erneut durchlaufen, ist sie erneut zu notieren 	  
		
   *oder*   
 
   Figur ( *ecken, kanten* )
   
      *ecken* : Liste mit den Eckpunkten; jeder Eckpunkt  ist ein Mal enthalten
      
      *kanten* : Liste mit den Kanten (2-elementige Listen/Tupel mit den 
      Indizes von Anfangs- und Endpunkt jeder Kante in der Eckenliste)
		
    """
		
		
    def __new__(cls, *args, **kwargs):  
			
        if kwargs.get("h") in (1, 2, 3):                         
            figur_hilfe(kwargs["h"])		
            return	

        try:
		
            if not args:
                raise AglaError("mindestens ein Argument angeben")
            a = args[0]
			
            if isinstance(a, Vektor):
                ecken_liste = list(args)
                if not ( all([isinstance(e, Vektor) for e in ecken_liste])
			          and  all([e.dim == 2 for e in ecken_liste]) ):
                    raise AglaError("als Ecken Punkte der Ebene angeben")
                ecken = [];
                for p in ecken_liste: 
                    if not p in ecken:
                        ecken += [p]
                if len (ecken) < 2:						
                    raise AglaError("mindestens 2 Ecken angeben")
                q = ecken_liste[0]
                ecken_liste = ecken
                pfad = list(args)				
                kanten_liste = [ [i, i+1] for i in range(len(list(args))-1) ]             			
                if pfad[-1] == pfad[0]:	
                    kanten_liste[-1] = [len(list(args))-2, 0]				
            elif isinstance(a, list):
                if not len(args) in (1, 2) :
                    raise AglaError("es müssen eine oder zwei Listen angegeben werden")
					
                ecken_liste = args[0]
                if len(args) == 1:
                    return Figur(*ecken_liste)
					
                kanten_liste = args[1]
                if not isinstance(kanten_liste, list):
                    raise AglaError("Kanten als Liste angeben")
					
                if len(ecken_liste) < 2 or len(kanten_liste) < 1:
                    txt = "mindestens zwei Ecken und eine Kante "+\
                          "angeben"
                    raise AglaError(txt)
			
                if not ( all([isinstance(e, Vektor) for e in ecken_liste]) \
			          and   all([e.dim == 2 for e in ecken_liste]) ):
                    raise AglaError("als Ecken Punkte der Ebene " + \
                         "angeben")
                if not ( all([isinstance(k, list) for k in kanten_liste]) \
                    and   all([len(k) == 2 for k in kanten_liste]) ):
                    txt = "in der Kantenliste Listen der Länge 2 angeben"
                    raise AglaError(txt)
				
                elem = set()
                for kante in kanten_liste:
                    if kante[0] == kante[1]:
                        txt = "zu einer Kante sind verschiedene Punktnummern " + \
                              "anzugeben"
                        raise AglaError(txt)
                    elem |= {kante[0]}.union({kante[1]})
                elem = [sympify(e) for e in elem]
                if not ( all([isinstance(e, (Integer, Zero, One)) for e in elem]) \
                    and all([(0 <= e <= len(ecken_liste) - 1) for e in elem]) ):
                    raise AglaError("ein Index ist falsch")
                def f(x):
                    if x[0] < x[1]: 
                        return x 
                    else: 
                        return [x[1], x[0]]
                kanten_liste = [f(k) for k in kanten_liste]
				
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
				
                al = adjazenz_liste(ecken_liste, kanten_liste)			
                pfad = durchlauf(al, 0)
                pfad = [ecken_liste[pfad[i]] for i in range(len(pfad))]        		

            return AglaObjekt.__new__(cls, ecken_liste, kanten_liste, pfad)
		           
        except AglaError as e:
            print('agla:', str(e))
            return			
		
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            ss = str([el for el in par]).replace('[', '')
            ss = ss.replace(']', '')
            return "Figurschar(" + ss + ")"
        else:
            return "Figur"	
			
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def dim(self):              
        """Dimension"""
        return 2
		
    @property			
    def ecken(self):              
        """Eckenliste"""
        return self.args[0]
		
    punkte = ecken		
		
    @property			
    def kanten(self):              
        """Kantenliste"""		
        return self.args[1]
		
    linien = kanten		
	
    @property			
    def anz_ecken(self):              
        """Anzahl Ecken"""
        return len(self.ecken)
    anzEcken = anz_ecken	
	
    anz_punkte = anz_ecken
    anzPunkte = anz_ecken
	
    @property			
    def anz_kanten(self):              
        """Anzahl Kanten"""
        return len(self.kanten)
		
    anzKanten = anz_kanten	
    anz_linien = anz_kanten	
    anzLinien = anz_kanten	
		
    @property			
    def is_geschlossen(self):              
        """Test auf geschlossene Figur"""
        p = self.pfad
        return p[-1] == p[0]
		
    isGeschlossen = is_geschlossen 		
    is_zu = is_geschlossen	
    isZu = is_geschlossen	

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
    def pfad(self):
        """Pfad; Durchlaufen aller Kanten der Figur in einem Zug"""
        return self.args[2]	
		
    @property			
    def matrix(self):
        """Matrix (aus den Punkten des Pfades)"""
        pfad = self.pfad        		
        return Matrix(*pfad)	
						
		
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar; für einen Parameter"""
		 
        if not self.is_schar or len(self.sch_par) > 1:
            print("agla: keine Schar mit einem Parameter")	
            return			
		
        if kwargs.get('h'):
            print("\nElement einer Figurschar\n")		
            print("Aufruf   figur . sch_el( wert )\n")		                     
            print("             figur   Figur")
            print("             wert    Wert des Scharparameters")			
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
        return Figur(ecken_neu, self.kanten)
		
    schEl = sch_el

	
    def bild(self, *abb, **kwargs):
        """Bild bei einer Abbildung"""
		
        if kwargs.get('h'):
            print("\nBild der Figur bei einer Abbildung\n")		
            print("Aufruf   figur . bild( abb )\n")		                     
            print("             figur   Figur")
            print("             abb     Abbildung\n")			
            return 				
			
        if len(abb) != 1:
            print("agla: eine Abbildung angeben")
            return			
        abb = abb[0]
        Abbildung = importlib.import_module('agla.lib.objekte.abbildung').Abbildung	
        if not (type(abb) is Abbildung and abb.dim == 2):
            print("agla: eine Abbildung der Ebene angeben")
            return
        pfad = [ e.bild(abb) for e in self.pfad ]
        return Figur(pfad)
	
	
    def graf(self, spez, **kwargs):                       
        """Grafikelement für Figur"""

		 # 'füll=True' - gefüllte Darstellung

        lin_farbe = UMG._default_lin_farbe2 if spez[1] == 'default' else spez[1]		
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
            aber = spez[3][-2], spez[3][-1]			
		
        if not anim:
            ecken = self.ecken
            pfad = self.pfad			
            plot = []
            for k in self.kanten:
                p, q = ecken[k[0]], ecken[k[1]] 
                x, y = [float(p.x), float(q.x)], [float(p.y), float(q.y)]
                plot += [plt.plot(x, y, linewidth=lin_staerke, color=lin_farbe)]      
            if fuell:			
                if pfad[-1] != pfad[0]:
                    pfad += [pfad[0]]
                ecken1 = [ [float(e.x), float(e.y)] for e in pfad ]						
                polygon = patches.Polygon(ecken1, closed=True, fill=True, 
                        edgecolor=lin_farbe, facecolor=lin_farbe, 
                        linewidth=lin_staerke)
                plt.gca().add_patch(polygon)
	
            return tuple(plot)		
	
	
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        figur_hilfe(3)	
		
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
    pfad = []
    for knoten in weg:
        pfad += [knoten]
        for nachbar in graph[knoten]:
            k = sorted([knoten, nachbar])		
            if not k in kanten:
                kanten += [k]
                pfad += [nachbar, knoten]	
				
    return pfad
	
						
	
# Benutzerhilfe für Figur
# -----------------------

def figur_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print("\nFigur - Objekt\n")
        print("Erzeugung in der Ebene R^2:\n")
        print("             Figur( ecke1, ecke2, ... )\n")
        print("                 ecke    Eckpunkt\n")
        print("                 Zur Ermittlung der Eckenfolge wird bei einer")
        print("                 Ecke begonnen und die gesamte Kantenmenge der ") 
        print("                 Figur in einem Zug durchlaufen, wobei alle auf")  
        print("                 dem Weg liegenden Ecken eingetragen werden; ") 
        print("                 wird eine Ecke erneut durchlaufen, ist sie erneut")
        print("                 zu notieren\n")        
        print("     oder    Figur( ecken, kanten )\n")
        print("                 ecken    Liste mit den Eckpunkten")  		
        print("                 kanten   Liste mit den Kanten (2-elementige")
        print("                          Listen/Tupel mit Anfangs- und Endpunkt")
        print("                          jeder Kante)\n")
        print("                 Die Ecken-Liste enthält jeden Eckpunkt ein Mal")		
        print("                 in der Kanten-Liste werden die Punkte über ihre")
        print("                 Indizes in der Ecken-Liste eingetragen\n")
        print("Zuweisung     f = Figur(...)   (f - freier Bezeichner)\n")
        print("Beispiele\n")
        print("Figur(v(-2, 0), v(0, 4), v(-1, 2), v(1, 2), v(0, 4), v(-2, 0)) - ein 'A'\n")
        print("k = Kreis(O2, 3)")
        print("ecken = [ k.pkt(i/5 * 360) for i in range(6) ]")
        print("kanten = [ [0, 1], [1, 2], [2, 3], [3, 4], [4, 0] ]")
        print("Figur(ecken, kanten) - ein regelmäßiges Fünfeck\n")
        return        
		
    if h == 3:   
        print("\nEigenschaften und Methoden (M) für Figur\n")
        print("f.hilfe              Bezeichner der Eigenschaften und Methoden")
        print("f.anz_ecken          Anzahl Ecken") 
        print("f.anz_kanten         Anzahl Kanten") 		
        print("f.anz_linien         = f.anz_kanten") 
        print("f.anz_punkte         = f.anz_ecken") 
        print("f.bild(...)       M  Bild bei einer Abbildung") 
        print("f.dim                Dimension") 
        print("f.ecken              Erzeugende Eckpunkte") 
        print("f.is_geschlossen     Test auf geschlossene Figur")
        print("f.is_schar           Test auf Schar")
        print("f.is_zu              = f.is_geschlossen")
        print("f.kanten             Kanten") 
        print("f.pfad               Durchlaufen aller Kanten; eventuell mehrfach")
        print("f.linien             = f.kanten")
        print("f.matrix             Matrix aus den Punkten des Pfades f.pfad")
        print("f.punkte             = f.ecken") 
        print("f.sch_par            Parameter einer Schar")
        print("f.sch_el(...)     M  Element einer Figurenschar\n")
        print("Synonyme Bezeichner\n")
        print("hilfe          :  h")
        print("anz_ecken      :  anzEcken")
        print("anz_kanten     :  anzKanten")
        print("anz_linien     :  anzLinien")
        print("anz_punkte     :  anzPunkte")
        print("is_geschlossen :  isGeschlossen")
        print("is_zu          :  isZu")
        print("sch_par        :  schPar")
        print("sch_el         :  schEl\n")
        return			
   		
	
	