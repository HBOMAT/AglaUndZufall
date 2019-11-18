#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  ZufallsExperiment - Klasse  von zufall           
#                                                 
                                  
#
#  This file is part of zufall
#
#
#  Copyright (c) 2019 Holger Böttcher  hbomat@posteo.de
#
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  



import importlib
import copy
from itertools import product
from inspect import isfunction

from IPython.display import display, Math

import numpy as np
from scipy.stats import rv_discrete

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from sympy.core.numbers import Integer, Rational, Float, Tuple
from sympy import Add
from sympy.core.symbol import Symbol
from sympy import sympify, sqrt, nsimplify
from sympy.printing.latex import latex
from sympy.core.compatibility import iterable

from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.zufalls_groesse import ZufallsGroesse 
from zufall.lib.objekte.datenreihe import DatenReihe 
from zufall.lib.funktionen.graf_funktionen import verlauf
from zufall.lib.funktionen.funktionen import kombinationen, anzahl_treffer
	
from zufall.lib.objekte.ausnahmen import ZufallError

import zufall



# ZufallsExperiment - Klasse  
# --------------------------
	
class ZufallsExperiment(ZufallsObjekt):                                         
    """

Zufallsexperiment

**Kurzname** **ZE**

**Synonym** ZV (ZufallsVersuch)
	
**Erzeugung** 
	
   ZE(*liste /[, stufen ]* )

      *stufen* :   Anzahl Stufen; Standard = 1
				 
   *oder*

   ZE( *liste1, liste2, ...*)
   
      bei mehrstufigem Experiment je Sufe eine Liste, diese 
      können unterschiedlich sein
				 
   *oder*

   ZE( *v_liste* )
   
                 vollständige Liste bei einem mehrstufigen Zufallsexperiment
				 
**Parameter**

   *liste* : liste_1 | liste_2 | dict
		 
   *v_liste* : 
   
      | *liste_1* | 
      | *[(obj1, zahl1), v_liste1, (obj2, zahl2),* 
                  *v_liste2, ...]* 
      | (*vollständige Liste*)
				
   *liste_1* : 
   
      | *[ (obj1, zahl1), (obj2, zahl2), ...]*  |
      | *[ [obj1, zahl1], [obj2, zahl2], ...]* 				 
      | (obj-zahl-Paare als Tupel oder Liste)
				     
   *liste_2* :
	  
      | *[obj1, obj2, ...]*  
      | (äquivalent zu *[ (obj1, 1), (obj2, 1), ...]* )

   *Stufen* : 

      Anzahl Stufen
	  
   *dict* : *{ obj1:zahl1, obj2:zahl2, ...}*  (dictionary)
	  
   *obj* : Bezeichner | ganze Zahl >= 0
				 
**Zusatz**
   `a=nein` - keine Beachtung der Anordnung/Reihenfolge; Standard=ja
   
   `w=nein` - keine Wiederholung von Elementen; Standard=ja
   
   `f=funktions_name` - Name einer ZG-Funktion (diese ordnet den Elementen 
   der Ergebnismenge Zahlen zu)
		 
Wird eine Liste mit nur zwei unterschiedlichen Objekten angegeben, wird
bei Verwendung der Funktion ``anzahl_treffer``
 
   | bei Wiederholung von Elementen ein BernoulliKette - Objekt
   
   | bei Nicht-Wiederholung von Elementen ein HyperGeometrischeVerteilung -
      Objekt
	   
erzeugt

Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette 
eingegeben oder vordeklariert werden, etwa  ``Raucher = Symbol('Raucher')``
		
    """

	
    def __new__(cls, *args, **kwargs):  
        			
        if kwargs.get("h") in (1, 2, 3):                         
            zufalls_experiment_hilfe(kwargs["h"])		
            return	
					
        def list_kontrolle(liste):
            if all([isinstance(x, (Symbol, str, int, Integer)) for x in liste]):
                return True
            if all([isinstance(x, (list, tuple)) and len(x) == 2 for x in liste]):
                s = all([isinstance(x[0], (Symbol, str, int, Integer)) for x in liste])		
                w = all([isinstance(x[1], (int, Integer)) for x in liste])
                if s and w:
                    return True
                return False
            return False				
  
        def einfach(liste):
            if any([isinstance(x, list) for x in liste]):
                return False			
            return True
			
        def einfacheinfach(liste):
            if all([isinstance(x, (Symbol, str, int, Integer)) for x in liste]):
                return True
            return False
 			
        def dict_kontrolle(dict):
            s = all([isinstance(x, (Symbol, str, int, Integer)) for x in dict])		
            w = all([isinstance(dict[x], (int, Integer, Rational, float, Float)) \
                for x in dict])
            if s and w:
                return True
            return False
			
        def dict2list(di):
            if not isinstance(di, dict):
                return di			
            return [(x, di[x]) for x in di]	

        def normierung(liste):
            summe = 0
            for x in liste:
                summe += x[1]
            return [(x[0], nsimplify(x[1] / summe)) for x in liste]							
		
        wiederh = True
        if kwargs.get('w') == False:
            wiederh = False
        anordn = True
        if kwargs.get('a') == False:
            anordn = False
        funktion = kwargs.get('f')	
		
        if funktion:
            if isinstance(funktion, str):	
                funktion = eval(funktion)
            if not isfunction(funktion):
                print('zufall: Gültige ZG-Funktion angeben')
                return				
        		
        try:						
            if len(args) == 1:
                aa = args[0]
                if isinstance(aa, list):
                    if einfacheinfach(aa):
                        aa = [[x, 1] for x in aa]		
                        aa = dict(aa)							
                    if all([isinstance(x, list)	and len(x)==2 for x in aa]):
                        aa = [tuple(x) for x in aa]					
                    try:
                        if einfach(aa):					
                            aa = dict(aa)	
                    except ValueError:
                        print('zufall: Liste überprüfen')					
                        return		
                if not isinstance(aa, (list, dict, tuple, Tuple)):
                    raise ZufallError("eine Liste oder ein dictionary angeben")
                listen = [aa]
                if isinstance(aa, list):
                    fall = 'liste1'
                    if not einfach(aa):	
                        fall = 'voll'
                        liste = aa[:]						
                else:
                    fall = 'dict1'				
            elif len(args) == 2:
                a1, a2 = args
                fall = 'listen'				
                if not (isinstance(a1, (list, dict)) and isinstance(a2, (list, dict, int, Integer))):
                    raise ZufallError("zwei Listen/dict oder Liste/dict und Stufenanzahl angeben")
                if isinstance(a1, (list, dict)) and isinstance(a2, (list, dict)):				
                    listen = [a1, a2]
                else:
                    if a2 <= 0:
                        raise ZufallError("die Stufenanzahl muß > 0 sein")
                    listen = [a1 for i in range(a2)]
            else:
                listen = []
                fall = 'listen'				
                for a in args:
                    if not isinstance(a, (list, dict)):
                        raise ZufallError("nur Listen oder dict's angeben")
                    listen += [a]						                    					
        except ZufallError as e:
            print('zufall:', str(e))
            return	
			
        if fall == 'listen' and len(listen) == 1 or fall == 'voll':
            if not wiederh:
                print('zufall: die Angabe zur Wiederholung wird ignoriert')
                wiederh = True			
            if not anordn:
                print('zufall: die Angabe zur Anordnung wird ignoriert')
                anordn = True

        stufen = len(listen)	
        listen1 = []		
        for li in listen:
            if isinstance(li, dict):
                if not dict_kontrolle(li):
                    print('zufall: Eingabe-dict überprüfen')
                    return
                li = dict2list(li)
                li.sort(key=lambda x: str(x))					                				
                listen1 += [li]
            else:
                if einfacheinfach(li):
                    li = [[x, 1] for x in li]
                if not list_kontrolle(li) and fall != 'voll':
                    print('zufall: Eingabe-Liste überprüfen')
                    return
                if all([isinstance(x, (Symbol, str, int, Integer)) for x in li]):
                    li = [(x, 1) for x in li]
                li.sort(key=str)					
                listen1 += [li]								
        listen = listen1

        if fall != 'voll':
            if funktion:
                li = listen[0]		
                if isinstance(li, list):
                    li = dict(li)				
                nn = set([x for x in list(li.keys())])
                if len(nn) == 2 and funktion == anzahl_treffer and stufen > 1:
                    nnl = list(nn)				
                    treffer, niete = nnl
                    t = kwargs.get('treffer')	
                    if t:
                        if t not in nnl:
                            print('Gültges Treffer-Objekt angeben')
                            return
                        treffer = t
                        niete = nnl[1] if treffer == nnl[0] else nnl[0]						
                    if wiederh:   # Erzeugen BernoulliKette
                        vert = li
                        summe = vert[treffer] + vert[niete]
                        for k in vert:
                            vert[k] = Rational(vert[k], summe)					
                        p = vert[treffer]                        						
                        print('Erzeugung eines BernoulliKette-Objektes')
                        print('(Treffer=' + str(treffer) + ', Niete=' + str(niete) + ', AnzahlVersuche=' + 
						        str(stufen) + ', TrefferWahrscheinlichkeit=' + str(p) + ')')	
                        if kwargs.get('a') == False:						
                            print('\nDie Angabe zur Anordnung wird nicht beachtet')						
                        if not t:						
                            print('\nDas als Treffer benutzte Objekt kann durch die Zusatz-Angabe treffer=...')						
                            print('geändert werden (danach ist die Anweisung nochmals auszuführen)')
                        bk = importlib.import_module('zufall.lib.objekte.bernoulli_kette')
                        BernoulliKette = bk.BernoulliKette
						
                        return BernoulliKette(stufen, p, tn=[treffer, niete])	
						
                    else:   # Erzeugen HyperGeometrischeVerteilung
                        N = li[treffer] + li[niete]
                        M = li[treffer]
                        n = stufen						
                        print('Erzeugung eines HyperGeometrischeVerteilung-Objektes')
                        print('(Treffer=' + str(treffer) + ', GrößePopulation=' + str(N) + ', GrößeTrefferMenge=' + 
                              str(M) + ', AnzahlVersuche=' + str(n) + ')')	
                        if kwargs.get('a') == False:						
                            print('\nDie Angabe zur Anordnung wird nicht beachtet')						
                        if not t:						
                            print('\nDas als Treffer benutzte Objekt kann durch die Zusatz-Angabe treffer=...')						
                            print('geändert werden (danach ist die Anweisung nochmals auszuführen)')
                        hgv = importlib.import_module('zufall.lib.objekte.hyper_geometrische_verteilung')							
                        HyperGeometrischeVerteilung = hgv.HyperGeometrischeVerteilung							
						
                        return HyperGeometrischeVerteilung(N, M, n)					
								
                ze = ZufallsExperiment(*args, w=wiederh, a=anordn)
                om = ze.omega_(l=1)			
                ve = ze._vert
                if stufen == 1:
                   ve = dict([[Symbol(str(k)), ve[k]] for k in ve])				
                vert = dict()
                for el in om:
                    w = funktion(el)
                    try:                  
                        vert[w] += ve[kurz_form(el)]
                    except KeyError:
                        vert[w] = ve[kurz_form(el)]
                if kwargs.get('info') != False:						
                    print('Erzeugung eines ZufallsGroesse-Objektes')
                return ZufallsGroesse(vert, kontrolle=False)
			
            # Weiterbehandlung ZE ohne funktion		
            listen = [normierung(li) for li in listen]
            if len(listen) == 1:
                tupel_liste = listen
                vert = dict(listen[0])				
            else:	
                # Erzeugen der Gesamt-Tupelmenge 
                # Aufbau   [ ( (a=P), (b=P), (c=P) ), ..]  bei anordn = True
                #          [ (a,b,c,P), .. ]               bei anordn = False
			
                if wiederh and anordn:			
                    tupel_liste = list(product(*listen))
                    li = []
                    for el in tupel_liste:
                        ss = ''
                        ww = 1
                        for tt in el:
                            ss = ss + str(tt[0])
                            ww *= tt[1]
                        li += [[Symbol(ss), ww]]				
                    vert = dict(li)				
                elif wiederh and not anordn:
                    li = set([])
                    for l in listen:
                        nn = [x[0] for x in l]					
                        li = li.union(set(nn))
                    li = sorted(list(li),key=str)
                    tupel = kombinationen(li, stufen, True, False, l=1)	
                    tupel_liste = tupel
                    tupel = [tuple([str(x[i]) for i in range(len(x))]) for x in tupel]	
                    if fall == 'listen':					
                        ze = ZufallsExperiment(*args)
                    else:
                        ze = ZufallsExperiment(args[0], stufen)					
                    vv = ze._vert
                    tupel1 = ze.omega_(l=1)	
                    tupel1 = [tuple([str(x[i]) for i in range(len(x))]) for x in tupel1]					
                    vert = dict()
                    for x in tupel:
                        vert[kurz_form(x)] = 0
                        for y in tupel1:
                            if sorted(y) == sorted(x):
                                vert[kurz_form(x)] += vv[kurz_form(y)]
                elif not wiederh and anordn:
                    vert = args[0]	
                    if isinstance(vert, list) and isinstance(vert[0], (str, Symbol)):
                        vert = dict([[x, 1] for x in vert])
                    if stufen > Add(*[vert[k] for k in vert])	:
                        print('zufall: die Stufenzahl ist zu groß')
                        return						
                    vert = dict(listen[0])	
                    if isinstance(vert, list) and isinstance(vert[0], (str, Symbol)):
                        vert = dict([[x, 1] for x in vert])					
                    li = sorted(list(dict(listen[0])), key=str)
                    stufli = [[(k, vert[k]) for k in li]]
                    vert = args[0] 
                    if isinstance(vert, list) and isinstance(vert[0], (str, Symbol)):
                        vert = dict([[x, 1] for x in vert])
                    # sukzessiver Aufbau der Tupelliste					
                    for j in range(1, stufen):
                        tuli = []	
                        for elem in stufli[-1]:					                        
                            if j == 1:
                                pfad = [elem[0]]
                            else:								
                                pfad = [el[0] for el in elem]
                            di = dict()
                            for el in pfad:
                                if el in di:
                                    di[el] += 1
                                else:
                                    di[el] = 1
                            vv = dict()
                            for el in vert:
                                if not el in di:
                                    vv[el] = vert[el]
                                else:
                                    if vert[el] - di[el] > 0:
                                        vv[el] = vert[el] - di[el]
                            namen = sorted(list(vv.keys()), key=str)	
                            tt = Add(*[vv[k] for k in vv])							
                            for na in namen:
                                if j == 1:								
                                    elem1 = elem, (na, vv[na] / tt)							
                                else:								
                                    elem1 = *elem, (na, vv[na] / tt)							
                                tuli += [elem1]
                        stufli += [tuli]													
                    tupel_liste = stufli[-1]	
                    vert = dict()								
                    for elem in tupel_liste:
                        name, pw = [], 1				
                        for el in elem:
                            name += [el[0]]
                            pw *= el[1]
                        vert[kurz_form(name)] = pw							
					
                elif not wiederh and not anordn:	   
                    vert = args[0]
                    if isinstance(vert, list) and isinstance(vert[0], (str, Symbol)):
                        vert = dict([[x, 1] for x in vert])
                    if stufen > Add(*[vert[k] for k in vert])	:
                        print('zufall: die Stufenzahl ist zu groß')
                        return
                    if fall == 'listen':
                        ze = ZufallsExperiment(*args, w=False)
                    else:					
                        ze = ZufallsExperiment(args[0], args[1], w=False)
                    li = ze.omega_(l=1)
                    tupel = [sorted(x, key=str) for x in li]
                    tupel = [tuple([str(y) for y in x]) for x in tupel]
                    vv = ze._vert
                    tupel1 = []					
                    for x in tupel:
                        if not sorted(x) in tupel1:
                            tupel1 += [sorted(x)]
                    tupel_liste = tupel1       										
                    vert = dict()							
                    for x in tupel1:
                        vert[kurz_form(x)] = 0
                        for y in tupel:					
                            if sorted(y) == sorted(x):
                                vert[kurz_form(x)] += vv[kurz_form(y)]
        # vollständige Liste				
        else:
		
            def volliste2tupel( liste ):
                rliste = []
                if not any( [isinstance(x, list) for x in liste]):
                    rliste += [[x] for x in liste] 
                else:
                    for i in range(0, len(liste), 2):
                        li = volliste2tupel(liste[i+1])
                        for l in li: 
                            if isinstance(l, list):
                                rliste += [[liste[i], *l]]
                            else:
                                rliste += [[liste[i], l]]       
                return rliste 

            def name(zeile, stufe):
               if stufe == 0:
                   return str(liste[zeile][stufe][0])
               else:
                   na =''
                   for s in range(stufe):
                       na = na + str(liste[zeile][s][0])
                   return na
	
            liste = volliste2tupel(liste)
            stufen = len(liste[0])
            liste1 = copy.deepcopy(liste)

            # Stufe 0	
            s, erl = 0, set()		
            for zeile in range(len(liste1)):
                na = name(zeile, 0)
                if na not in erl:				
                    s += liste1[zeile][0][1]
                    erl |= {na}			
            for zeile in range(len(liste1)):			
                liste1[zeile][0] = liste1[zeile][0][0], \
				      nsimplify(liste1[zeile][0][1] / s, rational=True)

            for stufe in range(1, stufen):
                summen = []
                vgl = name(0, stufe)
                wechsel = [0]
    
                for zeile in range(len(liste)):
                    na = name(zeile, stufe)
                    if na == vgl:
                        continue
                    else:
                        wechsel += [zeile]
                        vgl = na
            
                wechsel += [len(liste)]
                von_bis = [(wechsel[i-1], wechsel[i]) for i in range(1, len(wechsel))]
                for w in von_bis:
                    sum, erl = 0, set()
                    for i in range(*w):
                        if not liste1[i][stufe][0] in erl:		
                            sum += liste1[i][stufe][1]
                            erl |= {liste1[i][stufe][0]}							
                    for i in range(*w):
                        summen += [nsimplify(sum, rational = True)]
               
                for zeile in range(len(liste1)):     
                   liste1[zeile][stufe] = liste1[zeile][stufe][0], \
				          liste1[zeile][stufe][1] / summen[zeile]
					
            tupel_liste = liste1
            vert = dict()
            for zeile in range(len(liste1)):			
                nn, pp = '', 1			
                for stufe in range(stufen):
                    nn += str(liste1[zeile][stufe][0])				
                    pp *= liste1[zeile][stufe][1]	
                vert[Symbol(nn)] = nsimplify(pp)
			 
        return ZufallsObjekt.__new__(cls, tupel_liste, vert, stufen, wiederh, anordn)

			
    def __str__(self):  
        txt1 = (', mit' if self.wiederh else ', ohne') + ' Wiederholung '
        txt2 = (', mit' if self.anordn else ', ohne') + ' Anordnung)'
        return "ZufallsExperiment"	+ "(Stufen=" + str(self.stufen) + txt1 + txt2
		
		
# Eigenschaften + Methoden
# ------------------------

    @property
    def wiederh(self):
        """Wiederholung von Elementen"""
        return self.args[3]		

    @property
    def anordn(self):
        """Beachten der Anordnung"""	
        return self.args[4]		
		
    @property
    def omega(self):
        """Ergebismenge"""	
        return set(list(self._vert.keys()))
    def omega_(self, **kwargs):		
        """Ergebismenge; zugehörige Methode"""	
        if kwargs.get('h'):
            print("\nZusatz")		
            print("l=ja - Listenausgabe")
            print("t=ja - Tabellenausgabe")
            print("g=ja - Größe der Ergebnismenge\n")
            return			
        if kwargs.get('l'):
            liste = []	
            om = self.args[0]
            if self.anordn:			
                if isinstance(om[0], list):
                    liste = [[el[0]]for el in om[0]]
                else:
                    liste = [[el[i][0] for i in range(len(om[0])) ] for el in om]	
            else:
                if self.stufen == 1:
                   liste = [[el[0]] for el in self.args[0][0]]
                else:				   
                    liste = [[el[i] for i in range(len(om[0])) ] for el in om]	                			
            return liste		
        elif kwargs.get('t'):
            om = sorted(list(self.omega), key=str)
            n = self.n_omega			
            for i in range((n // 10) + 1):
                ss = ''
                for j in range(min(n - i*10, 10)):		
                    ss += str(om[i*10 + j]) + ' \\quad '
                display(Math(ss))	
            return				
        elif kwargs.get('g'):
            return self.n_omega	
        return self.omega		
		
    Omega = omega_       
		
    @property
    def n_omega(self):
        """Größe der Ergebnismenge"""	
        return len(self.omega)
		
    nOmega = n_omega      
		
    @property
    def _vert(self):
        """Wahrscheinlichkeitsverteilung; intern"""	
        return self.args[1]
		
    @property				
    def vert(self):
        """Wahrscheinlichkeitsverteilung"""	
        return self._vert			
    def vert_(self, s=None, p=None, sp=None, **kwargs):		
        """Wahrscheinlichkeitsverteilung; zugehörige Methode"""
        if kwargs.get('h'):
            print("\nZusatz")
            print("p=ja  - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben")
            print("d=n   - ebenso, dezimal mit n Kommastellen")
            print("s=ja  - Spaltenausgabe")
            print("sp=ja - ebenso, Prozentwerte")
            print("sd=n  - ebenso, dezimal mit n Kommastellen\n")
            return			
        di = self._vert
        di1 = dict()
        d = kwargs.get('d')			
        sd = kwargs.get('sd')			
        if p or d or sp or sd:
            if sd:
                d = sd
            if d and	not (isinstance(d, (int, Integer)) and (1 < d <= 12)):
                print("zufall: für d einen Wert aus [2, 12] angeben")
                return				
            for k in di.keys():
                if p or sp:
                    di1[k] = eval(format(float(100*di[k]), ".2f"))	
                elif d or sd:
                    di1[k] = eval(format(float(di[k]), ".%df" % d))
        if s or sp or sd:
            if sp or sd:
                di = di1			
            kk = list(di.keys()) 
            try:
                kk.sort()	
            except TypeError:
                pass			
            for k in kk:		
                display(Math(latex(k) + '\\quad ' + latex(di[k])))	
            print(' ')			
            return			
        elif d or p:
            return di1
        return di			
						
    Vert = vert_

    @property	
    def stufen(self):
        """Stufenanzahl des Experimentes"""
        return self.args[2]
				
    @property	
    def baum(self):
        """Baum-Diagramm"""
        return self.baum_(p=None, d=None)		
    def baum_(self, **kwargs):
        """Baum-Diagramm; zugehörige Methode"""
        if kwargs.get('h'):
            print("\np=ja - Wahrscheinlichkeiten werden als Prozentwerte ausgegeben")
            print("d=n  - Wahrscheinlichkeiten werden als Dezimalzahlen mit n Komma-")
            print("       stellen ausgegeben\n")
            return			
        getp = kwargs.get('p')
        getd = kwargs.get('d')
        if getd:
            if isinstance(getd, (int, Integer)):
                if not (1 < getd <= 12):
                    print("zufall: für d einen Wert aus [2, 12] angeben")
                    return					
        kt = _knoten_tabelle(self)
        tab = kt.tabelle
        kt.logisch_einordnen()
        kt.plot(self, getp, getd) 				
		
    Baum = baum_        
		
    @property	
    def versuch(self):
        """Versuch"""
        om = list(self.omega)
        ve = self._vert
        dive = dict([[i, ve[om[i]]] for i in range(len(om))])		
        xk = [float(x) for x in list(dive.keys())] 
        pk = [float(x) for x in list(dive.values())]
        X = rv_discrete(name='X', values=(xk, pk))		
        return om[int(X.rvs())]
		
    ausfall = versuch
    wurf = versuch
    ziehen = versuch
	
    def stich_probe(self, *args, **kwargs):
        """Stichprobe"""
        if kwargs.get('h'):
            print("\nStichprobe\n")		
            print("Aufruf   ze . stich_probe( m )\n")		                     
            print("              ze   Zufallexperiment")
            print("              m    Umfang (Anzahl Versuche)\n")
            print("Zusatz   l=ja   Ausgabe mit den Versuchsausgängen in Listenform\n")
            return 
        if len(args) != 1:
            print('zufall: ganze Zahl > 0 angeben')
            return
        m = sympify(args[0])
        if not isinstance(m, Integer) and m > 0:			
            print('zufall: ganze Zahl > 0 angeben')
            return
			
        ve = self._vert
        if not kwargs.get("l"):		
            om = list(self.omega)
            dive = dict([[i, ve[om[i]]] for i in range(len(om))])
        else:
            oml = self.omega_(l=True)
            dive = dict([[i, ve[kurz_form(oml[i])]] for i in range(len(oml))])
        xk = [float(x) for x in list(dive.keys())] 
        pk = [float(x) for x in list(dive.values())]
        X = rv_discrete(name='X', values=(xk, pk))		
        ll = X.rvs(size=m)
        if not kwargs.get("l"):		
            def f(x):
                if x - int(x) == 0.0:
                    return int(x)
                return x
            ll = [f(x) for x in ll]
            ll = [om[x] for x in ll]
        else:			
            ll = [oml[x] for x in ll]
        return ll

    stichProbe = stich_probe  
		
    def P(self, *args, **kwargs):
        """Wahrscheinlichkeit eines Ereignisses"""
		
        if kwargs.get('h'):
            print("\nWahrscheinlichkeit eines Ereignisses\n")
            print("Aufruf   ze . P( e /[, e1 ] )\n")		                     
            print("              ze     Zufallsexperiment")
            print("              e      Ereignis   Element | Liste|Tupel|Menge von Elemen-")
            print("                                ten der Ergebnismenge\n")
            print("Bei der Angabe von zwei Ereignissen wird die bedingte Wahrscheinlichkeit")
            print("P( e | e1 ) berechnet\n")			
            print("Zusatz   p=ja   Darstellung als Prozentwert")			
            print("         d=n    Darstellung dezimal mit n Kommastellen\n")			
            print("Beispiele")
            print("ze = ZE( { a : 2, b : 5 }, 3 )")
            print("     mit ze.omega = {aaa, aab, aba, abb, baa, bab, bba, bbb}")
            print("ze.P( { 'aba', 'baa', 'bbb' } ) = ze.P( [ 'aba', 'baa', 'bbb' ] ) ")
            print("   = ze.P( ( 'aba', 'baa', 'bbb' ) )")
            print("ze.P( 'aaa' ) = ze.P( { 'aaa' } ) ")
            print("oder aaa = Symbol('aaa');  ze.P( aaa ) = ze.P( 'aaa' )\n")
            return			
			
        om = list(self.omega)
        ve = self._vert
        if len(args) not in (1, 2):
            print('zufall: ein oder zwei Ereignisse angeben')  
            return			
        eig = args[0]
        if not iterable(eig):
            eig = [eig]	   
        pp = 0
        for i, e in enumerate(eig):
            if isinstance(e, str):
                e = Symbol(e)
                eig[i] = e
            if e not in om:
                print('zufall: Elemente der Ergebnismenge angeben (eventuell als Zeichenketten)')
                return
            pp += ve[e]				

        if len(args) == 2:			
            eig1 = args[1]
            if not iterable(eig1):
                eig1 = [eig1]	   
            pp1 = self.P(eig1)
            if pp1 is None:
                return			
            eig, eig1 = set(eig), set(eig1)
            eig2 = eig.intersection(eig1)	
            pp2 = self.P(eig2)
            if pp2 is None:
                return			
            if pp1 == 0:
                print('zufall: Division durch 0 ist nicht erlaubt')
                return				
            pp = nsimplify(pp2 / pp1, rational=True)			
		
        if kwargs.get('p'):
            return eval(format(float(100*pp), ".2f"))			
        d = kwargs.get('d')
        if d:
            if isinstance(d, (int, Integer)):
                if 0 < d <= 12:
                    return eval(format(float(pp), ".%df" % d))			
        return pp	

		
    def relh2p(self, *args, **kwargs):
        """Stabilisierung der relativen Häufigkeiten"""
		
        if kwargs.get('h'):
            print("\nStabilisierung der relativen Häufigkeiten\n")
            print("Aufruf   ze . relh2p( e, m )\n")		                     
            print("              ze     Zufallsexperiment")
            print("              e      Ereignis   Element | Liste|Tupel|Menge von Elementen")
            print("                                der Ergebnismenge")
            print("              m      Anzahl Versuche\n")
            print("Zusatz   d=ja   Rückgabe einer DatenReihe mit den Versuchsausgängen")
            print("                1-Ereignis ist eingetreten / 0-Ereignis ist nicht")
            print("                eingetreten\n") 
            print("relh2p = 'rel'ative 'H'äufigkeit 'to' 'P' (Wahrscheinlichkeit)\n")
            return	
			
        om = self.omega
        if len(args) != 2:
            print('zufall: zwei Argumente angeben')
            return
        eig, m = args
        if not iterable(eig):
            eig = [eig]	   
        for i, e in enumerate(eig):
            if isinstance(e, str):
                e = Symbol(e)
                eig[i] = e
            if e not in om:
                print('zufall: Elemente der Ergebnismenge angeben (eventuell als Zeichenketten)')
                return
        if not isinstance(m, (int, Integer)) and m > 0:
            print('zufall: für Anzahl Versuche ganze Zahl > 0 angeben')
            return
        p = float(self.P(e))
        X = rv_discrete(name='X', values=([1, 0], [p, 1-p]))		
        daten = X.rvs(size=m)
        print(' ')
        dm = lambda x: display(Math(x))				
        dm("\mathrm{Stabilisierung\;der\; relativen\; Häufigkeiten\; eines\; Ereignisses}")		
        dm("\mathrm{Es \;werden\; die\; relativen\; Häufigkeiten\; eines\; Ereignisses\; bei\; wach} \
            \mathrm{sender\; Ver-}")
        dm("\mathrm{suchsanzahl\; dargestellt}")
        dm("\mathrm{grüne\; Linie:\; theoretische\; Wahrscheinlichkeit\; des\; Ereignisses}")
        verlauf(daten, vergl=p, art='mittel', xlabel='Anzahl Versuche')
        if kwargs.get('d'):
            def f(x):
                if int(x) - x == 0.0:
                    return int(x)
                return x
            daten = [f(x) for x in daten]				
            print("Rückgabe DatenReihe\n")			
            return DatenReihe(daten)			
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        zufalls_experiment_hilfe(3)	
		
    h = hilfe					
		

		
# Benutzerhilfe für ZufallsExperiment
# -----------------------------------

def zufalls_experiment_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:
        print(""" \
		
ZufallsExperiment - Objekt

Kurzname     ZE
		
Synonyme     ZufallsVersuch ZV	
	
Erzeugung    ZE( liste /[, stufen ] )

                 stufen   Anzahl Stufen, ist > 1 bei mehrstufigem Ex-
                          periment
				 
   oder      ZE( liste1, liste2, ... )
   
                 bei mehrstufigem Experiment je Sufe eine Liste, diese 
                 können unterschiedlich sein
				 
   oder      ZE( v_liste )
   
                 vollständige Liste bei einem mehrstufigen ZE
				 
                 liste    liste_1 | liste_2 | dictionary
                 v_liste  liste_1 | [ (obj1, zahl1), v_liste1, (obj2, zahl2), 
                                     v_liste2, ...] 
                          (vollständige Liste)
                 liste_1  [ (obj1, zahl1), (obj2, zahl2), ...]  oder
                          [ [obj1, zahl1], [obj2, zahl2], ...] 				 
                          (obj-zahl-Paare als Tupel oder Liste)
                 liste_2  [ obj1, obj2, ...]  
                          (äquivalent zu [ (obj1, 1), (obj2, 1), ...] )
                 dict	  { obj1:zahl1, obj2:zahl2, ...}  (dictionary)
                 obj      Bezeichner | ganze Zahl >= 0
				 
Zusatz   a=nein  keine Beachtung der Anordnung/Reihenfolge; Standard=ja
         w=nein  keine Wiederholung von Elementen; Standard=ja
         f=funktions_name   Name einer ZG-Funktion (Element der Ergebnis-
                                                    menge -> Zahl)
		 
Wird eine Liste mit nur zwei unterschiedlichen Objekten angegeben, wird
bei Verwendung der Funktion anzahl_treffer
 
   bei Wiederholung von Elementen ein BernoulliKette-Objekt\n
   bei Nicht-Wiederholung von Elementen ein HyperGeometrischeVerteilung-
       Objekt\n
erzeugt\n
Bezeichner, die länger als ein Zeichen sind, müssen als Zeichenkette ein-
gegeben oder vordeklariert werden, etwa  Raucher = Symbol('Raucher')
		
Zuweisung     ze = ZE(...)   (ze - freier Bezeichner)

Beispiele
		
   Einfache Liste\n	
      ZE([a, b, c])   ist äquivalent zu  ZE([[a,1], [b,1], [c,1]]) 
                      bzw. ZE({a:1, b:1, c:1})
	  
      ZE( [ ('Männer', 15), ('Frauen', 25) ] )
	  
   4-stufiges Zufallsexperiment ohne Beachtung der Anordnung
   
      ZE( { r:5, b:3, g:2 }, 4, a=nein)
	  
   Einfache Liste mit 2 Einträgen, Funktion ist anzahl_treffer, Stufen 
      = 100  ( Münzwurf )
   
      ZE([ W, Z ], 100, f=anzahl_treffer)
	  
   3 Stufen, unterschiedliche Wahrscheinlichkeiten je Stufe
   
      ZE( { h:4, s:3, k:2 }, { h:3, s:3, k:3 }, { h:3, s:4, k:2 } )
	  
   Vollständige Listen
   
     ZE( [ ('Männer', 780), [ ('Raucher', 35), ('NichtRaucher', 65) ], 
           ('Frauen', 856),  [ ('Raucher', 55), ('NichtRaucher', 45) ] ] )
		   
     ZE( [ ('M', 780), [ ('R', 35),  [ ('jung', 40), ('alt', 60) ],  
                       ('N', 65),  [ ('jung', 30), ('alt', 70) ] ], 
           ('F', 856), [ ('R', 55),  [ ('jung', 60), ('alt', 40) ], 
                       ('N', 45),  [ ('jung', 20), ('alt', 80) ] ] ] )		
	   """)		
        return        
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für ZufallsExperiment
 
ze.hilfe                Bezeichner der Eigenschaften und Methoden
ze.anordn               Beachtung der Anordnung/Reihenfolge
ze.ausfall              = ze.versuch
ze.baum                 Baumdiagramm
ze.baum_(...)        M  ebenso; zugehörige Methode
ze.n_omega              Größe der Ergebnismenge
ze.omega                Ergebnismenge
ze.omega_(...)       M  ebenso; zugehörige Methode
ze.P(...)            M  Wahrscheinlichkeit eines Ereignisses
ze.relh2p(...)       M  Stabilisierung der relativen Häufigkeiten
ze.stich_probe(...)  M  Stichprobe
ze.stufen               Stufenanzahl des Experimentes
ze.versuch              Versuch
ze.vert                 Wahrscheinlichkeitsverteilung
ze.vert_(...)        M  ebenso; zugehörige Methode
ze.wiederh              Wiederholung von Elementen
ze.wurf                 = ze.versuch
ze.ziehen               = ze.versuch

Synonyme Bezeichner

hilfe        h
baum_        Baum
n_omega      nOmega
omega_       Omega
stich_probe  stichProbe
vert_        Vert
	   """)		
        return
	
	
ZE = ZufallsExperiment
ZufallsVersuch = ZufallsExperiment
ZV = ZufallsExperiment
		
		
		
# Hilfsklasse für Baumknoten		
# --------------------------
#
class _knoten(ZufallsObjekt):                                      

    def __init__(cls, pos=None,          # (Zeilen-, Spaltennummer) in der Grundtabelle
                     name=None,          # Name des Knotens
                     vorgaenger=None,    # siehe pos
                     wert=None,          # Wert für die Kante vom Vorgänger
                     is_visible=None):   # Sichtbarkeit
        cls.pos = pos					 
        cls.name = name 
        cls.vorgaenger = vorgaenger
        cls.wert = wert  
        cls.is_visible = None		
        cls.x = None    # phys. Koordinate
        cls.y = None    # ebenso
        cls.length = None   # pys. Laenge zwischen linkem und rechtem Mittelpunkt
		

# Hilfsklasse für Knotentabelle		
# -----------------------------	
class _knoten_tabelle(ZufallsObjekt):                                      

    def __new__(cls, ze, **kwargs):   # ze - ZufallsExperiment
        if ze.anordn:	
            if ze.stufen == 1:
                tupel = []
                for el in sorted(list(ze.omega), key=str):
                    tupel += [tuple( [('.', None), (el, ze._vert[el])])]
            else:		
                liste = ze.args[0]	
                tupel = []
                for el in liste:				
                    tupel += [tuple( [('.', None), *[el[i] for i in range(ze.stufen)]] )]
        elif not ze.anordn:
            if ze.stufen == 1:
                tupel = []				
                for el in ze.args[0][0]:				
                    tupel  += [('.', el[0], el[1])]                				
            else:				
                tupel = []		
                for el in ze.args[0]:				
                    tupel += [tuple( ['.', *[el[i] for i in range(ze.stufen)]] )]
						
        cls.zeilen = ze.n_omega
        cls.spalten = ze.stufen + 1	
        kt = dict()
        for i in range(cls.zeilen):		
            for j in range(cls.spalten):
                isvis = False			
                if j == cls.spalten - 1:
                    isvis = True	
                if ze.anordn:						
                    kt[i, j] = _knoten( pos=(i, j), 
                                      name=tupel[i][j][0], 
                                      vorgaenger=None,	
                                      wert=tupel[i][j][1],
                                      is_visible=isvis)
                elif not ze.anordn:						
                    kt[i, j] = _knoten( pos=(i, j), 
                                      name=tupel[i][j], 
                                      vorgaenger=None,	
                                      is_visible=isvis)
								  
        return ZufallsObjekt.__new__(cls, kt)
			
    # die Tabelle selbst			
    @property
    def tabelle(self):
        return self.args[0]	

    # Sichtbarkeit der Knoten, Bestimmung der Vorgänger		
    def logisch_einordnen(self):	
        tab = self.tabelle	
        n, m = self.zeilen, self.spalten
        
        def spalte(j):
            index = range(n)     
            # Ermitteln der Bereiche mit gleichem Namen			
            wechsel = []
            for l in range(len(index) - 1):
                n1, n2 = '', ''
                for m in range(j):				
                    n1 += str(tab[index[l], m].name)
                    n2 += str(tab[index[l+1], m].name)
                if n1 != n2:				
                    wechsel += [index[l]]    
            wechsel = [-1] + wechsel + [n-1]	
            bereiche = [ [wechsel[i]+1, wechsel[i+1]] for i in range(len(wechsel)-1) ]	
            # Einstellen der Vorgänger			
            for b in bereiche:
                pos = b[0] + (b[1] - b[0]) // 2 
                if (b[1]-b[0]) % 2 != 0:
                    pos += 1							
                for k in range(b[0], b[1]+1):
                    tab[k, j].vorgaenger = (pos, j-1)
                tab[pos, j-1].is_visible = True         					
            return 
			
        for j in (range(1, m)):
            spalte(j)						
			
        # Behandlung von Spalte 0 
        pos = 0 + (n-1 -0) // 2
        if (n-1 - 0) % 2 != 0:
            pos += 1
        for i in range(n):
           if tab[i, 1]:		
               tab[i, 1].vorgaenger = (pos, 0)
			   
    # Plotten des Diagramms		
    def plot(self, ze, getp, getd):
        # node.breite = 0.15*len(node.name) + 2*r
        tab = self.tabelle	
        n, m = self.zeilen, self.spalten

        if m > 8:	
            print('zufall: nicht implementiert (der Baum ist zu groß)')
            return
        if ze.anordn:			
            dx = 1.6
        else:
            dx = 1.3		
        dy = 0.55
		
        if m == 2:
            r = 0.3
            dx, dy = 1.4, 0.6
        else:			
            r = 0.35		
		
        def loes(xv, yv, xn, yn, sign): 
            m = (yn-yv)/(xn-xv)
            a = 1 + m**2
            if sign == '-':
                b, c = -2*(1+m**2)*xn, (1+m**2)*xn**2-r**2/4	
            else:
                b, c = -2*(1+m**2)*xv, (1+m**2)*xv**2-r**2/4		
            d = sqrt(b**2-4*a*c)
            x1, x2 = (-b+d)/(2*a), (-b-d)/(2*a)	
            if sign == '+':
                return max(x1, x2)
            return min(x1, x2)

        def ger(xv, yv, xn, yn, par): 
            p, q = np.array([xv, yv]), np.array([xn, yn])  
            pp = p + par*(q - p) 
            return pp[0], pp[1]     		
			
        def width(s):
            if len(str(s)) == 1:
                return 0			
            return 0.12*len(str(s))		
		
        breite = 0		
        for j in range(m):
            breite += max([width(tab[i, j].name)+2*r for i in range(n)]) + dx			
						
        widthes = [0.12]
        for j in range(1, m):
            widthes += [ max([width(tab[i, j].name) for i in range(n)]) ]			
        xpos = [0]   # linke Mittelpunkte der Knoten	
        for j in range(1, m):		
            xpos += [xpos[j-1] + dx + widthes[j-1]]

        if ze.anordn:			
            p_werte = []
            for i in range(n):	
                wert = tab[i, m-1].wert	
                vor = i, m-1		
                for j in reversed(range(m-2)):
                    vor = tab[vor].vorgaenger
                    wert *= tab[vor].wert
                p_werte += [wert]
		
        for i in range(n):
            for j in range(m):
                tab[i, j].x = xpos[j]			
                tab[i, j].y = (n - i)*dy			
                tab[i, j].length = width(tab[i, j].name)	
                if j == m-1:
                    tab[i, j].is_visible = True				
		
        def plot_node(node):
            i, j = node.pos
            if not node.is_visible:
                return			
            x, y = node.x, node.y
            ll = node.length
            arc_left = patches.Arc((x, y), r, r, theta1=90.0, 
                                  theta2=270.0, facecolor=(0, 0, 0), alpha=0.5)
            arc_right = patches.Arc((x+ll, y), r, r, theta1=270.0, 
                                  theta2=90.0, facecolor=(0, 0, 0), alpha=0.5)
            plt.gca().add_patch(arc_left)
            plt.gca().add_patch(arc_right)
            if j != 0:
                ax.text(x+0.5*ll, y, '$'+str(node.name)+'$', fontsize=11, horizontalalignment='center',
                        verticalalignment='center')
            if ll:
                xx = x, x+ll
                y1 = y-r/2, y-r/2			
                y2 = y+r/2+0.01, y+r/2+0.01			
                plt.plot(xx, y1, color=(0, 0, 0), alpha=0.5)      
                plt.plot(xx, y2, color=(0, 0, 0), alpha=0.5)      
            if j == m-1:
                if ze.anordn:			
                    if getp:
                        pwert = eval(format(float(100*p_werte[i]), ".2f"))			
                    elif getd:
                        pwert = eval(format(float(p_werte[i]), ".%df" % getd))			
                    else:
                        if len(str(p_werte[i])) < 12:					
                            pwert = p_werte[i]
                        else:
                            pwert = eval(format(float(p_werte[i]), ".4f"))									
                    ax.text(x+widthes[m-1]+(0.8 if m==2 else 0.6)*dx, y, 'P(Pfad) = '+str(pwert), 
                        fontsize=8, horizontalalignment='center', verticalalignment='center',
                        fontname='Arial', alpha=0.8)               			
                elif not ze.anordn:			
                    pfad = str(tab[i, m-1].name)                    	
                    vor = i, m-1		
                    for j in reversed(range(m-2)):
                        vor = tab[vor].vorgaenger
                        pfad = str(tab[vor].name) + pfad
                    wert = ze._vert[Symbol(pfad)]	
                    if getp:
                        pwert = eval(format(float(100*wert), ".2f"))			
                    elif getd:
                        pwert = eval(format(float(wert), ".%df" % getd))			
                    else:
                        if len(str(wert)) < 12:					
                            pwert = wert
                        else:
                            pwert = eval(format(float(wert), ".4f"))															
                    ax.text(x+widthes[m-1]+(0.8 if m==2 else 0.5)*dx, y, ' \
                            P = '+str(pwert), fontsize=8, horizontalalignment='center', \
							verticalalignment='center', fontname='Arial')               			
            if node.vorgaenger:			
                k, l = node.vorgaenger
                vorg = tab[k, l]				
                if k == 0:					
                    xn, xv = node.x, vorg.x					
                    yn, yv = node.y, vorg.y					
                else:
                    xn, xv = node.x, vorg.x + vorg.length 
                    yn, yv = node.y, vorg.y
                xx1 = loes(xv, yv, xn, yn, '-')
                xx2 = loes(xv, yv, xn, yn, '+') 
                yy1 = (yn-yv)/(xn-xv)*(xx1-xv) + yv				
                yy2 = (yn-yv)/(xn-xv)*(xx2-xv) + yv													
                x11, y11 = ger(xx1, yy1, xx2, yy2, 0)
                x12, y12 = ger(xx1, yy1, xx2, yy2, 0.35)
                x21, y21 = ger(xx1, yy1, xx2, yy2, 0.65)
                x22, y22 = ger(xx1, yy1, xx2, yy2, 1.0)
                if ze.anordn:				
                    xxx1 = x11, x12				
                    yyy1 = y11, y12
                    xxx2 = x21, x22				
                    yyy2 = y21, y22
                    plt.plot(xxx1, yyy1, color=(0, 0, 0), linewidth=0.5, alpha=0.5)  
                    plt.plot(xxx2, yyy2, color=(0, 0, 0), linewidth=0.5, alpha=0.5)  
                    hx, hy = 0.5*(xn+xv), 0.5*(yn+yv)	
                    if getp:
                        wert = eval(format(float(100*node.wert), ".2f"))			
                    elif getd:
                        wert = eval(format(float(node.wert), ".%df" % getd))			
                    else:
                        if len(str(node.wert)) < 12:					
                            wert = node.wert
                        else:							
                            wert = eval(format(float(node.wert), ".4f"))									
                    ax.text(hx, hy, str(wert), fontsize=8, horizontalalignment='center',
                            verticalalignment='center', fontname='Arial', alpha=0.8)	
                elif not ze.anordn:				
                    xxx = x11, x22				
                    yyy = y11, y22
                    plt.plot(xxx, yyy, color=(0, 0, 0), linewidth=0.5, alpha=0.5)  
					
        plt.close('all')					
        fig = plt.figure(figsize=(breite, (n+1)*dy))
        ax = fig.add_subplot(111, aspect='equal')

        plt.xlim(-2*r,  breite)
        plt.ylim(0.3, (n+1)*dy-0.3)
        ax.axis('off')
        for j in reversed(range(m)):
            for i in range(n):
                plot_node(tab[i, j])
			
        plt.show()


	
# Kurzform für Tupel
# ------------------
def kurz_form(tupel):
    s = ''
    for el in tupel:
       if isinstance(el, (tuple, list)):	
           s += str(el[0])
       else:
           s += str(el)   
    return	Symbol(s)	
		