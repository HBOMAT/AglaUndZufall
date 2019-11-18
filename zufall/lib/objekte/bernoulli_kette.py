#!/usr/bin/python
# -*- coding: utf-8 -*-



#                                      
#  BernoulliKette - Klasse  von zufall           
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

from inspect import isfunction

from sympy.core.numbers import Integer   
from sympy.core.symbol import Symbol
from sympy import sympify, nsimplify
from sympy.core.compatibility import iterable

from zufall.lib.funktionen.funktionen import is_zahl
from zufall.lib.objekte.zufalls_experiment import ZufallsExperiment, kurz_form 
from zufall.lib.objekte.ausnahmen import ZufallError
import zufall	
	
bv = importlib.import_module('zufall.lib.objekte.binomial_verteilung')
BinomialVerteilung = bv.BinomialVerteilung
zg = importlib.import_module('zufall.lib.objekte.zufalls_groesse')
ZufallsGroesse = zg.ZufallsGroesse

	
	
	

# BernoulliKette - Klasse  
# -----------------------
#

class BernoulliKette(BinomialVerteilung):                                      
    """
	
BernoulliKette

**Kurzname** **BK**
	
**Erzeugung** 
	
   BK( *n*, *p* )

**Parameter**

   *n* : Anzahl Versuche
   
   *p* : TrefferWahrscheinlichkeit
							 
**Zusatz**
   `ze=ja` - Erzeugung eines ZufallsExperiment-Objektes
   
   `a=ja` - Beachtung der Anordnung der Ergebnisse (nur bei `ze=ja` 
   wirksam) 
			
   `f=funktion` - Erzeugung eines ZufallsGröße-Objektes anhand der
   angegebenen ZG-Funktion ``funktion``
					  
   `tn = [treffer, niete]` - Namen für Treffer/Niete, Standard=[1, 0];
   Bezeichner, die länger als ein Zeichen sind, müssen als  
   Zeichenkette eingegeben oder vordeklariert werden, etwa 
   ``Wappen = Symbol('Wappen')``
				  	  
    """
			    
    def __new__(cls, *args, **kwargs):  
					
        if kwargs.get("h") in (1, 2, 3):                         
            bernoulli_kette_hilfe(kwargs["h"])		
            return	
											
        try:						
            if len(args) != 2:
                raise ZufallError("zwei Argumente angeben")
            n, p = args
            n, p = sympify(n), sympify(p)
            if not (is_zahl(n) and is_zahl(p)):
                raise ZufallError("die Parameter müssen Zahlen sein")
            if not isinstance(n, (int, Integer)) or n <= 0:
                raise ZufallError("die Anzahl Versuche muß eine ganze positive Zahl sein")
            if not (0 <= p <= 1):
                raise ZufallError("die Trefferwahrscheinlichkeit muß aus [0,1] sein")
            p = nsimplify(p, rational=True)
			
            treffer, niete = 1, 0			
            if kwargs.get('tn'):
                tn = kwargs.get('tn')
                if not iterable(tn):				
                    raise ZufallError("für tn Liste oder Tupel angeben")
                if not iterable(tn) and len(tn) == 2:				
                    raise ZufallError("für tn Liste oder Tupel der Länge 2 angeben")
                treffer, niete = tn
                if not (isinstance(treffer, Symbol) and isinstance(niete, Symbol)):	
                    if isinstance(treffer, str) and isinstance(niete, str):
                        treffer, niete = Symbol(treffer), Symbol(niete)
                    else:						
                        raise ZufallError("für treffer und niete Namen angeben")
			
        except ZufallError as e:
            print('zufall:', str(e))
            return
			
        anordn = True
        if kwargs.get('a') == False:
            anordn = False
			
        if kwargs.get('ze'):
            cls._typ = 'ze'
            liste = { treffer:p, niete:1-p }
            if kwargs.get('info') != False:						
                print('Erzeugung eines BernoulliKette-ZufallsExperiment-Objektes')
            return ZufallsExperiment(liste, n, a=anordn)

        elif kwargs.get('f'):
            cls._typ = 'zg'
            funktion = kwargs.get('f')   
            if isinstance(funktion, str):	
                funktion = eval(funktion)
            if not isfunction(funktion):
                print('zufall: Gültige ZG-Funktion	 angeben')
                return				
            ze = ZufallsExperiment({treffer:p, niete:1-p}, n, w=True, a=anordn)
            om = ze.omega_(l=1)			
            ve = ze._vert				
            vert = dict()
            for el in om:
                w = funktion(el)
                try:                  
                    vert[w] += ve[kurz_form(el)]
                except KeyError:
                    vert[w] = ve[kurz_form(el)]
            print('Erzeugung eines ZufallsGröße-Objektes auf Basis der ZG-Funktion')
            return ZufallsGroesse(vert, kontrolle=False)
			
        cls._typ = 'bk'			
        bv = BinomialVerteilung(n, p)
        if kwargs.get('info') != False:						
            print('Erzeugung eines BernoulliKette-BinomialVerteilung-Objektes')
        return ZufallsGroesse.__new__(cls, bv._vert, parameter=(n, p, treffer, niete), 
                                 kontrolle=False)		
		

    def __str__(self):
        n, p = self.args[1][:2]
        treffer = ',\;Treffer=' + str(self.treffer)
        niete = ', \;Niete=' + str(self.niete)
        return "BernoulliKette(" + str(n) + ",\;" + str(p) + treffer + niete + ")"
								
	
	
# Eigenschaften
# -------------

    @property
    def n(self):
        """Länge (Anzahl Versuche)"""	
        n, p = self.args[1][:2]	
        return n
		
    anzahl = n		

    @property
    def p(self):
        """Trefferwahrscheinlichkeit"""	
        n, p = self.args[1][:2]	
        return p

    @property
    def treffer(self):
        """Treffer"""	
        return self.args[1][2]
		
    @property
    def niete(self):
        """Niete"""	
        return self.args[1][3]
		
    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        bernoulli_kette_hilfe(3)	
		
    h = hilfe					
		
		
	
				
# Benutzerhilfe für BernoulliKette
# --------------------------------

def bernoulli_kette_hilfe(h):
   
    if h == 1:
        print("h=2 - Erzeugung")
        print("h=3 - Eigenschaften und Methoden")
        return
		   
    if h == 2:		   
        print(""" \
		
BernoulliKette - Objekt
		 
Kurzname     BK	
		 
Erzeugung    	BK( n, p )		

                    n     Anzahl Versuche
                    p     TrefferWahrscheinlichkeit
							 
Zusatz   ze=ja   Erzeugung eines ZufallsExperiment-Objektes
         a=ja    Beachtung der Anordnung der Ergebnisse (nur bei ze=ja 
                 wirksam) 
         f=funktion   Erzeugung eines ZufallsGröße-Objektes anhand der
                      angegebenen ZG-Funktion funktion				
         tn = [treffer, niete]   Namen für Treffer/Niete, Standard=[1, 0]
         Bezeichner, die länger als ein Zeichen sind, müssen als Zeichen- 
         kette eingegeben oder vordeklariert werden, etwa 
         Wappen = Symbol('Wappen')
				  
Zuweisung     bk = BK(...)   (bk - freier Bezeichner)
		 
Beispiele
BK( 12, 0.2 )            
BK( 50, 1/2, tn=['W', 'Z'] )		 
	   """)				 
        return    
		
    if h == 3:   
        print(""" \
		
Eigenschaften und Methoden (M) für BernoulliKette
 
bk.hilfe               Bezeichner der Eigenschaften und Methoden
bk.anzahl              = bk.n  (Anzahl/Länge/Stufen)
bk.erw                 Erwartungswert	
bk.erw_(...)           ebenso, zugehörige Methode	
bk.e_sigma_umg         Sigma-Umgebungen des Erwartungswertes		
bk.F(...)           M  Verteilungsfunktion
bk.faust_regel         Faustregeln
bk.formeln             Formeln
bk.graf_F              Graf der Verteilungsfunktion
bk.hist                Histogramm
bk.hist_(...)       M  ebenso, zugehörige Methode
bk.hist_kum            ebenso, kumulierte Wahrscheinlichkeiten
bk.n                   Länge der Kette
bk.niete               Niete
bk.n_omega             Größe der Ergebnismenge 
bk.nv_approx           Approximation durch Normalverteilung 
bk.omega               Ergebnismenge
bk.p                   Trefferwahrscheinlichkeit 
bk.P(...)           M  Wahrscheinlichkeit eines Ereignisses
bk.poly_zug            Polygonzug-Diagramm der Wahrscheinlichkeiten
bk.poly_zug_(...)   M  ebenso, zugehörige Methode
bk.p_sigma_umg         Sigma-Umgebungen der Wahrscheinlichkeit
bk.quantil(...)     M  Quantile
bk.relh2p           M  Stabilisierung der relativen Häufigkeiten        
bk.sigma               Standardabweichung
bk.sigma_(...)      M  ebenso, zugehörige Methode	
bk.stich_probe(...) M  Stichprobe		
bk.treffer             Treffer
bk.var                 Varianz		
bk.var_(...)        M  ebenso, zugehörige Methode		
bk.versuch             Versuch		
bk.vert                Wahrscheinlichkeitsverteilung		
bk.vert_(...)       M  ebenso, zugehörige Methode		
bk.vert_kum            kumulierte Wahrscheinlichkeitsverteilung
bk.vert_kum_(...)   M  ebenso, zugehörige Methode	

Synonyme Bezeichner

hilfe         h
erw_          Erw
e_sigma_umg   eSigmaUmg
faust_regel   faustRegel
graf_F        grafF
hist_         Hist
hist_kum      histKum
n_omega       nOmega
poly_zug      polyZug
poly_zug_     PolyZug
p_sigma_umg   pSigmaUmg
sigma_        Sigma
stich_probe   stichProbe
var_          Var
vert_         Vert
vert_kum      vertKum
vert_kum_     VertKum

Bei der Erzeugung eines ZufallsExperiment- oder ZufallsGröße-Objektes  
siehe entsprechende Hilfeseiten		
	   """)		
        return
		
		
BK = BernoulliKette
		


	


