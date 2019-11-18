#!/usr/bin/python
# -*- coding utf-8 -*-



#                                                 
#  Vektor - Klasse  von zufall           
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

import numpy as np

import matplotlib.pyplot as plt

from IPython.display import display, Math

from sympy.core.sympify import sympify
from sympy import expand, N
from sympy.core.containers import Tuple
from sympy.matrices import Matrix as SympyMatrix
from sympy.core.compatibility import iterable
from sympy.simplify import simplify, nsimplify
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.numbers import Integer
from sympy.core.symbol import symbols, Symbol
from sympy.printing.latex import latex
            
from zufall.lib.objekte.basis import ZufallsObjekt
from zufall.lib.objekte.ausnahmen import ZufallError
from zufall.lib.objekte.umgebung import UMG
from zufall.lib.funktionen.funktionen import (is_zahl, wert_ausgabe, mit_param, 
    einfach)								
import zufall


	
# Vektor - Klasse	
# ---------------
	       
class Vektor(ZufallsObjekt):             
    """Vektor-Klasse von zufall"""
	
    printmethod = '_latex'
    
    def __new__(cls, *args, **kwargs):        
		
        h = kwargs.get('h')
        if h in (1, 2, 3, 4):   
            vektor_hilfe(h)		
            return	
        if kwargs.get('simpl') == False:
            simpl = False
        else:	
            simpl = UMG.SIMPL
			
        try:
            if not args:
                raise ZufallError('mindestens 2 Komponenten angeben')                
            if iterable(args[0]):
                komp = Tuple(*args[0])
            elif isinstance(args[0], Vektor):
                if len(args) == 1:
                    return args[0]
                else:
                    raise ZufallError('hier ist nur ein Vektor möglich')                			
            else:
                komp = Tuple(*args)
            if len(komp) < 2:
                txt = "ein Vektor muss mindestens zwei Komponenten haben"
                raise ZufallError(txt)                			
            komp1 = []			
            for c in komp:
                if not is_zahl(c):
                    raise ZufallError('die Komponenten müssen Zahlen sein')
                if simpl:
                    try:
                        cc = nsimplify(simplify(c))
                        if abs(N(c) - N(cc)) > 1e-8:    # wegen Unsicherheit
                            raise RecursionError       # von nsimplify 						
                        komp1 += [cc]
                    except (RecursionError, TypeError):
                        komp1 += [simplify(c)] 					
                else:					
                    komp1 += [c]
		
            return ZufallsObjekt.__new__(cls, *komp1)
		
        except ZufallError as e:
            print('zufall:', str(e))
            return			
					
		
    def __str__(self):  
        par = self.sch_par
        if len(par) > 0:
            return "Vektorschar(" + str([el for el in par]) + ")"
        return "Vektor"			
		
    def _latex(self, printer):	
        lat = latex(self.vektor2sympy)
        lat = lat.replace('[', '(').replace(']', ')')		
        return lat

    def __hash__(self):
        return super(Vektor, self).__hash__()	

		
		
# Eigenschaften
# ------------

    @property                      
    def vektor2sympy(self):                          
        """Konvertierung in eine SympyMatrix"""
        spalte = [ [k] for k in self.komp ] 
        return SympyMatrix(spalte)

    @property                      
    def dim(self):
        """Anzahl der Komponenten (Dimension) des Vektors"""
        return len(self.args)	

    @property
    def komp(self):
        """Komponenten des Vektors"""
        return self.args

    @property
    def koord(self):
        """Koordinaten des Punktes, der dem Vektor entspricht"""
        return self.komp

    @property
    def O(self): 
        """Nullvektor in der Dimension des Vektors"""		 
        return Vektor([0] * self.dim)

    @property
    def betrag(self):
        """Betrag des Vektors"""
        return sqrt(self * self)	
    def betrag_(self, **kwargs):
        """Betrag des Vektors; Dezimaldarstellung"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Nachkomma-/Stellen\n')
            return
        b = self.betrag
        d = kwargs.get('d')
        return wert_ausgabe(b, d)
		
    Betrag = betrag_		
    laenge = betrag		
    laenge_ = betrag_		
    Laenge = betrag_		
			
    @property
    def dez(self):                                    
        """Dezimaldarstellung"""
        li = [N(k) for k in self.komp]
        return Vektor(*li, simpl=False)
    def dez_(self, *n, **kwargs):                                
        """Dezimaldarstellung"""
        if kwargs.get('h'):
            print('\nkein Agument oder d=n - Dezimaldarstellung')
            print('n - Anzahl der Stellen\n')
            return 		
        d = kwargs.get('d')
        li = []
        for k in self.komp:
            if d:
                li.append(N(k, d))
            else:
                li.append(N(k))
        return Vektor(*li, simpl=False)
		
    Dez = dez_		
		
    @property
    def zeil(self):                           
        """Zeilenvektor """
        komp = []
        for i in range(self.dim):
            komp += [self.komp[i]]        
        return _ZeilenVektor(*komp)
		
    T = zeil		
	 
    @property						
    def einfach(self):
        """Vereinfachung des Vektors"""
        li = [einfach(k) for k in self.komp]
        return Vektor(li)

    @property
    def is_schar(self):                                       
        """Test auf eine Schar von Vektoren mit einem Parameter"""	      
        return len(self.sch_par) == 1  

    isSchar = is_schar		
				
    @property
    def sch_par(self):
        """Parameter einer Schar"""
        return self.free_symbols

    schPar = sch_par		
		
		
# Methoden
# --------

    def abstand(self, *other, **kwargs):
        """Abstand des Punktes zu einem anderen Punkt"""
		
        if kwargs.get('h'):
            print("\nAbstand des Punktes zu einem anderen Punkt\n")		
            print("Aufruf   punkt . abstand( punkt1 )\n")		
            print("             punkt    Punkt\n")
            print("Rückgabe 0, wenn punkt1 mit punkt identisch ist\n")
            print("Zusatz       d=n   Dezimaldarstellung")
            print("                   n - Anzahl der Nachkomma-/Stellen\n")
            return 

        try:			
            if not other:
                raise ZufallError('Punkt angeben')
            if len(other) != 1:
                raise ZufallError('nur ein anderes Objekt angeben')
            other = other[0]  
            if not isinstance(other, Vektor):       
                raise ZufallError('Punkt angeben')
            if self.dim == other.dim:
                wert = sqrt(expand(sum([(x-y)**2 
				             for x, y in zip(self.komp, other.komp)]))) 
                d = kwargs.get('d')							 
                if not isinstance(d, (Integer, int)):
                    return wert
                if d <= 0:
                    return wert					
                if mit_param(wert):
                    if d:
                        return N(wert, d)
                    else:							
                        return wert
                if kwargs.get('d'):
                    wert = float(wert)
                    if d:
                        return eval(format(wert, ".%df" % d))
                    return eval(format(wert))
                return wert
            raise ZufallError('die Punkte haben unterschiedliche Dimension')
        except ZufallError as e:
            print('zufall:', str(e))
            return
		
						 
    def kette(self, *args, **kwargs):	                           
        """Verketten von Vektoren zu einer Matrix"""
			   
        if kwargs.get('h'):
            print("\nVerketten von Vektoren zu einer Matrix\n")		
            print("Aufruf   vektor . kette( vektor1, vektor2, ... )\n")
            print("oder     vektor | vektor1 | vektor2 ...\n")
            print("             vektor    Vektor\n")
            return 
		
        try:		
            if not args:
                raise ZufallError('mindestens ein Argument angeben')		
            if iterable(args[0]):
                vekt = Tuple(self, *args[0])
            else:
                vekt = Tuple(self, *args)
            if len(vekt) < 2:
                raise ZufallError('zwei oder mehr Vektoren angeben')			
            if not all(isinstance(v, Vektor) for v in vekt):
               raise ZufallError('nur Vektoren angeben')
            if not all(v.dim == self.dim for v in vekt):
                raise ZufallError('die Vektoren haben unterschiedliche Dimension')			
        except ZufallError as e:
            print('zufall:', str(e))	
            return			
			
        liste = [ [k for k in v.komp] for v in vekt ]
        m = SympyMatrix(liste)
        return m.T                                  
	
	
    def sp(self, *other, **kwargs):       
        """Skalarprodukt zweier Vektoren"""

        if kwargs.get('h'):
            print("\nSkalarprodukt des Vektors mit einem anderen Vektor\n")		
            print("Aufruf   vektor * vektor1     ( Operator * )\n")		            
            print("  oder   vektor ° vektor1     ( Operator ° )\n")		            
            print("  oder   vektor . sp( vektor1 )\n")
            print("             vektor    Vektor\n")
            return 
		
        try:		
            if len(other) != 1:		
                raise ZufallError('einen anderen Vektor angeben')
            other = other[0]		
            if isinstance(other, Vektor) and other.dim == self.dim:
                return sum([x*y for x, y in zip(self.komp, other.komp)])
            else: 
                if isinstance(other, Vektor):		
                    raise ZufallError('die Vektoren haben unterschiedliche' + \
                                   'Dimension')
                else:
                    txt = ("das Skalarprodukt für %s und %s ist nicht" + \
					           "definiert" % (self, other))			
                    raise ZufallError(txt)		
        except ZufallError as e:
            print('zufall:', str(e))            		
			
			
    def sch_el(self, *wert, **kwargs):
        """Element einer Schar mit einem Parameter"""
			
        if kwargs.get('h'):
            print("\nElement einer Schar von Vektoren\n")		
            print("Aufruf   vektor . sch_el( wert )\n")		                     
            print("             vektor    Vektor")
            print("             wert      Wert des Scharparameters\n")			
            print("Es ist nur ein Scharparameter zugelassen\n")    
            return 
        try:					
            if not self.is_schar or len(self.sch_par) > 1:
                raise ZufallError('keine Schar mit einem Parameter')					
            if not wert or len(wert) != 1:		
                raise ZufallError('einen Wert für den Scharparameter angeben')		
            if len(self.sch_par) != 1:
                raise ZufallError('keine Schar mit einem Parameter')
            p = self.sch_par.pop()
            wert = sympify(*wert)
            if not is_zahl(wert):
                raise ZufallError('für Scharparameter Zahl oder freien \
				                                      Parameter angeben')	
            return Vektor([k.subs(p, wert) for k in self.komp])
        except ZufallError as e:
            print('zufall:', str(e))		
	
    schEl = sch_el	

	
# Operationen
# -----------	
					
    def __add__(self, other):
        try:
            if isinstance(other, Vektor):		
                if other.dim == self.dim:
                    return Vektor(*[simplify(a + b) 
				             for a, b in zip(self.args, other.args)])
                else:
                    txt = "die Vektoren haben unterschiedliche Dimension"
                    raise ZufallError(txt)			
            else:
                raise ZufallError('Addition von %s und %s nicht möglich' 
			                      % (self, other))
        except ZufallError as e:
            print('zufall:', str(e))					
			
    def __mul__(self, other): 
        if isinstance(other, Vektor):	
            try:
                if other.dim == self.dim:	
                    return sum([x*y for x, y in zip(self.komp, other.komp)]) 
                txt = "die Vektoren haben unterschiedliche Dimension"				
                raise ZufallError(txt)
            except ZufallError as e:
                print('zufall:', str(e))
        else:
            factor = sympify(other)
            if is_zahl(factor):
                return Vektor([x*factor for x in self.args])	
            else:
                return NotImplemented                              
        		  
    def __rmul__(self, other):
        other = sympify(other)
        try:
            if is_zahl(other):
                return self * other	
            elif isinstance(other, _ZeilenVektor):      
                komp = []
                for i in range(len(other.args)):
                    komp += [other.args[i]]
                v1 = Vektor(*komp)
                return v1.sp(self)
            else:
                raise ZufallError('nicht implementiert', type(other))                                  	
        except ZufallError as e:
            print('zufall:', str(e))
				
    def __neg__(self):
        return Vektor([-x for x in self.args])

    def __sub__(self, other):
        return self + (-other)			

    def __div__(self, divisor):
        divisor = sympify(divisor)
        return Vektor([x/divisor for x in self.args])	

    def __or__(self, other):
        """Überladen des Operators '|' zur Verkettung von Vektoren/Matrizen"""         		
        try:
            if isinstance(other, (list, tuple, Tuple)):
                dim1 = other[0].dim
                t = [isinstance(o, Vektor) for o in other]
                if not all(t):
                    print('zufall: eine Liste mit Vektoren angeben')
                    return					
            elif isinstance(other, SympyMatrix):
                dim1 = other.dim[0]
            else:
                dim1 = other.dim		
        except AttributeError as e:
            print('zufall :  Vektor, Liste von Vektoren oder Matrix angeben')
            return			
        if self.dim != dim1:
            print('zufall: die Dimensionen sind unverträglich, ' + \
				                      'Verkettung ist nicht möglich')	
            return	
        if isinstance(other, (list, tuple, Tuple)):			
            return self.kette(*other)	
        elif isinstance(other, SympyMatrix):
            Matrix = importlib.import_module('zufall.lib.objekte.matrix').Matrix	
            vekt = [self] + other.vekt
            return Matrix(*vekt)			
        return self.kette(other)	

    def __and__(self, other):
        """Überladen des Operators '&' zur Berechnung des Vektorproduktes"""	
        try:
            if isinstance(other, Vektor):		
                if other.dim == self.dim:
                    return self.vp(other) 
                else:
                    txt = "die Vektoren haben unterschiedliche Dimension"
                    raise ZufallError(txt)			
            else:
                raise ZufallError('Vektor im Raum R^3 angeben')
        except ZufallError as e:
            print('zufall:', str(e))		
		
    __truediv__ = __div__

    @property		
    def hilfe(self):  
        """Bezeichner der Eigenschaften und Methoden"""
        vektor_hilfe(3)				
		
    h = hilfe					
		
			

# Benutzerhilfe für Vektor
# ------------------------

def vektor_hilfe(h):

    if h == 1:
        print("h=2 - Erzeugung, Operatoren")
        print("h=3 - Eigenschaften und Methoden")
        return		
		
    if h == 2:
        print("\nVektor - Objekt\n")
        print("Kurzname   v\n")		
        print("Repräsentation eines Vektors im n-dimensionalen Euklidischen ")
        print("Raum R^n (n>=2)\n")	
        print("Synonym       Punkt (Punkte werden mit ihren Ortsvektoren iden-")
        print("                     fiziert)\n")
        print("Erzeugung     Vektor( komp1, komp2, komp3, ... )\n")
        print("                 komp    Komponente\n")
        print("                 Wird mit einem Schlüsselwortparameter simpl=nein") 
        print("                 angegeben, erfolgt keine Umwandlung von float- ")
        print("                 Komponenten in rationale Zahlen")
        print("                 Das ist auch der Fall, wenn mit der Anweisung")
        print("                 UMG.SIMPL = nein die Umgebungsvariable UMG.SIMPL")
        print("                 global eingestellt wird\n")		
        print("Zuweisung  vek = v(...)   bzw.   vek = Vektor(...)")
        print("                 (v - reservierter, vek - freier Bezeichner)\n")
        print("Operatoren")
        print("  +  : Addition") 
        print("  -  : Negation/Subtraktion") 
        print("  *  : Multiplikation mit einem Skalar")                  
        print("  /  : Division durch einen Skalar")                        
        print("  *  : Skalarprodukt")                                  
        print("  °  : ebenso")                                  
        print("  |  : Verketten mit einem anderen Vektor\n")                   
        print("Beispiele")
        print("a = v(1, 2, 3, 4)  ist identisch mit  a = Vektor(1, 2, 3, 4)")
        print("b = v(4, -2, -5, 7)")
        print("a + b, a - b")
        print("v(1/2, 3/5, 1) ist identisch mit")
        print("               v(Rational(1, 2), Rational(3, 5), 1)")
        print("v(1.33, 4.6)   ist identisch mit v(133/100, 23/5)") 
        print("               (automatische Umwandlung von float-/Float-")
        print("               in Rational-Zahlen, falls nicht mit simpl")
        print("               bzw. UMG.SIMPL verhindert)")
        print("v(sqrt(3), 2*sqrt(5)+1, 1/2*sqrt(2))")
        print("2*a, sqrt(3)*b, 5*a-3*b")
        print("p8 = v(1, 2, 3, 4, 5, 6, 7, 8) - Vektor / Punkt im R^8")
        print("p8 * p8  - Skalarprodukt\n")
        return
		
    if h == 3:
        print("\nEigenschaften und Methoden (M) für Vektor\n")
        print("vek.hilfe             Bezeichner der Eigenschaften und Methoden")
        print("vek.abstand(...)   M  Abstand zu anderen Objekten")              
        print("vek.betrag            Betrag")
        print("vek.betrag_(...)   M  ebenso, zugehörige Methode")
        print("vek.dez               Dezimaldarstellung")
        print("vek.dez_(...)      M  ebenso, zugehörige Methode")
        print("vek.dim               Dimension (Anzahl Komponenten)")
        print("vek.einfach           Vereinfachung eines Vektors")    
        print("vek.is_schar          Test auf Schar")
        print("vek.kette(...)     M  Verketten zu einer Matrix")   
        print("vek.komp              Komponenten")
        print("vek.komp[i]           Zugriff auf i. Komponente (i>=0)")
        print("vek.koord             = vek.komp")
        print("vek.koord[i]          = vek.komp[i]")
        print("vek.länge             = vek.betrag (Länge)")
        print("vek.länge_(...)    M  ebenso, zugehörige Methode")
        print("vek.O                 Nullvektor (in der Dimension des Vektors)")
        print("vek.sch_el(...)    M  Element einer Schar")
        print("vek.sch_par           Parameter einer Schar") 
        print("vek.sp(...)        M  Skalarprodukt")        
        print("vek.T                 = vek.zeil")
        print("vek.vektor2sympy      Konvertierung in eine SympyMatrix")
        print("vek.zeil              Zeilenvektor\n")
        print("Synonyme Bezeichner\n")
        print("hilfe      :  h")
        print("betrag_    :  Betrag")
        print("dez_       :  Dez")
        print("is_schar   :  isSchar")
        print("länge_     :  Länge")
        print("sch_el     :  schEl")
        print("sch_par    :  schPar\n")
        return
		

# Hilfsklasse _ZeilenVektor
# ------------------------

# Zeilenvektor mit n Komponenten; nur zu Darstellungszwecken, 
# als Operation ist nur die Multiplikation mit Vektor/Matrix implementiert

class _ZeilenVektor(ZufallsObjekt):    

    printmethod = '_latex'

    def __new__(self, *args, **kwargs):        
		
        self.komp = args		
        li = []
        for i in range(len(self.komp)):
            li += [is_zahl(self.komp[i])]	
        try:				
            if not all(li):
                raise ZufallError('Zahlenwerte angeben')								        
            return ZufallsObjekt.__new__(self, *self.komp)
        except ZufallError as e:			
            print('zufall:', str(e))
		
    def __str__(self): 
        m = SympyMatrix([[k for k in self.komp]])	
        return str(m)
		
    def __repr__(self):                                
        m = SympyMatrix([[k for k in self.komp]])	
        return repr(m)

    def _latex(self, printer):	                          
        m = SympyMatrix([[k for k in self.komp]])	        
        return latex(m)
		
    def __mul__(self, other):
        if isinstance(other, (SympyMatrix, Vektor)):
            if isinstance(other, SympyMatrix) and len(self.args) != other.dim[0]:
                print('zufall: die Dimensionen sind unverträglich')
                return
            if isinstance(other, Vektor) and len(self.args) != other.dim:
                print('zufall: die Dimensionen sind unverträglich')
                return
            m = SympyMatrix([[k for k in self.komp]])
            if isinstance(other, Vektor):
                other = other.vektor2sympy	
                M = m * other
                return M[0, 0]
            M = m * other
            l = [M[0, i] for i in range(M.cols)]			
            return _ZeilenVektor(*l)		
		
    def __rmul__(self, other):
        args = self.args
        komp = [a * other for a in args]
        return _ZeilenVektor(*komp) 		

    
	
# Synonyme
# --------

v = Vektor
Punkt = Vektor		



	