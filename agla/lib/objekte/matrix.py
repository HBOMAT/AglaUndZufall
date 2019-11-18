#!/usr/bin/python
# -*- coding utf-8 -*-


#                                                 
# Matrix - Klasse von agla           
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

from IPython.display import display, Math

from sympy.abc import *
from sympy.matrices import Matrix as SympyMatrix
from sympy.core.containers import Tuple
from sympy.core.symbol import Symbol
from sympy.core.evalf import N

from sympy.core.sympify import sympify
from sympy.core.numbers import Integer, Float
from sympy.simplify import simplify, nsimplify
from sympy.core.compatibility import iterable
from sympy.printing import latex

from agla.lib.objekte.vektor import Vektor, _ZeilenVektor
from agla.lib.funktionen.funktionen import is_zahl, loese
from agla.lib.objekte.ausnahmen import *
from agla.lib.objekte.umgebung import UMG  



"""

Bereitstellung der Matrix-Klasse	
================================

agla hat keine eigene Matrix-Klasse (es ist nicht gelungen, die elegantere
Methode, diese durch Vererbung  von einer SymPy-Klasse bereitzustellen, 
zu realisieren). Stattdessen wird direkt die MutableDenseMatrix-Klasse von 
SymPy verwendet, die entsprechend angepasst wird. Somit sind alle Eigen-
schaften und Methoden für diese Matrizen automatisch verfügbar (siehe Sym-
PyDokumentation)

Zur Erzeugung einer Matrix dient die agla-Funktion 'Matrix', die neben der 
in SymPy verwendeten Art auch die Erzeugung über die (Spalten-) Vektoren 
gestattet

Aus Gründen der Kompatibilität mit den anderen agla-Klassen wurden einige 
wenige Eigenschaften/Methoden ergänzt und andere deutsch benannt

Die Multiplikation einer Matrix mit einem Vektor wird mittels Überschreiben 
der __mul__-Methode realisiert, die Verkettung einer Matrix mit einem Vektor 
(Operator '|') mittels  einer dazu definierten __or__-Methode 

Die Anbindung der überschriebenen und eigenen Methoden an die Matrix-Objekte 
erfolgt mittels der Funktion '_einrichten_matrix', die bei Bedarf aufgerufen 
werden kann 

"""


# Erzeuger-Funktion für Matrix in agla
# -------------------------------------

def Matrix(*args, **kwargs):  
    """*Funktion zur Erzeugung von Matrizen mit beliebiger Dimension"""
					
    h = kwargs.get("h")		
    if h in (1, 2, 3):                          
        matrix_hilfe(h)		
        return
    elif 	isinstance(h, (Integer, int)):
        matrix_hilfe(1)		
        return
		
    # Erzeugen einer SymPy-Matrix auf die übliche Art		
    if iterable(args) and not isinstance(args[0], Vektor):
        m = SympyMatrix(*args, **kwargs)
        for i in range(m.rows):
            for j in range(m.cols):
                try:			
                    m[i, j] = nsimplify(m[i, j])
                except RecursionError:
                    pass				
        return m
		
    # Erzeugen einer SymPy-Matrix anhand der Spaltenvektoren	
    try:		
        if not args:
            raise AglaError('mindestens zwei Vektoren angeben')		
        if isinstance(args[0], (tuple, Tuple, list, set)):
            vektoren = args[0]
            if not type(vektoren) == list:
                vektoren = list(vektoren)
        else: 
            vektoren = list(args) 
        if not all(isinstance(v, Vektor) for v in vektoren):
            raise AglaError('Vektoren angeben')
        if not all(v.dim == vektoren[0].dim for v in vektoren):
            raise AglaError('die Vektoren haben unterschiedliche Dimension')
    except AglaError as e:
        print('agla:', str(e)) 
	
    liste  = [ [k for k in v.komp] for v in vektoren ]
    m, n = vektoren[0].dim, len(vektoren)
    zeilen = [ [liste[i][j] for i in range(n)] for j in range(m) ]	
    M = SympyMatrix(zeilen)
		
    return M						


	
# Definition eigener Eigenschaften und Methoden
# ---------------------------------------------
#
# die Bindung an die Objekte erfolgt mit der Funktion
# _einrichten_matrix_klasse

@property				
def _anz_zeil(self):   
    """Zeilenanzahl"""
    return self.rows

@property				
def _anz_spalt(self):   
    """Spaltenanzahl"""
    return self.cols

@property				
def _char_poly(self):   
    """Charakteristisches Polynom"""
    if self.cols != self.rows:
        print('agla: keine quadratische Matrix')
        return
    la = Symbol('lamda')
    cp = self.charpoly(x=la)  
    cp = str(cp)
    cp = cp[9 : cp.find(",")]	
    try:	
        return nsimplify(eval(cp))	
    except RecursionError:
        return eval(cp)	
	
@property		
def _D(self):
    """Determinante"""
    if self.cols == self.rows:
        return simplify(self.det())
    print('agla: keine quadratische Matrix')
		
@property		
def _eig_wert(self):
    """Eigenwerte; für 2x2- und 3x3-Matrizen"""
    if self.rows in (2, 3) and self.cols == self.rows:
        L = loese(self.char_poly, lamda)
    else:		
        print('agla: keine 2x2- bzw. 3x3-Matrix')
        return		
    if len(L) == 1:
        return L[lamda]
    else:
        return [l[lamda] for l in L]
		
@property		
def _eig_vekt(self):
    """Eigenvektoren; für 2x2- und 3x3-Matrizen"""
    if self.rows in (2, 3) and self.cols == self.rows:
        L = self.eigenvects()
        if 	not L:
            print("agla: nicht implementiert")
            return			
        ev = []
        for el in L:
            par = el[1]
            vekt = el[2]
            i = 0
            while par:
               ev.append(matrix2vektor(vekt[i]))
               par -= 1
               i += 1
        l = len(str(ev))
        if l > 250:    # Verhinderung der komplexen Ausgabe
                      # Übergang zu nummerischen Werten	
            print('agla: Übergang zur nummerischen Berechnung wegen komplexer Ausgabe')					  
            from sympy import N
            simpl = UMG.SIMPL			
            UMG.SIMPL = False			
            if self.dim[0] == 2:
                ev = [Vektor(N(el.x, 12), N(el.y, 12)) for el in ev]	
            else:
                ev = [Vektor(N(el.x, 12), N(el.y, 12), N(el.z, 12)) for el in ev]			
            UMG.SIMPL = simpl			
        return ev			
    print('agla: keine 2x2- bzw. 3x3-Matrix')

@property		
def _einfach(self):
    """Vereinfachung"""
    m = Matrix(*[v.einfach for v in self.vekt])
    return m
		
@property		
def _inverse(self):
    """Inverse"""
    if self.cols != self.rows:
        print('agla: keine quadratische Matrix')
        return 
    if self.det() == 0:
        print('agla: die Inverse existiert nicht (die Determinante ist = 0)')
        return
    return self.inv()
		
@property		
def _vekt(self):
    """Spaltenvektoren"""
    vekt = []
    for j in range(self.shape[1]):
        vekt.append(Vektor([self[i, j] for i in range(self.shape[0])]))
    return vekt

@property		
def _dez(self):
    """Dezimalausgabe"""
    vekt = []
    for j in range(self.shape[1]):
        vekt.append(Vektor([N(self[i, j]) for i in range(self.shape[0])], simpl=False))
    return Matrix(*vekt)
		
@property		
def _is_schar(self):    
    """Test auf Schar"""
    return len(self.sch_par) == 1
	
@property		
def _sch_par(self):    
    """Scharparameter"""
    p = set()
    for ve in self.vekt:
        p = p.union(ve.sch_par)
    return p					
		
def _sch_el(self, *wert, **kwargs):
    """Element einer Schar; für einen Parameter"""
    if kwargs.get('h'):
        print("\nElement einer Schar von Matrizen\n")		
        print("Aufruf   matrix . sch_el( wert )\n")		                     
        print("             matrix    Matrix")
        print("             wert      Wert des Scharparameters")			
        print("\nEs ist nur ein Scharparameter zugelassen\n")    
        return 			
    schar = any([ve.is_schar for ve in self.vekt])			
    if not schar or len(self.sch_par) > 1:
        print('agla: keine Schar mit einem Parameter')	
        return		
    if not wert or len(wert) != 1:
        print('agla: einen Wert für den Scharparameter angeben') 
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
    vekt = []
    for ve in self.vekt:
        if p in ve.sch_par:
            vekt.append(ve.sch_el(wert))
        else:
            vekt.append(ve)     
    return Matrix(*vekt)
						
@property		
def _hilfe(self):  
    """Bezeichner der Eigenschaften und Methoden"""
    matrix_hilfe(3)	
					
	
# Anbinden der Funktionen an die Matrix-Objekte 
# ---------------------------------------------

def _einrichten_matrix():
    from time import time
    t0 = time()
    # Überschreiben von Methoden
    #---------------------------

    # Sichern von Original-Methoden:

    matrix_mul = copy.deepcopy(SympyMatrix.__mul__)    
    matrix_rmul	= copy.deepcopy(SympyMatrix.__rmul__)   
    Float_mul 	= copy.deepcopy(Float.__mul__)

    # Definition der Methoden zum Überschreiben:

    def _mul(self, other):  
        """Multiplikation Matrix * Vektor"""	
        if not isinstance(other, Vektor):
            return matrix_mul(self, other)		
        if self.anzSpalt != other.dim:
            print('agla: die Dimensionen sind unverträglich, Multiplikation nicht möglich')
            return
        f = other.vektor2sympy
        m1 = matrix_mul(self, f) 
        return matrix2vektor(m1)

    def _rmul(self, other):
        """Multiplikation _ZeilenVektor * Matrix"""	
        if isinstance(other, _ZeilenVektor):
            m = SympyMatrix(other.args)
            m = m.T
            if m.cols != self.rows:
                print('agla: die Dimensionen sind unverträglich, Multiplikation nicht möglich')
                return
            return matrix_mul(m, self)				
        return matrix_rmul(self, other)            																    

    def _or(self, other):
        """Verkettung einer Matrix mit einem Vektor"""	
        if isinstance(other, Vektor) and other.dim == self.dim[0]:
            vekt = copy.deepcopy(self.vekt)
        else:
            print('agla: Vektor mit passender Dimension angeben')
            return 			
        vekt.append(other)
        return Matrix(*vekt)

		
    # Überschreiben

    SympyMatrix.__mul__ 	= _mul
    SympyMatrix.__rmul__  	= _rmul
    SympyMatrix.__or__		= _or	
	
    # Erzeugen eigener Eigenschaften/Methoden
    # ---------------------------------------
    #
    # (Anbinden der Funktionen an die Matrix-Objekte)

    SympyMatrix.hilfe		= _hilfe		
    SympyMatrix.anz_spalt	= _anz_spalt		
    SympyMatrix.anz_zeil	= _anz_zeil		
    SympyMatrix.char_poly	= _char_poly
    SympyMatrix.D			= _D		
    SympyMatrix.dez			= _dez		
    SympyMatrix.dim			= SympyMatrix.shape		
    SympyMatrix.eig_wert	= _eig_wert
    SympyMatrix.eig_vekt	= _eig_vekt
    SympyMatrix.einfach   	= _einfach
    SympyMatrix.inverse		= _inverse
    SympyMatrix.is_schar	= _is_schar
    SympyMatrix.sch_par		= _sch_par
    SympyMatrix.sch_el		= _sch_el
    SympyMatrix.transp		= SympyMatrix.T				
    SympyMatrix.vekt		= _vekt
    SympyMatrix.h			= SympyMatrix.hilfe		
    SympyMatrix.anzZeil		= SympyMatrix.anz_zeil		
    SympyMatrix.anzSpalt	= SympyMatrix.anz_spalt		
    SympyMatrix.charPoly	= SympyMatrix.char_poly		
    SympyMatrix.eigWert		= SympyMatrix.eig_wert
    SympyMatrix.eigVekt		= SympyMatrix.eig_vekt
    SympyMatrix.isSchar		= SympyMatrix.is_schar
    SympyMatrix.schPar		= SympyMatrix.sch_par
    SympyMatrix.schEl		= SympyMatrix.sch_el
			
		
# Hilfsfunktion	
# -------------

def matrix2vektor(m):
    """Konvertierung Matrix --> Vektor"""
    if not isinstance(m, SympyMatrix):
        print('agla: Matrix angeben')
        return
    if m.shape[1] != 1:
        print('agla: die Spaltenanzahl ist > 1, Konvertierung nicht möglich')
        return		
    ve = m.vekt
    return Vektor(*ve)

	
# Benutzerhilfe für Matrix
# ------------------------

def matrix_hilfe(h):
    """Hilfe-Funktion"""
	
    if h == 1:
        print("h=2 - Erzeugung, Operatoren")
        print("h=3 - Eigenschaften und Methoden")
        return
		
    if h == 2:
        print("\nMatrix - Objekt\n")     
        print("Für mxn - Matrizen mit beliebiger Dimension,  m,n >= 2\n")		
        print("Erzeugung     Matrix( vekt1, vekt2, ... )\n")
        print("                 vekt   (Spalten-)Vektor\n")
        print("     oder     vekt1 | vekt2 | ...\n")                 
        print("Alle Vektoren müssen die gleiche Dimension haben\n")
        print("Zuweisung   M = Matrix(...)  bzw.  M = vekt1 | vekt2 ...")
        print("                             (M - freier Bezeichner)\n")
        print("Zugriff auf das Element in Zeile i und Spalte j:\n")
        print("           M[i, j], i=0...m-1, j=0...n-1\n")
        print("           mittels Zuweisung können so auch einzelne Elemente") 
        print("           verändert werden\n")
        print("Operatoren")
        print("  +  : Addition") 
        print("  -  : Negation/Subtraktion") 
        print("  *  : Multiplikation mit einem Skalar")                  
        print("       Multiplikation mit einer Matrix (mit passender Dimension)")
        print("       Multiplikation mit einem Vektor (mit passender Dimension)")
        print("  ** : Potenzieren mit einer ganzen Zahl")   
        print("  ^  : ebenso")   
        print("  |  : Verketten mit einem Vektor (mit passender Dimension)\n")                        
        print("Beispiele")
        print("m  = Matrix(v(1, 2, 3), v(-1, 0, 4))")
        print("m1 = m | v(3, 1, -2)")
        print("2 * m, sqrt(3) * m1")
        print("m1 * m")
        print("m1 * v(x,y,z)")
        print("m3 = m1**(-1); m4 = m1.inverse")
        print("m3, m4")
        print("m3 * m1, m1 * m4\n")	
        print("Vordefinierte Matrizen")
        print("NullMat    Nullmatrix im Raum R^3")
        print("EinhMat    Einheitsmatrix im Raum R^3")
        print("NullMat2   Nullmatrix in der Ebene R^2")
        print("EinhMat2   Einheitsmatrix in der Ebene R^2\n")
        return
		
    if h == 3:
        print("\nEigenschaften und Methoden für Matrix\n")	
        print("Für ein Matrix-Objekt stehen alle Eigenschaften und Methoden")
        print("eines MutableDenseMatrix-Objektes von SymPy zur Verfügung")
        print("(Näheres ist der SymPy-Dokumentation zu entnehmen)\n")		
        print("Die folgenden ausgewählten Eigenschaften/Methoden wurden aus ")
        print("Kompatibilitätsgründen deutsch benannt bzw. ergänzt\n")
        print("Eig./Meth.      in SymPy")
        print("m.hilfe         -                Bezeichner d. Eig./Meth.")
        print("m.anz_spalt     m.cols           Anzahl Spalten")
        print("m.anz_zeil      m.rows           Anzahl Zeilen")
        print("m.char_poly     m.charpoly()     Charakterist. Polynom   (*)")         
        print("m.D             m.det()          Determinante            (*)")
        print("m.dim           m.shape          Dimension")
        print("m.eig_wert      m.eigenvects()   Eigenwerte             (**)") 
        print("m.eig_vekt      ebenso           Eigenvektoren           (**)") 
        print("m.einfach       simplify(m)      Vereinfachung")
        print("m.inverse       m.inv()          Inverse (= m^-1)        (*)")        
        print("m.is_schar      -                Test auf Schar")
        print("m.sch_el(...)   -                Element einer Schar")		
        print("m.sch_par       -                Scharparameter") 
        print("m.transp        m.T              Transponierte")
        print("                m.transpose()    ebenso")
        print("m.vekt          -                Spaltenvektoren\n")
        print("Synonyme Bezeichner\n")
        print("hilfe     :  h")
        print("anz_spalt :  anzSpalt")
        print("anz_zeil  :  anzZeil")
        print("char_poly :  charPoly")
        print("eig_wert  :  eigWert")
        print("eig_vekt  :  eigVekt")
        print("is_schar  :  isSchar")
        print("sch_el    :  schEl")
        print("sch_par   :  schPar")		
        print("\n(*) für nxn Matrizen")
        print("(**) für 2x2- und 3x3-Matrizen\n")
		

		
# Vordefinierte Matrizen
# ----------------------
		
NullMat 	= Matrix(Vektor(0, 0, 0), Vektor(0, 0, 0), Vektor(0, 0, 0))
NullMat2 	= Matrix(Vektor(0, 0), Vektor(0, 0)) 
EinhMat 	= Matrix(Vektor(1, 0, 0), Vektor(0, 1, 0), Vektor(0, 0, 1))
EinhMat2 	= Matrix(Vektor(1, 0), Vektor(0, 1)) 


